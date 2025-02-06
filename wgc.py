def webgeocalc(sc, ut_start, ut_end, step, obs, ref, timesystem, state):
    # Define the webgeocalc function to calculate state vectors
    
    """
    Calculate state vectors using the webgeocalc API.

    Parameters
    ----------
    sc : str
        Spacecraft ID (e.g., 'MEX', 'JUICE', etc.)
    ut_start : str
        Start time in UTC format (e.g., '2018-06-04T02:37:10')
    ut_end : str
        End time in UTC format (e.g., '2018-06-04T02:38:20')
    step : str
        Time step in seconds (e.g., '10s', '1m', etc.)
    obs : str
        Observer (e.g., 'EARTH', 'SOLAR_SYSTEM_BARYCENTER', etc.)
    ref : str
        Reference frame (e.g., 'J2000', 'EARTH_FIXED', etc.)
    timesystem : str
        Time system (e.g., 'TDB', 'UTC', etc.)
    state : str
        State representation (e.g., 'RECTANGULAR', 'RA_DEC', etc.)

    Returns
    -------
    A pandas DataFrame containing the state vectors in the specified state representation.
    """

    import importlib
    
    # Get spacecraft ID, kernel ID, and API type from findKernels function
    sc_id, kernel_sc, apis = findKernels(sc)[3], findKernels(sc)[2], findKernels(sc)[0]
                
    # Determine API and kernel IDs based on API type
    if apis == 'ESA':
        from webgeocalc import ESA_API as API
        from webgeocalc import StateVector
        kernel_solar = 3
        kernel_leap = 4
    else:
        from webgeocalc import API
        from webgeocalc import StateVector
        kernel_solar = 1
        kernel_leap = 2

    # Get API URL
    ap=API.url
    print('\nUsing API: ', ap, '\n')
    
    # Create StateVector object with API, kernel IDs, and calculation parameters
    vectors = StateVector(api=ap,kernels=[kernel_sc,kernel_solar,kernel_leap],
                          intervals=[ut_start, ut_end],
                          time_step = step,
                          time_step_units='SECONDS',
                          target=str(sc_id),
                          observer = obs,
                          time_system = timesystem,
                          reference_frame=ref,
                          state_representation=state,
                          aberration_correction='NONE'
    )
    
    # Run the state vector calculation and return the result
    return vectors.run()def webgeocalc(sc, ut_start, ut_end, step, obs, ref, timesystem, state):

    import importlib
    
    sc_id, kernel_sc, apis = findKernels(sc)[3], findKernels(sc)[2], findKernels(sc)[0]
                
    if apis == 'ESA':
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
                          target=str(sc_id),
                          observer = obs,
                          time_system = timesystem,
                          reference_frame=ref,
                          state_representation=state,
                          aberration_correction='NONE'
    )
    return vectors.run()


def findKernels(sc):
    import json
    with open('sc.json') as sc_file:
        data = json.load(sc_file)
        for i in range(len(data)):
            if sc.upper() in data[i]['Names']:
                kernel_data = data[i]['API'], data[i]['mission_id'], data[i]['kernel_id'], data[i]['NAIF ID']
    return kernel_data


def inputs(sc, utstart, utend, frame):
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
    elif frame == 'orb':
        obs='MARS'
        steps = 20
         
    params = [sc, utstart, utend, steps, obs, ref, ts, state_repr]
    return params

def calc(sc,ut1,ut2,rs):

    import pandas as pd
    import numpy as np
    from astropy.coordinates import SkyCoord
    from astropy import units as u
    import re
    
    for frames in range(len(rs)):
        stateVectors=pd.DataFrame(webgeocalc(*inputs(sc,ut1,ut2,rs[frames])))
        if rs[frames] == 'geo':
            filename = 'sources.coord'
            coords =  stateVectors[['DATE', 'RIGHT_ASCENSION', 'DECLINATION']]
            with open(filename, 'w') as f:
                for i in range(len(coords.DATE)):
                    source = coords.at[i,'DATE'][11:13]+coords.at[i,'DATE'][14:16]+coords.at[i,'DATE'][17:19]
                    coord = SkyCoord(ra=coords.at[i,'RIGHT_ASCENSION']*u.degree,dec=coords.at[i,'DECLINATION']*u.degree)
                    ra = str(int(coord.ra.hms[0])).zfill(2)+':'+str(int(coord.ra.hms[1])).zfill(2)+':'+'{:0>12.9f}'.format(abs(float(coord.ra.hms[2])))
                    if coord.dec < 0:
                        dec = str(abs(int(coord.dec.dms[0]))).zfill(2)+':'+str(abs(int(coord.dec.dms[1]))).zfill(2)+':'+'{:0>10.7f}'.format(abs(float(coord.dec.dms[2])))
                        line = "source='"+source+"' ra="+ra+" dec=-"+dec+" equinox='j2000' /\n"
                    else:
                        dec = str(int(coord.dec.dms[0])).zfill(2)+':'+str(int(coord.dec.dms[1])).zfill(2)+':'+'{:0>10.7f}'.format(abs(float(coord.dec.dms[2])))
                        line = "source='"+source+"' ra="+ra+" dec="+dec+" equinox='j2000' /\n"
                    f.write(line)
        else:
            filename = sc.lower()+'.'+rs[frames]+'.'+inputs(sc,ut1,ut2,rs[frames])[-1].lower()+'.'\
                +inputs(sc,ut1,ut2,rs[frames])[1][2:4]+inputs(sc,ut1,ut2,rs[frames])[1][5:7]+inputs(sc,ut1,ut2,rs[frames])[1][8:10]+'.eph'
    
            vects = stateVectors[['DATE','X','Y','Z','D_X_DT','D_Y_DT','D_Z_DT']]
            date_re = re.compile('(.*).*(UTC|TDB)(.*)')
            vects = vects.assign(DATE=vects['DATE'].str.extract(date_re)[0])
            vects['DATE'] = pd.to_datetime(vects['DATE'],format='%Y-%m-%d %H:%M:%S')
            vects['DATE'] = vects['DATE'].astype('datetime64').dt.strftime('%Y %m %d %H %M %S.%f')
            with open(filename, 'w') as f:
                np.savetxt(filename, vects.values, fmt='%s')
                

if __name__ == '__main__':
    
    spacecraft = 'juice'
    ### typeCoord = ['geo','bcrs', 'gcrs', 'gtrs','orb'] ###
    typeCoord = ['geo']
    utStart = '2025-08-31 04:00:00'
    utEnd   = '2025-08-31 14:00:00'
    calc(spacecraft,utStart,utEnd,typeCoord)
