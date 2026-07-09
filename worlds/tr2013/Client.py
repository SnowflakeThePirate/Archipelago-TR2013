from CommonClient import (
    ClientCommandProcessor,
    CommonContext,
    logger,
    get_base_parser,
    gui_enabled,
    server_loop,
)
from Utils import init_logging
import multiprocessing
import asyncio
from .Connector import TR2013Connector
from .Data import Data

POLL_INTERVAL = 0.5

class TR2013CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: "TR2013Context"):
        super().__init__(ctx)


class TR2013Context(CommonContext):
    command_processor = TR2013CommandProcessor
    game = "Tomb Raider (2013)"
    items_handling = 0b111
    
    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.conn: TR2013Connector | None = None
        self._connect_warned = False
        self._disconnect_warned = True
        self.loc_id_to_offset = {
            loc["id"]: int(loc["item_object"], 16)
            for loc in Data.location_table
            if loc.get("item_object", "").startswith("0x")
        }

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(TR2013Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

        
    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.slot_data = args["slot_data"]

    def ensure_connected(self) -> bool:
        """Attach to TombRaider.exe if not already attached. Returns True while attached."""
        if self.conn is not None:
            return True
        try:
            self.conn = TR2013Connector.attach()
            logger.info("Connected to TombRaider")
            self._connect_warned = False
            self._disconnect_warned = False
            return True
        except Exception:
            if not self._disconnect_warned:
                logger.info("Disconnected from TombRaider")
                self._disconnect_warned = True
                self._connect_warned = False
            if not self._connect_warned:
                logger.warning("Waiting to connect to TombRaider...")
                self._connect_warned = True
            return False


async def game_monitor_task(ctx: "TR2013Context"):
    while not ctx.exit_event.is_set():
        if ctx.ensure_connected() and ctx.conn:
            try:
                manager = ctx.conn.collectible_manager()
                if manager and ctx.server and ctx.slot is not None:
                    found = [
                        loc_id
                        for loc_id, offset in ctx.loc_id_to_offset.items()
                        if ctx.conn.read_collectible_flag(manager, offset)
                    ]
                    if found:
                        await ctx.check_locations(found)
                        for loc_id in found:
                            ctx.conn.clear_collectible_flag(manager, ctx.loc_id_to_offset[loc_id])
            except Exception:
                ctx.conn = None
        await asyncio.sleep(POLL_INTERVAL)

def launch():
    init_logging("Tomb Raider (2013) Client")

    async def main():
        multiprocessing.freeze_support()
        parser = get_base_parser()
        args = parser.parse_args()
        ctx = TR2013Context(args.connect, args.password)
        logger.info("Connecting to server...")
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        monitor = asyncio.create_task(game_monitor_task(ctx), name="GameMonitor")
        await ctx.exit_event.wait()
        monitor.cancel()
        await ctx.shutdown()


    import colorama

    colorama.init()

    asyncio.run(main())
    colorama.deinit()


if __name__ == "__main__":
    launch()
