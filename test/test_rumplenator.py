from bot.rumplenator import Rumplenator


def test_bot_initialized_correctly():
    bot = Rumplenator()
    assert bot.nick == 'rumplenator_test'
    assert bot.initial_channels == ['test_channel']
