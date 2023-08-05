"""
    Delphix DCT API

    Delphix DCT API  # noqa: E501

    The version of the OpenAPI document: 3.3.0
    Contact: support@delphix.com
    Generated by: https://openapi-generator.tech
"""


import unittest

import delphix.api.gateway
from delphix.api.gateway.api.vcdbs_api import VCDBsApi  # noqa: E501


class TestVCDBsApi(unittest.TestCase):
    """VCDBsApi unit test stubs"""

    def setUp(self):
        self.api = VCDBsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_vcdb_tags(self):
        """Test case for create_vcdb_tags

        Create tags for a vCDB.  # noqa: E501
        """
        pass

    def test_delete_vcdb_tags(self):
        """Test case for delete_vcdb_tags

        Delete tags for a vCDB.  # noqa: E501
        """
        pass

    def test_get_tags_vcdb(self):
        """Test case for get_tags_vcdb

        Get tags for a vCDB.  # noqa: E501
        """
        pass

    def test_get_vcdb_by_id(self):
        """Test case for get_vcdb_by_id

        Get a CDB by ID (Oracle only).  # noqa: E501
        """
        pass

    def test_get_vcdbs(self):
        """Test case for get_vcdbs

        List all vCDBs (Oracle only).  # noqa: E501
        """
        pass

    def test_search_vcdbs(self):
        """Test case for search_vcdbs

        Search for vCDBs (Oracle only).  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
