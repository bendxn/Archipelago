from worlds.AutoWorld import World
from worlds.LauncherComponents import Component, components, Type, icon_paths

class ProgressionSendsWorld(World):
    game = "Progression Sends"
    hidden = True
    item_name_to_id = {}
    location_name_to_id = {}


# TODO: black magic
# class CustomKvuiFinder(importlib.abc.MetaPathFinder):
#     virtual_name = 'kvui'
#
#     def find_spec(self, fullname, path, target=None):
#         if fullname == self.virtual_name:
#             if path is None or path == "":
#                 path = [os.getcwd()]  # top level import --
#             if "." in fullname:
#                 *parents, name = fullname.split(".")
#             else:
#                 name = fullname
#             for entry in path:
#                 if os.path.isdir(os.path.join(entry, name)):
#                     # this module has child modules
#                     filename = os.path.join(entry, name, "__init__.py")
#                     submodule_locations = [os.path.join(entry, name)]
#                 else:
#                     filename = os.path.join(entry, name + ".py")
#                     submodule_locations = None
#                 if not os.path.exists(filename):
#                     continue
#             spec = importlib.util.spec_from_file_location(fullname, filename, submodule_search_locations=submodule_locations)
#             loader = getattr(spec, "loader", None)
#
#             if loader and not isinstance(loader, CustomKvuiLoader):
#                 spec.loader = CustomKvuiLoader(loader)
#             return spec
#         return None
#
#
# class CustomKvuiLoader(importlib.abc.Loader):
#
#     def __init__(self, loader):
#         self.loader = loader
#
#     def create_module(self, spec: ModuleSpec) -> types.ModuleType | None:
#         pass
#
#     def exec_module(self, module):
#         pass
        # original_game_manager = module.__dict__.get("GameManager")
        # print("wheeee")
        # if fullname != self.virtual_name:
        #     raise ImportError(fullname)
        # from kvui import GameManager, UILog
        #
        # original_build = GameManager.build
        # original_print_json = GameManager.print_json
        #
        # def wrapped_build(self):
        #     result = original_build(self)
        #     progression_sends_log = self.add_client_tab("Progression", UILog())
        #     self.log_panels["Progression"] = progression_sends_log.content
        #     return result
        #
        # def wrapped_print_json(self, data: typing.List[JSONMessagePart]):
        #     data_copy = copy.deepcopy(data)
        #     original_print_json(self, data)
        #
        #     def is_self_sent_progression(s, d: typing.List[JSONMessagePart]):
        #         hint_status_nodes = [node for node in d if node.get("type", None) == JSONTypes.hint_status]
        #         hint_status_node = hint_status_nodes[0] if 0 < len(hint_status_nodes) else None
        #         if hint_status_node is not None:
        #             return False
        #         item_nodes = [node for node in d if node.get("type", None) == JSONTypes.item_id]
        #         item_node = item_nodes[0] if 0 < len(item_nodes) else None
        #         if item_node is None:
        #             return False
        #         player_nodes = [node for node in d if node.get("type", None) == JSONTypes.player_id]
        #         player_node = player_nodes[0] if 0 < len(player_nodes) else None
        #         if player_node is not None and item_node is not None:
        #             player = int(player_node["text"])
        #             if s.ctx.slot_concerns_self(player) and item_node.get("flags") & 0b001:
        #                 return True
        #         return False
        #
        #     is_self_sent_progression = is_self_sent_progression(self, copy.deepcopy(data_copy))
        #     if is_self_sent_progression:
        #         log_text = self.json_to_kivy_parser(copy.deepcopy(data_copy))
        #         self.log_panels["Progression"].on_message_markup(log_text)
        #
        # GameManager.build = wrapped_build
        # GameManager.print_json = wrapped_print_json
        #
        # # PEP#302 says to return the module if the loader object (i.e,
        # # this class) successfully loaded the module.
        # # Note that a regular class works just fine as a module.
        # return GameManager
#
#
# sys.meta_path.insert(0, CustomKvuiFinder())

def launch_client(*args):
    from worlds.LauncherComponents import launch
    from .ProgressionClient import run_as_textclient
    launch(run_as_textclient, name="Progression Client", args=args)

icon_paths["prog_ico"] = f"ap:{__name__}/icon.png"
components.append(Component("Progression Client", None, func=launch_client, component_type=Type.CLIENT, icon="prog_ico"))