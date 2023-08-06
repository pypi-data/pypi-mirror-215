r"""
Copyright &copy; 2023 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SnapmirrorTransferErrorInfo", "SnapmirrorTransferErrorInfoSchema"]
__pdoc__ = {
    "SnapmirrorTransferErrorInfoSchema.resource": False,
    "SnapmirrorTransferErrorInfoSchema.opts": False,
    "SnapmirrorTransferErrorInfo": False,
}


class SnapmirrorTransferErrorInfoSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnapmirrorTransferErrorInfo object"""

    code = Size(data_key="code")
    r""" Error code

Example: 6620046 """

    message = fields.Str(data_key="message")
    r""" Error message

Example: Transfer aborted """

    @property
    def resource(self):
        return SnapmirrorTransferErrorInfo

    gettable_fields = [
        "code",
        "message",
    ]
    """code,message,"""

    patchable_fields = [
        "code",
        "message",
    ]
    """code,message,"""

    postable_fields = [
        "code",
        "message",
    ]
    """code,message,"""


class SnapmirrorTransferErrorInfo(Resource):

    _schema = SnapmirrorTransferErrorInfoSchema
