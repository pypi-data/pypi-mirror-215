class BadRPCRequestException(Exception):
    def __init__(self, message: str, errors: str = None) -> None:
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors


class BadRestRequestException(Exception):
    def __init__(self, message: str, errors: str = None) -> None:
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors
