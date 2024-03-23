import ipaddress

from fastapi import HTTPException, status
from dataclasses import dataclass
from typing import List, Type

from sqlalchemy.orm import Session

from src.models.network import Network


@dataclass(slots=True)
class NetworkValidatedData:
    valid_interfaces: List[Type[Network]]
    invalid_interfaces: List[int]
    not_exists_interfaces: List[int]
    already_assign_interface: List[Type[Network]]

    def is_valid(self) -> bool:
        if any((self.invalid_interfaces, self.not_exists_interfaces, self.invalid_interfaces,)):
            return False

        return True


class NetworkInterfaceValidator:

    def __init__(self):
        self.data: NetworkValidatedData = NetworkValidatedData(
            valid_interfaces=[],
            invalid_interfaces=[],
            already_assign_interface=[],
            not_exists_interfaces=[],
        )

    def validate(self, session: Session, networks_id: List[int]) -> None:
        networks_obj: List[Type[Network]] = session.query(Network).filter(Network.id.in_(networks_id)).all()

        not_exists_id = set(networks_id).difference(set(obj.id for obj in networks_obj))

        if not_exists_id:
            self.data.not_exists_interfaces.extend(not_exists_id)

        for obj in networks_obj:
            if obj.device:
                self.data.already_assign_interface.append(obj)
                continue

            if ipaddress.IPv4Network(obj.network).num_addresses != 1:
                self.data.invalid_interfaces.append(obj.id)
                continue

            self.data.valid_interfaces.append(obj)

    def raise_error(self):
        if self.data.invalid_interfaces:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'invalid networks for host: {self.data.invalid_interfaces}'
            )

        if self.data.already_assign_interface:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'networks already assign to another device: {self.data.already_assign_interface}'
            )

        if self.data.not_exists_interfaces:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'networks does not exists: {self.data.not_exists_interfaces}'
            )
