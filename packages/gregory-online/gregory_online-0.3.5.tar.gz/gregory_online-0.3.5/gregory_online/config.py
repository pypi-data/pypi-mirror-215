#!/usr/bin/env python3
from gregory_online.version import __version__
from fire import Fire

import json
import os
import sys




#-------==========---------------------------
# changing 20230616
# common :  polltime  window
# def online0 online1 ...
CONFIG={
    "version":3,
    "poll_time":5,
    "window":30,
    "online0":{
        "online":True,
        "spectrum":"b0c00",
        "description":"local server - channel 0",
        "server":"127.0.0.1",
        "udp_ip":"127.0.0.1",
        "influx":False,
        "data_folder":"./",
    },
    "online1":{
        "online":True,
        "spectrum":"b0c01",
        "description":"local server - channel 1",
        "server":"127.0.0.1",
        "udp_ip":"127.0.0.1",
        "influx":False,
        "data_folder":"./",
    },
    "offline":{
        "online":False,
        "description":"offline, local files",
        "data_folder":"./",
    },
    "offlineweb":{
        "online":False,
        "description":"offline, NAS 20 concrete files",
        "data_folder":"http://10.10.104.20/WEBDATA/20220906_LOCAL_NPI_REZ_ORTEC_ALL/DATA_20230605_20230614_concrete2/"
    },
    "placeholder": True
}





#CFG_DEBUG = True
#CFG_DEBUG = False


#===========================================================
#===========================================================
#===========================================================

def verify_config(filename = ""):
    '''used inside, verification of bak json version'''
    global CONFIG
    if filename != "":
        CONFIG['filename'] = filename
    cfg = CONFIG['filename']
    #if CFG_DEBUG:print("D... verifying config from",cfg)
    ok = False
    try:
        if os.path.isfile( os.path.expanduser(cfg)):
            with open(os.path.expanduser(cfg), "r") as f:
                dicti = json.load(f)
        ok = True
        #if CFG_DEBUG:print("D... config verified")
    except:
        #if CFG_DEBUG:
        print("D... verification config FAILED")
    return ok



def get_config_file():
    ''' returns the filename where config is stored'''
    global CONFIG
    return CONFIG['filename']



def show_config( cdict=None , filename = ""):
    '''used inside, shows current config dictionary OR other dict'''
    global CONFIG
    if filename != "":
        CONFIG['filename'] = filename
    if cdict==None:
        print( json.dumps(CONFIG, indent=1) )
    else:
        print( json.dumps(cdict, indent=1) )



def cfg_to_bak(filenamebk="", filename = ""):
    '''used inside, rename config (before save)'''
    global CONFIG
    if filename != "":
        CONFIG['filename'] = filename

    if filenamebk=="":
        cfg = CONFIG['filename']
    else:
        cfg = filenamebk

    cfgbak = cfg + ".bak"
    #print("D... cfg:",cfg)
    #print("D... cfgbak:",cfgbak)
    #if CFG_DEBUG:
    #print("D... creating a backup config:", cfgbak )
    if not os.path.isfile( os.path.expanduser(cfg)):
        print(f"X... config {cfg} doesnt exist (yet?, OK)")
        return True

    ### rozXXXX
    try:
        os.rename(os.path.expanduser(cfg),
                  os.path.expanduser(cfgbak))
        result = True
    except:
        print("X... couldnt rename old:", cfg,"no bak file created")
        result = False
    return result


def bak_to_cfg(filenamebk="", filename = ""):
    '''used inside, rename back the bak version'''
    global CONFIG
    if filename != "":
        CONFIG['filename'] = filename

    if filenamebk=="":
        cfg = CONFIG['filename']
    else:
        cfg = filenamebk

    cfgbak = cfg + ".bak"
    #if CFG_DEBUG:
    print("D... testing if backup config exists:", cfgbak)
    if os.path.isfile( os.path.expanduser(cfgbak)):
        #if CFG_DEBUG:
        print("D... BACUP config exists:",cfgbak, "... renaming to:", cfg)
        os.rename(os.path.expanduser(cfgbak),
                  os.path.expanduser(cfg))
        #if CFG_DEBUG:print("D... config is recovered from:", cfgbak)
    else:
        #if CFG_DEBUG:
        print("D... bak config did not exist:", cfgbak,"no bak file recovery")


def save_config(filenamesv="", filename = ""): # duplicit... filename overrides
    '''FRONT function, save config to filename'''
    global CONFIG
    if filename != "":
        CONFIG['filename'] = filename

    if filenamesv=="":
        cfg = CONFIG['filename']
    else:
        cfg = filenamesv

    #print("D... calling cfg_to_bak:", cfg)
    if not cfg_to_bak(cfg):
        sys.exit(1)

    print("D... writing config:", cfg)

    ### rozxxx
    dir2create = os.path.dirname( cfg )
    #print("D...",dir2create)
    if not os.path.isdir( os.path.expanduser(dir2create )):
        print(f"D... trying to create directory {dir2create} if needed")
        result = False
        os.mkdir( os.path.expanduser(dir2create ))

    with open(os.path.expanduser(cfg), "w+") as f:
        f.write(json.dumps(CONFIG, indent=1))
        #if CFG_DEBUG:print("D... config was written:", cfg)

    if verify_config(filename):
        #if CFG_DEBUG:

        #print("D... verified by verify_config ... ok ... ending here")
        return True
    #====ELSE RECOVER BAK
    return bak_to_cfg()



def load_config(filename=""):
    '''FRONT function, load config file'''
    global CONFIG
    if filename != "":
        CONFIG['filename'] = filename
    cfg = CONFIG['filename']
    cfg = cfg+".from_memory"
    #if CFG_DEBUG:
    #print("D... calling save_config:")
    save_config( cfg )

    cfg = CONFIG['filename']
    #if CFG_DEBUG:print("D... loading config from",cfg)

    if not verify_config(filename):
        print("X... FAILED on verifications")
        return False

    #if CFG_DEBUG:
    #print("D... passed verification of:",cfg)
    dicti = CONFIG

    #if CFG_DEBUG:
    #print("D... directly loading json:",cfg)
    if os.path.isfile( os.path.expanduser(cfg)):
        with open(os.path.expanduser(cfg), "r") as f:
            dicti = json.load(f)

    # rewriting in memory
    if sorted(dicti.keys()) == sorted(CONFIG.keys()):
        #if CFG_DEBUG:
        #print("D... memory and disk identical:")
        pass
    else:
        #if CFG_DEBUG:
        print("X... memory and disk differ:")
        # show_config(CONFIG)
        # there may be more lines in the CODE after upgrade.
        for k in CONFIG.keys(): # search CODE version
            if not (k in dicti.keys()):
                print("D... key not on DISK:", k )
                dicti[k] = CONFIG[k]


    CONFIG = dicti
    ##if CFG_DEBUG:
    #print("D... final CONFIG:")
    ##show_config(filename)
    ##if CFG_DEBUG:
    #print("D... end load")


def loadsave(filename = ""):
    '''FRONT function, if DISK is earlier version than CODE, this may update DISK'''
    if filename != "":
        CONFIG['filename'] = filename

    load_config(filename)
    save_config() #?



#==========================================================



def func(debug = False):

    print("D... in unit config function func DEBUG may be filtered")
    print("i... in unit config function func - info")
    print("X... in unit config function func - ALERT")
    return True

def test_func():
    print("i... TESTING function func")
    assert func() == True

if __name__ == "__main__":
    print("i... in the __main__ of config of codeframe")
    Fire()
