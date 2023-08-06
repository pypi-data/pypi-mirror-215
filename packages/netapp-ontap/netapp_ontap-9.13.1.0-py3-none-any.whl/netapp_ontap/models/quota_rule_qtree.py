r"""
Copyright &copy; 2023 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["QuotaRuleQtree", "QuotaRuleQtreeSchema"]
__pdoc__ = {
    "QuotaRuleQtreeSchema.resource": False,
    "QuotaRuleQtreeSchema.opts": False,
    "QuotaRuleQtree": False,
}


class QuotaRuleQtreeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the QuotaRuleQtree object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links")
    r""" The links field of the quota_rule_qtree. """

    id = Size(data_key="id")
    r""" The unique identifier for a qtree.

Example: 1 """

    name = fields.Str(data_key="name")
    r""" The name of the qtree.

Example: qt1 """

    @property
    def resource(self):
        return QuotaRuleQtree

    gettable_fields = [
        "links",
        "id",
        "name",
    ]
    """links,id,name,"""

    patchable_fields = [
        "name",
    ]
    """name,"""

    postable_fields = [
        "name",
    ]
    """name,"""


class QuotaRuleQtree(Resource):

    _schema = QuotaRuleQtreeSchema
