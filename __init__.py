import unrealsdk
from Mods.ModMenu import (
    SDKMod,
    Mods,
    RegisterMod,
    ModTypes,
    EnabledSaveType,
    KeybindManager,
    Keybind,
    Options,
    Game,
)


class SkillToggles(SDKMod):
    Name: str = "Skill Toggles"
    Author: str = "Relentless, Chronophylos"
    Description: str = "Disable Action Skills by holding a configurable hotkey"
    Version: str = "1.0.0"

    SupportedGames: Game = Game.BL2
    Types: ModTypes = ModTypes.Utility
    SaveEnabledState: EnabledSaveType = EnabledSaveType.LoadWithSettings

    Keybinds = [
        Keybind("Deactivate Action Skill", "F", True),
    ]

    def __init__(self) -> None:
        super().__init__()

        option_buzzaxe_skill_toggle = Options.Boolean(
            "Enable Psycho Skill Toggle", "Allow returning from Buzzaxe", False
        )
        option_deathtrap_skill_toggle = Options.Boolean(
            "Enable Mechromancer Skill Toggle", "Allow recalling Deathtrap", False
        )
        option_dual_wield_skill_toggle = Options.Boolean(
            "Enable Gunzerker Skill Toggle", "Allow stopping Dual Wield", False
        )
        option_execute_skill_toggle = Options.Boolean(
            "Enable Assassin Skill Toggle", "Allow stopping Execute", False
        )
        option_lift_skill_toggle = Options.Boolean(
            "Enable Siren Skill Toggle", "Allow stopping Phaselog", False
        )
        option_scorpio_skill_toggle = Options.Boolean(
            "Enable Commando Skill Toggle", "Allow recalling Turrets", False
        )

        self._classToOption = {
            "Psycho": option_buzzaxe_skill_toggle,
            "Mechromancer": option_deathtrap_skill_toggle,
            "Gunzerker": option_dual_wield_skill_toggle,
            "Assassin": option_execute_skill_toggle,
            "Siren": option_lift_skill_toggle,
            "Commando": option_scorpio_skill_toggle,
        }

        self.Options = [*self._classToOption.values()]

    def _log(self, message: str) -> None:
        unrealsdk.Log(f"[{self.Name}] {message}")

    def _isSkillToggleEnabledForClass(self, name: str) -> bool:
        if name not in self._classToOption:
            return False

        return self._classToOption[name].CurrentValue

    def _deactivateActionSkill(self) -> None:
        engine = unrealsdk.GetEngine()
        player = engine.GamePlayers[0].Actor
        skill_manager = player.GetSkillManager()
        action_skill = player.PlayerSkillTree.GetActionSkill()

        if skill_manager.IsSkillActive(player, action_skill):
            self._log("Prematurely deactivating ActionSkill")
            player.Behavior_DeactivateSkill(action_skill, False)

    def _getCurrentPlayerClassName(self) -> str:
        engine = unrealsdk.GetEngine()
        player = engine.GamePlayers[0].Actor
        return str(player.PlayerClass.CharacterNameId.CharacterClassId.ClassName)

    def GameInputPressed(
        self, bind: KeybindManager.Keybind, event: KeybindManager.InputEvent
    ) -> None:
        class_name = self._getCurrentPlayerClassName()
        if not self._isSkillToggleEnabledForClass(class_name):
            return

        if event != KeybindManager.InputEvent.Repeat:
            return

        self._deactivateActionSkill()


instance = SkillToggles()
if __name__ == "__main__":
    unrealsdk.Log(f"[{instance.Name}] Manually loaded")
    for mod in Mods:
        if mod.Name == instance.Name:
            if mod.IsEnabled:
                mod.Disable()
            Mods.remove(mod)
            unrealsdk.Log(f"[{instance.Name}] Removed last instance")

            # Fixes inspect.getfile()
            instance.__class__.__module__ = mod.__class__.__module__
            break
RegisterMod(instance)
