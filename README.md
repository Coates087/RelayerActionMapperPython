#  Relayer Action Mapper PE
 
Hello. Welcome to the Relayer Action Remapper PE (Python Edition) tool. This utility tool is designed to make customizing the controls for Relayer Advanced on PC easier to do.

Currently, you can change the game's controls by editing the KeyConfig.json inside the (game directory)\KeyConfig\ directory. There are two problems with this. First, all of control actions in the file are referred to the keys and not the actions their selves. What I mean is, instead of having:
`jump = "keyname"`, the game uses the following:
`"Enter" = ["Return","Space"]`

In the above example, the "Enter" action acts as the "confirm" button.

The second problem with this is that even if the user can get used to editing the json file by hand for the keys, it will make it difficult to customize the controls with the Controller Prompts Mod from [Nexus Mods](https://www.nexusmods.com/relayeradvanced/mods/1) or [Game Banana](https://gamebanana.com/mods/490768)

This tool aims to solve both of those problems.

Unlike the original [Relayer Action Mapper Tool](https://github.com/Coates087/RelayerActionMapper/tree/main), this tool is specifically designed to be compatible with Linux. As to why? The according to Steam, this game does have support for the Steam Deck, which uses a version of Linux.


## Credits
Special thanks to **Meekurukuru** from Nexus Mods. Check out some of his mods below:\
[https://www.nexusmods.com/users/189494967?tab=user+files&BH=0](https://www.nexusmods.com/users/189494967?tab=user+files&BH=0)
