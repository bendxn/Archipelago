import asyncio
import copy
import logging
import sys
import typing

from CommonClient import CommonContext, server_loop, gui_enabled, \
    get_base_parser, handle_url_arg
from NetUtils import JSONMessagePart, JSONTypes


class ProgressionContext(CommonContext):
    def __init__(self, server_address, password):
        super().__init__(server_address, password)

    def run_gui(self):
        from kvui import GameManager, UILog

        class ProgressionManager(GameManager):
            base_title = "Archipelago Progression Client"

            def build(self):
                result = super().build()
                progression_log = self.add_client_tab("Progression", UILog())
                self.log_panels["Progression"] = progression_log.content
                progression_sends_log = self.add_client_tab("Prog. Sends", UILog())
                self.log_panels["Prog. Sends"] = progression_sends_log.content
                return result

            def print_json(self, data: typing.List[JSONMessagePart]):
                data_copy = copy.deepcopy(data)
                super().print_json(data)

                def is_progression(s, d: typing.List[JSONMessagePart]):
                    hint_status_nodes = [node for node in d if node.get("type", None) == JSONTypes.hint_status]
                    hint_status_node = hint_status_nodes[0] if 0 < len(hint_status_nodes) else None
                    if hint_status_node is not None:
                        return False
                    item_nodes = [node for node in d if node.get("type", None) == JSONTypes.item_id]
                    item_node = item_nodes[0] if 0 < len(item_nodes) else None
                    if item_node is not None and item_node.get("flags") & 0b001:
                        return True
                    return False

                def is_self_sent_progression(s, d: typing.List[JSONMessagePart]):
                    is_p = is_progression(s, d)
                    if is_p:
                        player_nodes = [node for node in d if node.get("type", None) == JSONTypes.player_id]
                        player_node = player_nodes[0] if 0 < len(player_nodes) else None
                        if player_node is not None:
                            player = int(player_node["text"])
                            if s.ctx.slot_concerns_self(player):
                                return True
                    return False

                is_prog = is_progression(self, copy.deepcopy(data_copy))
                if is_prog:
                    log_text = self.json_to_kivy_parser(copy.deepcopy(data_copy))
                    self.log_panels["Progression"].on_message_markup(log_text)

                is_self_sent_prog = is_self_sent_progression(self, copy.deepcopy(data_copy))
                if is_self_sent_prog:
                    log_text = self.json_to_kivy_parser(copy.deepcopy(data_copy))
                    self.log_panels["Prog. Sends"].on_message_markup(log_text)


        self.ui = ProgressionManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_print_json(self, args):
        data = args["data"]
        super().on_print_json(args)



def run_as_textclient(*args):
    class TextContext(ProgressionContext):
        # Text Mode to use !hint and such with games that have no text entry
        tags = CommonContext.tags | {"TextOnly"}
        game = ""  # empty matches any game since 0.3.2
        items_handling = 0b111  # receive all items for /received
        want_slot_data = False  # Can't use game specific slot_data

        async def server_auth(self, password_requested: bool = False):
            if password_requested and not self.password:
                await super(TextContext, self).server_auth(password_requested)
            await self.get_username()
            await self.send_connect(game="")

        def on_package(self, cmd: str, args: dict):
            if cmd == "Connected":
                self.game = self.slot_info[self.slot].game

        async def disconnect(self, allow_autoreconnect: bool = False):
            self.game = ""
            await super().disconnect(allow_autoreconnect)

    async def main(args):
        ctx = TextContext(args.connect, args.password)
        ctx.auth = args.name
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="Gameless Archipelago Client, for text interfacing.")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    args = parser.parse_args(args)

    args = handle_url_arg(args, parser=parser)

    # use colorama to display colored text highlighting on windows
    colorama.just_fix_windows_console()

    asyncio.run(main(args))
    colorama.deinit()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)  # force log-level to work around log level resetting to WARNING
    run_as_textclient(*sys.argv[1:])  # default value for parse_args