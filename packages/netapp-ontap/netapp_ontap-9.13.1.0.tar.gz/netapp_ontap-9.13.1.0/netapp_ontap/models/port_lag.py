r"""
Copyright &copy; 2023 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["PortLag", "PortLagSchema"]
__pdoc__ = {
    "PortLagSchema.resource": False,
    "PortLagSchema.opts": False,
    "PortLag": False,
}


class PortLagSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the PortLag object"""

    active_ports = fields.List(fields.Nested("netapp_ontap.resources.port.PortSchema", unknown=EXCLUDE), data_key="active_ports")
    r""" Active ports of a LAG (ifgrp). (Some member ports may be inactive.) """

    distribution_policy = fields.Str(data_key="distribution_policy")
    r""" Policy for mapping flows to ports for outbound packets through a LAG (ifgrp).

Valid choices:

* port
* ip
* mac
* sequential """

    member_ports = fields.List(fields.Nested("netapp_ontap.resources.port.PortSchema", unknown=EXCLUDE), data_key="member_ports")
    r""" Array of ports belonging to the LAG, regardless of their state. """

    mode = fields.Str(data_key="mode")
    r""" Determines how the ports interact with the switch.

Valid choices:

* multimode_lacp
* multimode
* singlemode """

    @property
    def resource(self):
        return PortLag

    gettable_fields = [
        "active_ports.links",
        "active_ports.name",
        "active_ports.node",
        "active_ports.uuid",
        "distribution_policy",
        "member_ports.links",
        "member_ports.name",
        "member_ports.node",
        "member_ports.uuid",
        "mode",
    ]
    """active_ports.links,active_ports.name,active_ports.node,active_ports.uuid,distribution_policy,member_ports.links,member_ports.name,member_ports.node,member_ports.uuid,mode,"""

    patchable_fields = [
        "member_ports.name",
        "member_ports.node",
        "member_ports.uuid",
    ]
    """member_ports.name,member_ports.node,member_ports.uuid,"""

    postable_fields = [
        "distribution_policy",
        "member_ports.name",
        "member_ports.node",
        "member_ports.uuid",
        "mode",
    ]
    """distribution_policy,member_ports.name,member_ports.node,member_ports.uuid,mode,"""


class PortLag(Resource):

    _schema = PortLagSchema
