"""
    Delphix DCT API

    Delphix DCT API  # noqa: E501

    The version of the OpenAPI document: 3.3.0
    Contact: support@delphix.com
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import delphix.api.gateway
from delphix.api.gateway.model.dataset_group import DatasetGroup
from delphix.api.gateway.model.paginated_response_metadata import PaginatedResponseMetadata
globals()['DatasetGroup'] = DatasetGroup
globals()['PaginatedResponseMetadata'] = PaginatedResponseMetadata
from delphix.api.gateway.model.list_groups_response import ListGroupsResponse


class TestListGroupsResponse(unittest.TestCase):
    """ListGroupsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testListGroupsResponse(self):
        """Test ListGroupsResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ListGroupsResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
