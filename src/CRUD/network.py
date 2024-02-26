import ipaddress

from fastapi import HTTPException, status

from src.depends import SessionDep
from src.models.network import Network
from src.schemas.network import NetworkRead, NetworkCreate


async def networks_get(session: SessionDep, offset: int = 0, limit: int = 100):
    networks = session.query(Network).offset(offset).limit(limit=limit)
    return networks.all()


async def network_read(session: SessionDep, id: int):
    network = session.query(Network).filter(Network.id == id).first()

    if not network:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='network does not found')

    return NetworkRead(
        id=network.id,
        network=network.network,
        create_at=network.create_at,
        last_update=network.last_update,
        parent_network=network.parent_network,
        sub_networks=network.sub_networks,
    )


async def network_create(session: SessionDep, network: NetworkCreate):
    try:
        network_interface = ipaddress.IPv4Network(network.network)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid network')

    if session.query(Network).filter(Network.network == str(network_interface)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='network already exists')

    if network.parent_id:
        parent_network = session.get(Network, network.parent_id)

        if not parent_network:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='parent network does not exists')

        parent_interface = ipaddress.IPv4Network(parent_network.network)

        if not network_interface.subnet_of(parent_interface):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'network is not a subnetwork of {parent_network.network}'
            )

    if not network.parent_id and not list(network_interface.hosts()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='please provide parent network for host'
        )

    network = Network(network=network.network, parent_id=network.parent_id)
    session.add(network)
    session.commit()
    session.refresh(network)

    return network


async def network_delete(session: SessionDep, network_id: int):
    print(network_id)
    network = session.get(Network, network_id)
    if not network:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='network does not exists'
        )
    session.delete(network)
    session.commit()
    return
