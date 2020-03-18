This repository already has filter folders in correct format for bagpipes.  The filters listed here can be reproduced by running convert_RES_filter_files.py which basically extracts individual filter curves from the filter.RES files (you probably already have something this). Run with python convert_RES_filter_files.py uvista_FILTER.RES for example.

BAGPIPES load data functions are tricky because I can't see a way to pass them arguments.  Therefore for each different catalogue you need a different load data function (you could possibly stack COSMOS 352 and 544 catalogues ontop of each other but CDFS has different flux processing.)

run_bagpipes.py is just an example of running bagpipes but I'm sure you already have your own.
