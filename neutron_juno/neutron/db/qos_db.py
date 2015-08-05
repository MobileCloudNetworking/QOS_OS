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


# DB table entry representing a QoS parameter resource
class QosParam(model_base.BASEV2, models_v2.HasId, models_v2.HasTenant):
    """Represents a Qos parameter Object."""
    __tablename__ = 'qos_parameters'
    type = sa.Column(sa.String(64), nullable=False)
    policy = sa.Column(sa.String(64), nullable=False)


# DB table entry representing the relationship between a QoS resource and
# a QoS parameter resource
class QosParamsList(model_base.BASEV2):
    """Represents a QoS parameter object contained by a QoS object"""
    __tablename__ = 'qos_params_lists'
    qos_id = sa.Column(sa.String(36), nullable=False, primary_key=True,
                       sa.ForeignKey('qoss.id', ondelete="CASCADE"))
    qos_param_id = sa.Column(sa.String(36), nullable=False, primary_key=True,
                             sa.ForeignKey('qos_parameters.id',
                                           ondelete="CASCADE")


# DB table entry representing a QoS classifier resource
class QosClassifier(model_base.BASEV2, models_v2.HasId, models_v2.HasTenant):
    """Represents a Qos classifier Object."""
    __tablename__ = 'qos_classifiers'
    type = sa.Column(sa.String(64), nullable=False)
    policy = sa.Column(sa.String(64), nullable=False)


# DB table entry representing the relationship between a QoS parameter
# resource and a QoS classifier resource
class QosClassifiersList(model_base.BASEV2):
    """Represents a QoS classifier object contained bt a QoS parameter object"""
    __tablename__ = 'qos_classifiers_lists'
    qos_param_id = sa.Column(sa.String(36), nullable=False, primary_key=True,
                             sa.ForeignKey('qos_parameters.id',
                                           ondelete="CASCADE")
    qos_classifier_id = sa.Column(sa.String(36), nullable=False,
                                  primary_key=True,
                                  sa.ForeignKey('qos_classifiers.id',
                                                ondelete="CASCADE"))


# Utility class to manipulate the qoss table
class QosDBManager(base_db.CommonDbMixin):
    """Qos database class using SQLAlchemy models."""

    # prepare a disctionary with the associated params
    def _make_qos_dict(self, qos, fields=None):
        res = {'id': qos['id'],
               'tenant_id': qos['tenant_id'],
               'type': qos['type'],
               'ingress_id': qos['ingress_id'],
               'egress_id': qos['egress_id'],
               'net_id': qos['net_id']}
        return self._fields(res, fields)

    
    def _get_resource(self, context, model, id_):
        try:
            return self._get_by_id(context, model, id_)
        except exc.NoResultFound:
            with excutils.save_and_reraise_exception(reraise=False) as ctx:
                if issubclass(model, Qos):
                    raise neutron.extensions.qos.QosNotFound(qos_id=id_)
                ctx.reraise = True

    def create_qos(self, context, qos_value):
        with context.session.begin(subtransactions=True):
            qos_db = Qos(id=uuidutils.generate_uuid(),
                         tenant_id=qos_value.get('tenant_id'),
                         type=qos_value.get('type'),
                         ingress_id=qos_value.get('ingress_id'),
                         egress_id=qos_value.get('egress_id'),
                         net_id=qos_value.get('net_id'))
            context.session.add(qos_db)
            #qos_param=qos_value.get('qos_param')
        return self._make_qos_dict(qos_db)

    def update_qos(self, context, id_, qos):
        with context.session.begin(subtransactions=True):
            qos_db = self._get_resource(context, qos, id_)
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
    
    # return all the Qos entries
    def get_qoss(self, context, filters=None, fields=None):
        return self._get_collection(context, Qos,
                                    self._make_qos_dict,
                                    filters=filters, fields=fields)


# Utility class to manipulate the qos_parameters table
class QosParamDBManager(base_db.CommonDbMixin):
    """QosParam database class using SQLAlchemy models."""

    def _make_qos_param_dict(self, qos_param, fields=None):
        res = {'id': qos_param['id'],
               'tenant_id': qos_param['tenant_id'],
               'type': qos_param['type'],
               'policy':qos_param['policy']}
        return self._fields(res, fields)

    def _get_resource(self, context, model, id_):
        try:
            return self._get_by_id(context, model, id_)
        except exc.NoResultFound:
            with excutils.save_and_reraise_exception(reraise=False) as ctx:
                if issubclass(model, QosParam):
                    raise neutron.extensions.qos.QosParamNotFound(qos_param_id=id_)
                ctx.reraise = True

    def create_qos_param(self, context, qos_param):
        with context.session.begin(subtransactions=True):
            qos_param_db = QosParam(id=uuidutils.generate_uuid(),
                                    tenant_id=qos_param.get('tenant_id'),
                                    type=qos_param.get('type'),
                                    policy=qos_param.get('policy'))
            context.session.add(qos_param_db)
            #qos_classifier=qos_param.get('qos_classifier')
        return self._make_qos_param_dict(qos_param_db)

    def update_qos_param(self, context, id_, qos_param):
        with context.session.begin(subtransactions=True):
            qos_param_db = self._get_resource(context, qos_param, id_)
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


# Utility class to manipulate the qos_params_lists table
class QosParamsListDBManager(base_db.CommonDbMixin):
    """QosParamsList database class using SQLAlchemy models."""

    def _make_qos_params_list_dict(self, row, fields=None):
        res = {'qos_id': row['qos_id'],
               'qos_param_id': row['qos_param_id']}
        return self._fields(res, fields)

    def _get_resource(self, context, row, id_):
        try:
            return self._get_by_id(context, row, id_)
        except exc.NoResultFound:
            with excutils.save_and_reraise_exception(reraise=False) as ctx:
                if issubclass(row, QosParamsList):
                    raise neutron.extensions.qos.QosParamNotFound(qos_param_id=id_)
                ctx.reraise = True

    def create_qos_params_list(self, context, value):
        with context.session.begin(subtransactions=True):
            row = QosParamsList(qos_id=value.get('qos_id'),
                                qos_param_id=value.get('qos_param_id'))
            context.session.add(row)
        return self._make_qos_params_list_dict(row)

    def update_qos_params_list(self, context, id_, value):
        with context.session.begin(subtransactions=True):
            row = self._get_resource(context, value, id_)
            if row:
                row.update(value)
        return self._make_qos_params_list_dict(row)

    def delete_qos_params_list(self, context, id_):
        with context.session.begin(subtransactions=True):
            row = self._get_resource(context, QosParamsList, id_)
            context.session.delete(row)

    def get_qos_params_list(self, context, id_, fields=None):
        row = self._get_resource(context, QosParamsList, id_)
        return self._make_qos_params_list_dict(row, fields)

    def get_qos_params_lists(self, context, filters=None, fields=None):
        return self._get_collection(context, QosParamsList,
                                    self._make_qos_params_list_dict,
                                    filters=filters, fields=fields)


# Utility class to manipulate the qos_classifiers table
class QosClassifierDBManager(base_db.CommonDbMixin):
    """QosClassifier database class using SQLAlchemy models."""

    def _make_qos_classifier_dict(self, qos_classifier, fields=None):
        res = {'id': qos_classifier['id'],
               'tenant_id': qos_classifier['tenant_id'],
               'type': qos_classifier['type'],
               'policy': qos_classifier['policy']}
        return self._fields(res, fields)

    def _get_resource(self, context, model, id_):
        try:
            return self._get_by_id(context, model, id_)
        except exc.NoResultFound:
            with excutils.save_and_reraise_exception(reraise=False) as ctx:
                if issubclass(model, QosClassifier):
                    raise neutron.extensions.qos.QosClassifierNotFound(qos_classifier_id=id_)
                ctx.reraise = True

    def create_qos_classifier(self, context, qos_classifier):
        with context.session.begin(subtransactions=True):
            qos_classifier_db = QosClassifier(id=uuidutils.generate_uuid(),
                                tenant_id=qos_classifier.get('tenant_id'),
                                type=qos_classifier.get('type'),
                                policy=qos_classifier.get('policy'))
            context.session.add(qos_classifier_db)
        return self._make_qos_classifier_dict(qos_classifier_db)

    def update_qos_classifier(self, context, id_, qos_classifier):
        with context.session.begin(subtransactions=True):
            qos_classifier_db = self._get_resource(context, qos_classifier, id_)
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
