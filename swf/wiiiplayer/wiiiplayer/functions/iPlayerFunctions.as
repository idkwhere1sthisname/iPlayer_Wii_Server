class wiiiplayer.functions.iPlayerFunctions {
    static var systemRoot = _global.my.extensions.WiiSystem;
    static var mxEventDispatcher = _global.mx.events.EventDispatcher;
    static var BroadcasterMX = _global.mx.transitions.BroadcasterMX;
    static var mxOnEnterFrameBeacon = _global.mx.transitions.OnEnterFrameBeacon;
    static var mxDelegate = _global.mx.utils.Delegate;
    static var systemBuildTime_Fmt = new Date(Number(_global.my.extensions.WiiSystem.getBuildTime() * 1000));
    static var USER_CHOSE_SECT = "HOMESECT";
    static var ALLOWED_SECT = ["HOMESECT", "RADIOSECT", "TVSECT", "SEARCHSECT"]
    static var CMN_ERROR_CODE = "375003";
    static var CMN_ERROR_TEXT = "An error has occurred.";
    static var PROTOCOL = "http";
    static var METHOD_GET = "GET";
    static var METHOD_POST = "POST";
    static var METHOD_OPTIONS = "OPTIONS";
    static var METHOD_HEAD = "HEAD";
    static var BUILD_TIME = "0"
    static var _hbmEnabled = true;
    static var _dimmingEnabled = true;
    static var IS_DEBUG = false; // set to false to hide menu
    //static var MAIN_TIMELINE = this;
    static var PARENTAL_CONTROLS = _global.my.extensions.WiiSystem.isParentalControlEnabled();
	static var BASE_HOST = "iplayer.idkwh.ct8.pl";
    static var BASE_URL = _global.wiiiplayer.functions.iPlayerFunctions.PROTOCOL + "://"+_global.wiiiplayer.functions.iPlayerFunctions.BASE_HOST;
    static var iplayer_flashVars = {};
    static function postStartup() {
        trace("onPostStartup");
        if (_global.mx == undefined) {
            _parent.displayAlert("An error has occurred. \n Error Code: 375003", "To try again go back to the Wii Menu");
            trace("MX Std is missing...");
            return undefined;
        }
        if (!_global.my.extensions.WiiSystem.isWii() && !_global.wiiiplayer.functions.iPlayerFunctions.IS_DEBUG) {
            _parent.displayAlert("An error has occurred. \n Error Code: 375003", "To try again go back to the Wii Menu");
            trace("Not a wii...");
            return undefined;
        }
        _parent.hasLoaded(); // !!! removes WiiSystem (not my.extensions) and displayAlerts
        _global.my.extensions.WiiSystem.allowHomeButton(true);
        _global.wiiiplayer.functions.iPlayerFunctions._hbmEnabled = true;
        return undefined;
    }
    static function unload() {
        trace("onCleanup");
        delete _global.WiiiPlayer;
        delete wiiiplayer;
        return undefined;
    }
    static function get homeButtonEnabled() {
        return _global.wiiiplayer.functions.iPlayerFunctions._hbmEnabled;
    }
    static function set homeButtonEnabled(v) {
        if (v == _global.wiiiplayer.functions.iPlayerFunctions._hbmEnabled) {
            return;
        }
        _global.wiiiplayer.functions.iPlayerFunctions._hbmEnabled = v;
        _global.my.extensions.WiiSystem.allowHomeButton(_global.wiiiplayer.functions.iPlayerFunctions._hbmEnabled);
    }
    static function get dimmingEnabled() {
        return _global.wiiiplayer.functions.iPlayerFunctions._dimmingEnabled;
    }
    static function set dimmingEnabled(v) {
        if (v == _global.wiiiplayer.functions.iPlayerFunctions) {
            return;
        }
        _global.wiiiplayer.functions.iPlayerFunctions._dimmingEnabled = v;
        _global.my.extensions.WiiSystem.enableDimming(_global.wiiiplayer.functions.iPlayerFunctions._dimmingEnabled);
    }
    static function load() {
        trace("onStartup");
        _global.WiiiPlayer = _global.wiiiplayer.functions.iPlayerFunctions;
        return true;
    }
    static function loadCrossDomainXML() {
        System.security.loadPolicyFile(_global.wiiiplayer.functions.iPlayerFunctions.BASE_URL + "/crossdomain.xml");
        trace("crossdomain.xml loaded successfully");
    }
    static function getSystem() {
        return _global.my.extensions.WiiSystem;
    }
	static function loadWiiiPlayerFlashVars() {
		var lv_r = new LoadVars();
		var url;
		if (!_global.wiiiplayer.functions.iPlayerFunctions.IS_DEBUG) {
			url = _global.wiiiplayer.functions.iPlayerFunctions.BASE_URL + "/wiiiplayer_vars.txt";
		} else {
			url = "http://127.0.0.1/WiiiPlayer_vars.txt";
		}
		lv_r.onLoad = function(success) {
			if (!success) {
				trace("Load failed");
				return;
			}
			for (var fv in lv_r) {
				if (typeof(lv_r[fv]) == "string") {
					_global.wiiiplayer.functions.iPlayerFunctions.iplayer_flashVars[fv] = lv_r[fv];
				}
			}
			_global.hasLoadedWiiiPlayerFV = true;
			if (_root.onDataReady != undefined) {
				_root.onDataReady();
			}
		};
		lv_r.load(url);
	}
    static function fixElements(elementsArray) {
        Stage.scaleMode = "noScale";
        Stage.align = "TL";

        //var stageWidth = 640; // for debug (4:3)
        //var stageWidth = 854; // for debug (16:9)
        var stageWidth = Stage.width; // prod

        var i = 0;
        var element;

        while (i < elementsArray.length) {
            element = elementsArray[i];

            if (element.clip != undefined && element.clip._x != undefined) {
                var clip = element.clip;

                if (clip.originalX == undefined) {
                    clip.originalX = clip._x;
                }

                if (stageWidth <= 640) {
                    clip._x = clip.originalX + element.offsetX;
                } else {
                    clip._x = clip.originalX;
                }

            } else {
                trace("element " + i + " is undefined or missing");
            }

            i++;
        }

        _global.hasShifted = true;
    }

    static function jumpToMenu() {
        trace("Should be returning to menu...");
        _global.my.extensions.WiiSystem.removeAllHeaders();
        _global.wiiiplayer.functions.iPlayerFunctions.unload();
        _global.my.extensions.WiiSystem.returnToMenu();
    }

    static function jumpToParental() {
        trace("Should be prompting parental controls...");
        _global.my.extensions.WiiSystem.promptParentalControlPin();
    }
	
	static function getFreeMem(arena) {
		if (arena == 2) {
			return int(_global.my.extensions.WiiSystem.getFreeMemory2());
		}
		if (arena == 3) {
			var MEM1_Arena = int(_global.my.extensions.WiiSystem.getFreeMemory1());
			var MEM2_Arena = int(_global.my.extensions.WiiSystem.getFreeMemory2());
			return String(MEM1_Arena+MEM2_Arena);
		}
		return int(_global.my.extensions.WiiSystem.getFreeMemory1());
	}
	
    static function jumpToVODFPlayer(id) {
        trace("onVodfPlayerJump with id " + id);
		if (_global.wiiiplayer.functions.iPlayerFunctions_IS_DEBUG) {
			_global.my.extensions.WiiSystem.addHeader("Mem1-Arena",_global.wiiiplayer.functions.iPlayerFunctions.getFreeMem(1));
			_global.my.extensions.WiiSystem.addHeader("Mem2-Arena",_global.wiiiplayer.functions.iPlayerFunctions.getFreeMem(2));
			_global.my.extensions.WiiSystem.addHeader("Free-Mem",_global.wiiiplayer.functions.iPlayerFunctions.getFreeMem(3));
		}
        loadMovieNum("VODFPlayer.swf", 1);
    }

    static function jumpToWiiiPlayer(id) {
        trace("onWiiiplayerJump with id " + id);
        unloadMovieNum(1);
    }

    static function changeHoverColorTex(ItemTex, ItemTexCode) {
        if (ItemTexCode == "" || ItemTexCode == undefined) {
            trace("No ITEMTEXCODE, aborting...");
            return undefined;
        }
        if (ItemTexCode == _global.wiiiplayer.functions.iPlayerFunctions.USER_CHOSE_SECT) {
            trace("ITEMTEXCODE same as USER_CHOSE_SECT");
            return undefined;
        }
        if (ItemTex != undefined) {
            ItemTex.textColor = 0xF54896;
            return undefined;
        }
        return undefined;
    }

    static function restoreHoverColorTex(ItemTex, ItemTexCode) {
        if (ItemTexCode == wiiiplayer.functions.iPlayerFunctions.USER_CHOSE_SECT) {
            trace("ITEMTEXCODE same as USER_CHOSE_SECT");
            return undefined;
        }
        if (ItemTexCode != wiiiplayer.functions.iPlayerFunctions.USER_CHOSE_SECT) {
            ItemTex.textColor = 0xFFFFFF;
            return undefined;
        }
        return undefined;
    }

    static function jumpToVODFPlayerFRAME() {
        trace("Jumping to VODF Player...");
        _root.gotoAndStop("VODFPlayer");
    }

    static function jumpToNewPlayerTexFrame(target, frameN, ItemTexCode) {
        if (!ItemTexCode) {
            trace("No ItemTexCode, aborting...");
            return undefined;
        }

        if (ItemTexCode != wiiiplayer.functions.iPlayerFunctions.USER_CHOSE_SECT) {
            if (frameN != undefined && frameN != null) {
                _global.mainTimeline.gotoAndStop(frameN);
                wiiiplayer.functions.iPlayerFunctions.USER_CHOSE_SECT = ItemTexCode;
                trace("set ITEMTEXCODE to " + ItemTexCode);
                return null;
            } else {
                trace("frameN is null or undefined, aborting...");
                return undefined;
            }
        } else {
            trace("ItemTexCode same as USER_CHOSE_SECT, aborting...");
            return undefined;
        }
    }
}
