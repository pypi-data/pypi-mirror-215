import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from boids_api.boids.system_event_list import SystemEventList  # noqa: E501
from boids_api import util


def get_event(sort_field=None, sort_asc=None, page_offset=None, page_size=None):  # noqa: E501
    """get_event

    Retrieve system events in reverse time order (most recent first) # noqa: E501

    :param sort_field: Field name to sort by
    :type sort_field: str
    :param sort_asc: Sort ascending vs descending
    :type sort_asc: bool
    :param page_offset: Pagination offset (0-based)
    :type page_offset: int
    :param page_size: Pagination size
    :type page_size: int

    :rtype: Union[List[SystemEventList], Tuple[List[SystemEventList], int], Tuple[List[SystemEventList], int, Dict[str, str]]
    """
    return 'do some magic!'
