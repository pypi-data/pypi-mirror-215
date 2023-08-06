#!/usr/bin/env python3
#
# FROM READ_VME_OFFLINE ----------------
#
from fire import Fire
# from read_vme_offline.version import __version__

import configparser
from math import exp

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

import sys
import os

from console import fg,bg
#print("!!!...  USE READ_VME_OFFLINE FROM 2022/07 ...... ")
#sys.exit(1)

CROW = 0


def is_float(n): # FROM FLASHCAM
    try:
        float_n = float(n)
    except ValueError:
        return False
    else:
        return True


def get_sections( configfile = 'dpp_pha.ini' ):
    """
    returns list of sections. Check if COMMON or channel present
    """
    config = configparser.ConfigParser( delimiters=(" ","\t") )
    config.read( configfile)
    return config.sections()


def get_setting( config, parameter, channel=0, retfloat = True):
    """
    search parameter like TRG_HOLDOFF in configparser - first in [CHAN] then in COMMON
    normally return float
    """
    ch = f"{channel}"
    res = None
    if  not ch in config:
        print(f"X... {fg.red}channel {channel} NOT in config {fg.default}")
        return None
    if parameter in config[ch]:
        res = config[ ch ][parameter]
        print(f"D... {parameter:20s} @ch {channel} ...",res)
    else:
        res = config[f'COMMON'][parameter]
        print(f"D... {parameter:20s} @comm ...",res)
    if retfloat:
        if is_float(res) :
            return float(res)
        else:
            print("X... {fg.red}NOT A FLOAT NUMBER{fg.default}", res)
            return None
    return None


def open_parser( inifile, channel ):
    config = configparser.ConfigParser( delimiters=(" ","\t") )
    config.read( inifile)

    print("D... SECTIONS:",config.sections() )
    if len(config.sections())==0:
        print("X... NO SECTIONS FOUND IN ",inifile)
        return None

    if channel is not None:
        if not str(channel) in config:
            print(f"X... channel {channel} {bg.red}     NOT PRESENT     {bg.default}")
            return None
        else:
            print(f"D... channel {channel} IS PRESENT")
    return config


def extract_holdoffs( inifile, channel):
    config = open_parser( inifile, channel)
    if config is None: return 0,0,0
    TRG_HOLDOFF      = get_setting( config, 'TRG_HOLDOFF'      ,channel  )
    TF_PEAK_HOLDOFF  = get_setting( config, 'TF_PEAK_HOLDOFF'  ,channel  )
    TF_SHAPING_TIME  = get_setting( config, 'TF_SHAPING_TIME'  ,channel  )
    TF_SEL_PEAKMEAN  = get_setting( config, 'TF_SEL_PEAKMEAN'  ,channel  )
    TF_PEAKING_DELAY = get_setting( config, 'TF_PEAKING_DELAY' ,channel  )
    TF_FLAT_TOP      = get_setting( config, 'TF_FLAT_TOP'      ,channel  )
    ECALa            = get_setting( config, 'CALIBRATION_A'    ,channel  )
    ECALb            = get_setting( config, 'CALIBRATION_B'    ,channel  )

    WID=0.01
    if TF_SEL_PEAKMEAN==0:WID=0.01
    elif TF_SEL_PEAKMEAN==1:WID=0.01*4
    elif TF_SEL_PEAKMEAN==2:WID=0.01*16
    elif TF_SEL_PEAKMEAN==3:WID=0.01*64
    else: WID=3

    # i dont knwow why 0.16 is here
    TWIN_US = round(0.16 + TF_SHAPING_TIME+TF_PEAKING_DELAY + WID,1)
    PKHOLD  = round(0.16+   TF_SHAPING_TIME+TF_FLAT_TOP +TF_PEAK_HOLDOFF )

    TAG = f"{bg.green}{fg.white}"
    if TWIN_US==0 or TRG_HOLDOFF==0 or PKHOLD==0:
        f"{bg.red}{fg.white}"
    print(f"{TAG}TRG_HOLDOFF     {TRG_HOLDOFF:5.1f} us{bg.default}{fg.default}" )
    # print(f"{TAG}TF_PEAK_HOLDOFF {TF_PEAK_HOLDOFF:5.1f}{bg.default}{fg.default}" )
    print(f"{TAG}PKHOLD          {PKHOLD:5.1f} us{bg.default}{fg.default}" )
    print(f"{TAG}TWIN_US         {TWIN_US:5.1f} us{bg.default}{fg.default}" )


    return TRG_HOLDOFF, PKHOLD, TWIN_US, ECALa, ECALb


def main( inifile = 'dpp_pha.ini', channel=None):
    """ Make jpg image from INI config file - timing
    """
    global ACROW
    # config = configparser.ConfigParser( delimiters=(" ","\t") )
    # config.read( inifile)

    # print("D... SECTIONS:",config.sections() )
    # if len(config.sections())==0:
    #     print("X... NO SECTIONS FOUND IN ",inifile)
    #     return

    # if channel is not None:
    #     if not str(channel) in config:
    #         print(f"X... channel {channel} {fg.red} NOT PRESENT")
    #         return
    #     else:
    #         print(f"D... channel {channel} IS PRESENT")
    extract_holdoffs(inifile, channel)

    config = open_parser( inifile, channel)
    if config is None: return
    #=============everything will be in microseconds
    STEP=0.01

    #CALA = get_setting( config, "CALIBRATION_A", channel )
    #RECORD_LENGTH=int(config['COMMON']['RECORD_LENGTH'])*STEP
    RECORD_LENGTH    = get_setting( config, "RECORD_LENGTH", channel )*STEP
    PRE_TRIGGER      = get_setting( config, 'PRE_TRIGGER', channel )*STEP
    RISE_TIME        = get_setting( config, 'RISE_TIME' ,channel  )
    TF_DECAY_TAU     = get_setting( config, 'TF_DECAY_TAU' ,channel  )
    TF_SHAPING_TIME  = get_setting( config, 'TF_SHAPING_TIME' ,channel  )
    TF_FLAT_TOP      = get_setting( config, 'TF_FLAT_TOP' ,channel  )
    TF_PEAKING_DELAY = get_setting( config, 'TF_PEAKING_DELAY' ,channel  )
    TF_SEL_PEAKMEAN  = get_setting( config, 'TF_SEL_PEAKMEAN' ,channel  )
    TRG_HOLDOFF      = get_setting( config, 'TRG_HOLDOFF' ,channel  )
    TF_PEAK_HOLDOFF  = get_setting( config, 'TF_PEAK_HOLDOFF' ,channel  )
    RT_DISCR_WINDOW  = get_setting( config, 'RT_DISCR_WINDOW' ,channel  )
    ENABLE_RT_DISCR  = get_setting( config, 'ENABLE_RT_DISCR', channel , retfloat = False)




    if ENABLE_RT_DISCR=="NO":
        ENABLE_RT_DISCR = False
    else:
        ENABLE_RT_DISCR = True

    # it seems that it includes the pretrigger..........
    RECORD_LENGTH = RECORD_LENGTH - PRE_TRIGGER #


    plt.figure( figsize=(10,14))


    loc = plticker.MultipleLocator( base= 0.5 )


    ROWS=11
    ACROW = 0
    def incac():  # jump to next panel
        global ACROW
        ACROW+=1
        return ACROW

    INP=plt.subplot( ROWS, 1,incac())
    plt.setp(INP.get_xticklabels(), visible=False )
    INP.xaxis.set_major_locator(loc)
    INP.grid()
    INP.text(1.0,0.5,'INPUT',
            horizontalalignment='right',
            transform=INP.transAxes)

    DEL=plt.subplot(ROWS,1,incac(),sharex = INP)
    plt.setp(DEL.get_xticklabels(), visible=False)
    DEL.xaxis.set_major_locator(loc)
    DEL.grid()
    DEL.text(1.0,.5,'DELTA',
            horizontalalignment='right',
            transform=DEL.transAxes)

    DEL2=plt.subplot(ROWS,1,incac(),sharex = INP)
    plt.setp(DEL2.get_xticklabels(), visible=False)
    DEL2.xaxis.set_major_locator(loc)
    DEL2.grid()
    DEL2.text(1.0,.5,'DELTA2',
            horizontalalignment='right',
            transform=DEL2.transAxes)

    ARM=plt.subplot(ROWS,1,incac(),sharex = INP)
    plt.setp(ARM.get_xticklabels(), visible=False)
    ARM.xaxis.set_major_locator(loc)
    ARM.grid()
    ARM.text(1.0,.5,'ARMED',
            horizontalalignment='right',
            transform=ARM.transAxes)

    TRG=plt.subplot(ROWS,1,incac(),sharex = INP)
    plt.setp(TRG.get_xticklabels(), visible=False)
    TRG.grid()
    TRG.text(1.0,.5,'TRG_REQ',
            horizontalalignment='right',
            transform=TRG.transAxes)

    RTD=plt.subplot(ROWS,1,incac(),sharex = INP)
    plt.setp(RTD.get_xticklabels(), visible=False)
    RTD.grid()
    RTD.text(1.0,.5,'RTDwin: acceptance win for TRG_REQ, discr.pileups',
            horizontalalignment='right',
            transform=RTD.transAxes)

    TRGHO=plt.subplot(ROWS,1,incac(),sharex = INP)
    plt.setp(TRGHO.get_xticklabels(), visible=False)
    TRGHO.grid()
    TRGHO.text(1.0,.5,'TRG_HOLDOFF: prevent TRG gen on overshoot',
            horizontalalignment='right',
            transform=TRGHO.transAxes)

    TRAP=plt.subplot(ROWS,1,incac(),sharex = INP)
    plt.setp(TRAP.get_xticklabels(), visible=False)
    TRAP.grid()
    TRAP.text(1.0,.5,'TRAPEZOID',
            horizontalalignment='right',
            transform=TRAP.transAxes)


    PEAK=plt.subplot(ROWS,1,incac(),sharex = INP)
    plt.setp(PEAK.get_xticklabels(), visible=False)
    PEAK.grid()
    PEAK.text(1.0,.5,'PEAKING',
            horizontalalignment='right',
            transform=PEAK.transAxes)



    PEAKHO=plt.subplot(ROWS,1,incac(),sharex = INP)
    plt.setp(PEAKHO.get_xticklabels(), visible=False)
    PEAKHO.grid()
    PEAKHO.text(1.0, 0.5 ,'PEAK_HOLDOFF',
            horizontalalignment='right',
            transform=PEAKHO.transAxes)



    PKRUN=plt.subplot(ROWS,1,incac(),sharex = INP)
    plt.setp(PKRUN.get_xticklabels(), visible=True)
    PKRUN.grid()
    PKRUN.text(1.0,.5,'PEAKRUN',
            horizontalalignment='right',
            transform=PKRUN.transAxes)


    # TXTF=plt.subplot(10,1,1,sharex = INP)
    # plt.setp(TXTF.get_xticklabels(), visible=True)
    # #TXTF.grid()


    # TXTF.text(1.0, 0.5 ,'info',
    #         horizontalalignment='right',
    #         transform=TXTF.transAxes)
    # TXTF.text(0.0, 0. ,'TRG_HOLDOFF ... we tried 0.4, but 0.8 made a great improvement with 6MeV - no pileups',
    #         horizontalalignment='left',
    #         transform=TXTF.transAxes)
    # TXTF.text(0.0, 0.25 ,'TRG_HOLDOFF ... we tried 0.4, but 0.8 made a great improvement with 6MeV - no pileups',
    #         horizontalalignment='left',
    #         transform=TXTF.transAxes)
    # TXTF.text(0.0, 0.5 ,'TRG_HOLDOFF ... we tried 0.4, but 0.8 made a great improvement with 6MeV - no pileups',
    #         horizontalalignment='left',
    #         transform=TXTF.transAxes)
    # TXTF.text(0.0, 0.75 ,'TRG_HOLDOFF ... we tried 0.4, but 0.8 made a great improvement with 6MeV - no pileups',
    #         horizontalalignment='left',
    #         transform=TXTF.transAxes)




    #========================================================== PLOTS=========
    # make a little extra space between the subplots
    #fig.subplots_adjust(hspace=0.5)

    #INP.set_xlim(0, RECORD_LENGTH)
    INP.set_xlim(-PRE_TRIGGER, RECORD_LENGTH)

    #ax2.set_xlim(0, RECORD_LENGTH)
    #ax1.get_shared_x_axes().join(ax1, ax2)
    #ax1 = plt.subplot(gs[1], sharex = ax0)
    #ax2.grid()



    #==============================  INPUT CALC
    t=RECORD_LENGTH-PRE_TRIGGER
    t=RECORD_LENGTH
    INP_AT_RC=exp(-t/TF_DECAY_TAU)
    #INP.plot([0,PRE_TRIGGER,PRE_TRIGGER+ RISE_TIME, RECORD_LENGTH],[0,0, 1 , INP_AT_RC],'b.-')
    INP.plot([-PRE_TRIGGER, -RISE_TIME,0 , RECORD_LENGTH],[0,0, 1 , INP_AT_RC],'b.-')
    #plt.subplots_adjust(hspace=.0)

    #==============================   DELTA
    #t=[0,PRE_TRIGGER, PRE_TRIGGER+ RISE_TIME,PRE_TRIGGER+ RISE_TIME*2, RECORD_LENGTH]
    t=[-PRE_TRIGGER, -RISE_TIME, 0 ,0+ RISE_TIME, RECORD_LENGTH]
    s=[0, 0,           1 ,                     0,                      0]
    DEL.plot(t,s,'g.-')
    #plt.subplots_adjust(hspace=.0)
    T_TRIGGER=RISE_TIME


    #==============================  DELTA2
    t=[0,PRE_TRIGGER, PRE_TRIGGER+ T_TRIGGER/2,
       PRE_TRIGGER+ T_TRIGGER,
       PRE_TRIGGER+ T_TRIGGER*1.5,
       PRE_TRIGGER+ T_TRIGGER*2,
       RECORD_LENGTH]

    t=[-PRE_TRIGGER,
       -RISE_TIME, -3*RISE_TIME/4, -RISE_TIME/2,
       0,  RISE_TIME/2,
       RISE_TIME, RECORD_LENGTH]
    s=[0,
       0,  0.5, 1 ,
       0, -1,
       0,0]
    DEL2.plot(t,s,'g.-')
    plt.subplots_adjust(hspace=.0)


    #==============================  ARMED
    THRESHOLD = -3*RISE_TIME/4
    t=[-PRE_TRIGGER,
       -RISE_TIME, THRESHOLD, THRESHOLD,  # threshold here
       0,  TRG_HOLDOFF, TRG_HOLDOFF,
        RECORD_LENGTH]
    s=[0,
       0,  0,1,
       1, 1, 0,
       0]
    ARM.plot(t,s,'m.-')
    plt.subplots_adjust(hspace=.0)


    #========================================--TRG-REQ
    t=[0, PRE_TRIGGER+T_TRIGGER,PRE_TRIGGER+T_TRIGGER,PRE_TRIGGER+T_TRIGGER,RECORD_LENGTH]
    t=[0, 0+T_TRIGGER,0+T_TRIGGER,0+T_TRIGGER,RECORD_LENGTH]
    t=[-PRE_TRIGGER, 0,0,0,RECORD_LENGTH]
    s=[0,0,1,0,0]
    TRG.plot(t,s,'r-*' )


    #========================================--RTDwin
    t=[-PRE_TRIGGER,
       THRESHOLD, THRESHOLD,  # at -rise3/4 ~
       THRESHOLD+RT_DISCR_WINDOW,THRESHOLD+RT_DISCR_WINDOW,
       RECORD_LENGTH]
    s=[0,
       0,1,
       1,0,
       0]
    if ENABLE_RT_DISCR:
        RTD.plot(t,s,'r-*' )
    else:
        RTD.plot(t,s,':.', color='gray' )



    #========================================--TRGHO
    t=[0,
          PRE_TRIGGER+T_TRIGGER, PRE_TRIGGER+T_TRIGGER,
          PRE_TRIGGER+T_TRIGGER+TRG_HOLDOFF,PRE_TRIGGER+T_TRIGGER+TRG_HOLDOFF,
          RECORD_LENGTH]
    t=[-PRE_TRIGGER,
          0, 0,
          TRG_HOLDOFF,TRG_HOLDOFF,
          RECORD_LENGTH]
    s=[0,
       0, 1,
       1, 0,
      0]
    TRGHO.plot(t,s,'m*-' )

    #========================================--TRAP  16 clock cycles delay after trgreq
    t=[0, PRE_TRIGGER+T_TRIGGER+0.16,
          PRE_TRIGGER+T_TRIGGER+0.16 + TF_SHAPING_TIME,
          PRE_TRIGGER+T_TRIGGER+0.16 + TF_SHAPING_TIME+TF_FLAT_TOP,
          RECORD_LENGTH]
    t=[-PRE_TRIGGER, 0.16,
          0.16 + TF_SHAPING_TIME,
          0.16 + TF_SHAPING_TIME+TF_FLAT_TOP,
          0.16 + 2*TF_SHAPING_TIME+TF_FLAT_TOP,
          RECORD_LENGTH]
    s=[0,0,
       1,
       1,
       0,
      0]
    TRAP.plot(t,s,'g.-' )


    #========================================--PEAK
    WID=0.01
    if TF_SEL_PEAKMEAN==0:WID=0.01
    elif TF_SEL_PEAKMEAN==1:WID=0.01*4
    elif TF_SEL_PEAKMEAN==2:WID=0.01*16
    elif TF_SEL_PEAKMEAN==3:WID=0.01*64
    else: WID=3
    t=[-PRE_TRIGGER,
          PRE_TRIGGER+T_TRIGGER+0.16 + TF_SHAPING_TIME+TF_PEAKING_DELAY,
          PRE_TRIGGER+T_TRIGGER+0.16 + TF_SHAPING_TIME+TF_PEAKING_DELAY,
          PRE_TRIGGER+T_TRIGGER+0.16 + TF_SHAPING_TIME+TF_PEAKING_DELAY+WID,
          PRE_TRIGGER+T_TRIGGER+0.16 + TF_SHAPING_TIME+TF_PEAKING_DELAY+WID,
          RECORD_LENGTH]
    t=[-PRE_TRIGGER,
          0.16 + TF_SHAPING_TIME+TF_PEAKING_DELAY,
          0.16 + TF_SHAPING_TIME+TF_PEAKING_DELAY,
          0.16 + TF_SHAPING_TIME+TF_PEAKING_DELAY + WID,
          0.16 + TF_SHAPING_TIME+TF_PEAKING_DELAY + WID,
          RECORD_LENGTH]
    s=[0,
       0, 1,
       1, 0,
      0]
    PEAK.plot(t,s,'r-*' )




    #========================================--PEAKHOLDOFF
    t=[-PRE_TRIGGER,
          0.16+   TF_SHAPING_TIME+TF_FLAT_TOP ,
          0.16+   TF_SHAPING_TIME+TF_FLAT_TOP ,
          0.16+   TF_SHAPING_TIME+TF_FLAT_TOP +TF_PEAK_HOLDOFF ,
          0.16+   TF_SHAPING_TIME+TF_FLAT_TOP +TF_PEAK_HOLDOFF ,
          RECORD_LENGTH]
    s=[0,
       0, 1,
       1, 0,
      0]
    PEAKHO.plot(t,s,'g*-' )


    #========================================--PEAKRUN
    t=[-PRE_TRIGGER,
          0, 0,
          0.16+   TF_SHAPING_TIME+TF_FLAT_TOP ,
          0.16+   TF_SHAPING_TIME+TF_FLAT_TOP +TF_PEAK_HOLDOFF ,
          0.16+   TF_SHAPING_TIME+TF_FLAT_TOP  +TF_PEAK_HOLDOFF,
          RECORD_LENGTH]
    s=[0,
       0, 1,
       1,
       1,
       0,
      0]
    PKRUN.plot(t,s,'m*-' )

    plt.xlabel('t [us]', fontsize=18)
    OUTFILE =  "dpp_pha.ini.jpg"
    OUTFILE = os.path.splitext( inifile )[0] + ".png"
    plt.savefig(OUTFILE, bbox_inches='tight')
    plt.show()





if __name__=="__main__":
    Fire(main)
