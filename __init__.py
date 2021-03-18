import unrealsdk
from Mods.ModMenu import (
    SDKMod,
    Mods,
    ModTypes,
    EnabledSaveType,
    Options,
    Keybind,
    KeybindManager,
    Game,
    Hook,
    RegisterMod
)

class SkillToggles(SDKMod):
    Name: str = "Skill Toggles"
    Author: str = "Relentless, Chronophylos"
    Description: str = "Deactivate Action Skills by holding a configurable hotkey."
    Version: str = "1.1.0"

    SupportedGames: Game = Game.BL2
    Types: ModTypes = ModTypes.Utility
    SaveEnabledState: EnabledSaveType = EnabledSaveType.LoadWithSettings

    def __init__(self) -> None:
        super().__init__()

        option_custom_keybind = Options.Boolean(
            "Custom Keybind", "Do you want to use a custom keybind to toggle the Action Skills? If this is off, you have to use your default Action Skill keybind.", False
        )
        option_buzzaxe_skill_toggle = Options.Boolean(
            "Psycho Skill Toggle", "Allows Krieg to return from the Buzzaxe Rampage.", True
        )
        option_deathtrap_skill_toggle = Options.Boolean(
            "Mechromancer Skill Toggle", "Allows Gaige to recall Deathtrap.", True
        )
        option_dual_wield_skill_toggle = Options.Boolean(
            "Gunzerker Skill Toggle", "Allows Salvador to stop his Dual Wield.", True
        )
        option_execute_skill_toggle = Options.Boolean(
            "Assassin Skill Toggle", "Allows Zer0 to stop Decepti0n.", True
        )
        option_lift_skill_toggle = Options.Boolean(
            "Siren Skill Toggle", "Allows Maya to stop her Phaselock.", True
        )
        option_scorpio_skill_toggle = Options.Boolean(
            "Commando Skill Toggle", "Allows Axton to recall his turrets.", True
        )

        self._classOptions = {
            "Psycho": option_buzzaxe_skill_toggle,
            "Mechromancer": option_deathtrap_skill_toggle,
            "Gunzerker": option_dual_wield_skill_toggle,
            "Assassin": option_execute_skill_toggle,
            "Siren": option_lift_skill_toggle,
            "Commando": option_scorpio_skill_toggle,
        }

        self.Options = [option_custom_keybind, *self._classOptions.values()]
        self._setupKeybinds()

    def ModOptionChanged(self, option, newValue):
        if option.Caption == "Custom Keybind":
            self._setupKeybinds()

    def _log(self, message: str) -> None:
        unrealsdk.Log(f"[{self.Name}] {message}")

    def _setupKeybinds(self) -> None:
        self.Keybinds = [
            Keybind("Deactivate Action Skill", "F", True, self.Options[0].CurrentValue)
        ]

    def _getPlayerController(self):
        return unrealsdk.GetEngine().GamePlayers[0].Actor

    def _isSkillToggleable(self) -> bool:
        player = self._getPlayerController()
        className = player.PlayerClass.CharacterNameId.CharacterClassId.ClassName

        if className not in self._classOptions:
            return False

        return self._classOptions[className].CurrentValue

    def _handleSkillToggling(self) -> None:
        player = self._getPlayerController()
        skillManager = player.GetSkillManager()
        actionSkill = player.PlayerSkillTree.GetActionSkill()

        if skillManager.IsSkillActive(player, actionSkill):
            actionSkill.bCanBeToggledOff = True
            player.StartActionSkill()

    def GameInputPressed(
        self, bind: KeybindManager.Keybind, event: KeybindManager.InputEvent
    ) -> None:
        if event != KeybindManager.InputEvent.Repeat or not self._isSkillToggleable():
            return

        self._handleSkillToggling()

    @Hook("WillowGame.WillowUIInteraction.InputKey")
    def _inputKey(self, caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct):
        if self.Options[0].CurrentValue or params.Event != KeybindManager.InputEvent.Repeat:
            return True

        player = self._getPlayerController()
        hotkey = player.PlayerInput.GetKeyForAction("ActionSkill", True)

        if params.Key != hotkey or not self._isSkillToggleable():
            return True

        self._handleSkillToggling()

        return True

    @Hook("WillowGame.ActionSkill.OnActionSkillEnded")
    def _onActionSkillEnded(self, caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct):
        actionSkill = self._getPlayerController().PlayerSkillTree.GetActionSkill()

        if actionSkill.bCanBeToggledOff == True:
            actionSkill.bCanBeToggledOff = False

        return True

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
