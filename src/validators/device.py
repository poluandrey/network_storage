import ipaddress
from dataclasses import dataclass
from typing import List, Type

from sqlalchemy.orm import Session

from src.models.network import Network


@dataclass(slots=True)
class ValidatedNetwork:
    valid_interfaces: List[Type[Network]]
    invalid_interfaces: List[int]
    not_exists_interfaces: List[int]


def device_create_network_validator(networks_id: List[int], session: Session) -> ValidatedNetwork:
    validate_data = ValidatedNetwork(valid_interfaces=[], invalid_interfaces=[], not_exists_interfaces=[])
    for interface_id in networks_id:
        interface_obj = session.get(Network, interface_id)

        if not interface_obj:
            validate_data.not_exists_interfaces.append(interface_id)

        interface = ipaddress.IPv4Network(interface_obj)

        if interface.num_addresses != 1:
            validate_data.invalid_interfaces.append(interface_id)

        validate_data.valid_interfaces.append(interface_obj)

    return validate_data
