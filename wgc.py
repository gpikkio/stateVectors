def webgeocalc(sc, ut_start, ut_end, step, obs, ref, timesystem):

    from webgeocalc import StateVector
    
    vectors = StateVector(kernel_paths=['pds/data/mex-e_m-spice-6-v2.0/mexsp_2000/EXTRAS/MK/MEX_V03.TM'],
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
                
    utstart = '2018-06-04 02:37:10'
    utend   = '2018-06-04 02:37:20'
    steps=1

    params = [sc, utstart, utend, steps, obs, ref, ts]
    return params


if __name__ == '__main__':

    import pandas as pd
    import numpy as np
    import re

    sc = 'MEX'
    rs = ['bcrs', 'gcrs', 'gtrs']

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
