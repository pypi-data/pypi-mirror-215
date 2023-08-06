import random
import re
import os
import getpass
import yaml
import time


import asyncio

import click

from glom import glom


from .main import main, CONTEXT_SETTINGS
from .config import (
    config,
    banner,
    RESET,
    BLUE,
    PINK,
    YELLOW,
    GREEN,
)


from ..sequencers import Sequencer, expand_network
from .. import parse_uri, soft, expandpath
from ..containers import gather_values, deindent_by
from ..mixer import save_yaml
from ..persistence import find_files

from pycelium.definitions import IP_INFO, REAL, ETC
from pycelium.shell import Reactor, DefaultExecutor, LoopContext
from pycelium.scanner import HostInventory
from pycelium.installer import Installer
from pycelium.pastor import Pastor


INVENTORY_ROOT = 'inventory/'


def extend_config(env):
    """Extend the config environment with some files."""
    cfg = env.__dict__

    # folders for searching
    parent = os.path.join(*os.path.split(os.path.dirname(__file__))[:-1])

    for p in [os.path.abspath("."), parent]:
        env.folders[p] = None


@main.group(context_settings=CONTEXT_SETTINGS)
@click.pass_obj
def inventory(env):
    # banner("User", env.__dict__)
    pass


# def get_or_create_eventloop():
# try:
# return asyncio.get_running_loop()
# except RuntimeError as ex:
# if "There is no current event loop in thread" in str(ex):
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# return asyncio.get_event_loop()


def explore_host(ctx, **kw):
    with LoopContext():
        # loop = get_or_create_eventloop()
        reactor = Reactor(env=ctx)
        conn = DefaultExecutor(retry=-1, **ctx)
        reactor.attach(conn)

        stm = HostInventory(daemon=False)
        # stm = Pastor(daemon=False)
        reactor.attach(stm)

        # magic ...
        asyncio.run(reactor.main())

        # loop.close()

    return reactor.ctx


def rename_host(ctx, hostname, **kw):
    with LoopContext():
        reactor = Reactor(env=ctx)
        conn = DefaultExecutor(retry=-1, **ctx)
        reactor.attach(conn)

        stm = RenameHost()
        reactor.attach(stm)

        # magic ...
        asyncio.run(reactor.main())

        return reactor.ctx


def get_mac(data):
    specs = {
        '.*enp.*mac.*': None,
        '.*enp.*type.*': 'ether',
        '.*wlo.*mac.*': None,
        '.*wlo.*type.*': 'ether',
        '.*ens.*mac.*': None,
        '.*ens.*type.*': 'ether',
    }
    blueprint = gather_values(data, **specs)

    # blueprint = deindent_by(blueprint, IP_INFO)
    if 'mac' in blueprint:
        if blueprint.get('type') in ('ether',):
            return blueprint.get('mac')

    keys = list(blueprint)
    keys.sort()
    for iface in keys:
        info = blueprint.get(iface)
        if info.get('type') in ('ether',):
            return info.get('mac')


HW_TAGGING_FILE = 'hardware.tagging.yaml'


def _get_host_tags(data):
    """Try to figure out which kind of node is"""
    blueprint = {
        r'processor.0.*address_sizes': '36\s+bits',
        r'processor.0.*model_name': '.*celeron.*',
        r'processor.0.*siblings': '4',
        r'processor.0.*stepping': '8',
        r'ip.enp1s0.*type': 'ether',
    }
    keys = ['address_sizes', 'model_name', 'siblings', 'stepping', 'type']

    tags = ['node', 'venoen', 'ntp']

    block = {
        'blueprint': blueprint,
        'keys': keys,
        'tags': tags,
    }

    info = {}
    info['venoen'] = block

    yaml.dump(
        info, stream=open('hardware.tagging.yaml', 'w'), Dumper=yaml.Dumper
    )

    info = gather_values(data, **blueprint)

    return


def get_host_tags(data):
    """Try to figure out which kind of node is 'data'

    Datase looks like:

    venoen:
        blueprint:
          ip.enp1s0.*type: ether
          processor.0.*address_sizes: 36\s+bits
          processor.0.*model_name: .*celeron.*
          processor.0.*siblings: '4'
          processor.0.*stepping: '8'
        keys:
        - address_sizes
        - model_name
        - siblings
        - stepping
        - type
        tags:
        - node
        - venoen



    """
    db = yaml.load(open(HW_TAGGING_FILE), Loader=yaml.Loader)
    tags = set()
    for name, info in db.items():
        blueprint = info['blueprint']
        values = gather_values(data, **blueprint)
        keys = set(info['keys'])
        if keys.issubset(values):
            tags.update(info['tags'])
            tags.add(name)
    tags = list(tags)
    tags.sort()
    return tags


def gen_credentials(network, user, password=[], env={}, shuffle=False):
    used = set()
    for pattern in network:
        seq = expand_network(pattern)  # iterator for erally large ranges

        # print(f"Exploring: {pattern}  --> {total} items")
        for addr in seq:
            addr = '.'.join(addr)
            for i, cred in enumerate(user):
                # test initial uri
                uri = f'{cred}@{addr}'
                if False and uri not in used:  # TODO: remove False
                    yield uri
                    used.add(uri)

                # test without passwd and default password
                m = re.match(r'(?P<user>[^:]+)(?P<password>.*)?', cred)
                if m:
                    _user, _password = m.groups()
                    # test adding no passwd
                    uri = f'{_user}@{addr}'
                    if False and uri not in used:  # TODO: remove False
                        yield uri
                        used.add(uri)

                for _passwd in password:
                    #  test with default passwd
                    uri = f'{_user}:{_passwd}@{addr}'
                    if uri not in used:
                        yield uri
                        used.add(uri)

                _password = env.get('password')
                if _password:
                    #  test with default passwd
                    uri = f'{_user}:{_password}@{addr}'
                    if uri not in used:
                        yield uri
                        used.add(uri)


def credentials(network, user, shuffle=False, password=None, env={}, **kw):
    """
    password is the default password when is not provided
    """
    if isinstance(network, str):
        network = [network]

    if isinstance(user, str):
        user = [user]

    if not user:
        user = [getpass.getuser()]

    if isinstance(password, str):
        password = [password]

    total = 1
    if shuffle:
        universe = list(
            gen_credentials(network, user, password, env, shuffle)
        )
        random.shuffle(universe)
        total = len(universe)
    else:
        total = len(user)
        for pattern in network:
            seq = expand_network(pattern)
            total *= seq.total

        universe = gen_credentials(network, user, password, env, shuffle)

    for i, uri in enumerate(universe):
        ctx = parse_uri(uri)
        ctx['uri'] = uri
        ctx['_progress'] = i / total
        soft(ctx, user=getpass.getuser(), host='localhost')

        if ctx.get('password'):
            # ctx['shadow'] = ':' + '*' * len(ctx['password'])
            ctx['shadow'] = ':' + str(ctx.get('password'))

        else:
            ctx['shadow'] = ''

        ctx['_printable_uri'] = "{user}{shadow}@{host}".format_map(ctx)

        yield ctx


@inventory.command()
# @click.argument('filename', default='sample.gan')
@click.option("--network", multiple=True)
@click.option("--user", multiple=True, default=['user'])
@click.option("--password", multiple=True, default=['123456'])
@click.option("--shuffle", default=True, type=bool)
@click.option("--cycles", default=1, type=int)
@click.pass_obj
def explore(env, network, user, shuffle, password, cycles):
    """
    - [ ] get users from config yaml file or command line
    """
    config.callback()

    conquered = dict()
    ctx = dict(env.__dict__)

    top = expandpath(INVENTORY_ROOT)
    while cycles != 0:
        print(f"{YELLOW} Remain cycles: {cycles}{RESET}")
        cycles -= 1
        print(f"network: {network}")
        print(f"user: {user}")
        for ctx in credentials(
            network, user, shuffle, password, env.__dict__
        ):
            print("{_progress:.2%} {_printable_uri:>40}".format_map(ctx))
            host = ctx['host']
            if host in conquered:
                print(f"{host} is alredy conquered! :), skiping")
                continue

            data, path = explore_single_host(ctx, host)
            if data:
                ctx['observed_hostname'] = observed_hostname = (
                    data.get('observed_hostname') or host
                )
                conquered[host] = data
                conquered[observed_hostname] = data

                foo = 1
        time.sleep(10)


def explore_single_host(ctx, host, top=None, save=False):
    data = explore_host(ctx)

    mac = get_mac(data)
    if mac:
        if save:
            data, path = save_blueprint(data, default_host=host, **ctx)
            return data, path
        return data, None
    return {}, None


def save_blueprint(data, default_host, top='.', **ctx):
    # ABAILABLE = set('')
    mac = get_mac(data)
    if mac:
        mac = mac.replace(':', '')

        ctx['observed_hostname'] = observed_hostname = glom(
            data, 'real.etc.hostname', default=default_host
        )

        # data = data.get('real')
        tags = get_host_tags(data)
        _tags = '/'.join(tags)
        path = f"{top}/{_tags}/{observed_hostname}.{mac}.yaml"
        data['_context'] = ctx
        data['_tags'] = tags

        save_yaml(data, path)
        return data, path
    return {}, None


@inventory.command()
# @click.argument('filename', default='sample.gan')
@click.option("--email", default=None)
@click.option("--cost", default=30)
@click.pass_obj
def show(env, email, cost=0):
    config.callback()
    top = expandpath(INVENTORY_ROOT) + '/'
    found = find_files(top, includes=['.*yaml'])
    lines = {k.split(top)[-1]: v for k, v in found.items()}

    banner("Inventory", lines=lines)
    foo = 1


@inventory.command()
# @click.argument('filename', default='sample.gan')
@click.option("--email", default=None)
@click.option("--cost", default=30)
@click.pass_obj
def query(env, email, cost=0):
    raise NotImplementedError("not yet!")
