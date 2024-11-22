from secret.secret import ID_TO_NAME_MAP

NAME_TO_ID_MAP = {v: k for k, v in ID_TO_NAME_MAP.items()}


class NaughtyList:
    def __init__(self):
        self._naughty_list = []  # only store user_ids

    def _add_user_name_to_list(self, user_name: str) -> None:
        if user_name not in NAME_TO_ID_MAP:
            raise ValueError(f"{user_name} not found in NAME_TO_ID_MAP")

        user_id = NAME_TO_ID_MAP[user_name]

        if user_id in self._naughty_list:
            raise ValueError(f"{user_name} is already in the naughty list")

        self._naughty_list.append(user_id)

    def get_add_user_name_message(self, user_name: str) -> str:
        try:
            self._add_user_name_to_list(user_name)
        except ValueError as e:
            return str(e)

        return f"{user_name} has been added to the naughty list"

    def _remove_user_name_from_list(self, user_name: str) -> None:
        if user_name not in NAME_TO_ID_MAP:
            raise ValueError(f"{user_name} not found in NAME_TO_ID_MAP")

        user_id = NAME_TO_ID_MAP[user_name]

        if user_id not in self._naughty_list:
            raise ValueError(f"{user_name} is not in the naughty list")

        self._naughty_list.remove(user_id)

    def get_remove_user_name_message(self, user_name: str) -> str:
        try:
            self._remove_user_name_from_list(user_name)
        except ValueError as e:
            return str(e)

        return f"{user_name} has been removed from the naughty list"

    def get_formatted_list(self) -> str:
        return "\n".join([ID_TO_NAME_MAP[user_id] for user_id in self._naughty_list])

    def is_user_id_list(self, user_id: str) -> bool:
        return user_id in self._naughty_list
