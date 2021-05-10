def get_message_content(message: str, command_name: str):
    command_length = len(command_name) + 2
    message_content = str(message[command_length:])
    return message_content

def get_message_command(message: str):
    return message.split()[0][1:]

def has_pomo_mod_flag(message: str):
    return '[mod]' in message