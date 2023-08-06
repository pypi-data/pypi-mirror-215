r"""
Copyright &copy; 2023 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["BgpPeerGroupLocalIp", "BgpPeerGroupLocalIpSchema"]
__pdoc__ = {
    "BgpPeerGroupLocalIpSchema.resource": False,
    "BgpPeerGroupLocalIpSchema.opts": False,
    "BgpPeerGroupLocalIp": False,
}


class BgpPeerGroupLocalIpSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the BgpPeerGroupLocalIp object"""

    address = fields.Str(data_key="address")
    r""" The address field of the bgp_peer_group_local_ip. """

    netmask = fields.Str(data_key="netmask")
    r""" The netmask field of the bgp_peer_group_local_ip. """

    @property
    def resource(self):
        return BgpPeerGroupLocalIp

    gettable_fields = [
        "address",
        "netmask",
    ]
    """address,netmask,"""

    patchable_fields = [
        "address",
        "netmask",
    ]
    """address,netmask,"""

    postable_fields = [
        "address",
        "netmask",
    ]
    """address,netmask,"""


class BgpPeerGroupLocalIp(Resource):

    _schema = BgpPeerGroupLocalIpSchema
