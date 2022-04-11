def rect(prog_dir,target,ut_start,ut_end,interval):

    import spiceypy as spice
    import numpy as np
        
    float_formatter = "{:17.6f}".format
    np.set_printoptions(formatter={'float_kind':float_formatter})
    
    metakernel = prog_dir+'meta_'+target.lower()+'.tm'

    spice.kclear()
    
    spice.furnsh(metakernel)

    # Convert start UTC time to TDT.
    et1TDB = spice.utc2et(ut_start)
    et1 = spice.unitim(et1TDB, 'TDB', 'TDT')
            
    # Convert end UTC time to TDT.
    et2TDB =  spice.utc2et(ut_end)
    et2 = spice.unitim(et2TDB, 'TDB', 'TDT')

    et = et1
    
    while (et <= et2):
        times = et
        timesUTC = spice.et2utc(et,'ISOC',3)

        vecs = spice.spkezr(target, et, 'J2000', 'NONE ', '0')[0]
        print(vecs)
        
        et = et + interval

    spice.kclear()
    
    
def webgeocalc(ut_start):

    from webgeocalc import StateVector
    
    vectors = StateVector(kernel_paths=['pds/data/mex-e_m-spice-6-v2.0/mexsp_2000/EXTRAS/MK/MEX_V03.TM'],
                           times = ut_start,
                           target='MEX',
                           observer = 'SOLAR_SYSTEM_BARYCENTER',
                           reference_frame='J2000',
                           aberration_correction='NONE'
                           #state_representation='RECTANGULAR')
                          )
    return vectors.run()    


def steps(step):
    if step[-1]=='s':
        timestep=float(step[:-1])
    elif step[-1]=='m':
        timestep=float(step[:-1])*60.
    else:
#       This catches a wrong input (only m or s are valid!)
        str(int(step))+1
    return timestep


if __name__ == '__main__':
    
    import pprint
    
    directory = '/home/cimo/Programs/makekey/SPICE/meta/'
    sc = 'MEX'
    
    utstart = '2018-06-04T02:37:10'
    utend   = '2018-06-04T02:37:20'
    step = steps('1s')
    print(rect(directory,sc,utstart,utend,step))
    pprint.pprint(webgeocalc(utstart))
    
