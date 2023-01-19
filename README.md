# wgc
The program calculates the coordinates of spacecraft using webgeocalc APIs

wgc.py is the main program to calculate state vectors amd coordinates. It workd also as a module.

It uses the ESA or NASA API of webgeocalc to create state vectors wrt solar system baricentrer and earth, as required to run pypride. It can also create the source.coords file (with RA and DEC) needed by MakeKey to generate .key file for VLBI scheduling.


   webgeocalc: https://github.com/esaSPICEservice/python-webgeocalc

   pypride: https://gitlab.com/gofrito/pypride

   MakeKey: https://gitlab.com/gofrito/makekey


# stateVectors
Test program to calculate rectangular coordinates of spacecraft wrt solar system baricenter

The program compares different methods.

1) Locally downloaded SPICE kernels and spiceypy
2) webgeocalc API from JPL
3) JPL Horizons via astroquery
