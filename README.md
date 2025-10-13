# iPlayer_Wii_Server

Custom server for the BBC iPlayer for the Wii

## Prepatched WAD

A prepatched and hosted WAD is available [here](https://stuff.idkwh.ct8.pl/other/BBC%20iPlayer%20Revival%20(Europe).wad) (Europe only)

**~~If the Wii Shop says an update is available for the iPlayer, DO <u>NOT</u> UPDATE! It will overwrite the patch~~** The iPlayer version was changed to the latest `(v768)`, the Wii Shop Channel cannot update the WAD.

## Self hosting (optional)

Install the requirements by running

```cmd
pip install -r requirements.txt
```

Then run

```cmd
py server.py
```

**No HTTPS is required.**

Get a v256 version of the BBC iPlayer WAD

Unpack the WAD using WADMii

Unpack 000000002.app using U8Mii

Modify the content_domain in /config/config.common.pcf to your domain

Open `/trusted/startup.swf` with JPEXS Free Flash Decompiler, go to `scripts/frame2/DoAction[6]` and add these 2 lines:

```as
Wii.System.WiiSystem.addCAMapping("{yourdomain}",1);
Wii.System.WiiSystem.addUserNameMapping("{yourdomain}");
```

Repack 00000002.app and the WAD

Patch the WAD with [RiiConnect24's Wiimmfi Patcher](https://github.com/RiiConnect24/WiiWare-Patcher/).

This method **works on real hardware**.

## Credits

[idkwh](https://github.com/idkwhere1sthisname): Server and Patching

[YourTooSlow](https://github.com/your2slow): WiiiPlayer.swf recreation (Work in progress)

## Progress on WiiiPlayer.swf

- Home page UI is semi-complete, video thumbnails load and scrolling through videos with the arrows also work. Exit button redirects to the Wii Menu

- Other pages and features (like playing videos and almost every button) **do not work at this time**.
