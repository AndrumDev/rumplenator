from bot.commands.command_logic.dyson import get_dyson_message

expected_output_dry = "The Dyson Supersonic™ hairdryer provides high-velocity airflow..."
expected_output_style = "The Dyson Airwrap™ comes with a combination of 30mm and 40mm barrels..."


def test_get_dyson_message():
    message = get_dyson_message()
    assert message == expected_output_dry or message == expected_output_style


def test_get_dyson_message_dry():
    message = get_dyson_message('dry')
    assert message == expected_output_dry


def test_get_dyson_message_style():
    message = get_dyson_message('style')
    assert message == expected_output_style


def test_get_dyson_message_category_not_found():
    message = get_dyson_message('lel')
    assert message == 'We currently do not have that in stock. Please choose from our current range: hand, heat, dry, fan, style, and vac.'
    