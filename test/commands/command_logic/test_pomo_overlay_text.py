from bot.commands.command_logic.pomo import pomo_overlay
from bot.commands.command_logic.pomo.pomo_timer import PomoTimer, PomoState
from twitchio.dataclasses import User
import pytest


async def _mock_notify_user(arg1, arg2):
    pass

async def _mock_callback():
    pass

def _create_mock_user(username='test_user'):
    return User(ws=None, author=username)


@pytest.mark.asyncio
async def test_default_pomo_text():
    pomo_timer = PomoTimer(
        user=_create_mock_user(),
        work_minutes=20,
        break_minutes=10,
        sessions=1,
        topic='',
        on_pomo_complete=_mock_callback,
        on_countdown_start=_mock_callback,
        notify_user=_mock_notify_user
    )
    await pomo_timer.begin()
    pomo_text = pomo_overlay.__build_pomo_text(pomo_timer)
    assert pomo_text == 'test_user - work 20'
    pomo_timer.cancel()


@pytest.mark.asyncio
async def test_pomo_text_topic():
    pomo_timer = PomoTimer(
        user=_create_mock_user(),
        work_minutes=50,
        break_minutes=10,
        sessions=1,
        topic='duolingo',
        on_pomo_complete=_mock_callback,
        on_countdown_start=_mock_callback,
        notify_user=_mock_notify_user
    )
    await pomo_timer.begin()
    pomo_text = pomo_overlay.__build_pomo_text(pomo_timer)
    assert pomo_text == 'test_user - duolingo 50'
    pomo_timer.cancel()


@pytest.mark.asyncio
async def test_pomo_text_session():
    pomo_timer = PomoTimer(
        user=_create_mock_user(),
        work_minutes=50,
        break_minutes=10,
        sessions=3,
        topic='',
        on_pomo_complete=_mock_callback,
        on_countdown_start=_mock_callback,
        notify_user=_mock_notify_user
    )
    await pomo_timer.begin()
    pomo_text = pomo_overlay.__build_pomo_text(pomo_timer)
    assert pomo_text == 'test_user - work 50 (1 of 3)'
    pomo_timer.cancel()


@pytest.mark.asyncio
async def test_pomo_text_truncated_with_sessions():
    pomo_timer = PomoTimer(
        user=_create_mock_user(),
        work_minutes=50,
        break_minutes=10,
        sessions=3,
        topic='ich sollte meine Deutsch-Hausaufgabe machen',
        on_pomo_complete=_mock_callback,
        on_countdown_start=_mock_callback,
        notify_user=_mock_notify_user
    )
    await pomo_timer.begin()
    pomo_text = pomo_overlay.__build_pomo_text(pomo_timer)
    assert pomo_text == 'test_user - ich sollte meine Deutsch-Haus... 50 (1 of 3)'
    pomo_timer.cancel()

@pytest.mark.asyncio
async def test_pomo_text_truncated_without_sessions():
    pomo_timer = PomoTimer(
        user=_create_mock_user(),
        work_minutes=50,
        break_minutes=10,
        sessions=1,
        topic='ich sollte meine Deutsch-Hausaufgabe machen',
        on_pomo_complete=_mock_callback,
        on_countdown_start=_mock_callback,
        notify_user=_mock_notify_user
    )
    await pomo_timer.begin()
    pomo_text = pomo_overlay.__build_pomo_text(pomo_timer)
    assert pomo_text == 'test_user - ich sollte meine Deutsch-Hausaufgabe m... 50'
    pomo_timer.cancel()


@pytest.mark.asyncio
async def test_promo_break_text():
    pomo_timer = PomoTimer(
        user=_create_mock_user(),
        work_minutes=50,
        break_minutes=10,
        sessions=3,
        topic='ich sollte meine Deutsch-Hausaufgabe machen',
        on_pomo_complete=_mock_callback,
        on_countdown_start=_mock_callback,
        notify_user=_mock_notify_user
    )
    
    await pomo_timer.begin()
    pomo_timer.state = PomoState.BREAK
    pomo_text = pomo_overlay.__build_pomo_text(pomo_timer)
    assert pomo_text == 'test_user - relax! 10 (1 of 3)'
    pomo_timer.cancel()
