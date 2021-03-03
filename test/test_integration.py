from bot.rumplenator import Rumplenator
from unittest.mock import patch, AsyncMock
import pytest
import asyncio
import signal

# equivalent of annotating all tests with @pytest.mark.asyncio
pytestmark = pytest.mark.asyncio


def cancel_tasks():
    print('Stopping')
    for task in list(asyncio.all_tasks):
        task.cancel()


@patch('bot.rumplenator.Context')
async def test_whip_command_response(mock_context):
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, cancel_tasks)

    bot = Rumplenator()
    ctx = mock_context.return_value
    ctx.send = AsyncMock()
    ctx.content = '!whip'

    await bot.run_command(ctx)

    ctx.send.assert_called_once()
    ctx.send.assert_called_with('/me *cracks whip* BACK TO WORK!')


# @patch('bot.rumplenator.Context')
# async def test_focus_command_response(mock_context):
#     ctx = mock_context.return_value
#     ctx.send = AsyncMock()
#     ctx.content = '!focus bezos'
#     ctx.author.name = 'gladys'

#     await Rumplenator().run_command(ctx)

#     ctx.send.assert_called_once()
#     ctx.send.assert_called_with('/me gladys is requesting that bezos focus on the task at hand! Never give up!')


# @patch('bot.rumplenator.Context')
# async def test_unknown_command_key(mock_context):
#     bot = Rumplenator()
#     ctx = mock_context.return_value
#     ctx.send = AsyncMock()
#     ctx.content = '!bad_command'

#     with pytest.raises(NotImplementedError):
#         await Rumplenator().run_command(ctx)

#     ctx.send.assert_not_called()
