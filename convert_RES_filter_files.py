##############################################################################################################################################
## Program takes command line argument for name of FILTER.RES.info file and creates folders with individual filter files required for BAGPIPES 
##############################################################################################################################################

import matplotlib.pyplot as plt
from astropy.io import ascii
import numpy as np
import os,sys


def filter_order(trans_file):
    '''
    Returns row numbers for ez translate files.  Used to create filter list that don't include every filter in FILTER.RES file.
    '''
    translate = ascii.read(trans_file,format='no_header')

    if translate['col1'][0]=='Ks_tot':
        phot_id = [str(id_) for id_ in translate['col1'][1::2]]
        trans_id = np.array([int(id_[1:]) for id_ in translate['col2'][1::2]])
    else:
        phot_id = [str(id_) for id_ in translate['col1'][::2]]
        trans_id = np.array([int(id_[1:]) for id_ in translate['col2'][::2]])
    return trans_id


def write_filters_to_file(infile):
    '''
    Parses eazy FILTER.RES files and makes filter folder containing individual filter transmission files.
    The FILTER.RES file should have a format in which the second column should have a directory name like COSMOS/SUBARU_filter_z.txt, with no spaces.  
    HSC NB816-band will not break the code but will only write to HSC and therefore filters will be lost.
    '''
    parsing_file = True
    filter_list = []

    with open(infile,'r') as file:
        filter_trans = []
        header = file.readline()
        #now loop through rest of filter file and stop when you hit the end i.e. header == ''
        while parsing_file:
            #length of filter transmission array
            length = int(header.split()[0])
            #name in filter transmission file
            fname = header.split()[1]

            print(f"parsing {fname}...")

            filt_data = []

            for i in range(length):

                temp_data = file.readline().strip('\n').split()

                filt_data.append( temp_data[1:] )

            filter_array = np.array(filt_data,dtype=float).reshape(length,2)

            # make directory and write out filter file with name in header

            if '/' in fname:
                os.system('mkdir -p filters/'+'/'.join(fname.split('/')[:-1]))

            print(f"writing filter out to filters/{fname}")

            np.savetxt('filters/'+fname,filter_array)

            #save list of files for ease of reading in later
            filter_list.append( fname )

            # now should be at next header of the following filter

            header = file.readline()

            # check if still parsing file

            parsing_file = header

    filter_list = np.array(['filters/'+filt_dir for filt_dir in filter_list])
    # only writes out filters list for those in .translate file, and in that order
    np.savetxt('filters/'+infile.split('/')[-1].strip('FILTER.RES')+'filters.txt',filter_list[ filter_order( infile.split('/')[-1]+'.translate' ) - 1 ],fmt='%s')

def parse_info_file(infile='zfourge_FILTER.RES.info'):
    filt_id = []; length = []; fnames = []; central_wv = []
    with open(infile,'r') as file:
        for line in file:
            line_data = line.strip('\n')
            id_,filt_length,file_name = line_data.split()[:3]
            filt_id.append(int(id_)); length.append(int(filt_length)); fnames.append(file_name)
            if 'lambda_c' in line_data:
                lambda_c = float(line_data.split('lambda_c=')[-1][1:10])
            else:
                lambda_c = np.nan
            central_wv.append(float(lambda_c))
    filt_id = np.array(filt_id); length = np.array(length); fnames = np.array(fnames); central_wv = np.array(central_wv)
    return filt_id,length,fnames,central_wv

if __name__ == '__main__':
    write_filters_to_file(sys.argv[1])
