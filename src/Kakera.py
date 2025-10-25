from asyncio import sleep

from discord.errors import NotFound, InvalidData
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
    async def claim_dk(self, channel, prefix, cooldown=86000) -> None:
        while True:
            try:
                await channel.send(f"{prefix}dk")
            except NotFound:
                continue
            break

        self.value = self.total
        print(f"Claimed dk on {channel.guild.name}.\n")
        await self.dk.set_cooldown(cooldown)

    async def can_claim(self, channel, cost) -> bool:
        """
        Checks if you can claim kakera in the given channel.
        If you don't uses dk.
        :param channel: The Discord channel to check.
        :param key: Whether the user has 10 keys to reduce the cost.
        """
        print(f"Cheking if you can claim kakera on {channel.guild.name}...")
        if self.value >= cost:
            print(f"... You can claim kakera on {channel.guild.name}.\n")
            return True

        if not self.dk.on_cooldown:
            print(f"... You can claim kakera on {channel.guild.name}.\n")
            await self.dk.set_cooldown()
            return True

        print(
            f"... You don't have enough kakera ({self.value}) on {channel.guild.name}.\n"
        )
        return False

    async def claim(self, message, half: bool = False, delay=0) -> None:
        """
        Claims kakera from the given message.
        :param message: The Discord message to claim kakera from.
        """
        channel = message.channel
        print(f"Waiting {delay} to claim kakera on {channel.guild.name}.\n")
        await sleep(delay)

        # I don't know if Mudae rounds to floor or ceil.
        cost = self.cost // 2 if half else self.cost

        if not await self.can_claim(channel, cost):
            return

        # I don't know what causes this, that's why im not putting While True
        try:
            await message.components[0].children[0].click()
        except InvalidData:
            print(f"Could not claim Kakera {channel.guild.name}.\n")
            return

        print(f"Claimed Kakera on {channel.guild.name}.\n")
        self -= cost
