import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from boids_api.boids.boid import Boid  # noqa: E501
from boids_api.boids.boid_list import BoidList  # noqa: E501
from boids_api.boids.error_model import ErrorModel  # noqa: E501
from boids_api import util


def delete_boid(id):  # noqa: E501
    """delete_boid

     # noqa: E501

    :param id: 
    :type id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_boid(id, history=None):  # noqa: E501
    """get_boid

     # noqa: E501

    :param id: 
    :type id: int
    :param history: 
    :type history: int

    :rtype: Union[Boid, Tuple[Boid, int], Tuple[Boid, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_boid_list(sort_field=None, sort_asc=None, page_offset=None, page_size=None):  # noqa: E501
    """get_boid_list

    Return the list of Boids # noqa: E501

    :param sort_field: Field name to sort by
    :type sort_field: str
    :param sort_asc: Sort ascending vs descending
    :type sort_asc: bool
    :param page_offset: Pagination offset (0-based)
    :type page_offset: int
    :param page_size: Pagination size
    :type page_size: int

    :rtype: Union[BoidList, Tuple[BoidList, int], Tuple[BoidList, int, Dict[str, str]]
    """
    return 'do some magic!'


def post_boid(boid=None):  # noqa: E501
    """post_boid

    Create a Boid.  The &#39;id&#39; and &#39;timestamp&#39; fields must not be present. The newly created Boid is assigned an ID by the simulation.  # noqa: E501

    :param boid: 
    :type boid: dict | bytes

    :rtype: Union[Boid, Tuple[Boid, int], Tuple[Boid, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        boid = Boid.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
