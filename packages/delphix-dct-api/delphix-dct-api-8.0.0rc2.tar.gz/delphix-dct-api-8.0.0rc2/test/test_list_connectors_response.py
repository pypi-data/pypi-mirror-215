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
from delphix.api.gateway.model.connector import Connector
from delphix.api.gateway.model.paginated_response_metadata import PaginatedResponseMetadata
globals()['Connector'] = Connector
globals()['PaginatedResponseMetadata'] = PaginatedResponseMetadata
from delphix.api.gateway.model.list_connectors_response import ListConnectorsResponse


class TestListConnectorsResponse(unittest.TestCase):
    """ListConnectorsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testListConnectorsResponse(self):
        """Test ListConnectorsResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ListConnectorsResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
