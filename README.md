# wgc
The program calculates the coordinates of spacecraft using webgeocalc APIs.

It uses the ESA or NASA API of webgeocalc to create state vectors wrt solar system baricentrer and earth, as required to run pypride. It can also create the source.coords file (with RA and DEC) needed by MakeKey to generate .key file for VLBI scheduling.

wgc.py is the main program to calculate state vectors and coordinates. It works also as a module.

      import wgc
      wgc.calc('spacecraft','utStart','utEnd',['typeCoord'])

where:

   *spacecraft* is the name of a spacecraft included in the sc.json file

   *utStart* and *utEnd* are the start and end UT times of the calculations

   *typeCoord* is a list of possible outputs ['geo','bcrs', 'gcrs', 'gtrs','orb'] (respectively for geocentric RA DEC, solar baricentric, Earth and orbital rectangular coordinates)


sc.json contains the kernel IDs of the spacecraft. ESA and NASA keep changing them. The latest versions can be found here:

ESA: http://spice.esac.esa.int/webgeocalc/api/kernel-sets

NASA: https://wgc2.jpl.nasa.gov:8443/webgeocalc/api/kernel-sets



# stateVectors
Test program to calculate rectangular coordinates of spacecraft wrt solar system baricenter

The program compares different methods.

1) Locally downloaded SPICE kernels and spiceypy
2) webgeocalc API from JPL
3) JPL Horizons via astroquery


# Related repositories:

   * webgeocalc: https://github.com/esaSPICEservice/python-webgeocalc

   * pypride: https://gitlab.com/gofrito/pypride

   * MakeKey: https://gitlab.com/gofrito/makekey
