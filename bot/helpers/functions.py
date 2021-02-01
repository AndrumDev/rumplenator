def get_message_content(message: str, command_name: str):
    command_length = len(command_name) + 2
    message_content = str(message[command_length:])
    return message_content
