from bot.commands.command_logic.pomo import pomo_overlay
from bot.commands.command_logic.pomo.pomo_timer import PomoTimer, PomoState
from twitchio.dataclasses import User


def _mock_callback():
    pass

def _mock_user(username='test_user'):
    return User(ws=None, author=username)

def test_default_pomo_text():
    pomo_timer = PomoTimer(
         user=_mock_user(),
        work_minutes=20,
        break_minutes=10,
        sessions=1,
        topic='',
        on_pomo_complete=_mock_callback,
        on_countdown_start=_mock_callback,
        notify_user=_mock_callback
    )
    pomo_timer.state = PomoState.WORK
    pomo_text = pomo_overlay.__build_pomo_text(pomo_timer)

    assert pomo_text == 'test_user - work 20'

def test_pomo_text_topic():
    pomo_timer = PomoTimer(
        user=_mock_user(),
        work_minutes=50,
        break_minutes=10,
        sessions=1,
        topic='duolingo',
        on_pomo_complete=_mock_callback,
        on_countdown_start=_mock_callback,
        notify_user=_mock_callback
    )
    pomo_timer.state = PomoState.WORK
    pomo_text = pomo_overlay.__build_pomo_text(pomo_timer)

    assert pomo_text == 'test_user - duolingo 50'


def test_pomo_text_session():
    pomo_timer = PomoTimer(
        user=_mock_user(),
        work_minutes=50,
        break_minutes=10,
        sessions=3,
        topic='',
        on_pomo_complete=_mock_callback,
        on_countdown_start=_mock_callback,
        notify_user=_mock_callback
    )
    pomo_timer.state = PomoState.WORK
    pomo_text = pomo_overlay.__build_pomo_text(pomo_timer)

    assert pomo_text == 'test_user - work 50 (1 of 3)'


def test_pomo_text_truncated_with_sessions():
    pomo_timer = PomoTimer(
        user=_mock_user(),
        work_minutes=50,
        break_minutes=10,
        sessions=3,
        topic='ich sollte meine Deutsch-Hausaufgabe machen',
        on_pomo_complete=_mock_callback,
        on_countdown_start=_mock_callback,
        notify_user=_mock_callback
    )
    pomo_timer.state = PomoState.WORK
    pomo_text = pomo_overlay.__build_pomo_text(pomo_timer)

    assert pomo_text == 'test_user - ich sollte meine Deutsch... 50 (1 of 3)'

def test_pomo_text_truncated_without_sessions():
    pomo_timer = PomoTimer(
        user=_mock_user(),
        work_minutes=50,
        break_minutes=10,
        sessions=1,
        topic='ich sollte meine Deutsch-Hausaufgabe machen',
        on_pomo_complete=_mock_callback,
        on_countdown_start=_mock_callback,
        notify_user=_mock_callback
    )
    pomo_timer.state = PomoState.WORK
    pomo_text = pomo_overlay.__build_pomo_text(pomo_timer)

    assert pomo_text == 'test_user - ich sollte meine Deutsch-Hausaufg... 50'
    

def test_promo_break_text():
    pomo_timer = PomoTimer(
        user=_mock_user(),
        work_minutes=50,
        break_minutes=10,
        sessions=3,
        topic='ich sollte meine Deutsch-Hausaufgabe machen',
        on_pomo_complete=_mock_callback,
        on_countdown_start=_mock_callback,
        notify_user=_mock_callback
    )
    pomo_timer.state = PomoState.BREAK
    pomo_text = pomo_overlay.__build_pomo_text(pomo_timer)

    assert pomo_text == 'test_user - relax! 10 (1 of 3)'

