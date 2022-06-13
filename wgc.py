def webgeocalc(sc, ut_start, ut_end, step, obs, ref, timesystem):

    from webgeocalc import StateVector
    
    vectors = StateVector(kernel_paths=['pds/data/mex-e_m-spice-6-v2.0/mexsp_2000/EXTRAS/MK/MEX_V03.TM'],
                          #times = ut_start,
                          intervals=[ut_start, ut_end],
                          time_step = step,
                          time_step_units='SECONDS',
                          target=sc,
                          observer = obs,
                          time_system = timesystem,
                          reference_frame=ref,
                          aberration_correction='NONE'
                          #state_representation='RECTANGULAR')
    )
    return vectors.run()    

def inputs(frame):
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
    
    params = [utstart, utend, steps, obs, ref, ts]
    return params

if __name__ == '__main__':

    import pandas as pd
    import numpy as np
    import re

    sc = 'MEX'
    rs = ['bcrs', 'gcrs', 'gtrs']
    
    stateVectors=pd.DataFrame(webgeocalc(sc, *inputs(rs[2])))#utstart,utend,steps,sc,obs,ref,ts))
    vects = stateVectors[['DATE','X','Y','Z','D_X_DT','D_Y_DT','D_Z_DT']]
    np.savetxt(r'tmp.txt', vects.values, fmt='%s')
        
    date_re = re.compile('(\d{4})-(\d{2})-(\d{2}).(\d{2})\:(\d{2})\:(\d{2}.\d{3}).*(UTC|TDB)(.*)')
    for lines in open('tmp.txt'):
        match_date = date_re.match(lines)
        if match_date:
            print(match_date.group(1), match_date.group(2), match_date.group(3), match_date.group(4),
                  match_date.group(5),match_date.group(6), match_date.group(8).format())
            
