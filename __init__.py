import unrealsdk
import webbrowser
from typing import Dict, Optional

from Mods.ModMenu import (
    EnabledSaveType,
    Game,
    Hook,
    Keybind,
    KeybindManager,
    Mods,
    ModTypes,
    Options,
    RegisterMod,
    SDKMod,
    ServerMethod,
)

try:
    from Mods.EridiumLib import (
        getCurrentPlayerController,
        getLatestVersion,
        isClient,
        isLatestRelease,
        log,
    )
    from Mods.EridiumLib.keys import KeyBinds
except ModuleNotFoundError or ImportError:
    webbrowser.open("https://github.com/RLNT/bl2_eridium#-troubleshooting")
    raise

if __name__ == "__main__":
    import importlib
    import sys

    importlib.reload(sys.modules["Mods.EridiumLib"])
    importlib.reload(sys.modules["Mods.EridiumLib.keys"])

    # See https://github.com/bl-sdk/PythonSDK/issues/68
    try:
        raise NotImplementedError
    except NotImplementedError:
        __file__ = sys.exc_info()[-1].tb_frame.f_code.co_filename  # type: ignore


class SkillToggles(SDKMod):
    # region Mod Info
    Name: str = "Skill Toggles"
    Author: str = "Relentless, Chronophylos"
    Description: str = "Deactivate Action Skills by holding a configurable hotkey."
    Version: str = "1.2.0"

    SupportedGames: Game = Game.BL2
    Types: ModTypes = ModTypes.Utility
    SaveEnabledState: EnabledSaveType = EnabledSaveType.LoadWithSettings

    SettingsInputs: Dict[str, str] = {
        KeyBinds.Enter.value: "Enable",
        KeyBinds.G.value: "GitHub",
        KeyBinds.D.value: "Discord",
    }
    # endregion Mod Info

    # region Mod Setup
    def __init__(self) -> None:
        super().__init__()

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
        self.Options = [*self._classOptions.values()]

        self.Keybinds = [
            Keybind(
                "Deactivate Action Skill",
                "F",
                True,
                OnPress=self._skillDeactivationHotkey,
            )
        ]

    def Enable(self) -> None:
        super().Enable()

        log(self, f"Version: {self.Version}")
        latest_version = getLatestVersion("RLNT/bl2_skilltoggles")
        log(
            self,
            f"Latest release tag: {latest_version}",
        )
        if isLatestRelease(latest_version, self.Version):
            log(self, "Up-to-date")
        else:
            log(self, "There is a newer version available {latest_version}")

    def SettingsInputPressed(self, action: str) -> None:
        if action == "GitHub":
            webbrowser.open("https://github.com/RLNT/bl2_skilltoggles")
        elif action == "Discord":
            webbrowser.open("https://discord.com/invite/Q3qxws6")
        else:
            super().SettingsInputPressed(action)

    # endregion Mod Setup

    # region Hotkey Handling
    def _skillDeactivationHotkey(self, event: KeybindManager.InputEvent) -> None:
        """
        handles the modded hotkey input
        """
        if event == KeybindManager.InputEvent.Repeat:
            self._skillDeactivation()

    # endregion Hotkey Handling

    # region Skill Deactivation
    def _skillDeactivation(self) -> None:
        """
        handles the skill deactivation
        """
        if isClient():
            self._requestSkillDeactivation()
        else:
            self._executeSkillDeactivation()

    @ServerMethod
    def _requestSkillDeactivation(
        self,
        PC: Optional[unrealsdk.UObject] = None,
    ) -> None:
        self._executeSkillDeactivation(PC)

    def _executeSkillDeactivation(
        self,
        PC: Optional[unrealsdk.UObject] = None,
    ) -> None:
        # if PC is None, get current local player
        if PC is None:
            PC = getCurrentPlayerController()

        # check if the skill for the current local player is toggleable (config option)
        className: str = PC.PlayerClass.CharacterNameId.CharacterClassId.ClassName
        if (
            className not in self._classOptions
            or self._classOptions[className].CurrentValue is False
        ):
            return

        # deactivate the action skill if it's active
        gameInfo = unrealsdk.GetEngine().GetCurrentWorldInfo().Game
        skillManager = gameInfo.GetSkillManager()
        actionSkill = PC.PlayerSkillTree.GetActionSkill()

        if skillManager.IsSkillActive(PC, actionSkill):
            actionSkill.bCanBeToggledOff = True
            PC.ServerStartActionSkill()

    # endregion Skill Deactivation

    # region Info Reset
    @Hook("WillowGame.ActionSkill.OnActionSkillEnded")
    def _onActionSkillEnded(
        self,
        caller: unrealsdk.UObject,
        function: unrealsdk.UFunction,
        params: unrealsdk.FStruct,
    ) -> bool:
        """
        handles reset of the changed player information
        runs on player and host so it needs info checks
        """
        if isClient():
            self._requestInfoReset()
        else:
            self._executeInfoReset()

        return True

    @ServerMethod
    def _requestInfoReset(self, PC: Optional[unrealsdk.UObject] = None) -> None:
        self._executeInfoReset(PC)

    def _executeInfoReset(self, PC: Optional[unrealsdk.UObject] = None) -> None:
        # if PC is None, get current local player
        if PC is None:
            PC = getCurrentPlayerController()

        # only reset if it was changed because the hook is called for player and host
        actionSkill = PC.PlayerSkillTree.GetActionSkill()
        if actionSkill.bCanBeToggledOff is True:
            actionSkill.bCanBeToggledOff = False

    # endregion Info Reset


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
