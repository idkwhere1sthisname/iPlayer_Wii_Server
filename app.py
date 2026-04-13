from __future__ import print_function
import requests as reqs
from flask import Flask,Response,send_from_directory,send_file,request,abort
import os
from werkzeug.serving import WSGIRequestHandler
import xml.etree.ElementTree as ET
CONFIG = os.path.join(os.path.dirname(__file__),"config.xml")
STATIC = os.path.join(os.path.dirname(__file__),"static")
app = Flask("iplayer-wii",static_folder="static")
def loadcfg():
    global IPLAYER_HOST,IPLAYER_STATUS,IPLAYER_VERSION_REQUIRED,IPLAYER_PORT,STATUS_MSG,PRELOAD_SWF,MAIN_APP,WII_IPLAYER,DEBUG
    tree = ET.parse(CONFIG)
    root = tree.getroot()
    IPLAYER_HOST = root.find("host").text
    IPLAYER_PORT = root.find("port").text
    IPLAYER_STATUS = root.find("status").text or "active"
    IPLAYER_VERSION_REQUIRED = root.find("versionRequired").text or "Wii 1.0.12"
    STATUS_MSG = root.find("statusMessage").text or ""
    PRELOAD_SWF = root.find("preloadFiles").text or ""
    MAIN_APP = root.find("mainApplication").text
    DEBUG = root.find("debug").text.lower() == "true"
@app.route("/version.txt")
def versiontxt():
    VERSION_CONTENTS = (
        f"status={IPLAYER_STATUS}&"
        f"versionRequired={IPLAYER_VERSION_REQUIRED}&"
        f"statusMessage={STATUS_MSG}&"
        f"mainApplication={MAIN_APP}&"
        f"preloadFiles={PRELOAD_SWF}"
    )
    return Response(VERSION_CONTENTS,status=200,mimetype="application/x-www-form-urlencoded")

@app.route("/<string:filename>.swf")
def serveswf(filename):
    if not os.path.exists(os.path.join(STATIC,filename+".swf")):
        return abort(404)
    return send_from_directory(STATIC,filename+".swf"),200,{"Content-Type":"application/x-shockwave-flash"}
@app.route("/proxy.asp", methods=["GET", "POST"]) # used?
def WiiiPlayerProxy():
    data = request.args
    url = data.get("url")
    key = data.get("key")
    if not url:
        return abort(400)
    if not key or key != "nstnstnst": # constant
        return abort(403)
    try:
        res = reqs.get(url, stream=True)
        return Response(
            res.iter_content(chunk_size=1024),
            status=res.status_code,
            content_type=res.headers.get("Content-Type")
        )
    except reqs.RequestException as e:
        return f"Error trying to fetch URI: {e}", 500
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
    if not os.path.exists(os.path.join(STATIC,"thumbnails.xml")):
        return abort(404)
    return send_from_directory(STATIC,"thumbnails.xml")
if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    try:
        if not os.path.exists(CONFIG):
            host = input("Where should the server run? (0.0.0.0 for all interfaces): ")
            port = None
            while port is None:
                try:
                    port_in = input("On what port should the server run? (80 is recommended): ")
                    port = int(port_in)
                except ValueError:
                    print("Invalid input. Please enter a valid number")
            port = str(port)
            dbg = input("Should the server run with debug enabled? (yes/no): ").lower()
            while dbg not in ["yes","no"]:
                dbg = input("Please enter either yes or no: ").lower()
            debug = dbg == "yes"
            config = ET.Element("configuration")
            ET.SubElement(config,"host").text = host
            ET.SubElement(config,"port").text = port
            ET.SubElement(config,"debug").text = str(debug).lower()
            print("(now is the actual BBC iPlayer channel configuration)")
            versionRequired = input("Please enter the version required for the BBC iPlayer channel (if unsure, press enter and it'll automatically set to \"Wii 1.0.12\"): ")
            if versionRequired == "":
                versionRequired = "Wii 1.0.12"
            status = input('Please enter the service status (it can be "maintenance" for a maintenance message, "disabled" for a discontinuation message, or anything for it to load) (default: active): ')
            if status == "":
                status = "active"
            mainApplication = input("Please enter the main SWF's filename (it shouldn't end with the .swf extension, it also has to be stored in the static folder): ")
            preloadFiles = input("Please enter a comma-separated list of SWFs the channel should preload (NOTES: every file must not have the .swf extension, do not include the main application, each SWF has to be stored in the static folder, if empty, \"PRELOADME\" is automatically added, as the channel cannot proceed without preloading at least one SWF): ")
            if preloadFiles == "":
                preloadFiles = "PRELOADME"
            statusMessage = input('Please enter the status message that is shown when the staus is set to "maintenance" or "disabled", or if the version required doesn\'t match (leave blank for the default message set by channel): ')
            ET.SubElement(config,"versionRequired").text = versionRequired
            ET.SubElement(config,"status").text = status
            ET.SubElement(config,"mainApplication").text = mainApplication
            ET.SubElement(config,"preloadFiles").text = preloadFiles
            ET.SubElement(config,"statusMessage").text = statusMessage
            ET.ElementTree(config).write(CONFIG,encoding="UTF-8",xml_declaration=True)
        loadcfg()
        app.run(host=IPLAYER_HOST,port=int(IPLAYER_PORT),debug=DEBUG)
    except KeyboardInterrupt:
        print("\nExiting")
