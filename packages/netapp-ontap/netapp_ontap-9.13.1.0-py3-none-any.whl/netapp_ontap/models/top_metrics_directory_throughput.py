r"""
Copyright &copy; 2023 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["TopMetricsDirectoryThroughput", "TopMetricsDirectoryThroughputSchema"]
__pdoc__ = {
    "TopMetricsDirectoryThroughputSchema.resource": False,
    "TopMetricsDirectoryThroughputSchema.opts": False,
    "TopMetricsDirectoryThroughput": False,
}


class TopMetricsDirectoryThroughputSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TopMetricsDirectoryThroughput object"""

    error = fields.Nested("netapp_ontap.models.top_metric_value_error_bounds.TopMetricValueErrorBoundsSchema", unknown=EXCLUDE, data_key="error")
    r""" The error field of the top_metrics_directory_throughput. """

    read = Size(data_key="read")
    r""" Average number of read bytes received per second.

Example: 3 """

    write = Size(data_key="write")
    r""" Average number of write bytes received per second.

Example: 20 """

    @property
    def resource(self):
        return TopMetricsDirectoryThroughput

    gettable_fields = [
        "error",
        "read",
        "write",
    ]
    """error,read,write,"""

    patchable_fields = [
        "error",
    ]
    """error,"""

    postable_fields = [
        "error",
    ]
    """error,"""


class TopMetricsDirectoryThroughput(Resource):

    _schema = TopMetricsDirectoryThroughputSchema
