import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from boids_api.boids.boid import Boid  # noqa: E501
from boids_api.boids.system_event import SystemEvent  # noqa: E501
from boids_api import util


def kafka_topic_boids_boids_get():  # noqa: E501
    """kafka_topic_boids_boids_get

     # noqa: E501


    :rtype: Union[Boid, Tuple[Boid, int], Tuple[Boid, int, Dict[str, str]]
    """
    return 'do some magic!'


def kafka_topic_boids_system_events_get():  # noqa: E501
    """kafka_topic_boids_system_events_get

     # noqa: E501


    :rtype: Union[SystemEvent, Tuple[SystemEvent, int], Tuple[SystemEvent, int, Dict[str, str]]
    """
    return 'do some magic!'
