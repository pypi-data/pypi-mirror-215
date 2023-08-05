"""
    Delphix DCT API

    Delphix DCT API  # noqa: E501

    The version of the OpenAPI document: 3.3.0
    Contact: support@delphix.com
    Generated by: https://openapi-generator.tech
"""


import unittest

import delphix.api.gateway
from delphix.api.gateway.api.cdbs_api import CDBsApi  # noqa: E501


class TestCDBsApi(unittest.TestCase):
    """CDBsApi unit test stubs"""

    def setUp(self):
        self.api = CDBsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_cdb_tags(self):
        """Test case for create_cdb_tags

        Create tags for a CDB.  # noqa: E501
        """
        pass

    def test_delete_cdb_tags(self):
        """Test case for delete_cdb_tags

        Delete tags for a CDB.  # noqa: E501
        """
        pass

    def test_get_cdb_by_id(self):
        """Test case for get_cdb_by_id

        Get a CDB by ID (Oracle only).  # noqa: E501
        """
        pass

    def test_get_cdbs(self):
        """Test case for get_cdbs

        List all CDBs (Oracle only).  # noqa: E501
        """
        pass

    def test_get_tags_cdb(self):
        """Test case for get_tags_cdb

        Get tags for a CDB.  # noqa: E501
        """
        pass

    def test_search_cdbs(self):
        """Test case for search_cdbs

        Search for CDBs (Oracle only).  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
