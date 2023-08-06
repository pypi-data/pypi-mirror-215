r"""
Copyright &copy; 2023 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FcPortSpeed", "FcPortSpeedSchema"]
__pdoc__ = {
    "FcPortSpeedSchema.resource": False,
    "FcPortSpeedSchema.opts": False,
    "FcPortSpeed": False,
}


class FcPortSpeedSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FcPortSpeed object"""

    configured = fields.Str(data_key="configured")
    r""" The configured speed of the FC port in gigabits per second.


Valid choices:

* 1
* 2
* 4
* 8
* 10
* 16
* 32
* 64
* auto """

    maximum = fields.Str(data_key="maximum")
    r""" The maximum speed supported by the FC port in gigabits per second.


Valid choices:

* 1
* 2
* 4
* 8
* 10
* 16
* 32
* 64
* auto """

    @property
    def resource(self):
        return FcPortSpeed

    gettable_fields = [
        "configured",
        "maximum",
    ]
    """configured,maximum,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class FcPortSpeed(Resource):

    _schema = FcPortSpeedSchema
