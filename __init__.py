import unrealsdk
from Mods.ModMenu import (
    SDKMod,
    Mods,
    RegisterMod,
    ModTypes,
    EnabledSaveType,
    KeybindManager,
    Keybind,
    OptionManager,
    Options,
    Game,
)
from typing import Any


class SkillToggles(SDKMod):
    Name: str = "Skill Toggles"
    Author: str = "DamnRelentless, Chronophylos"
    Description: str = ""
    Version: str = "0.1.0"

    SupportedGames: Game = Game.BL2
    Types: ModTypes = ModTypes.Utility
    SaveEnabledState: EnabledSaveType = EnabledSaveType.LoadWithSettings

    def __init__(self) -> None:
        super().__init__()

        self._optionCustomKeybindEnable = Options.Boolean(
            "Enable Custom Keybinds", "Enable custom keybinds for each skill", False
        )

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

        self.Options = [self._optionCustomKeybindEnable, *self._classToOption.values()]

        self._keybindToggleBuzzaxe = Keybind("Toggle Buzzaxe", "F", True)
        self._keybindToggleDeathtrap = Keybind("Toggle Deathtrap", "F", True)
        self._keybindToggleDualWield = Keybind("Toggle Dual Wield", "F", True)
        self._keybindToggleExecute = Keybind("Toggle Execute", "F", True)
        self._keybindToggleLift = Keybind("Toggle Lift", "F", True)
        self._keybindToggleScorpio = Keybind("Toggle Scorpio", "F", True)

        self.Keybinds = [
            self._keybindToggleBuzzaxe,
            self._keybindToggleDeathtrap,
            self._keybindToggleDualWield,
            self._keybindToggleExecute,
            self._keybindToggleLift,
            self._keybindToggleScorpio,
        ]

        self._setKeybinds(self._optionCustomKeybindEnable.CurrentValue)

    def _setKeybinds(self, keybindsEnabled: bool) -> None:
        for keybind in self.Keybinds:
            keybind.IsHidden = not keybindsEnabled

    def _log(self, message: str) -> None:
        unrealsdk.Log(f"[{self.Name}] {message}")

    def _isSkillToggleEnabledForClass(self, name: str) -> bool:
        if name not in self._classToOption:
            return False

        return self._classToOption[name].CurrentValue

    def GameInputPressed(
        self, bind: KeybindManager.Keybind, event: KeybindManager.InputEvent
    ) -> None:
        if event != KeybindManager.InputEvent.Pressed:
            return

        self.DeactivateActionSkill()

    def ModOptionChanged(
        self, option: OptionManager.Options.Base, new_value: Any
    ) -> None:
        if option.Caption == self._optionCustomKeybindEnable.Caption:
            self._setKeybinds(new_value)

    def DeactivateActionSkill(self) -> None:
        engine = unrealsdk.GetEngine()
        player = engine.GamePlayers[0].Actor
        skill_manager = player.GetSkillManager()
        action_skill = player.PlayerSkillTree.GetActionSkill()

        class_name = player.PlayerClass.CharacterNameId.CharacterClassId.ClassName
        if not self._isSkillToggleEnabledForClass(class_name):
            return

        if skill_manager.IsSkillActive(player, action_skill):
            self._log("Prematurely deactivating ActionSkill")
            player.Behavior_DeactivateSkill(action_skill, False)


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
