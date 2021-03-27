# **Skill Toggles** [![Workflow Status][workflow_status_badge]][workflow_status_link] [![Total Downloads][total_downloads_badge]][total_downloads_link] [![License][license_badge]][license] [![Code Style][black_badge]][black_link]

> A [PythonSDK] mod for [Borderlands 2][borderlands2] and [Borderlands TPS][borderlandstps] to deactivate Action Skills with a configurable hotkey.

- [Discord][discord]
- PythonSDK: `v0.7.9`
- Mod Menu: `v2.4`
- EridiumLib: `v0.4.1`

---

## **📎 Features**
- deactivate the Action Skill for each character
- configurable hotkey
- options to enable the feature for each class individually


## **📑 Notes**
- this is a [PythonSDK] mod, you **can't** install it with BLCMM
- this mod needs the [EridiumLib] in order to run
- since this is often not the case with SDK mods: yes, this has multiplayer support
- deactivating Action Skills won't give you a cooldown bonus
  - there are some exceptions in Borderlands TPS where it works
- in a multiplayer environment, only the host settings of the mod are taken into account
  - that means only the host can define which Action Skills are deactivatable
  - you can still use your own hotkey
- the default toggle hotkey is `F` which also is the default Action Skill key
  - you need to *hold* the key, not just press it to avoid accidental deactivations
  - you can change it to anything in the modded keybinds but you can't change it back to `F` because it's already taken by the Action Skill
  - if you want to use the `F` key again or, generally spoken, the hotkey you have for activating the Action Skill, you need to delete the `settings.json` file in the mod directory, restart the game and reenable the mod
  - if you are using another hotkey for the Action Skill, you can also directly edit the modded hotkey in the `settings.json` file while the game is closed


## **🔧 Installation**
1. download the latest **release** of this mod from [releases]
2. download the latest **release** of the EridiumLib from [here][eridiumlib_releases]
3. extract it to:
   - `Borderlands 2\Binaries\Win32\Mods`
4. activate the mod in the Mod Menu within the game


## **⏰ Changelog**
Everything related to versions and their release notes can be found in the [changelog].


## **🎓 License**
This project is licensed under the [GNU GPL v3.0][license].

<!-- Badges -->
[workflow_status_badge]: https://img.shields.io/github/workflow/status/RLNT/bl2_skilltoggles/CI?style=flat-square
[workflow_status_link]: https://github.com/RLNT/bl2_skilltoggles/actions/workflows/main.yml
[total_downloads_badge]: https://img.shields.io/github/downloads/RLNT/bl2_skilltoggles/total?style=flat-square
[total_downloads_link]: https://github.com/RLNT/bl2_skilltoggles/releases/latest
[license_badge]: https://img.shields.io/github/license/RLNT/bl2_skilltoggles?style=flat-square
[black_badge]: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square
[black_link]: https://github.com/psf/black


<!-- Links -->
[pythonsdk]: http://borderlandsmodding.com/sdk-mods/
[borderlands2]: https://store.steampowered.com/app/49520/Borderlands_2/
[borderlandstps]: https://store.steampowered.com/app/261640/Borderlands_The_PreSequel/
[discord]: https://discordapp.com/invite/Q3qxws6
[releases]: https://github.com/RLNT/bl2_skilltoggles/releases
[eridiumlib]: https://github.com/RLNT/bl2_eridium
[eridiumlib_releases]: https://github.com/RLNT/bl2_eridium/releases
[changelog]: CHANGELOG.md
[license]: LICENSE
