# wgc
Calculate rectangular coordinates of spacecraft using webgeocalc APIs

wgc.py is the main program to calculate state vectors.

It uses the ESA or NASA API of webgeocalc to create state vectors wrt solar system baricentrer and earth, as required to run pypride.

webgeocalc: https://github.com/esaSPICEservice/python-webgeocalc

pypride: https://gitlab.com/gofrito/pypride


# stateVectors
Calculate rectangular coordinates of spacecraft wrt solar system baricenter

The program compares different methods.

1) Locally downloaded SPICE kernels and spiceypy
2) webgeocalc API from JPL
3) JPL Horizons via astroquery
