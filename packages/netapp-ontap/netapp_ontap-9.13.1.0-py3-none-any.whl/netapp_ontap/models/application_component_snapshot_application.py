r"""
Copyright &copy; 2023 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationComponentSnapshotApplication", "ApplicationComponentSnapshotApplicationSchema"]
__pdoc__ = {
    "ApplicationComponentSnapshotApplicationSchema.resource": False,
    "ApplicationComponentSnapshotApplicationSchema.opts": False,
    "ApplicationComponentSnapshotApplication": False,
}


class ApplicationComponentSnapshotApplicationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationComponentSnapshotApplication object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links")
    r""" The links field of the application_component_snapshot_application. """

    name = fields.Str(data_key="name")
    r""" Application Name """

    uuid = fields.Str(data_key="uuid")
    r""" Application UUID. Valid in URL """

    @property
    def resource(self):
        return ApplicationComponentSnapshotApplication

    gettable_fields = [
        "links",
        "name",
        "uuid",
    ]
    """links,name,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ApplicationComponentSnapshotApplication(Resource):

    _schema = ApplicationComponentSnapshotApplicationSchema
