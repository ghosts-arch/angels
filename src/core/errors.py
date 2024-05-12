class NoArgumentsError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(
            "This command requires arguments but none were provided", *args
        )
