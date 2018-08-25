import aiohttp_jinja2
import jinja2

from model import Message, Agent
from message_types import UI


async def ui_connect(_, agent: Agent) -> Message:
    return Message(
        UI.STATE,
        None,  # No ID needed
        {
            'initialized': agent.initialized,
            'agent_name': agent.owner,
            'connections': [conn for _, conn in agent.connections.items()]
        }
    )

@aiohttp_jinja2
async def root(request):
    agent = request.app['agent']
    agent.offer_endpoint = request.url.scheme + '://' + request.url.host
    agent.endpoint = request.url.scheme + '://' + request.url.host
    if request.url.port is not None:
        agent.endpoint += ':' + str(request.url.port) + '/indy'
        agent.offer_endpoint += ':' + str(request.url.port) + '/offer'
    else:
        agent.endpoint += '/indy'
        agent.offer_endpoint += '/offer'
    return {'ui_token': agent.ui_token}