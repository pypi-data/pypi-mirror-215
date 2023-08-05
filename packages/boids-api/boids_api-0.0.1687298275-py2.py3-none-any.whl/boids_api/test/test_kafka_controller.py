# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from boids_api.boids.boid import Boid  # noqa: E501
from boids_api.boids.system_event import SystemEvent  # noqa: E501
from boids_api.test import BaseTestCase


class TestKafkaController(BaseTestCase):
    """KafkaController integration test stubs"""

    def test_kafka_topic_boids_boids_get(self):
        """Test case for kafka_topic_boids_boids_get

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/kafka-topic/boids.boids',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_kafka_topic_boids_system_events_get(self):
        """Test case for kafka_topic_boids_system_events_get

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/kafka-topic/boids.system-events',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
