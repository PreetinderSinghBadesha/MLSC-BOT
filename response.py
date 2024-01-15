def get_response(user_input: str) -> str:
    lowered_input: str = user_input.lower()

    if 'hello' in lowered_input:
        return "Hello "