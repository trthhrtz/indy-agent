import json
from aiohttp import web
from indy import wallet

async def initialize_agent(request):
    print("initializing agent")
    agent = request.app['agent']
    data = await request.post()
    agent.me = data['agent_name']

    wallet_name = '%s-wallet' % agent.me

    try:
        await wallet.create_wallet('pool1', wallet_name, None, None, None)
    except Exception as e:
        pass

    try:
        agent.wallet_handle = await wallet.open_wallet(wallet_name, None, None)
    except Exception as e:
        print("Could not open wallet!")
        raise web.HTTPBadRequest

    agent.initialized = True

    raise web.HTTPFound('/')