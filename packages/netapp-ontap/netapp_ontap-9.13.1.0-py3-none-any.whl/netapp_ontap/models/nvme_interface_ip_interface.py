r"""
Copyright &copy; 2023 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeInterfaceIpInterface", "NvmeInterfaceIpInterfaceSchema"]
__pdoc__ = {
    "NvmeInterfaceIpInterfaceSchema.resource": False,
    "NvmeInterfaceIpInterfaceSchema.opts": False,
    "NvmeInterfaceIpInterface": False,
}


class NvmeInterfaceIpInterfaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeInterfaceIpInterface object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links")
    r""" The links field of the nvme_interface_ip_interface. """

    ip = fields.Nested("netapp_ontap.models.nvme_interface_ip_interface_ip.NvmeInterfaceIpInterfaceIpSchema", unknown=EXCLUDE, data_key="ip")
    r""" The ip field of the nvme_interface_ip_interface. """

    location = fields.Nested("netapp_ontap.models.nvme_interface_ip_interface_location.NvmeInterfaceIpInterfaceLocationSchema", unknown=EXCLUDE, data_key="location")
    r""" The location field of the nvme_interface_ip_interface. """

    @property
    def resource(self):
        return NvmeInterfaceIpInterface

    gettable_fields = [
        "links",
        "ip",
        "location",
    ]
    """links,ip,location,"""

    patchable_fields = [
        "ip",
        "location",
    ]
    """ip,location,"""

    postable_fields = [
        "ip",
        "location",
    ]
    """ip,location,"""


class NvmeInterfaceIpInterface(Resource):

    _schema = NvmeInterfaceIpInterfaceSchema
