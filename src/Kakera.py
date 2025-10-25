from discord.ext import tasks
from .Cooldown import Cooldown


class Kakera:
    def __init__(
        self,
        value: int,
        cost: int,
        total: int,
        dk: Cooldown,
    ):
        self.value: int = value
        self.cost: int = cost
        self.total: int = total
        self.dk: Cooldown = dk

    def __iadd__(self, n: int) -> None:
        if (self.value + n) <= self.total:
            self.value += n
        else:
            self.value = self.total

    def __isub__(self, n: int) -> None:
        if (self.value - n) > -1:
            self.value -= n
        else:
            self.value = 0

    @tasks.loop(minutes=3)
    async def auto_regen(self) -> None:
        self += 1

    @tasks.loop(count=1)
    async def claim_dk(self) -> None:
        while True:
            try:
                await self._channel.send(f"{self._prefix}dk")
            except discord.errors.NotFound:
                continue
            break
        self._dk = False
        self._value = self._total

        print(f"Claimed dk on {self._channel.guild.name}.\n")
        await asyncio.sleep(86400)
        self._dk = True
