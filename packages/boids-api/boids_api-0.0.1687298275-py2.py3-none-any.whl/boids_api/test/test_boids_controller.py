# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from boids_api.boids.boid import Boid  # noqa: E501
from boids_api.boids.boid_list import BoidList  # noqa: E501
from boids_api.boids.error_model import ErrorModel  # noqa: E501
from boids_api.test import BaseTestCase


class TestBoidsController(BaseTestCase):
    """BoidsController integration test stubs"""

    def test_delete_boid(self):
        """Test case for delete_boid

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/boid/{id}'.format(id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_boid(self):
        """Test case for get_boid

        
        """
        query_string = [('history', 0)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/boid/{id}'.format(id=56),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_boid_list(self):
        """Test case for get_boid_list

        
        """
        query_string = [('sort_field', '_id'),
                        ('sort_asc', True),
                        ('page_offset', 0),
                        ('page_size', 30)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/boid',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_boid(self):
        """Test case for post_boid

        
        """
        boid = {"id":"id","position":{"x":6.027456183070403,"y":1.4658129805029452,"z":5.962133916683182},"velocity":{"x":6.027456183070403,"y":1.4658129805029452,"z":5.962133916683182},"history":[null,null],"timestamp":{"elapsed_time":"elapsed_time","wall_clock":"2000-01-23T04:56:07.000+00:00","tick":0}}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/boid',
            method='POST',
            headers=headers,
            data=json.dumps(boid),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
