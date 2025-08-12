# WiiiPlayer SERVER

from __future__ import print_function
from flask import Flask, Response, Request, redirect, send_from_directory, send_file, request
import os
import dotenv as env
import ssl
from wsgiref.simple_server import WSGIRequestHandler

env.load_dotenv()

IPLAYER_HOST = os.getenv("HOST")
IPLAYER_STATUS = os.getenv("IPLAYER_STATUS") # disabled, maintenance, or null
IPLAYER_VERSION_REQUIRED = os.getenv("IPLAYER_VERREQ") # Wii 1.0.12
IPLAYER_PORT = os.getenv("IPLAYER_PORT") # int
STATUS_MSG = os.getenv("STATUSMSG") # anything or null
PRELOAD_SWF = os.getenv("PRELOAD_SWF") # csv, w/o .swf, SHOULD ALWAYS INCLUDE MAIN_APP
MAIN_APP = os.getenv("MAIN_SWF") # w/o .swf

app = Flask(__name__)
WII_IPLAYER = MAIN_APP+".swf"

@app.before_request
def log():
    print(f"{request.method}: {request.path}, Headers: {dict(request.headers)}")

@app.route("/version.txt")
def versionCheckFile():
    VERSION_CONTENTS = (
        f"versionRequired={IPLAYER_VERSION_REQUIRED}&status={IPLAYER_STATUS}&statusMessage={STATUS_MSG}&mainApplication={MAIN_APP}&preloadFiles={PRELOAD_SWF}"
    )

    return Response(VERSION_CONTENTS, mimetype="application/x-www-form-urlencoded") # can also be text/plain, but according to adobe docs, it should be application/x-www-form-urlencoded

@app.route("/WiiiPlayer.swf")
def WiiiPlayer01():
    return send_from_directory("static", WII_IPLAYER, mimetype="application/x-shockwave-flash")

@app.route("/wiiiplayer")
def WiiiPlayer02():
    return send_from_directory("static", WII_IPLAYER, mimetype="application/x-shockwave-flash")

@app.route("/WiiiPlayer")
def WiiiPlayer03():
    return send_from_directory("static", WII_IPLAYER, mimetype="application/x-shockwave-flash")

@app.route("/wiiiplayer.swf")
def WiiiPlayer04():
    return send_from_directory("static", WII_IPLAYER, mimetype="application/x-shockwave-flash")

@app.route("/proxy.asp")
def WiiiPlayerProxy():
    return "", 403 # to do

@app.route("/fonts.swf")
def iPlayerFonts():
    return send_from_directory("static", "fonts.swf", mimetype="application/x-shockwave-flash")

@app.route("/crossdomain.xml") # cant preload
def crossdomain():
    policy = """<?xml version="1.0"?>
<!DOCTYPE cross-domain-policy SYSTEM "http://www.macromedia.com/xml/dtds/cross-domain-policy.dtd">
<cross-domain-policy>
   <allow-access-from domain="*"/>
</cross-domain-policy>"""
    return Response(policy, mimetype="application/xml")

@app.route("/thumbnails.xml")
def thumbnails_onserver():
    return send_file("thumbnails.xml")

@app.route("/")
def index():
    return "<title>Server is running</title>", 200

if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

    try:
        ctx.load_cert_chain(certfile="ssl/server.pem", keyfile="ssl/server.key")
    except ssl.SSLError as e:
        print(f"SSL ERROR!\n{e}")
        exit()
    
    ctx.set_ciphers("ALL:@SECLEVEL=0")

    print(f"iPlayer Config:\nPreloading: {PRELOAD_SWF}\nStatus Message: {STATUS_MSG}\nRequired version: {IPLAYER_VERSION_REQUIRED}\nMain SWF: {WII_IPLAYER}")
    app.run(host=IPLAYER_HOST, port=IPLAYER_PORT, debug=True, ssl_context=ctx)