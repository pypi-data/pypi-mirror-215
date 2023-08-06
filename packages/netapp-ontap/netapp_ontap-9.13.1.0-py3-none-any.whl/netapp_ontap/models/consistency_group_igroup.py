r"""
Copyright &copy; 2023 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupIgroup", "ConsistencyGroupIgroupSchema"]
__pdoc__ = {
    "ConsistencyGroupIgroupSchema.resource": False,
    "ConsistencyGroupIgroupSchema.opts": False,
    "ConsistencyGroupIgroup": False,
}


class ConsistencyGroupIgroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupIgroup object"""

    comment = fields.Str(data_key="comment")
    r""" A comment available for use by the administrator. Valid in POST and PATCH. """

    igroups = fields.List(fields.Nested("netapp_ontap.models.consistency_group_child_luns_lun_maps_igroup_igroups.ConsistencyGroupChildLunsLunMapsIgroupIgroupsSchema", unknown=EXCLUDE), data_key="igroups")
    r""" Separate igroup definitions to include in this igroup. """

    initiators = fields.List(fields.Nested("netapp_ontap.models.consistency_group_child_luns_lun_maps_igroup_initiators.ConsistencyGroupChildLunsLunMapsIgroupInitiatorsSchema", unknown=EXCLUDE), data_key="initiators")
    r""" The initiators that are members of the group. """

    name = fields.Str(data_key="name")
    r""" The name of the initiator group. Required in POST; optional in PATCH.


Example: igroup1 """

    os_type = fields.Str(data_key="os_type")
    r""" The host operating system of the initiator group. All initiators in the group should be hosts of the same operating system. Required in POST; optional in PATCH.


Valid choices:

* aix
* hpux
* hyper_v
* linux
* netware
* openvms
* solaris
* vmware
* windows
* xen """

    protocol = fields.Str(data_key="protocol")
    r""" The protocols supported by the initiator group. This restricts the type of initiators that can be added to the initiator group. Optional in POST; if not supplied, this defaults to _mixed_.<br/>
The protocol of an initiator group cannot be changed after creation of the group.


Valid choices:

* fcp
* iscsi
* mixed """

    uuid = fields.Str(data_key="uuid")
    r""" The unique identifier of the initiator group.


Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return ConsistencyGroupIgroup

    gettable_fields = [
        "comment",
        "igroups",
        "initiators",
        "name",
        "os_type",
        "protocol",
        "uuid",
    ]
    """comment,igroups,initiators,name,os_type,protocol,uuid,"""

    patchable_fields = [
        "comment",
        "igroups",
        "initiators",
        "name",
        "os_type",
    ]
    """comment,igroups,initiators,name,os_type,"""

    postable_fields = [
        "comment",
        "igroups",
        "initiators",
        "name",
        "os_type",
        "protocol",
    ]
    """comment,igroups,initiators,name,os_type,protocol,"""


class ConsistencyGroupIgroup(Resource):

    _schema = ConsistencyGroupIgroupSchema
