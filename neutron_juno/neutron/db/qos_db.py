#    (c) Copyright 2013 Hewlett-Packard Development Company, L.P.
#    All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import sqlalchemy as sa
from sqlalchemy.orm import exc

from neutron.db import common_db_mixin as base_db
from neutron.db import model_base
from neutron.db import models_v2
import neutron.extensions.qos
from neutron.openstack.common import excutils
from neutron.openstack.common import log as logging
from neutron.openstack.common import uuidutils


LOG = logging.getLogger(__name__)


# DB table entry representing a QoS resource
class Qos(model_base.BASEV2, models_v2.HasId, models_v2.HasTenant):
    """Represents a Qos object."""
    __tablename__ = 'qoss'

    type = sa.Column(sa.String(64), nullable=False)
    ingress_id = sa.Column(sa.String(36), nullable=False,
                           sa.ForeignKey('ports.id', ondelete="CASCADE"))
    egress_id = sa.Column(sa.String(36), nullable=False,
                          sa.ForeignKey('ports.id', ondelete="CASCADE"))
    net_id = sa.Column(sa.String(36), nullable=False,
                       sa.ForeignKey('ports.id', ondelete="CASCADE"))
    qos_params = orm.relationship('QosQosParamAssociation',
                                  backref='qoss',
                                  cascade='all, delete-orphan')


# DB table entry representing a QoS parameter resource
class QosParam(model_base.BASEV2, models_v2.HasId, models_v2.HasTenant):
    """Represents a Qos parameter Object."""
    __tablename__ = 'qos_params'

    type = sa.Column(sa.String(64), nullable=False)
    policy = sa.Column(sa.String(64), nullable=False)
    qoss = orm.relationship('QosQosParamAssociation',
                            backref='qos_params',
                            cascade='all', lazy='joined')
    qos_classifiers = orm.relationship('QosParamQosClassifierAssociation',
                                        backref='qos_params',
                                        cascade='all, delete-orphan')


# DB table entry representing a QoS classifier resource
class QosClassifier(model_base.BASEV2, models_v2.HasId, models_v2.HasTenant):
    """Represents a Qos classifier Object."""
    __tablename__ = 'qos_classifiers'

    type = sa.Column(sa.String(64), nullable=False)
    policy = sa.Column(sa.String(64), nullable=False)
    qos_params = orm.relationship('QosParamQosClassifierAssociation',
                                  backref='qos_classifiers',
                                  cascade='all', lazy='joined')


# DB table entry representing the relationship between a QoS resource and
# a QoS parameter resource
class QosQosParamAssociation(model_base.BASEV2):
    """Represents a QoS parameter object contained by a QoS object"""
    __tablename__ = 'qos_qos_param_association'

    qos_id = sa.Column(sa.String(36), nullable=False,
                       sa.ForeignKey('qoss.id', ondelete="CASCADE"),
                       primary_key=True)
    qos_param_id = sa.Column(sa.String(36), nullable=False,
                             sa.ForeignKey('qos_params.id',
                                           ondelete="CASCADE"),
                             primary_key=True)


# DB table entry representing the relationship between a QoS parameter
# resource and a QoS classifier resource
class QosParamQosClassifierAssociation(model_base.BASEV2):
    """Represents a QoS classifier object contained bt a QoS parameter object"""
    __tablename__ = 'qos_param_qos_classifier_association'

    qos_param_id = sa.Column(sa.String(36), nullable=False,
                             sa.ForeignKey('qos_params.id',
                                           ondelete="CASCADE"),
                             primary_key=True)
    qos_classifier_id = sa.Column(sa.String(36), nullable=False,
                                  sa.ForeignKey('qos_classifiers.id',
                                                ondelete="CASCADE"),
                                  primary_key=True)


# Utility class to manipulate the QoS DB tables
class QosDBManager(base_db.CommonDbMixin):
    """QoS database classes using SQLAlchemy models."""

    def _get_resource(self, context, model, id_):
        try:
            return self._get_by_id(context, model, id_)
        except exc.NoResultFound:
            with excutils.save_and_reraise_exception(reraise=False) as ctx:
                if issubclass(model, Qos):
                    raise neutron.extensions.qos.QosNotFound(id=id_)
                elif issubclass(model, QosParam):
                    raise neutron.extensions.qos.QosParamNotFound(id=id_)
                elif issubclass(model, QosClassifier):
                    raise neutron.extensions.qos.QosClassifierNotFound(id=id_)
                ctx.reraise = True

    def _make_qos_dict(self, row, fields=None):
        qos_params = [x['id'] for x in row['qos_params']]
        res = {'id': row['id'],
               'tenant_id': row['tenant_id'],
               'type': row['type'],
               'ingress_id': row['ingress_id'],
               'egress_id': row['egress_id'],
               'net_id': row['net_id'],
               'qos_params': qos_params}
        return self._fields(res, fields)

    def _make_qos_param_dict(self, qos_param, fields=None):
        qos_classifiers = [x['id'] for x in row['qos_classifiers']]
        res = {'id': qos_param['id'],
               'tenant_id': qos_param['tenant_id'],
               'type': qos_param['type'],
               'policy': qos_param['policy'],
               'qos_classifiers': qos_classifiers}
        return self._fields(res, fields)

    def _make_qos_classifier_dict(self, qos_classifier, fields=None):
        res = {'id': qos_classifier['id'],
               'tenant_id': qos_classifier['tenant_id'],
               'type': qos_classifier['type'],
               'policy': qos_classifier['policy']}
        return self._fields(res, fields)

    def _set_params_for_qos(context, qos_db, qos_param_ids):
        with context.session.begin(subtransactions=True):
            qos_db.qos_params = []
            if not qos_param_ids:
                return

            for qpid in qos_param_ids:
                qry = context.session.query(QosQosParamAssociation)
                assoc = qry.filter_by(qos_id=qos_db['id'],
                                      qos_param_id=qpid).first()
                if assoc:
                    LOG.info(_("Association between %s and %s already exists") % (qos_db['id'], qpid))
                    continue

                assoc = QosQosParamAssociation(qos_id=qos_db['id'],
                                               qos_param_id=qpid)
                qos_db.qos_params.append(assoc)

    def _set_classifiers_for_qos_param(context, qos_param_db,
                                       qos_classifier_ids):
        with context.session.begin(subtransactions=True):
            qos_param_db.qos_classifiers = []
            if not qos_classifier_ids:
                return

            for qcid in qos_classifier_ids:
                qry = context.session.query(QosParamQosClassifierAssociation)
                assoc = qry.filter_by(qos_param_id=qos_param_db['id'],
                                      qos_classifier_id=qcid).first()
                if assoc:
                    LOG.info(_("Association between %s and %s already exists") % (qos_param_db['id'], qcid))
                    continue

                assoc = QosParamQosClassifierAssociation(qos_param_id=qos_param_db['id'],
                                                         qos_classifier_id=qcid)
                qos_param_db.qos_classifiers.append(assoc)

    # QoS
    def create_qos(self, context, value):
        with context.session.begin(subtransactions=True):
            qos_db = Qos(id=uuidutils.generate_uuid(),
                         tenant_id=value.get('tenant_id'),
                         type=value.get('type'),
                         ingress_id=value.get('ingress_id'),
                         egress_id=value.get('egress_id'),
                         net_id=value.get('net_id'))
            context.session.add(qos_db)

            self._set_params_for_qos(context, qos_db, value.get('qos_params'))

        return self._make_qos_dict(qos_db)

    def update_qos(self, context, id_, qos):
        with context.session.begin(subtransactions=True):
            qos_db = self._get_resource(context, Qos, id_)
            if qos:
                qos_db.update(qos)
        return self._make_qos_dict(qos_db)

    def delete_qos(self, context, id_):
        with context.session.begin(subtransactions=True):
            qos_db = self._get_resource(context, Qos, id_)
            context.session.delete(qos_db)

    def get_qos(self, context, id_, fields=None):
        qos_db = self._get_resource(context, Qos, id_)
        return self._make_qos_dict(qos_db, fields)
    
    def get_qoss(self, context, filters=None, fields=None):
        return self._get_collection(context, Qos,
                                    self._make_qos_dict,
                                    filters=filters, fields=fields)

    # QoS Param
    def create_qos_param(self, context, value):
        with context.session.begin(subtransactions=True):
            qos_param_db = QosParam(id=uuidutils.generate_uuid(),
                                    tenant_id=value.get('tenant_id'),
                                    type=value.get('type'),
                                    policy=value.get('policy'))
            context.session.add(qos_param_db)

            self._set_classifiers_for_qos_param(context, qos_param_db,
                                                value.get('qos_classifiers'))

        return self._make_qos_param_dict(qos_param_db)

    def update_qos_param(self, context, id_, qos_param):
        with context.session.begin(subtransactions=True):
            qos_param_db = self._get_resource(context, QosParam, id_)
            if qos_param:
                qos_param_db.update(qos_param)
        return self._make_qos_param_dict(qos_param_db)

    def delete_qos_param(self, context, id_):
        with context.session.begin(subtransactions=True):
            qos_param_db = self._get_resource(context, QosParam, id_)
            context.session.delete(qos_param_db)

    def get_qos_param(self, context, id_, fields=None):
        qos_param_db = self._get_resource(context, QosParam, id_)
        return self._make_qos_param_dict(qos_param_db, fields)

    def get_qos_params(self, context, filters=None, fields=None):
        return self._get_collection(context, QosParam,
                                    self._make_qos_param_dict,
                                    filters=filters, fields=fields)

    # QoS Classifier
    def create_qos_classifier(self, context, value):
        with context.session.begin(subtransactions=True):
            qos_classifier_db = QosClassifier(id=uuidutils.generate_uuid(),
                                tenant_id=value.get('tenant_id'),
                                type=value.get('type'),
                                policy=value.get('policy'))
            context.session.add(qos_classifier_db)
        return self._make_qos_classifier_dict(qos_classifier_db)

    def update_qos_classifier(self, context, id_, qos_classifier):
        with context.session.begin(subtransactions=True):
            qos_classifier_db = self._get_resource(context, QosClassifier, id_)
            if qos_classifier:
                qos_classifier_db.update(qos_classifier)
        return self._make_qos_classifier_dict(qos_classifier_db)

    def delete_qos_classifier(self, context, id_):
        with context.session.begin(subtransactions=True):
            qos_classifier_db = self._get_resource(context, QosClassifier, id_)
            context.session.delete(qos_classifier_db)

    def get_qos_classifier(self, context, id_, fields=None):
        qos_classifier_db = self._get_resource(context, QosClassifier, id_)
        return self._make_qos_classifier_dict(qos_classifier_db, fields)

    def get_qos_classifiers(self, context, filters=None, fields=None):
        return self._get_collection(context, QosClassifier,
                                    self._make_qos_classifier_dict,
                                    filters=filters, fields=fields)
