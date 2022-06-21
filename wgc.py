def webgeocalc(sc, ut_start, ut_end, step, obs, ref, timesystem):

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
    print(ap)
    vectors = StateVector(api=ap,kernels=[kernel_sc,kernel_solar,kernel_leap],
                          intervals=[ut_start, ut_end],
                          time_step = step,
                          time_step_units='SECONDS',
                          target=sc,
                          observer = obs,
                          time_system = timesystem,
                          reference_frame=ref,
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
    
    if frame == 'bcrs':
        obs = 'SOLAR_SYSTEM_BARYCENTER'
        ts = 'TDB'
    elif frame == 'gtrs':
        ref = 'EARTH_FIXED'
                
    utstart = '2020-06-04 02:37:10'
    utend   = '2020-06-04 02:37:20'
    steps=1

    params = [sc, utstart, utend, steps, obs, ref, ts]
    return params



if __name__ == '__main__':

    import pandas as pd
    import numpy as np
    import re

    sc = 'mex'
    rs = ['bcrs']#, 'gcrs', 'gtrs']

    for frames in range(len(rs)):
        filename = sc.lower()+'.'+rs[frames]+'.'+inputs(sc,rs[frames])[-1].lower()+'.'\
            +inputs(sc,rs[frames])[1][2:4]+inputs(sc,rs[frames])[1][5:7]+inputs(sc,rs[frames])[1][8:10]+'.eph'
    
        stateVectors=pd.DataFrame(webgeocalc(*inputs(sc,rs[frames])))
        vects = stateVectors[['DATE','X','Y','Z','D_X_DT','D_Y_DT','D_Z_DT']]
            
        #date_re = re.compile('(\d{4})-(\d{2})-(\d{2}).(\d{2})\:(\d{2})\:(\d{2}.\d{3}).*(UTC|TDB)(.*)')
        date_re = re.compile('(.*).*(UTC|TDB)(.*)')
        vects = vects.assign(DATE=vects['DATE'].str.extract(date_re)[0])
        np.savetxt(r'tmp.txt', vects.values, fmt='%s')
        with open(filename, 'w') as f:
            np.savetxt(filename, vects.values, fmt='%s')
    
    
