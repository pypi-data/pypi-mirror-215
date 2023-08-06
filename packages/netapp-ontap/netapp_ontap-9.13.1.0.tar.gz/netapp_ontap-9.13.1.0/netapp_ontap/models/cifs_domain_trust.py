r"""
Copyright &copy; 2023 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["CifsDomainTrust", "CifsDomainTrustSchema"]
__pdoc__ = {
    "CifsDomainTrustSchema.resource": False,
    "CifsDomainTrustSchema.opts": False,
    "CifsDomainTrust": False,
}


class CifsDomainTrustSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CifsDomainTrust object"""

    home_domain = fields.Str(data_key="home_domain")
    r""" Home Domain Name """

    node = fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node")
    r""" The node field of the cifs_domain_trust. """

    trusted_domains = fields.List(fields.Str, data_key="trusted_domains")
    r""" Trusted Domain Name """

    @property
    def resource(self):
        return CifsDomainTrust

    gettable_fields = [
        "home_domain",
        "node.links",
        "node.name",
        "node.uuid",
        "trusted_domains",
    ]
    """home_domain,node.links,node.name,node.uuid,trusted_domains,"""

    patchable_fields = [
        "home_domain",
        "node.name",
        "node.uuid",
        "trusted_domains",
    ]
    """home_domain,node.name,node.uuid,trusted_domains,"""

    postable_fields = [
        "home_domain",
        "node.name",
        "node.uuid",
        "trusted_domains",
    ]
    """home_domain,node.name,node.uuid,trusted_domains,"""


class CifsDomainTrust(Resource):

    _schema = CifsDomainTrustSchema
