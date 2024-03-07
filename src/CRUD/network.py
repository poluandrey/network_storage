import ipaddress

from fastapi import HTTPException, status
from sqlalchemy.dialects.postgresql import insert

from src.depends import SessionDep
from src.models.network import Network
from src.schemas.network import NetworkCreate, NetworkRead


async def networks_get(session: SessionDep, offset: int = 0, limit: int = 100):
    networks = session.query(Network).offset(offset).limit(limit=limit)
    return networks.all()


async def network_read(network: Network):
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


async def network_delete(session: SessionDep, network: Network):
    if network.sub_networks:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='could not delete networks with subnetworks')

    session.delete(network)
    session.commit()
    return


async def network_split_by_host(session: SessionDep, network: Network):
    parent_network_interface = ipaddress.IPv4Network(network.network)
    hosts = list(parent_network_interface.hosts())

    if not hosts:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='could not split by host')

    hosts_obj = [NetworkCreate(network=host, parent_id=network.id) for host in hosts]
    created_hosts = session.scalars(insert(Network).on_conflict_do_nothing().returning(Network), hosts_obj).all()

    if not created_hosts:
        return []

    session.commit()

    if isinstance(created_hosts, Network):
        session.refresh(created_hosts)
        created_hosts = [created_hosts]
        return created_hosts

    for host in created_hosts:
        session.refresh(host)

    return created_hosts


async def network_split(session: SessionDep, network: Network, network_prefix: int):
    parent_network_interface = ipaddress.IPv4Network(network.network)

    try:
        new_networks = parent_network_interface.subnets(new_prefix=network_prefix)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid network prefix')

    new_networks_obj = [NetworkCreate(network=new_network, parent_id=network.id) for new_network in new_networks]
    created_networks = session.scalars(
        insert(Network).on_conflict_do_nothing().returning(Network), new_networks_obj
    ).all()
    print(created_networks)

    session.commit()
    if not created_networks:
        return []

    if isinstance(created_networks, Network):
        session.refresh(created_networks)
        created_hosts = [created_networks]
        return created_hosts

    for network in created_networks:
        session.refresh(network)

    return created_networks
