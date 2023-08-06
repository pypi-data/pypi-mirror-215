r"""
Copyright &copy; 2023 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeConstituentsSpace", "VolumeConstituentsSpaceSchema"]
__pdoc__ = {
    "VolumeConstituentsSpaceSchema.resource": False,
    "VolumeConstituentsSpaceSchema.opts": False,
    "VolumeConstituentsSpace": False,
}


class VolumeConstituentsSpaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeConstituentsSpace object"""

    afs_total = Size(data_key="afs_total")
    r""" Total size of AFS, excluding snap-reserve, in bytes. """

    available = Size(data_key="available")
    r""" The available space, in bytes. """

    available_percent = Size(data_key="available_percent")
    r""" The space available, as a percent. """

    block_storage_inactive_user_data = Size(data_key="block_storage_inactive_user_data")
    r""" The size that is physically used in the block storage of the volume and has a cold temperature. In bytes. This parameter is only supported if the volume is in an aggregate that is either attached to a cloud store or could be attached to a cloud store. """

    capacity_tier_footprint = Size(data_key="capacity_tier_footprint")
    r""" Space used by capacity tier for this volume in the FabricPool aggregate, in bytes. """

    footprint = Size(data_key="footprint")
    r""" Data used for this volume in the aggregate, in bytes. """

    large_size_enabled = fields.Boolean(data_key="large_size_enabled")
    r""" Specifies whether the support for large volumes and large files is enabled on the volume. """

    local_tier_footprint = Size(data_key="local_tier_footprint")
    r""" Space used by the local tier for this volume in the aggregate, in bytes. """

    logical_space = fields.Nested("netapp_ontap.models.volume_constituents_space_logical_space.VolumeConstituentsSpaceLogicalSpaceSchema", unknown=EXCLUDE, data_key="logical_space")
    r""" The logical_space field of the volume_constituents_space. """

    metadata = Size(data_key="metadata")
    r""" Space used by the volume metadata in the aggregate, in bytes. """

    over_provisioned = Size(data_key="over_provisioned")
    r""" The amount of space not available for this volume in the aggregate, in bytes. """

    performance_tier_footprint = Size(data_key="performance_tier_footprint")
    r""" Space used by the performance tier for this volume in the FabricPool aggregate, in bytes. """

    size = Size(data_key="size")
    r""" Total provisioned size. The default size is equal to the minimum size of 20MB, in bytes. """

    snapshot = fields.Nested("netapp_ontap.models.volume_constituents_space_snapshot.VolumeConstituentsSpaceSnapshotSchema", unknown=EXCLUDE, data_key="snapshot")
    r""" The snapshot field of the volume_constituents_space. """

    total_footprint = Size(data_key="total_footprint")
    r""" Data and metadata used for this volume in the aggregate, in bytes. """

    used = Size(data_key="used")
    r""" The virtual space used (includes volume reserves) before storage efficiency, in bytes. """

    used_by_afs = Size(data_key="used_by_afs")
    r""" The space used by Active Filesystem, in bytes. """

    used_percent = Size(data_key="used_percent")
    r""" The virtual space used (includes volume reserves) before storage efficiency, as a percent. """

    @property
    def resource(self):
        return VolumeConstituentsSpace

    gettable_fields = [
        "afs_total",
        "available",
        "available_percent",
        "block_storage_inactive_user_data",
        "capacity_tier_footprint",
        "footprint",
        "large_size_enabled",
        "local_tier_footprint",
        "logical_space",
        "metadata",
        "over_provisioned",
        "performance_tier_footprint",
        "size",
        "snapshot",
        "total_footprint",
        "used",
        "used_by_afs",
        "used_percent",
    ]
    """afs_total,available,available_percent,block_storage_inactive_user_data,capacity_tier_footprint,footprint,large_size_enabled,local_tier_footprint,logical_space,metadata,over_provisioned,performance_tier_footprint,size,snapshot,total_footprint,used,used_by_afs,used_percent,"""

    patchable_fields = [
        "afs_total",
        "available_percent",
        "large_size_enabled",
        "logical_space",
        "size",
        "snapshot",
        "used_by_afs",
        "used_percent",
    ]
    """afs_total,available_percent,large_size_enabled,logical_space,size,snapshot,used_by_afs,used_percent,"""

    postable_fields = [
        "afs_total",
        "available_percent",
        "large_size_enabled",
        "logical_space",
        "size",
        "snapshot",
        "used_by_afs",
        "used_percent",
    ]
    """afs_total,available_percent,large_size_enabled,logical_space,size,snapshot,used_by_afs,used_percent,"""


class VolumeConstituentsSpace(Resource):

    _schema = VolumeConstituentsSpaceSchema
