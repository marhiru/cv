import time


class Timer:
    def __init__(self, print) -> None:
        self.print = print

    def debug(self) -> float:
        duration = time.time()
        result = duration - time.time() / 60
        if self.print is True:
            print(f"{result} segundos!")

        return result
