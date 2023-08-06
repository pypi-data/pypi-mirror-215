import json
import logging
from pathlib import Path
from typing import Callable

from open_prime_rando import dynamic_schema
from open_prime_rando.echoes import specific_area_patches, asset_ids, dock_lock_rando
from open_prime_rando.echoes.elevators import auto_enabled_elevator_patches
from open_prime_rando.echoes.elevators.elevator_rando import patch_elevator
from open_prime_rando.echoes.inverted import apply_inverted
from open_prime_rando.echoes.small_randomizations import apply_small_randomizations
from open_prime_rando.patcher_editor import PatcherEditor
from open_prime_rando.unique_area_name import get_name_for_area
from open_prime_rando.validator_with_default import DefaultValidatingDraft7Validator
from retro_data_structures.asset_manager import FileProvider
from retro_data_structures.formats.mlvl import AreaWrapper
from retro_data_structures.game_check import Game
from retro_data_structures.formats.strg import Strg

LOG = logging.getLogger("echoes_patcher")


def _read_schema():
    with Path(__file__).parent.joinpath("echoes", "schema.json").open() as f:
        return json.load(f)


def apply_area_modifications(editor: PatcherEditor, configuration: dict[str, dict], status_update: Callable[[str, float], None]):
    num_areas = sum(len(world_config["areas"]) for world_config in configuration.values())
    areas_processed = 0.0

    for world_name, world_config in configuration.items():
        world_meta = asset_ids.world.load_dedicated_file(world_name)
        mlvl = editor.get_mlvl(asset_ids.world.NAME_TO_ID_MLVL[world_name])

        areas_by_name: dict[str, AreaWrapper] = {
            get_name_for_area(area): area
            for area in mlvl.areas
        }

        for i, (area_name, area) in enumerate(areas_by_name.items()):
            if area_name not in world_config["areas"]:
                continue

            status_update(f"Processing {world_name} - {area_name}...", areas_processed/num_areas)
            areas_processed += 1

            area_config = world_config["areas"][area_name]
            low_memory = area_config["low_memory_mode"]

            for dock_name, dock_config in area_config["docks"].items():
                dock_number = world_meta.DOCK_NAMES[area_name][dock_name]

                if "new_door_type" in dock_config:
                    dock_lock_rando.apply_door_rando(
                        editor,
                        world_name,
                        area_name,
                        dock_name,
                        dock_config["new_door_type"],
                        dock_config.get("old_door_type"),
                        low_memory
                    )

                if "connect_to" in dock_config:
                    dock_target = dock_config["connect_to"]
                    LOG.debug("Connecting dock %s of %s - %s to %s - %s",
                              dock_name, world_name, area_name, dock_target["area"], dock_target["dock"])
                    area.connect_dock_to(dock_number, areas_by_name[dock_target["area"]],
                                         world_meta.DOCK_NAMES[dock_target["area"]][dock_target["dock"]])

            for layer_name, layer_state in area_config["layers"].items():
                LOG.debug("Setting layer %s of %s - %s to %s", layer_name, world_name, area_name, str(layer_state))
                area.get_layer(layer_name).active = layer_state

            for elevator in area_config["elevators"]:
                patch_elevator(
                    editor,
                    area,
                    elevator["instance_id"],
                    elevator["target_assets"]["world_asset_id"],
                    elevator["target_assets"]["area_asset_id"],
                    elevator["target_strg"],
                    elevator["target_name"]
                )

            if area_config["new_name"] is not None:
                old_strg = area._raw.area_name_id
                strg = editor.get_parsed_asset(old_strg, type_hint=Strg)
                strg.set_string(0, area_config["new_name"])
                paks = editor.find_paks(old_strg)
                new_strg = editor.add_file(f"custom_name_for_{area.internal_name}.STRG", strg, paks)
                area._raw.area_name_id = new_strg

            area.build_mlvl_dependencies(only_modified=True)


def patch_paks(file_provider: FileProvider,
               output_path: Path,
               configuration: dict,
               status_update: Callable[[str, float], None] = lambda s, _: LOG.info(s)):
    status_update(f"Will patch files at {file_provider}", 0)

    editor = PatcherEditor(file_provider, Game.ECHOES)

    status_update("Preparing schema", 0)
    schema = dynamic_schema.expand_schema(_read_schema(), editor)

    status_update("Validating schema", 0)
    DefaultValidatingDraft7Validator(schema).validate(configuration)

    status_update("Applying small patches", 0)
    dock_lock_rando.add_custom_models(editor)
    if configuration["auto_enabled_elevators"]:
        auto_enabled_elevator_patches.apply_auto_enabled_elevators_patch(editor)
    specific_area_patches.specific_patches(editor, configuration["area_patches"])
    apply_small_randomizations(editor, configuration["small_randomizations"])
    apply_area_modifications(editor, configuration["worlds"], status_update)

    if configuration["inverted"]:
        apply_inverted(editor)

    # Save our changes
    editor.flush_modified_assets()

    editor.save_modifications(output_path)
    status_update("Finished", 1.0)
