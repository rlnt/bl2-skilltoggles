import unrealsdk
import webbrowser
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
    RegisterMod,
)

try:
    from Mods.Eridium import log
    from Mods.Eridium.misc import getCurrentPlayerController
except ImportError:
    webbrowser.open("https://github.com/RLNT/bl2_eridium")
    raise

if __name__ == "__main__":
    import importlib
    import sys

    importlib.reload(sys.modules["Mods.Eridium"])
    importlib.reload(sys.modules["Mods.Eridium.misc"])

    # See https://github.com/bl-sdk/PythonSDK/issues/68
    try:
        raise NotImplementedError
    except NotImplementedError:
        __file__ = sys.exc_info()[-1].tb_frame.f_code.co_filename  # type: ignore


class SkillToggles(SDKMod):
    Name: str = "Skill Toggles"
    Author: str = "Relentless, Chronophylos"
    Description: str = "Deactivate Action Skills by holding a configurable hotkey."
    Version: str = "1.1.1"

    SupportedGames: Game = Game.BL2
    Types: ModTypes = ModTypes.Utility
    SaveEnabledState: EnabledSaveType = EnabledSaveType.LoadWithSettings

    def __init__(self) -> None:
        super().__init__()

        self._optionCustomKeybind = Options.Boolean(
            "Custom Keybind",
            "Do you want to use a custom keybind to toggle the Action Skills? If this is off, you have to use your default Action Skill keybind.",
            False,
        )
        optionPsychoToggle = Options.Boolean(
            "Psycho Skill Toggle",
            "Allows Krieg to return from his Buzzaxe Rampage.",
            True,
        )
        optionMechromancerToggle = Options.Boolean(
            "Mechromancer Skill Toggle", "Allows Gaige to recall her Deathtrap.", True
        )
        optionGunzerkerToggle = Options.Boolean(
            "Gunzerker Skill Toggle", "Allows Salvador to stop his Dual Wield.", True
        )
        optionAssassinToggle = Options.Boolean(
            "Assassin Skill Toggle", "Allows Zer0 to stop Decepti0n.", True
        )
        optionSirenToggle = Options.Boolean(
            "Siren Skill Toggle", "Allows Maya to stop her Phaselock.", True
        )
        optionCommandoToggle = Options.Boolean(
            "Commando Skill Toggle", "Allows Axton to recall his turrets.", True
        )

        self._classOptions = {
            "Psycho": optionPsychoToggle,
            "Mechromancer": optionMechromancerToggle,
            "Gunzerker": optionGunzerkerToggle,
            "Assassin": optionAssassinToggle,
            "Siren": optionSirenToggle,
            "Commando": optionCommandoToggle,
        }

        self.Options = [self._optionCustomKeybind, *self._classOptions.values()]
        self._setupKeybinds(False)

    def Enable(self) -> None:
        super().Enable()

        log(self, f"Version: {self.Version}")

    def ModOptionChanged(self, option, newValue):
        if option.Caption == "Custom Keybind":
            self._setupKeybinds(newValue)

    def _setupKeybinds(self, newValue: bool) -> None:
        self.Keybinds = [
            Keybind(
                "Deactivate Action Skill",
                "F",
                True,
                not newValue,
            )
        ]

    def _log(self, message: str) -> None:
        unrealsdk.Log(f"[{self.Name}] {message}")

    def _getPlayerController(self) -> unrealsdk.UObject:
        return unrealsdk.GetEngine().GamePlayers[0].Actor

    def _isSkillToggleable(self) -> bool:
        player = getCurrentPlayerController()
        className = player.PlayerClass.CharacterNameId.CharacterClassId.ClassName

        if className not in self._classOptions:
            return False

        return self._classOptions[className].CurrentValue

    def _handleSkillToggling(self) -> None:
        player = getCurrentPlayerController()
        skillManager = player.GetSkillManager()
        actionSkill = player.PlayerSkillTree.GetActionSkill()

        if skillManager.IsSkillActive(player, actionSkill):
            actionSkill.bCanBeToggledOff = True
            player.ServerStartActionSkill()

    def GameInputPressed(
        self, bind: KeybindManager.Keybind, event: KeybindManager.InputEvent
    ) -> None:
        if (
            event != KeybindManager.InputEvent.Repeat
            or not self._optionCustomKeybind.CurrentValue
            or not self._isSkillToggleable()
        ):
            return

        self._handleSkillToggling()

    @Hook("WillowGame.WillowUIInteraction.InputKey")
    def _inputKey(
        self,
        caller: unrealsdk.UObject,
        function: unrealsdk.UFunction,
        params: unrealsdk.FStruct,
    ):
        if (
            params.Event != KeybindManager.InputEvent.Repeat
            or self._optionCustomKeybind.CurrentValue
        ):
            return True

        player = getCurrentPlayerController()
        hotkey = player.PlayerInput.GetKeyForAction("ActionSkill", True)

        if params.Key != hotkey or not self._isSkillToggleable():
            return True

        self._handleSkillToggling()

        return True

    @Hook("WillowGame.ActionSkill.OnActionSkillEnded")
    def _onActionSkillEnded(
        self,
        caller: unrealsdk.UObject,
        function: unrealsdk.UFunction,
        params: unrealsdk.FStruct,
    ):
        actionSkill = getCurrentPlayerController().PlayerSkillTree.GetActionSkill()
        actionSkill.bCanBeToggledOff = False

        return True


instance = SkillToggles()
if __name__ == "__main__":
    log(instance, "Manually loaded")
    for mod in Mods:
        if mod.Name == instance.Name:
            if mod.IsEnabled:
                mod.Disable()
            Mods.remove(mod)
            log(instance, "Removed last instance")

            # Fixes inspect.getfile()
            instance.__class__.__module__ = mod.__class__.__module__
            break
RegisterMod(instance)
