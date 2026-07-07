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

POLL_INTERVAL = 0.5

class TR2013CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: "TR2013Context"):
        super().__init__(ctx)


class TR2013Context(CommonContext):
    game = "Tomb Raider (2013)"
    items_handling = 0b111
    
    def __init__(self, server_address, password):
        super().__init__(server_address, password)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(TR2013Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

        
    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.slot_data = args["slot_data"]



async def game_monitor_task(ctx: TR2013Context):
    logger.info("Game Monitor attatching to TombRaider.exe...")

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
