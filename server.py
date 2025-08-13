# WiiiPlayer SERVER

from __future__ import print_function
import requests as reqs
from flask import Flask, Response, Request, redirect, send_from_directory, send_file, request
import os
import ssl
from wsgiref.simple_server import WSGIRequestHandler
import xml.etree.ElementTree as ET

tree = ET.parse("config.xml")
root = tree.getroot()

IPLAYER_HOST = root.find("host").text
IPLAYER_STATUS = root.find("status").text
IPLAYER_VERSION_REQUIRED = root.find("version_required").text
IPLAYER_PORT = root.find("port").text
STATUS_MSG = root.find("status_message").text
PRELOAD_SWF = root.find("preload_swf").text
MAIN_APP = root.find("main_swf").text

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

@app.route("/proxy.asp", methods=["GET", "POST"]) # used?
def WiiiPlayerProxy():
    url = request.args.get("url")
    key = request.args.get("key")

    if not url:
        return "Bad request", 400
    
    if not key or key != "nstnstnst": # constant
        return "Unauthorized", 403
    
    try:
        res = reqs.get(url, stream=True)

        return Response(
            res.iter_content(chunk_size=1024),
            status=res.status_code,
            content_type=res.headers.get("Content-Type")
        )
    except reqs.RequestException as e:
        return f"Error trying to fetch URI: {e}", 500


@app.route("/fonts.swf")
def iPlayerFonts():
    return send_from_directory("static", "fonts.swf", mimetype="application/x-shockwave-flash")

@app.route("/crossdomain.xml")
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