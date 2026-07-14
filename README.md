# iPlayer_Wii_Server

Custom server for the BBC iPlayer for the Wii

## Prepatched WAD

A prepatched and hosted WAD is available below:
- [European Version](https://img.idkwh.ct8.pl/iPlayer_Wii_Server/wad/BBC%20iPlayer%20Revival%20(Europe).wad)
- [American Version](https://img.idkwh.ct8.pl/iPlayer_Wii_Server/wad/BBC%20iPlayer%20Revival%20(USA).wad) An update is available to the USA WAD, **this fixes every issue with the previous one.** (e.g. not being able to return to the Wii Menu)

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

- Decompress the DOL using [CUE's DS decompressors](https://github.com/PeterLemon/Nintendo_DS_Compressors) (LZX)

- Open the DOL in a hex editor and jump to offset `0x001691B8`

- Replace the next `0x3` bytes relative to said offset (`0x418200`) with `0x480000` (this is required to bypass an exception when opening the main U8 file)*

```asm
lwz        r5,0x0(r3)
subis      r0,r5,0x55aa
cmplwi     r0,0x382d
b          LAB_8016eeb4 ; HERE (beq->b)
lis        r5,-0x7fbd
subi       r3=>DAT_804d4570,r13
subi       r5=>s_ARCInitHandle:_bad_archive_forma_804284e   = "ARCInitHandle: bad archive fo(-rmat)"
li         r4,0x4a
```

- Compress the DOL

- Repack the WAD

These patching methods **works on real hardware**.

## Credits

[idkwh](https://github.com/idkwhere1sthisname): Server and old HTTPS patching method

[YourTooSlow](https://github.com/your2slow): WiiiPlayer.swf recreation (Work in progress)

[Tanjirokamado12](https://github.com/Tanjirokamado12): New HTTP patching method

## Progress on WiiiPlayer.swf

- Home page UI is semi-complete, video thumbnails load and scrolling through videos with the arrows also work. Exit button redirects to the Wii Menu

- Other pages and features (like playing videos and almost every button) **do not work at this time**.

## Other

- If hovering over text is glitched on Dolphin, go to Options->Graphics Settings->Hacks and drag the texture cache slider to the leftmost value (Safe), this will also fix channels like Kirby TV and YouTube (and every Flash-based "VC" inject)

- If the channel freezes with an invalid write while watching a video, go to Options->Configuration->Advanced, and enable Memory Override, then drag both the MEM1 and MEM2 sliders to the rightmost value, this will increase the MEM1 and MEM2 arena sizes (other titles might not work with this setting enabled)
