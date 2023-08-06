r"""
Copyright &copy; 2023 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmFcp", "SvmFcpSchema"]
__pdoc__ = {
    "SvmFcpSchema.resource": False,
    "SvmFcpSchema.opts": False,
    "SvmFcp": False,
}


class SvmFcpSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmFcp object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links")
    r""" The links field of the svm_fcp. """

    allowed = fields.Boolean(data_key="allowed")
    r""" If this is set to true, an SVM administrator can manage the FCP service. If it is false, only the cluster administrator can manage the service. """

    enabled = fields.Boolean(data_key="enabled")
    r""" If allowed, setting to true enables the FCP service. """

    @property
    def resource(self):
        return SvmFcp

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


class SvmFcp(Resource):

    _schema = SvmFcpSchema
