from bot.rumplenator import Rumplenator
from unittest.mock import patch, AsyncMock
import pytest
import asyncio

# equivalent of annotating all tests with @pytest.mark.asyncio
pytestmark = pytest.mark.asyncio


@pytest.fixture()
def cleanup():
    '''
    The twitch bot automatically creates a bunch of Tasks upon initialization.
    (see: twitchio.websocket.PubSub.handle_ping)
    We need to cancel them manually otherwise we get warnings in the logs
    '''
    yield # instructs fixture to be run after tests
    for task in list(asyncio.all_tasks()):
        if (task.get_coro().__name__ == 'handle_ping'):
            task.cancel()


@patch('bot.rumplenator.Context')
async def test_whip_command_response(mock_context):
    ctx = mock_context.return_value
    ctx.send = AsyncMock()
    ctx.content = '!whip'

    await Rumplenator().run_command(ctx)

    ctx.send.assert_called_once()
    ctx.send.assert_called_with('/me *cracks whip* BACK TO WORK!')


@patch('bot.rumplenator.Context')
async def test_focus_command_response(mock_context):
    ctx = mock_context.return_value
    ctx.send = AsyncMock()
    ctx.content = '!focus bezos'
    ctx.author.name = 'gladys'

    await Rumplenator().run_command(ctx)

    ctx.send.assert_called_once()
    ctx.send.assert_called_with('/me gladys is requesting that bezos focus on the task at hand! Never give up!')


@patch('bot.rumplenator.Context')
async def test_unknown_command_key(mock_context):
    ctx = mock_context.return_value
    ctx.send = AsyncMock()
    ctx.content = '!bad_command'

    with pytest.raises(NotImplementedError):
        await Rumplenator().run_command(ctx)

    ctx.send.assert_not_called()
