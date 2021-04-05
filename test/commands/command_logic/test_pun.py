from bot.commands.command_logic.pun import fetch_pun
from config import get_config


def test_fetch_pun():
    actual_pun_text = fetch_pun(get_config().get('pun_url'))
    expected_pun_text = "I think i want a job cleaning mirrors. It's just something i can see myself doing!"
    assert expected_pun_text == actual_pun_text
