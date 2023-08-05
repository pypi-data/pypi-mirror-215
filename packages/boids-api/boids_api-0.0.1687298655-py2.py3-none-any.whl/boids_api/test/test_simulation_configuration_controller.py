# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from boids_api.boids.error_model import ErrorModel  # noqa: E501
from boids_api.boids.simulation_config_status import SimulationConfigStatus  # noqa: E501
from boids_api.boids.simulation_config_update_request import SimulationConfigUpdateRequest  # noqa: E501
from boids_api.test import BaseTestCase


class TestSimulationConfigurationController(BaseTestCase):
    """SimulationConfigurationController integration test stubs"""

    def test_get_simulation_config(self):
        """Test case for get_simulation_config

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/config',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_simulation_config(self):
        """Test case for put_simulation_config

        
        """
        simulation_config_update_request = {"world_config":{"width":0,"height":6},"boids_config":{"avoid_walls":True,"speed_limits":{"min":1,"max":5},"quantity":5,"view_angle":253,"normalize_velocity":True,"view_range":2}}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/config',
            method='PUT',
            headers=headers,
            data=json.dumps(simulation_config_update_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
