from bot.commands.command_logic.pomo.pomo_timer import PomoTimer, PomoState
from datetime import datetime, timezone, timedelta


def _mock_notify_user():
    pass

def _mock_on_complete():
    pass


def test_work_minutes_remaining():
    pomo_timer = PomoTimer(
        username='test_user',
        work_minutes=20,
        break_minutes=10,
        sessions=1,
        topic='lel',
        on_pomo_complete=_mock_on_complete,
        notify_user=_mock_notify_user
    )
    # set the started_time to be 5 minutes in the past
    # i.e. there are 20 - 5 = 15 work minutes left
    pomo_timer.set_countdown_started(datetime.now(timezone.utc) - timedelta(minutes = 5))
    pomo_timer.state = PomoState.WORK

    assert pomo_timer.minutes_remaining == 15


def test_break_minutes_remaining():
    pomo_timer = PomoTimer(
        username='test_user',
        work_minutes=20,
        break_minutes=10,
        sessions=1,
        topic='lel',
        on_pomo_complete=_mock_on_complete,
        notify_user=_mock_notify_user
    )
    # set the started_time to be 2 minutes in the past
    # i.e. there are 10 - 2 = 8 break minutes left
    pomo_timer.set_countdown_started(datetime.now(timezone.utc) - timedelta(minutes = 2))
    pomo_timer.state = PomoState.BREAK

    assert pomo_timer.minutes_remaining == 8


def test_minutes_remaining_with_31_seconds_left_rounds_up():
    pomo_timer = PomoTimer(
        username='test_user',
        work_minutes=20,
        break_minutes=10,
        sessions=1,
        topic='lel',
        on_pomo_complete=_mock_on_complete,
        notify_user=_mock_notify_user
    )
    pomo_timer.set_countdown_started(datetime.now(timezone.utc) - timedelta(minutes = 19, seconds=29))
    pomo_timer.state = PomoState.WORK

    assert pomo_timer.minutes_remaining == 1


def test_minutes_remaining_with_29_seconds_left_rounds_down():
    pomo_timer = PomoTimer(
        username='test_user',
        work_minutes=20,
        break_minutes=10,
        sessions=1,
        topic='lel',
        on_pomo_complete=_mock_on_complete,
        notify_user=_mock_notify_user
    )
    pomo_timer.set_countdown_started(datetime.now(timezone.utc) - timedelta(minutes = 19, seconds=31))
    pomo_timer.state = PomoState.WORK

    assert pomo_timer.minutes_remaining == 0


def test_minutes_remaining_not_started():
    pomo_timer = PomoTimer(
        username='test_user',
        work_minutes=20,
        break_minutes=10,
        sessions=1,
        topic='lel',
        on_pomo_complete=_mock_on_complete,
        notify_user=_mock_notify_user
    )

    assert pomo_timer.minutes_remaining == None

