from bot.commands.command_logic.pomo.pomo_command import __get_pom_args


def test_get_pom_args_with_all_args():
    args = ['10', '20', '30', 'werk']
    work_time, break_time, num_sessions, topic = __get_pom_args(args)
    assert work_time == 10
    assert break_time == 20
    assert num_sessions == 30
    assert topic == 'werk'


def test_get_pom_with_one_arg():
    args = ['10']
    work_time, break_time, num_sessions, topic = __get_pom_args(args)
    assert work_time == 10
    assert break_time == 0
    assert num_sessions == 1
    assert topic == ''


def test_get_pom_with_two_args():
    args = ['10', '20']
    work_time, break_time, num_sessions, topic = __get_pom_args(args)
    assert work_time == 10
    assert break_time == 20
    assert num_sessions == 1
    assert topic == ''


def test_get_pom_with_three_args():
    args = ['10', '20', '30']
    work_time, break_time, num_sessions, topic = __get_pom_args(args)
    assert work_time == 10
    assert break_time == 20
    assert num_sessions == 30
    assert topic == ''
