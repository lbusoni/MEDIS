'''This code handles the relevant functionality of a Hawaii 2RG camera'''
import sys
sys.path.append('D:/dodkins/MEDIS/MEDIS')

import numpy as np
from params import ap, cp, tp, sp, hp
import pickle as pickle
import os
from Utils.plot_tools import loop_frames, quicklook_im
from . import readout as read
import matplotlib.pyplot as plt
H2RGhyperCubeFile = './BinnedH2RGhyper.pkl'
# tp.occulter_type = None  #

def scale_to_luminos(hypercube):
    scale_factor = ap.star_photons*1000*ap.exposure_time#/(tp.grid_size**2)
    print(scale_factor)
    hypercube *= scale_factor*np.ones((tp.grid_size,tp.grid_size))
    return hypercube

def add_readnoise(hypercube, std=30):
    # hypercube += 6000*np.ones_like((hypercube))*np.random.random() - 30
    hypercube += np.random.normal(0,std,(hypercube.shape[0],hypercube.shape[1],hypercube.shape[2],hypercube.shape[3]))
    # hypercube = np.abs(hypercube)
    return hypercube

def add_darkcurrent(hypercube):
    erate = 1
    dark_e = erate*num_exp*ap.exposure_time
    hypercube += dark_e*np.ones_like((hypercube))*np.random.random()*2 - erate
    return hypercube



def get_ref_psf():
    ap.numframes = 1

    print(tp.occulter_type)
    hypercube = run()
    frame = hypercube[0,0]
    quicklook_im(frame)
    with open('ref_psf.pkl', 'wb') as handle:
        pickle.dump(frame, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return frame





if __name__ == '__main__':
    import medis.Detector.get_photon_data as gpd
    tp.occulter_type = None
    tp.detector = 'H2RG'  # ''MKIDs'#
    sp.save_obs = False

    sp.show_cube = False
    sp.return_cube = True
    sp.show_wframe = False
    ap.companion = True
    tp.NCPA_type = 'Wave'

    # tp.use_atmos = True # have to for now because ao wfs reads in map produced but not neccessary
    # tp.use_ao = True
    # tp.active_null=False
    # tp.satelite_speck = True
    # tp.speck_locs = [[40,40]]
    # ap.frame_time = 0.001

    print(tp.occulter_type)
    get_ref_psf()

    # tp.occulter_type = 'Gaussian'#

    num_exp = 10
    ap.exposure_time = 0.01
    tp.NCPA_type = 'Wave'
    ap.numframes = int(num_exp * ap.exposure_time / cp.frame_time)
    print(ap.numframes)

    print(os.path.isfile(H2RGhyperCubeFile), H2RGhyperCubeFile)
    if os.path.isfile(H2RGhyperCubeFile):
        hypercube = read.open_hypercube(HyperCubeFile = H2RGhyperCubeFile)
    else:
        hypercube = gpd.run()
        print('finished run')
        print(np.shape(hypercube))
        hypercube = read.take_exposure(hypercube)
        print('here')
        read.save_hypercube(hypercube, HyperCubeFile = H2RGhyperCubeFile)
        print('here')
    # hypercube = take_exposure(hypercube)
    print(np.shape(hypercube[0,3]), np.shape(hypercube))
    loop_frames(hypercube[:,0])

    print('here')
    loop_frames(hypercube[0])
