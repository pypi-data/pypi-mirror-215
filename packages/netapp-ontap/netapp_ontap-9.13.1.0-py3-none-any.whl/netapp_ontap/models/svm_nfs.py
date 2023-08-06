r"""
Copyright &copy; 2023 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmNfs", "SvmNfsSchema"]
__pdoc__ = {
    "SvmNfsSchema.resource": False,
    "SvmNfsSchema.opts": False,
    "SvmNfs": False,
}


class SvmNfsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmNfs object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links")
    r""" The links field of the svm_nfs. """

    allowed = fields.Boolean(data_key="allowed")
    r""" If this is set to true, an SVM administrator can manage the NFS service. If it is false, only the cluster administrator can manage the service. """

    enabled = fields.Boolean(data_key="enabled")
    r""" If allowed, setting to true enables the NFS service. """

    @property
    def resource(self):
        return SvmNfs

    gettable_fields = [
        "links",
        "allowed",
        "enabled",
    ]
    """links,allowed,enabled,"""

    patchable_fields = [
        "allowed",
    ]
    """allowed,"""

    postable_fields = [
        "allowed",
        "enabled",
    ]
    """allowed,enabled,"""


class SvmNfs(Resource):

    _schema = SvmNfsSchema
