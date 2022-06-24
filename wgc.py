def webgeocalc(sc, ut_start, ut_end, step, obs, ref, timesystem, state):

    import importlib
    
    kernel_sc, apis = findKernels(sc)[0], findKernels(sc)[1]
                
    if apis == 'ESA_API':
        from webgeocalc import ESA_API as API
        from webgeocalc import StateVector
        kernel_solar = 3
        kernel_leap = 4
    else:
        from webgeocalc import API
        from webgeocalc import StateVector
        kernel_solar = 1
        kernel_leap = 2

    ap=API.url
    print('\nUsing API: ', ap, '\n')
    vectors = StateVector(api=ap,kernels=[kernel_sc,kernel_solar,kernel_leap],
                          intervals=[ut_start, ut_end],
                          time_step = step,
                          time_step_units='SECONDS',
                          target=sc,
                          observer = obs,
                          time_system = timesystem,
                          reference_frame=ref,
                          state_representation=state,
                          aberration_correction='NONE'
    )
    return vectors.run()


def findKernels(sc):
    import json
    import urllib.request
    from webgeocalc import ESA_API
    from webgeocalc import API

    if sc.lower() == 'tgo':
        sc = 'em16'
    s = sc+'_ops'
    link_esa = ESA_API.url+'/kernel-sets'
    link_nasa = API.url+'/kernel-sets'
    kernelSet = ''
    api = ''
    with urllib.request.urlopen(link_esa) as url:
        kernelSets = json.loads(url.read().decode())
        for i in range(len(kernelSets['items'])):
            if sc.lower() in kernelSets['items'][i]['missionId'].lower():
                api = 'ESA_API'
                if s.lower() in kernelSets['items'][i]['missionId'].lower() or s.lower() in kernelSets['items'][i]['caption'].lower():
                    kernelSet = kernelSets['items'][i]['kernelSetId']
        if api == '':
            api = 'NASA_API'
            with urllib.request.urlopen(link_nasa) as url:
                kernelSets = json.loads(url.read().decode())
                for i in range(len(kernelSets['items'])):
                    if sc.lower() in kernelSets['items'][i]['missionId'].lower() or sc.lower() in kernelSets['items'][i]['caption'].lower():
                        kernelSet = kernelSets['items'][i]['kernelSetId']
                             
    return int(kernelSet), api


def inputs(sc, frame):
    params = []
    obs= 'EARTH'
    ref = 'J2000'
    ts = 'UTC'
    state_repr = 'RECTANGULAR'
    steps = 1
    
    if frame == 'bcrs':
        obs = 'SOLAR_SYSTEM_BARYCENTER'
        ts = 'TDB'
    elif frame == 'gtrs':
        ref = 'EARTH_FIXED'
    elif frame =='geo':
        state_repr = 'RA_DEC'
        steps = 1200
        
    utstart = '2022-06-10 10:10:00'
    utend   = '2022-06-10 11:10:00'
    
    params = [sc, utstart, utend, steps, obs, ref, ts, state_repr]
    return params



if __name__ == '__main__':

    import pandas as pd
    import numpy as np
    from astropy.coordinates import SkyCoord
    from astropy import units as u
    import re

    sc = 'mex'
    rs = ['geo']#,'bcrs', 'gcrs', 'gtrs']
    
    for frames in range(len(rs)):
        stateVectors=pd.DataFrame(webgeocalc(*inputs(sc,rs[frames])))
        if rs[frames] == 'geo':
            filename = 'sources.coord'
            coords =  stateVectors[['DATE', 'RIGHT_ASCENSION', 'DECLINATION']]
            with open(filename, 'w') as f:
                for i in range(len(coords.DATE)):
                    print(coords.at[i,'RIGHT_ASCENSION'], coords.at[i,'DECLINATION'])
                    source = coords.at[i,'DATE'][11:13]+coords.at[i,'DATE'][14:16]+coords.at[i,'DATE'][17:19]
                    coord = SkyCoord(ra=coords.at[i,'RIGHT_ASCENSION']*u.degree,dec=coords.at[i,'DECLINATION']*u.degree)
                    ra = str(int(coord.ra.hms[0])).zfill(2)+':'+str(int(coord.ra.hms[1])).zfill(2)+':'+'{:0>11.9f}'.format(abs(float(coord.ra.hms[2])))
                    if coord.dec < 0:
                        dec = str(abs(int(coord.dec.dms[0]))).zfill(2)+':'+str(abs(int(coord.dec.dms[1]))).zfill(2)+':'+'{:0>10.7f}'.format(abs(float(coord.dec.dms[2])))
                        line = "source='"+source+"' ra="+ra+" dec=-"+dec+" equinox='j2000' /\n"
                    else:
                        dec = str(int(coord.dec.dms[0])).zfill(2)+':'+str(int(coord.dec.dms[1])).zfill(2)+':'+'{:0>10.7f}'.format(abs(float(coord.dec.dms[2])))
                        line = "source='"+source+"' ra="+ra+" dec="+dec+" equinox='j2000' /\n"
                    f.write(line)
        else:
            filename = sc.lower()+'.'+rs[frames]+'.'+inputs(sc,rs[frames])[-1].lower()+'.'\
                +inputs(sc,rs[frames])[1][2:4]+inputs(sc,rs[frames])[1][5:7]+inputs(sc,rs[frames])[1][8:10]+'.eph'
    
            vects = stateVectors[['DATE','X','Y','Z','D_X_DT','D_Y_DT','D_Z_DT']]
            
            date_re = re.compile('(.*).*(UTC|TDB)(.*)')
            vects = vects.assign(DATE=vects['DATE'].str.extract(date_re)[0])
            with open(filename, 'w') as f:
                np.savetxt(filename, vects.values, fmt='%s')
                
