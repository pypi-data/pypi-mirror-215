# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from boids_api.boids.system_event_list import SystemEventList  # noqa: E501
from boids_api.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_get_event(self):
        """Test case for get_event

        
        """
        query_string = [('sort_field', '_id'),
                        ('sort_asc', True),
                        ('page_offset', 0),
                        ('page_size', 30)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/event',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
