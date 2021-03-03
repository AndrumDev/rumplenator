from bot.rumplenator import Rumplenator


def test_bot_initialized_correctly():
    bot = Rumplenator()
    assert bot.nick == 'rumplenator_test'
    assert bot.initial_channels == ['test_channel']

    # sanity test to check that the commands are successfully registered
    assert 'hi' in bot.commands
    assert 'focus' in bot.commands
    assert 'dyson' in bot.commands
