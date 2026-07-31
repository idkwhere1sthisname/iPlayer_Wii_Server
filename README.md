# iPlayer_Wii_Server

Custom server for the BBC iPlayer for the Wii

## Prepatched WAD

You can download my WAD patcher from [here](https://github.com/idkwhere1sthisname/revival-patcher)

**~~If the Wii Shop says an update is available for the iPlayer, DO <u>NOT</u> UPDATE! It will overwrite the patch~~** The iPlayer version was changed to the latest `(v768)`, the Wii Shop Channel cannot update the WAD.

<div align="center">
    <img src="https://img.idkwh.ct8.pl/iPlayer_Wii_Server/preview_1.png" align="center" width="320" height="240" />
</div>

## Self hosting (optional)

Install the requirements by running

```cmd
pip install -r requirements.txt
```

Then run

```cmd
py server.py
```

**HTTPS is not required.**

- Get a v256 version of the BBC iPlayer WAD

- Unpack the WAD using WADMii

- Unpack `00000002.app` using U8Mii

- Modify `content_domain` in `/config/config.common.pcf` to your domain

```ini
####### iPlayer ########

content_domain                  {yourdomain}
#content_domain                 https://wii-test.nintendo.iplayer.bbc.co.uk/wii-test/tvp/
#content_domain                 https://wii.nintendo.iplayer.bbc.co.uk/testwiiiplayer/tvp/livetest/
content_url                     file:///trusted/startup.swf
```

- Open `/trusted/startup.swf` with JPEXS Free Flash Decompiler, go to `scripts/frame2/DoAction[6]` and add these 2 lines:

```as
// replace "{yourdomain}" with your actual domain or IP
Wii.System.WiiSystem.addCAMapping("{yourdomain}",1);
Wii.System.WiiSystem.addUserNameMapping("{yourdomain}");
```

- Repack `00000002.app` and the WAD

- Patch the WAD with [RiiConnect24's Wiimmfi Patcher](https://github.com/RiiConnect24/WiiWare-Patcher/).

- Optionally recompress the DOL with LZ11 encoding to save NAND/SD space.

## Convert the WAD to NTSC Video

- Unpack a BBC iPlayer v258 WAD
- Unpack `00000002.app`
- Navigate to `/config/EU/`
- Delete `IT`, `NL` and `DE` (those are languages that can't be set in an American console)
- For each remaining directory (`EN`, `ES` and `FR`):
    - Delete:
        - `config.prog.eurgb60.pcf`
        - `config.prog.eurgb60.wide.pcf`
          - Both of these are just includes.
        - `config.pal.pcf`
        - `config.pal.wide.pcf`
    - Rename:
        - `config.eurgb60.pcf` to `config.ntsc.pcf`
        - `config.eurgb60.wide.pcf` to `config.ntsc.wide.pcf`
    - Copy:
        - `config.ntsc.pcf` to `config.prog.ntsc.pcf`
        - `config.ntsc.wide.pcf` to `config.prog.ntsc.wide.pcf`
- Repack `00000002.app`
- Repack the WAD
These patching methods **works on real hardware**.

## Credits

[idkwh](https://github.com/idkwhere1sthisname): Server and old HTTPS patching method

[YourTooSlow](https://github.com/your2slow): WiiiPlayer.swf recreation (Work in progress)

[Tanjirokamado12](https://github.com/Tanjirokamado12): New HTTP patching method

## Progress on WiiiPlayer.swf

- Playing videos sometimes works, TV menu and basic animations are implemented (but almost every other button) **does not work at this time**.

## Other

- If hovering over text is glitched on Dolphin, go to Options->Graphics Settings->Hacks and drag the texture cache slider to the leftmost value (Safe), this will also fix channels like Kirby TV and YouTube (and every Flash-based "VC" inject)

- If the channel freezes with an invalid write while watching a video, go to Options->Configuration->Advanced, and enable Memory Override, then drag both the MEM1 and MEM2 sliders to the rightmost value, this will increase the MEM1 and MEM2 arena sizes (other titles might not work with this setting enabled)
