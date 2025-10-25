import time
from asyncio import sleep


class Cooldown:
    async def __init__(self, cooldown: float = 0, max_cooldown: float = 86000):
        """
        Initializes a Cooldown instance.
        If a cooldown time is provided, it sets the cooldown immediately.
        :param cooldown: The initial cooldown time in seconds.
        :param max_cooldown: The maximum cooldown time in seconds.
        """

        if cooldown:
            await self.set_cooldown(cooldown)

        self.on_cooldown: bool = False
        self.cooldown_time: float = 0.0
        self.max_cooldown: float = max_cooldown

    async def set_cooldown(self, tempo: float = 0) -> None:
        """
        Sets the cooldown for the specified duration if one is provided
        else uses the maximum cooldown time.
        """

        if tempo == 0:
            tempo = self.max_cooldown

        self.on_cooldown = True
        self.cooldown_time = time.time() + tempo
        await sleep(tempo)
        self.on_cooldown = False

    def get_current_cooldown(self) -> float:
        return self.cooldown_time - time.time()
