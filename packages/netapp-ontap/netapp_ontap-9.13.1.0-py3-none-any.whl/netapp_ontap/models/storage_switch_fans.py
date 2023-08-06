r"""
Copyright &copy; 2023 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageSwitchFans", "StorageSwitchFansSchema"]
__pdoc__ = {
    "StorageSwitchFansSchema.resource": False,
    "StorageSwitchFansSchema.opts": False,
    "StorageSwitchFans": False,
}


class StorageSwitchFansSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageSwitchFans object"""

    name = fields.Str(data_key="name")
    r""" Storage switch fan name """

    speed = Size(data_key="speed")
    r""" Storage switch fan speed """

    state = fields.Str(data_key="state")
    r""" Storage switch fan state

Valid choices:

* ok
* error """

    @property
    def resource(self):
        return StorageSwitchFans

    gettable_fields = [
        "name",
        "speed",
        "state",
    ]
    """name,speed,state,"""

    patchable_fields = [
        "name",
        "speed",
        "state",
    ]
    """name,speed,state,"""

    postable_fields = [
        "name",
        "speed",
        "state",
    ]
    """name,speed,state,"""


class StorageSwitchFans(Resource):

    _schema = StorageSwitchFansSchema
