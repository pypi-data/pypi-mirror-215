#!/usr/bin/env python3

from fire import Fire
#from read_vme_offline.version import __version__

#print("i... module read_vme_offline/ascdf is being run")

import pandas as pd
#import modin.pandas as pd
import tables # here, to avoid a crash when writing pandas
# import h5py not needed
import datetime
import subprocess as sp
import numpy as np

import os
import datetime as dt

import matplotlib.pyplot as plt

import ROOT

import sys
# import root_numpy# 2019 is old with newer numpy

# import psutil

import datetime as dt

from console import fg,bg,fx

import gregory_online.erlang as erlang
import gregory_online.dpp2jpg as dpp2jpg

import tempfile
import urllib.request


#
#  Works when apply is used: df.parallel_apply(func)
#
#
#from pandarallel import pandarallel
# Initialization
#pandarallel.initialize()








#------------------------------------------------------------------------

def get_number_of_lines(filename):
    """
    wc cli commad to count the lines of ASC
    """
    ps = sp.Popen( ['cat', filename], stdout=sp.PIPE)
    output = sp.check_output(('wc', '-l'), stdin=ps.stdout)
    ps.wait()
    nlines=int(output.decode("utf8").split()[0])
    return nlines

#------------------------------------------------------------------------

def get_number_of_columns(filename):
    """
    omit first 4 lines, take one line and tell
    """
    CMDL = ['head','-n','4', filename]
    ps = sp.Popen( CMDL , stdout=sp.PIPE)
    # print(" ".join(CMDL))
    output = sp.check_output(('tail','-n','1'), stdin=ps.stdout)
    ps.wait()
    ncolumns=len(output.decode("utf8").strip().split())
    if ncolumns==5:
      print(f"D... {ncolumns} cols ... 2020+ version with pile-up info (1/0)")
    elif ncolumns==4:
        print(f"D... {ncolumns} cols  ... 2018 version without extras column, pileup (3/0)")
    else:
        print(f"X... BAD NUMBER OF COLUMNS {ncolumns}")
        sys.exit()
    return ncolumns




# ----------------------------------------------ASC AND INI COPY TO TMP
def get_ini_copy(url):

    print(f"D... fetching {url}")
    filename = tempfile.NamedTemporaryFile(suffix='.ini', delete=False)
    txt = ""
    try:
        with urllib.request.urlopen( url ) as uf:
            txt = uf.read().decode('utf-8')
    except urllib.error.URLError as e:
        print("X... URL ERROR: ",e.reason)

    if len(txt)>10:
        with open( filename.name, 'w', encoding='utf8', newline='') as f:
            f.write( txt )

    return filename.name

# ==================================================== ASC AND INI =================


def load_ini_file(filename, channel = None ): # already complete filename

    inifilename = os.path.splitext(filename)[0]+".ini"
    if inifilename.find("http://")==0:
        inifilename = get_ini_copy( inifilename )


    if os.path.exists(inifilename):
        #print(f"D... {fg.green} OK - ini file exists {fg.default}")
        if channel is not None:
            print(f"D... {fg.green} OK channel {fg.default}")
            TRG_HOLDOFF,TF_PEAK_HOLDOFF, TWIN_US, ECALa, ECALb = dpp2jpg.extract_holdoffs( inifilename, channel )
            print(  TRG_HOLDOFF,TF_PEAK_HOLDOFF, TWIN_US)
            return TRG_HOLDOFF,TF_PEAK_HOLDOFF, TWIN_US, ECALa, ECALb

        return 0,0,0, 1,0 # last is calibration

    return None,None,None, 1,0 # last is calibatoin


# ==================================================== ASC AND INI =================



# ------------------- statistics for ascdf  NOT ascdf_chan

def stat_asc(df):
    print("+"*50,"BASICS TOTAL BEGIN")
    chan_available = df['ch'].unique()
    print("D... channels available:", chan_available)
    for i in chan_available:
        evts = len( df.loc[ (df['ch']==i) ])
        print(f"    {i}: {evts } events")
    print(f"D... pu        present: {df['pu'].unique()} ... 1 or 0 (3v0 before 2020)" )
    if 'extras' in df:
        print(f"D... extras    present: {df['extras'].unique()}... 1..satur,3..roll,4..reset,8..fake" )
        print(f"D... total saturations: ",len( df.loc[ (df['extras']&1)==1]  ) )
    #print( "D... Emin            :",df['E'].min() )
    #print( "D... Emax            :",df['E'].max() )
    print( "D... lasttime        :",df['time'].max() )
    print("+"*50,"BASICS TOTAL END")

    print(f" {bg.white}{fg.black} INPUT channel now{fg.default}{bg.default}")



    # print(f"D... calib           :  {CALA},  {CALB}  for chan {chan}" )

    # inifile = os.path.splitext( filename)[0]+".ini"
    # if inifile.find("http://")==0:
    #     inifile = get_ini_copy( inifile )
    # print(inifile)
    # CALA = 1
    # CALB = 0
    # if os.path.exists( inifile  ):
    #     config = configparser.ConfigParser( delimiters=(" ","\t") )
    #     config.read( inifile )
    #     CALA =config[f"{chan}"]['CALIBRATION_A']
    #     CALB =config[f"{chan}"]['CALIBRATION_B']
    #     CALA = float(CALA.split("#")[0].strip()) # avoid comments at the end of line
    #     CALB = float(CALB.split("#")[0].strip())
    #     print(f"D... INI file exists {inifile}, calibration =  {CALA} {CALB}")

    # return df






#------------------------------------------------------------------------

def filename_decomp(filename):
    """
    The ONLY procedure to get the start time from filename
    """
    # should work both with 2021mmdd and  21mmddd
    # returns the start time
    #

    basename = os.path.basename(filename)
    basename = os.path.splitext(basename)[0]
    # start-date
    startd = basename.split("_")[1]
    # start-time
    startt = basename.split("_")[2]

    # 4 digits always
    if len(startd)==6:
        print("D...  compensating 2 digit year to 4 digit year")
        startd="20"+startd

    print("D...  time start MARK=",startd+startt)


    #ok = False
    #try:
    start = dt.datetime.strptime(startd+startt,"%Y%m%d%H%M%S" )
    #ok = True
    print("D... succesfull start with 4 digit year")

    #except:
    #    print("x... year may not by 4 digits")
    #if not(ok):
    #    print("X... trying 2 digits for year")
    #    start = dt.datetime.strptime(startd+startt,"%y%m%d%H%M%S" )

    return start




#------------------------------------------------------------------------

def pd_read_table(filename, sort = True,  fourcolumns = False):
    """
    READ THE ASC TABLE:   two possibilities:  4 columns OR 5 columns
EARLIER:
         Events[ch][ev].TimeTag, ENERGY,(Events[ch][ev].Energy)>>MAXNBITS, ch
         MAXNBITS 15
Feb 2020+:
       Events[ch][ev].TimeTag, ENERGY,  (Events[ch][ev].Energy)>>MAXNBITS, ch, Events[ch][ev].Extras
       MAXNBITS 15
    >>t,e,PU (1/0) (or 3/0 old)  ,  channel,   Extras(2020+ only)


https://www.npl.washington.edu/TRIMS/sites/sand.npl.washington.edu.TRIMS/files/manuals-documentation/CAENDigitizer_SW_User_Manual_rel.5.pdf

EXTRAS: bit[0] = DEAD_TIME. This is set to 1 when a dead time occurred before this event. The dead time can be due to
either a signal saturation or a full memory status. Check Fig. B.4 and Fig. B.5 for more details
bit[1] = ROLL_OVER. Identify a trigger time stamp roll-over that occurred before this event
bit[2] = TT_RESET. Identify a trigger time stamp reset forced from external signals in S-IN (GPI for Desktop)
bit[3] = FAKE_EVENT. This is a fake event (which does not correspond to any physical event) that identifies a
time stamp roll-over. The roll-over can be due to an external or internal reset. The user can set bit[25]
= 1 of register 0x1n80 to enable the fake-event saving in case of reset from S-IN, and bit[26] = 1 of
register 0x1n80 to enable the fake-event saving in case of internal roll-over. In the first case the event
will have both bit[3] and bit[2] set to 1, while in the second case the event will have both bit[3] and
bit[1] set to 1.
    """
    #print(f"D... fourcolumns=={fourcolumns}")
    #print(f"D... fourcolumns=={fourcolumns}")
    #print(f"D... fourcolumns=={fourcolumns}")
    start = dt.datetime.now()
    df = pd.read_table( filename,
                        names=['time','E','pu','ch','extras'],
                        sep = r"\s+",
                        comment="#")

    meastime = (dt.datetime.now() - start).total_seconds()
    #print(f"D... table is in memory ...  {get_number_of_lines(filename)/meastime/1000/1000:.3f} Mrows/sec")
    print(f"D... table is in memory ...{len(df)/meastime/1000/1000:.1f} Mrows/sec")

    #print(f"D... fourcolumns=={fourcolumns}")

    #print( freemem() )
    # drop if 4 column
    df = df.dropna(axis='columns', how='all')


    df['time'] = df['time']/1e+8 # this is correct for 10ns step ADC
    # print("D... table last timestamp ",df.iloc[-1]["time"], "sec.")

    #print(df.dtypes)
    df['time'] = df['time'].astype('float64')
    df['E']    = df['E'].astype('int32')
    df['pu']    = df['pu'].astype('int32')
    df['ch']   = df['ch'].astype('int32')
    if 'extras' in df:
        df['extras'] = df['extras'].astype('int32')
    #print("D...    finale types ************************************")
    #print(df.dtypes)

    if fourcolumns:
       print("D... extra operation for four columns ...  FOURCOLUMNS TABLE !!!")
       print(df)
       df['E'] = df['E']+ (df['pu']&1) * 16384
       df['pu'] = df['pu'].apply(lambda x: x >> 1)
       print(df)
    # print(freemem())

    #    df.to_hdf('run'+str(number)+'.h5',
    #              "matrix",
    #              format='t',
    #              data_columns=True,
    #              mode='w')

    # print(freemem() )
    if sort:
        print("D... sorting (after read_table):")
        #print(df)
        df = df.sort_values(by="time")
        #print(df)
        df.reset_index(inplace=True, drop=True)
        #print(df)
        #print( freemem() )

    #print("D... table last timestamp ",df.iloc[-1]["time"], "sec.")
    #endblock()
    return df





#------------------------------------------------------------------------
def select_channels(df, chan, delete_original = False):
    """
    select channels bu not as view! COPY and DELETE
    """
    print("D... selecting channels:", chan, end="...  ", flush = True)

    channels = None
    if type(chan) is list:
        channels = chan
    else:
        channels = [chan]

    #print( freemem() )
    # CHANNEL (i hope it is sorted)
    if delete_original:
        df1 = df.loc[ df["ch"].isin( channels ) ].copy()
        del df
    else:
        df1 = df.loc[ df["ch"].isin( channels ) ]
    df1.reset_index(inplace=True, drop=True)
    #del df
    if len(df1) ==0 :
        print("X... no data for channels",channels)
        return None
        #sys.exit(1)
    return df1




def enhance_dt( df ):

    df1 = df

    print("i... enhancing DataFrame by dtus and dtus_prev ", end="...", flush=True)

    df1, dtusmin, dtusmax = enhance_by_dtus_and_next_E(df1)

    print(" ")

    tmin = df1['time'].min()
    tmax = df1['time'].max()
    interval = tmax - tmin
    chan_available = df1['ch'].unique()
    chan = chan_available[0]

    print("_"*50,"BASICS BEGIN CHANNEL ",chan)
    print("D... channels available:", chan_available)

    print(f"D... pu        present: {df1['pu'].unique()}... 1 or 0 (3v0 before 2020)" )
    #print(f"D... pu        present: {df1['pu'].unique()}... 1 or 0 (3v0 before 2020)" )
    pileups_ch = len(df1.loc[ df1['pu']==1])  # (3)for 4 columns, it is fixed in table_read
    print(f"D... pu       (pu==1) : {pileups_ch} ")
    if 'extras' in df:
        print(f"D... extras    present: {df1['extras'].unique()}... 1..satur,3..roll,4..reset,8..fake" )
        satu_n_ch = len(df1.loc[ (df1['extras']&1)!=0] )
        Tsatu_ch = df1.loc[ (df1['extras']&1)!=0]["prev_satu"].sum()/1e+6   # in sec...
        #print(f"D... SATURATIONS {satu_n_ch} total: {Tsatu_ch} sec. at maximum")
        #print(f"D... SATURATIONS {satu_n_ch} total: {100*Tsatu_ch/interval:.2f} % at maximum")
        print(f"D... number of saturations: ",len( df1.loc[ (df1['extras']&1)==1] ) , f" {Tsatu_ch:.2f} sec. at max;  {100*Tsatu_ch/interval:.2f} % at max"   )

    print(f"D... Emin Emax       : {df1['E'].min()} ...  {df1['E'].max()}    /2^15={2**15}/")
    print(f"D... Tmin Tmax       : {tmin:.2f} ... {tmax:.2f} ; total time {interval:.2f} sec")
    print("_"*50,"BASICS END     CHANNEL ",chan)


    #print(df1)
    ###print("  range of neighbours in [us]:",dtusmin, dtusmax)

    if 'extras' in  df1:
        satu_n_ch = len(df1.loc[ (df1['extras']&1)!=0] )
        Tsatu_ch = df1.loc[ (df1['extras']&1)!=0]["prev_satu"].sum()/1e+6   # in sec...
        # print(f"D... SATURATIONS {satu_n_ch} total: {Tsatu_ch} sec. at maximum")
        #print(f"D... SATURATIONS {satu_n_ch} total: {100*Tsatu_ch/interval:.2f} % at maximum")
    else:
        satu_n_ch = None
        Tsatu_ch = None

    #len_zeroes,len_dzeroes,len_szeroes,len_izeroes,len_stazeroes,zoutput = ascgeneric.pd_detect_zeroes(df1, chan, TIMEWIN_US=4.48) # df1[ (df1.E==0) ]
    #print(zoutput)

    return df1















#------------------------------------------------------------------------

def enhance_by_dtus_and_next_E(df):
    #print("D... adding dtus and next_E columns")
    #print( freemem() )


    #print(f"D... broadening table with dt :next event  in t+dtus")
    df['dtus'] = (df.time.shift(-1)-df.time)*1000*1000
    df['dtus'] = df['dtus'].astype('float32') #
    dtusmin = df['dtus'].min()
    dtusmax = df['dtus'].max()
    df.fillna(99999, inplace =True)
    #print(f"D... range of time-differences (erlang) values min/max : {dtusmin:.3f} us ...  {dtusmax:.3f}  usec." )


    #print(f"D... broadening table with dt :prev event  = t - dtus (to enable search for standalones)")
    df['dtuspr'] = (df.time - df.time.shift(+1))*1000*1000
    df['dtuspr'] = df['dtuspr'].astype('float32') #
    dtusminpr = df['dtuspr'].min()
    dtusmaxpr = df['dtuspr'].max()
    df.fillna(99999, inplace =True)
    #print(f"D... range of time differences (erlang) values : {dtusminpr:.3f} us ...  {dtusmaxpr:.3f}  usec. PREVIOUS" )

    # df['dtus3'] = (df.time.shift(-2)-df.time)*1000*1000 # for triple
    # #df.fillna(9999, inplace =True)
    # df['dtus3'] = df['dtus3'].astype('float32') #
    # dtusmin3 = df['dtus3'].min()
    # dtusmax3 = df['dtus3'].max()
    # df.fillna(99999, inplace =True)
    # print(f"D... range of time differences (erlang) values : {dtusmin3:.3f} us ...  {dtusmax3:.3f}  usec. TRIPLE" )

    # df['dtus4'] = (df.time.shift(-3)-df.time)*1000*1000 # for triple
    # #df.fillna(9999, inplace =True)
    # df['dtus4'] = df['dtus4'].astype('float32') #
    # dtusmin4 = df['dtus4'].min()
    # dtusmax4 = df['dtus4'].max()
    # df.fillna(99999, inplace =True)
    # print(f"D... range of time differences (erlang) values : {dtusmin4:.3f} us ...  {dtusmax4:.3f}  usec. QUADRUPLE" )

    # df['dtus5'] = (df.time.shift(-4)-df.time)*1000*1000 # for triple
    # #df.fillna(9999, inplace =True)
    # df['dtus5'] = df['dtus5'].astype('float32') #
    # dtusmin5 = df['dtus5'].min()
    # dtusmax5 = df['dtus5'].max()
    # df.fillna(99999, inplace =True)
    # print(f"D... range of time differences (erlang) values : {dtusmin5:.3f} us ...  {dtusmax5:.3f}  usec. PENTUPLE" )




    #print(f"D... broadening table - next_E")
    df['next_E'] = (df.E.shift(-1))
    df.fillna(0, inplace=True)
    df['next_E'] = df['next_E'].astype('int32') #

    # print(f"D... broadening table - next_E3")  # for triple
    # df['next_E3'] = (df.E.shift(-2))
    # df.fillna(0, inplace=True)
    # df['next_E3'] = df['next_E3'].astype('int32') #

    # print(f"D... broadening table - next_E4")  # for triple
    # df['next_E4'] = (df.E.shift(-3))
    # df.fillna(0, inplace=True)
    # df['next_E4'] = df['next_E4'].astype('int32') #

    # print(f"D... broadening table - next_E5")  # for triple
    # df['next_E5'] = (df.E.shift(-4))
    # df.fillna(0, inplace=True)
    # df['next_E5'] = df['next_E5'].astype('int32') #




    #print(f"D... broadening table - next_ch")
    df['next_ch'] = (df.ch.shift(-1))
    df.fillna(0, inplace=True)
    df['next_ch'] = df['next_ch'].astype('int32') #

    if 'extras' in df.columns:
        #print(f"D... broadening table - prev_dtus SATU  previous time")
        df['prev_satu'] = (df.time - df.time.shift(+1))*1000*1000
        #  this says - if no saturation flag=> set 0
        df['prev_satu'] = np.where((df['extras']&1)==1, df['prev_satu'] , 0)
        #  same as
        # df.loc[  (df.extras&1)!=1, 'prev_satu' ] =  0
        #
        #
        df.fillna(0, inplace = True)
        df['prev_satu'] = df['prev_satu'].astype('float32') #

    #----------nice debug print ---------------------
    #print(df)
    #endblock()
    return df, dtusmin, dtusmax







#----------------------------------------------------------------------
def asc_stat_print( df, TIMEWIN_US = 4.2 , filename = "", TRGHOLD = 0):
#pd_detect_zeroes(df, channel,  TIMEWIN_US = 4.2 ):
    """
   2-dtus
    get number of zeroes, single zeroes, double zeroes, standalone zeroes
    -
      2nd phase - SZ and DZ - make one event from these PILEUPs
      3rd phase - create

    #len_zeroes,len_dzeroes,len_szeroes,len_izeroes,len_stazeroes,zoutput = ascgeneric.pd_detect_zeroes(df1, chan, TIMEWIN_US=4.48) # df1[ (df1.E==0) ]
    #print(zoutput)

    """
    print( f"D... detection of zeroes: WINDOW == {bg.red}{fg.white} {TIMEWIN_US:.1f} us {bg.default}{fg.default}")



    # vycisteny kanal, ----------------------------------- DFZ
    # I PREPARE SEVERAL VIEWS : only this channel :
    dfz = df[:-1] # WHY????????????
    chan_available = df['ch'].unique()
    if len(chan_available)>1:
        print(f"X... {fg.red} select ONE channel only - this is statistics over all channels{fg.default}")
        stat_asc(dfz)
        return None
    channel = chan_available[0]
    #index_names = dfz[  (dfz.ch!=channel)].index
    #dfz = dfz.drop(  index_names )
    zeroes = len(  dfz.loc[ (dfz.E==0) ] )
    #print( f" ... TOTAL ZEROES  = {zeroes}")

    # same as dfz for the moment -------------------------- DFALONE IS ALONE !!!!!!!!!!
    dfalone = df # drop the close (cluster) events to count standalones
    index_names = dfalone[ (dfalone.ch!=channel)].index
    dfalone = dfalone.drop( index_names )
    # STANDALONE EVENTS  - drop all events close to another event
    index_names = dfalone[ (dfalone.dtus<=TIMEWIN_US) | (dfalone.dtuspr<=TIMEWIN_US)  ].index
    dfalone = dfalone.drop( index_names) # NOT inplace, else it changes the df!!! # LAST REDEFINITION ALONE

    #print(f"i... purely isolated events {len(dfalone)}" )
    isoevents = len( dfalone )
    isozeroes = len( dfalone.loc[ (dfalone.E==0)  ])
    isononzeroes = len( dfalone.loc[ (dfalone.E!=0)  ])
    # print(f" ... purely isolated zeroes {stazeroes}")


    # playing on clusters---------------------------- DFZ IS CLUSTERS !!!!!!!!!!!
    # ----------- COMPLEMENT TO STANDALONES ... drop all isolated, keep clusters
    dfcluster = dfz[~dfz.isin(dfalone) ].dropna()
    # COMBINED ZEROES ... PAIRS treatment --- INSIDE dfcluster --- i look forward and check that nextE is not out of cluster
    # ilogic zeroes
    izeroes = len( dfcluster.loc[ ((dfcluster.E==0) & (dfcluster.next_E!=0))  & (dfz.dtus<=TIMEWIN_US)  ] )
    #print( f" ... ilogiczeroes = {izeroes}" )
    szeroes = len(dfcluster.loc[ ((dfcluster.E!=0) & (dfcluster.next_E==0)) & (dfz.dtus<=TIMEWIN_US)  ] )
    #print( f" ... singlezeroes = {szeroes} " )
    dzeroes = len(dfcluster.loc[ ((dfcluster.E==0) & (dfcluster.next_E==0))  & (dfz.dtus<=TIMEWIN_US) ] )
    #print( f" ... doblezeroes = {dzeroes} " )
    dnonzeroes = len(dfcluster.loc[ ((dfcluster.E!=0) & (dfcluster.next_E!=0))  & (dfz.dtus<=TIMEWIN_US) ] )

    nclusters =  len(dfcluster.loc[  (dfz.dtus>TIMEWIN_US) ] )


    #dfz.reset_index(inplace=True)
    # print(f" ... clustered events    = {len(dfz)}")

    #index_names = dfz[ (dfz.E!=0) ].index # drop nonzeroes
    #dfz = dfz.drop( index_names )
    #print(f" ... clustered where E=0 = {len(dfz)}")

    t1 = df['time'].max()
    t0 = df['time'].min()
    rate = len(df)/(t1-t0)
    # ---------------
    wind_erlang = erlang.erlang_cum(float(TIMEWIN_US)*1e-6, rate, 1)*100  # in %    bellow window 4.48us
    trgh_erlang = erlang.erlang_cum(float(TRGHOLD)*1e-6, rate, 1)*100  # in %    bellow window 4.48us

    satun_n_ch = None # n saturations
    Tsatu_ch = None # time max in satu
    Tsatu_pr = None # percent max in satu
    if 'extras' in df:
        #print(f"D... extras    present: {df1['extras'].unique()}... 1..satur,3..roll,4..reset,8..fake" )
        satu_n_ch = len(df.loc[ (df['extras']&1)!=0] )
        Tsatu_ch = df.loc[ (df['extras']&1)!=0]["prev_satu"].sum()/1e+6   # in sec...
        Tsatu_pr = 100*Tsatu_ch/(t1-t0)
        #print(f"D... SATURATIONS {satu_n_ch} total: {Tsatu_ch} sec. at maximum")
        #print(f"D... SATURATIONS {satu_n_ch} total: {100*Tsatu_ch/interval:.2f} % at maximum")

        #print(f"D... number of saturations: ",len( df.loc[ (df['extras']&1)==1] ) , f" {Tsatu_ch:.2f} sec. at max;  {Tsatu_pr:.2f} % at max"   )


    output = f"""________________________________________________________________________
 {filename:40s}        {t0:.2f} ... {t1:.2f} sec.
________________________________________________________________________
    D... total    events (chan={channel}) = {len(df):8d}
    D... isolated events (chan={channel}) = {isoevents:8d}
    D... clusterd events (chan={channel}) = {len(df)-isoevents:8d}  (in {nclusters} clusters)

    D... total    nonzero(chan={channel}) = {len(df)-zeroes:8d}
    D... isolated nonzero(chan={channel}) = {isoevents-isozeroes:8d}
    D... clusterd nonzero(chan={channel}) = {len(df)-zeroes-isononzeroes:8d}

    D... total    zeroes (chan={channel}) = {zeroes:8d} ~ {zeroes/len(df)*100:5.2f}% {fg.green}/DT-caen/{fg.default}
    D... isolated zeroes (chan={channel}) = {isozeroes:8d} ~ {isozeroes/len(df)*100:5.2f}%  [glitches]
    D... clusterd zeroes (chan={channel}) = {zeroes-isozeroes:8d}
    D... single   zeroes (chan={channel}) = {szeroes:8d} (E-0)  /{100*szeroes/len(df):.2f} %/
    D... double   zeroes (chan={channel}) = {dzeroes:8d} (0-0)  /{2*100*dzeroes/len(df):.2f} %/ {fg.yellow}/?clusters/{fg.default}
    D... ilogic   zeroes (chan={channel}) = {izeroes:8d} (0-E)  /should be 0/
    D... double   E      (chan={channel}) = {dnonzeroes:8d} (E-E)  /should be 0/

    D... blind erlang    (chan={channel}) = {wind_erlang:.2f} %  {fg.green}/DT from ERLANG/{fg.default} {TIMEWIN_US:.1f} us
    D... blind erlang    (chan={channel}) = {trgh_erlang:.2f} %  {fg.green}/DT from ERLANG/{fg.default} {TRGHOLD:.1f} us

    D... n_sat,tmax_sat  (chan={channel}) = {satu_n_ch:8d}, {Tsatu_ch:.2f} s. {Tsatu_pr:.1f} %  {fg.green}/DT from ERLANG/{fg.default} {TRGHOLD:.1f} us
all blind10==lost ~~ all zeroes+blind0.5==lost; maybe some 0 are exagerated @ortec; NEED [satur-median] estimation HERE
_______________________________________________________________________________
"""
    # {fg.red}D... double zeroes (chan={channel}) = {dzeroes:8d} ~  {2*dzeroes/len(df)*100:5.2f}% ( % counted correctly 2x){fg.default}
    # D... => zrs@HigherClusters  = {zeroes-isozeroes-2*dzeroes:8d}  (zeroes in longer than 2 clusters)
    # D... ______________________ end of zero detection
    # D...  window {TIMEWIN_US} us   ....  crutial for correct double zeroes detection

    print(output)
    #     # returns length for now
    #     # endblock()
    return zeroes/len(df)*100
    return None # zeroes,dzeroes,szeroes,izeroes,isozeroes,output




def cut_asc(df, t_from, t_to):
    t0 = float(t_from)
    t1 = float(t_to)
    df1 = df.loc[ (df.time>t0)&(df.time<t1)]
    return df1



#------------------------------------------------------ FROM GENERAL READVMEOFFLINE
def fill_hist( his, narr):
    """
    FILL TH1D(?) histogram by  np.histogram data.
    simple way bin by bin
    """
    #print(f"D... filling TH  bin by bin ({narr.shape[0]}) bins")
    if len(narr.shape) == 1: # 1D
        for i in range(narr.shape[0]):
            #if narr.shape[0]<6:
            #    print(i, narr[i], "  ", end=";")
            # we start with 0, bin starts with 1 in ROOT
            his.SetBinContent( i+1, narr[i] )
        his.SetEntries( narr.sum() ) # complete with setting entries == integral

    elif narr.shape[1] == 2: #  2D not tested
        print("X... 2D not tested ... returning None", narr.shape )
        return None
        for i in range(narr.shape[0]):
            for j in range(narr.shape[1]):
                his.SetBinContent( i+1, j+1, narr[i][j] )
    #print("D... filling TH DONE")

#------------------------------------------------------------------------  FROM GENERAL READVMEOFFLINE
def column_to_newhisto( dfcol , binmax = 32*1024, himax=32*1024, savename = None, hname = "h1", writeondisk = False , writetxt = False, calibration = None ):
    """
    df["E"] ... creates NEW histogram from df column
    - converts to numpy array; creates HIST;
    - saves txt
    - updates allhist.root too
    """
    narr = dfcol.to_numpy()
    print(f"D... ========= creating histo {hname} ======= len={len(narr)}; bins=", binmax)
    #print("D... len=", len(narr), narr.dtype, "...  ndarray to np histo")
    #print(dfcol)
    #print(narr)
    his,bins = np.histogram(narr,bins=binmax,range=(0.0,himax) )
    #    print("D... histo:", his)
    #    print("D... bins :", bins)
    del narr

    #
    basename = hname
    hname2 = hname
    if hname2.find(";"):
        hname2 = hname2.split(";")[0]
    if savename is not None:
        basename = os.path.basename(savename) # title without path...

    #basename = f"{basename}; [us]"
    print( f"th1f = ROOT.TH1D( /{hname2}/, /{basename}/, /{binmax}/, 0 , /{himax}/ ) ")
    th1f = ROOT.TH1D(hname2, basename, binmax, 0.0 , himax )
    #for i in range(len(his)):
    #    th1f.SetBinContent( i, his[i] )
    #print("D... narr=",narr)

    #print(narr.shape  ,len(narr.shape) )
    #print(narr.shape[0] )
    fill_hist( th1f,  his )

    if not calibration is None:
        CALA = calibration[0]
        CALB = calibration[1]
        Cxmin = th1f.GetXaxis().GetXmin() * CALA + CALB
        Cxmax =th1f.GetXaxis().GetXmax() * CALA + CALB
        th1f.GetXaxis().SetLimits(Cxmin,Cxmax)
    #th1f.Print()

    if (savename is not None) and  writeondisk:
        if writetxt:
            print(f"D...          text spectrum = {savename}")
            np.savetxt(savename, his, fmt="%d")
        # rootname = os.path.splitext(savename)[0]+".root"
        rootname = os.path.dirname(savename)
        if len(rootname)>3:
            rootname+="/"
        rootname+="all_histograms.root"
        print("D...          root spectum at", rootname, "name=", hname )
        f = ROOT.TFile(rootname,"UPDATE")
        # print(f"D...          {th1f.GetName():13s} @ {rootname}")
        th1f.Write()
        f.Close()
    #endblock(nomem=True)
    return th1f # WAS RETURNIG HIS -- NUMPY ARRAY



def histo_erlang( df1 , hname = 'erlang2' ):
    hise2 = column_to_newhisto(df1['dtus'].loc[(df1.E!=0)],
    #hise2 = column_to_newhisto(df1['dtus'],
                               binmax=200, himax=20,
                                     hname = f"{hname}; dt [us]")
    hise2.Print()
    return hise2

def histo_dzeroes( df1 , hname = 'dzeroes' ):
    hisdz = column_to_newhisto(df1['dtus'].loc[(df1.E==0)&(df1.next_E==0)],
                                       binmax=200, himax=20,
                                  hname = f"{hname}; dt [us]")

    hisdz.Print()
    return hisdz

def histo_szeroes( df1 , hname = 'szeroes' ):
    hissz = column_to_newhisto(df1['dtus'].loc[(df1.E!=0)&(df1.next_E==0)],
                                       binmax=200, himax=20,
                                  hname = f"{hname}; dt [us]")

    hissz.Print()
    return hissz

def histo_energy( df1 , hname = 'energy' , calibration = None ):
    units = "[ch]"
    maxc = df1.E.max() # should not be more than int 2**15

    if maxc > 2**15-1:
        maxc = 2**14
    maxc = 2**15
    print("D... max E", maxc)

    #chan0 = df1.ch.min()
    chan = df1.ch.max()

    if calibration is not None:
        units = "[keV]"
        print("D... calibration",calibration)
        if calibration[0]==1 and calibration[1]==0:
            units  = "(chan)"
    else:
        units = "[chan]"
    hisene = column_to_newhisto(df1['E'].loc[(df1.E!=0)],
                                binmax=maxc, himax=maxc,
                                hname = f"{hname}; Energy {units}; channel {chan}", calibration = calibration)
    hisene.Print()
    return hisene


def histo_time( df1 , hname = 'time' , lowe=-99999, hie=99999 ):
    maxc = df1.time.max()
    c = df1.ch.max()
    hist = column_to_newhisto(  df1['time'].loc[ (df1.E!=0) & (df1.E>=lowe) & (df1.E<=hie) ],
                                       binmax=int(maxc)+1, himax=maxc,
                                  hname = f"{hname}; time [s]; chan {c}")


    #print( df1.loc[ (df1.E!=0) & (df1.E>=lowe) & (df1.E<=hie) ] )
    hist.Print()
    return hist
