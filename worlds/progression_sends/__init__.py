import copy
import typing
from NetUtils import JSONTypes, JSONMessagePart
from worlds.AutoWorld import World


class ProgressionSendsWorld(World):
    game = "Progression Sends"
    hidden = True
    item_name_to_id = {}
    location_name_to_id = {}

def add_progression_hook():
    from kvui import GameManager, UILog
    original_build = GameManager.build
    original_print_json = GameManager.print_json

    def wrapped_build(self):
        result = original_build(self)
        progression_sends_log = self.add_client_tab("Progression", UILog())
        self.log_panels["Progression"] = progression_sends_log.content
        return result
    def wrapped_print_json(self, data: typing.List[JSONMessagePart]):
        text = copy.deepcopy(data)
        original_print_json(self, data)
        def is_self_sent_progression(s, d: typing.List[JSONMessagePart]):
            hint_status_nodes = [node for node in d if node.get("type", None) == JSONTypes.hint_status]
            hint_status_node = hint_status_nodes[0] if 0 < len(hint_status_nodes) else None
            if hint_status_node is not None:
                return False
            item_nodes = [node for node in d if node.get("type", None) == JSONTypes.item_id]
            item_node = item_nodes[0] if 0 < len(item_nodes) else None
            if item_node is None:
                return False
            player_nodes = [node for node in d if node.get("type", None) == JSONTypes.player_id]
            player_node = player_nodes[0] if 0 < len(player_nodes) else None
            if player_node is not None and item_node is not None:
                player = int(player_node["text"])
                if s.ctx.slot_concerns_self(player) and item_node.get("flags") & 0b001:
                    return True
            return False

        is_self_sent_progression = is_self_sent_progression(self, copy.deepcopy(text))
        if is_self_sent_progression:
            other_text = self.json_to_kivy_parser(copy.deepcopy(text))
            self.log_panels["Progression"].on_message_markup(other_text)

    GameManager.build = wrapped_build
    GameManager.print_json = wrapped_print_json

add_progression_hook()