class Logger:
    def __init__(self, message) -> None:
        self.message = message

    def FileNotFoundError(self) -> None:
        print(f"\n[\x1b[48;5;1m\x1b[38;5;0m  VariableError  \x1b[0m] {self.message}")
