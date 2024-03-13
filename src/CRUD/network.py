import ipaddress
import logging

from fastapi import HTTPException, status
from sqlalchemy.dialects.postgresql import insert

from src.depends import SessionDep
from src.models.network import Network
from src.schemas.network import NetworkCreate, NetworkRead, NetworkSplit

logger = logging.getLogger('network')


async def networks_get(session: SessionDep, request_id: str, offset: int = 0, limit: int = 100):
    logger.info(f'[{request_id}] start handling')
    networks = session.query(Network).offset(offset).limit(limit=limit)
    logger.info(f'[{request_id}] finished handling')
    return networks.all()


async def network_read(network: Network, request_id: str):
    logger.debug(f'[{request_id}] start handling')
    logger.debug(f'[{request_id}] finished handling')
    return NetworkRead(
        id=network.id,
        network=network.network,
        create_at=network.create_at,
        last_update=network.last_update,
        parent_network=network.parent_network,
        sub_networks=network.sub_networks,
    )


async def network_create(session: SessionDep, network: NetworkCreate, request_id):
    logger.info(f'[{request_id}] start handling')
    try:
        network_interface = ipaddress.IPv4Network(network.network)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid network')

    if session.query(Network).filter(Network.network == str(network_interface)).first():
        logger.warning(f'[{request_id}] network: {network.network} already exists')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='network already exists')

    if network.parent_id:
        parent_network = session.get(Network, network.parent_id)

        if not parent_network:
            logger.warning(f'[{request_id}] parent_network_id: {network.parent_id} does not exists')
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='parent network does not exists')

        parent_interface = ipaddress.IPv4Network(parent_network.network)

        if not network_interface.subnet_of(parent_interface):
            logger.warning(f'[{request_id}] network: {network.network} is not a subnetwork of {parent_network.network}')
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'network is not a subnetwork of {parent_network.network}'
            )

    if not network.parent_id and not list(network_interface.hosts()):
        logger.warning(f'[{request_id} could not create host: {network.network} without parent network')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='please provide parent network for host'
        )

    network = Network(network=network.network, parent_id=network.parent_id)
    session.add(network)
    session.commit()
    session.refresh(network)
    logger.info(f'[{request_id} network: {network.network} created')
    logger.info(f'[{request_id}] finished handling')
    return network


async def network_delete(session: SessionDep, network: Network, request_id: str):
    logger.info(f'[{request_id}] start handling')
    if network.sub_networks:
        logger.warning(f'[{request_id}] could not delete network {network.network} with subnetworks')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='could not delete networks with subnetworks')

    session.delete(network)
    session.commit()
    logger.info(f'[{request_id}] {network.network} deleted')
    logger.info(f'[{request_id}] finished handling')
    return


async def network_split_by_host(session: SessionDep, network: Network, request_id: str):
    logger.info(f'[{request_id}] start handling')
    parent_network_interface = ipaddress.IPv4Network(network.network)
    hosts = list(parent_network_interface.hosts())
    logger.info(f'[{request_id}] start create hosts: {hosts}')
    if not hosts:
        logger.warning(f'[{request_id}] nothing to create')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='could not split by host')

    hosts_obj = [NetworkCreate(network=host, parent_id=network.id) for host in hosts]
    created_hosts = session.scalars(insert(Network).on_conflict_do_nothing().returning(Network), hosts_obj).all()

    if not created_hosts:
        logger.info(f'[{request_id}] all hosts already exists')
        logger.info(f'[{request_id}] finished handling')
        return NetworkSplit(
            network=[],
            count=0
        )

    session.commit()

    if isinstance(created_hosts, Network):
        session.refresh(created_hosts)
        created_hosts = [created_hosts]
        logger.info(f'[{request_id} host: {created_hosts} was create')
        logger.info(f'[{request_id}] finished handling')
        return NetworkSplit(
            networks=created_hosts,
            count=1,
        )

    for host in created_hosts:
        session.refresh(host)
    logger.info(f'[{request_id} host: {created_hosts} was create')
    logger.info(f'[{request_id}] finished handling')
    return NetworkSplit(
        networks=created_hosts,
        count=len(created_hosts)
    )


async def network_split(session: SessionDep, network: Network, network_prefix: int, request_id: str):
    logger.info(f'[{request_id}] start handling')
    parent_network_interface = ipaddress.IPv4Network(network.network)

    try:
        new_networks = parent_network_interface.subnets(new_prefix=network_prefix)
    except ValueError:
        logger.warning(f'[{request_id}] could not split network {network.network} by prefix {network_prefix}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid network prefix')

    new_networks_obj = [NetworkCreate(network=new_network, parent_id=network.id) for new_network in new_networks]
    logger.info(f'[{request_id}] start create hosts: {new_networks_obj}')

    created_networks = session.scalars(
        insert(Network).on_conflict_do_nothing().returning(Network), new_networks_obj
    ).all()
    logger.info(f'[{request_id}] created networks: {created_networks}')

    if not created_networks:
        logger.info(f'[{request_id}] finished handling')
        return NetworkSplit(
            count=0
        )
    session.commit()
    if isinstance(created_networks, Network):
        session.refresh(created_networks)
        created_hosts = [created_networks]
        logger.info(f'[{request_id}] finished handling')
        return NetworkSplit(
            networks=created_hosts,
            count=1,
        )

    for network in created_networks:
        session.refresh(network)
    logger.info(f'[{request_id}] finished handling')
    return NetworkSplit(
        networks=created_networks,
        count=len(created_networks)
    )
