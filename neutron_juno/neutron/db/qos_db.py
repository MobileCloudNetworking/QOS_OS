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

__author__ = "Marco Del Seppia"
__version__ = "0.1"
__maintainer__ = "Marco Del Seppia"
__email__ = "m.delseppia@nextworks.it"
__status__ = "Developing"

import sqlalchemy as sa
from sqlalchemy.orm import exc

from neutron.db import common_db_mixin as base_db
from neutron.db import model_base
from neutron.db import models_v2
from neutron.extensions import qos
from neutron.openstack.common import excutils
from neutron.openstack.common import log as logging
from neutron.openstack.common import uuidutils

LOG = logging.getLogger(__name__)

# describe a DB table columns represent a Qos resource
class qos(model_base.BASEV2, models_v2.HasId, models_v2.HasTenant):
    """Represents a Qos Object."""
    __tablename__ = 'qos'
	qos_param = sa.Column(sa.String(64)),
				sa.ForeignKey('qos_param.id', ondelete="CASCADE")
				nullable=False)
    
# describe a DB table columns represent a Qos param resource
class qos_param(model_base.BASEV2, models_v2.HasId, models_v2.HasTenant):
    """Represents a Qos parameter Object."""
    __tablename__ = 'qos_param'
    param_type = sa.Column(sa.String(64),
			nullable=False)
    policy = sa.Column(sa.String(64),
			 nullable=False)
    classifier = sa.Column(sa.String(64),
				 sa.ForeignKey('qos_calssifier.id', ondelete="CASCADE")
    
# describe a DB table columns represent a Qos classifier resource
class qos_classifier(model_base.BASEV2, models_v2.HasId, models_v2.HasTenant):
    """Represents a Qos classifier Object."""
    __tablename__ = 'qos_classifier'
    classifier_type = sa.Column(sa.String(64),
			nullable=False)
    policy = sa.Column(sa.String(64),
			 nullable=False)


class qosDBManager(base_db.CommonDbMixin):
    """qos database class using SQLAlchemy models."""

    def _make_qos_dict(self, qos, fields=None):
        res = {'id': qos['id'],
               'tenant_id': qos['tenant_id'],
               'qos_param': qos['qos_param']}
        return self._fields(res, fields)

    def _get_resource(self, context, model, id_):
        try:
            return self._get_by_id(context, model, id_)
        except exc.NoResultFound:
            with excutils.save_and_reraise_exception(reraise=False) as ctx:
                if issubclass(model, qos):
                    raise qoq.qosNotFound(qos_id=id_)
                ctx.reraise = True

    def create_qos(self, context, qos):
        with context.session.begin(subtransactions=True):
            qos_db = qos(id=uuidutils.generate_uuid(),
                                  tenant_id=qos.get('tenant_id'),
                                  qos_param=qos.get('qos_param'))
            context.session.add(qos_db)
        return self._make_qos_dict(qos_db)

    def update_qos(self, context, id_, qos):
        with context.session.begin(subtransactions=True):
            qos_db = self._get_resource(context, qos, id_)
            if qos:
                qos_db.update(qos)
        return self._make_qos_dict(qos_db)

    def delete_qos(self, context, id_):
        with context.session.begin(subtransactions=True):
            qos_db = self._get_resource(context, qos, id_)
            context.session.delete(qos_db)

    def get_qos(self, context, id_, fields=None):
        qos_db = self._get_resource(context, qos, id_)
        return self._make_qos_dict(qos_db, fields)

    def get_qoss(self, context, filters=None, fields=None):
        return self._get_collection(context, qos,
                                    self._make_qos_dict,
                                    filters=filters, fields=fields)
                                    
class qos_paramDBManager(base_db.CommonDbMixin):
    """qos database class using SQLAlchemy models."""

    def _make_qos_dict(self, qos, fields=None):
        res = {'id': qos['id'],
               'tenant_id': qos['tenant_id'],
               'qos_param': qos['qos_param']}
        return self._fields(res, fields)

    def _get_resource(self, context, model, id_):
        try:
            return self._get_by_id(context, model, id_)
        except exc.NoResultFound:
            with excutils.save_and_reraise_exception(reraise=False) as ctx:
                if issubclass(model, qos):
                    raise qoq.qosNotFound(qos_id=id_)
                ctx.reraise = True

    def create_qos(self, context, qos):
        with context.session.begin(subtransactions=True):
            qos_db = qos(id=uuidutils.generate_uuid(),
                                  tenant_id=qos.get('tenant_id'),
                                  qos_param=qos.get('qos_param'))
            context.session.add(qos_db)
        return self._make_qos_dict(qos_db)

    def update_qos(self, context, id_, qos):
        with context.session.begin(subtransactions=True):
            qos_db = self._get_resource(context, qos, id_)
            if qos:
                qos_db.update(qos)
        return self._make_qos_dict(qos_db)

    def delete_qos(self, context, id_):
        with context.session.begin(subtransactions=True):
            qos_db = self._get_resource(context, qos, id_)
            context.session.delete(qos_db)

    def get_qos(self, context, id_, fields=None):
        qos_db = self._get_resource(context, qos, id_)
        return self._make_qos_dict(qos_db, fields)

    def get_qoss(self, context, filters=None, fields=None):
        return self._get_collection(context, qos,
                                    self._make_qos_dict,
                                    filters=filters, fields=fields)
