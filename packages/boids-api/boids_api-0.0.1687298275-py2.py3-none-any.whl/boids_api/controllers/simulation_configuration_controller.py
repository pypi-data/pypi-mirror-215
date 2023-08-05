import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from boids_api.boids.error_model import ErrorModel  # noqa: E501
from boids_api.boids.simulation_config_status import SimulationConfigStatus  # noqa: E501
from boids_api.boids.simulation_config_update_request import SimulationConfigUpdateRequest  # noqa: E501
from boids_api import util


def get_simulation_config():  # noqa: E501
    """get_simulation_config

    Get the current simulation configuration # noqa: E501


    :rtype: Union[SimulationConfigStatus, Tuple[SimulationConfigStatus, int], Tuple[SimulationConfigStatus, int, Dict[str, str]]
    """
    return 'do some magic!'


def put_simulation_config(simulation_config_update_request=None):  # noqa: E501
    """put_simulation_config

    Update the simulation configuration # noqa: E501

    :param simulation_config_update_request: 
    :type simulation_config_update_request: dict | bytes

    :rtype: Union[SimulationConfigStatus, Tuple[SimulationConfigStatus, int], Tuple[SimulationConfigStatus, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        simulation_config_update_request = SimulationConfigUpdateRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
