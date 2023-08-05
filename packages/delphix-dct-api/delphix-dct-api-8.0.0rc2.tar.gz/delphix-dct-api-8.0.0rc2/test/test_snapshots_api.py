"""
    Delphix DCT API

    Delphix DCT API  # noqa: E501

    The version of the OpenAPI document: 3.3.0
    Contact: support@delphix.com
    Generated by: https://openapi-generator.tech
"""


import unittest

import delphix.api.gateway
from delphix.api.gateway.api.snapshots_api import SnapshotsApi  # noqa: E501


class TestSnapshotsApi(unittest.TestCase):
    """SnapshotsApi unit test stubs"""

    def setUp(self):
        self.api = SnapshotsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_snapshot_tags(self):
        """Test case for create_snapshot_tags

        Create tags for a Snapshot.  # noqa: E501
        """
        pass

    def test_delete_snapshot(self):
        """Test case for delete_snapshot

        Delete a Snapshot.  # noqa: E501
        """
        pass

    def test_delete_snapshot_tags(self):
        """Test case for delete_snapshot_tags

        Delete tags for a Snapshot.  # noqa: E501
        """
        pass

    def test_find_by_location(self):
        """Test case for find_by_location

        Get the snapshots at this location for a dataset.  # noqa: E501
        """
        pass

    def test_find_by_timestamp(self):
        """Test case for find_by_timestamp

        Get the snapshots at this timestamp for a dataset.  # noqa: E501
        """
        pass

    def test_get_snapshot_by_id(self):
        """Test case for get_snapshot_by_id

        Get a Snapshot by ID.  # noqa: E501
        """
        pass

    def test_get_snapshot_tags(self):
        """Test case for get_snapshot_tags

        Get tags for a Snapshot.  # noqa: E501
        """
        pass

    def test_get_snapshot_timeflow_range(self):
        """Test case for get_snapshot_timeflow_range

        Return the provisionable timeflow range based on a specific snapshot.  # noqa: E501
        """
        pass

    def test_get_snapshots(self):
        """Test case for get_snapshots

        Retrieve the list of snapshots.  # noqa: E501
        """
        pass

    def test_search_snapshots(self):
        """Test case for search_snapshots

        Search snapshots.  # noqa: E501
        """
        pass

    def test_unset_snapshot_retention(self):
        """Test case for unset_snapshot_retention

        Unset a Snapshot's expiration, removing expiration and retain_forever values for the snapshot.  # noqa: E501
        """
        pass

    def test_update_snapshot(self):
        """Test case for update_snapshot

        Update values of a Snapshot.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
