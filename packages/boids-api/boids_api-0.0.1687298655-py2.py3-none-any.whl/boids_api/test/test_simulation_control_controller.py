# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from boids_api.boids.error_model import ErrorModel  # noqa: E501
from boids_api.boids.simulation_control_status import SimulationControlStatus  # noqa: E501
from boids_api.boids.simulation_control_update_request import SimulationControlUpdateRequest  # noqa: E501
from boids_api.test import BaseTestCase


class TestSimulationControlController(BaseTestCase):
    """SimulationControlController integration test stubs"""

    def test_get_simulation(self):
        """Test case for get_simulation

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/simulation',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_simulation(self):
        """Test case for put_simulation

        
        """
        simulation_control_update_request = {"rate":0.8008282}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/simulation',
            method='PUT',
            headers=headers,
            data=json.dumps(simulation_control_update_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
