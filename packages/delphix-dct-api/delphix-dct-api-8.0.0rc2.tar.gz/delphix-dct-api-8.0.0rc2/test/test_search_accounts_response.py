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
from delphix.api.gateway.model.account import Account
from delphix.api.gateway.model.paginated_response_metadata import PaginatedResponseMetadata
globals()['Account'] = Account
globals()['PaginatedResponseMetadata'] = PaginatedResponseMetadata
from delphix.api.gateway.model.search_accounts_response import SearchAccountsResponse


class TestSearchAccountsResponse(unittest.TestCase):
    """SearchAccountsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSearchAccountsResponse(self):
        """Test SearchAccountsResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SearchAccountsResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
