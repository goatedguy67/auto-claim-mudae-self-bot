import time
from asyncio import sleep


class Cooldown:
    def __init__(self):
        self.in_cooldown: bool = False
        self.cooldown_time: float = 0.0

    async def set_cooldown(self, tempo: float) -> None:
        self.in_cooldown = True
        self.cooldown_time = time.time() + tempo
        await sleep(tempo)
        self.in_cooldown = False

    def get_current_cooldown(self) -> float:
        return self.cooldown_time - time.time()
