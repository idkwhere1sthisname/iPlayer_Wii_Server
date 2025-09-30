# iPlayer_Wii_Server
Custom server for the BBC iPlayer for the Wii

# Setup

Install the requirements by running

```cmd
pip install -r requirements.txt
```

Then run

```cmd
py server.py
```

# Setup
**No HTTPS is required.**

Get a v256 version of the BBC iPlayer WAD

Unpack the WAD using WADMii

Unpack 000000002.app using U8Mii

Modify the content_domain in /config/config.common.pcf to your domain

Open /trusted/startup.swf with JPEXS, go to scripts/frame2/DoAction\[6\] and add these 2 lines:

```as
Wii.System.WiiSystem.addCAMapping("{yourdomain}",1);
Wii.System.WiiSystem.addUserNameMapping("{yourdomain}");
```

Repack 00000002.app and the WAD

# Credits

idkwh: Server and Patching

YourTooSlow: WiiiPlayer.swf recreation (Work in progress)

# Progress on WiiiPlayer.swf

- Home page UI is semi-complete, video thumbnails load and scrolling through videos with the arrows also work. Exit button redirects to the Wii Menu

- Other pages and features (like playing videos and almost every button) **do not work at this time**.
