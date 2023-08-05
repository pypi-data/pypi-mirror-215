import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from boids_api.boids.error_model import ErrorModel  # noqa: E501
from boids_api.boids.simulation_control_status import SimulationControlStatus  # noqa: E501
from boids_api.boids.simulation_control_update_request import SimulationControlUpdateRequest  # noqa: E501
from boids_api import util


def get_simulation():  # noqa: E501
    """get_simulation

    Get the current simulation status # noqa: E501


    :rtype: Union[SimulationControlStatus, Tuple[SimulationControlStatus, int], Tuple[SimulationControlStatus, int, Dict[str, str]]
    """
    return 'do some magic!'


def put_simulation(simulation_control_update_request=None):  # noqa: E501
    """put_simulation

    Modify the simulation state # noqa: E501

    :param simulation_control_update_request: 
    :type simulation_control_update_request: dict | bytes

    :rtype: Union[SimulationControlStatus, Tuple[SimulationControlStatus, int], Tuple[SimulationControlStatus, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        simulation_control_update_request = SimulationControlUpdateRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
