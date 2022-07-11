

class LogFormatter:
    def __init__(self, message: str):
        self.message = message

        self.repr_fields = [
            'message',
        ]

    def get_dict_record(self) -> dict:
        return {
            repr_parameter: getattr(self, repr_parameter, None)
            for repr_parameter in self.repr_fields
        }

    def get_str_record(self) -> str:
        return ', '.join(
            [
                f'{name}={value}'
                for name, value in self.get_dict_record().items()
            ]
        )
