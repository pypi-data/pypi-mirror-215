r"""
Copyright &copy; 2023 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmIscsi", "SvmIscsiSchema"]
__pdoc__ = {
    "SvmIscsiSchema.resource": False,
    "SvmIscsiSchema.opts": False,
    "SvmIscsi": False,
}


class SvmIscsiSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmIscsi object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links")
    r""" The links field of the svm_iscsi. """

    allowed = fields.Boolean(data_key="allowed")
    r""" If this is set to true, an SVM administrator can manage the iSCSI service. If it is false, only the cluster administrator can manage the service. """

    enabled = fields.Boolean(data_key="enabled")
    r""" If allowed, setting to true enables the ISCSI service. """

    @property
    def resource(self):
        return SvmIscsi

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


class SvmIscsi(Resource):

    _schema = SvmIscsiSchema
