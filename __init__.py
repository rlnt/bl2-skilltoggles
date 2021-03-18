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
    RegisterMod,
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
            player.ServerStartActionSkill()

    def GameInputPressed(
        self, bind: KeybindManager.Keybind, event: KeybindManager.InputEvent
    ) -> None:
        if (
            event != KeybindManager.InputEvent.Repeat
            or self._optionCustomKeybind.CurrentValue == False
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
            or self._optionCustomKeybind.CurrentValue == True
        ):
            return True

        player = self._getPlayerController()
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
        actionSkill = self._getPlayerController().PlayerSkillTree.GetActionSkill()
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
