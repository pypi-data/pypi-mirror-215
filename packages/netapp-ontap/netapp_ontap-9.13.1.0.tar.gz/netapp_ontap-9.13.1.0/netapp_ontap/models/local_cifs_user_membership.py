r"""
Copyright &copy; 2023 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LocalCifsUserMembership", "LocalCifsUserMembershipSchema"]
__pdoc__ = {
    "LocalCifsUserMembershipSchema.resource": False,
    "LocalCifsUserMembershipSchema.opts": False,
    "LocalCifsUserMembership": False,
}


class LocalCifsUserMembershipSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LocalCifsUserMembership object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links")
    r""" The links field of the local_cifs_user_membership. """

    name = fields.Str(data_key="name")
    r""" Local group name. The maximum supported length of a group name is 256 characters.


Example: SMB_SERVER01\group """

    sid = fields.Str(data_key="sid")
    r""" The security ID of the local group which uniquely identifies the group. The group SID is automatically generated in POST and it is retrieved using the GET method.


Example: S-1-5-21-256008430-3394229847-3930036330-1001 """

    @property
    def resource(self):
        return LocalCifsUserMembership

    gettable_fields = [
        "links",
        "name",
        "sid",
    ]
    """links,name,sid,"""

    patchable_fields = [
        "name",
    ]
    """name,"""

    postable_fields = [
        "name",
    ]
    """name,"""


class LocalCifsUserMembership(Resource):

    _schema = LocalCifsUserMembershipSchema
