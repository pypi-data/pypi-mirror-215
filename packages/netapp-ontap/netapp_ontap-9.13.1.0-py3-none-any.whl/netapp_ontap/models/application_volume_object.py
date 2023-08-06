r"""
Copyright &copy; 2023 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationVolumeObject", "ApplicationVolumeObjectSchema"]
__pdoc__ = {
    "ApplicationVolumeObjectSchema.resource": False,
    "ApplicationVolumeObjectSchema.opts": False,
    "ApplicationVolumeObject": False,
}


class ApplicationVolumeObjectSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationVolumeObject object"""

    creation_timestamp = ImpreciseDateTime(data_key="creation_timestamp")
    r""" Creation time """

    name = fields.Str(data_key="name")
    r""" Name """

    size = Size(data_key="size")
    r""" Size """

    uuid = fields.Str(data_key="uuid")
    r""" UUID """

    @property
    def resource(self):
        return ApplicationVolumeObject

    gettable_fields = [
        "creation_timestamp",
        "name",
        "size",
        "uuid",
    ]
    """creation_timestamp,name,size,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ApplicationVolumeObject(Resource):

    _schema = ApplicationVolumeObjectSchema
