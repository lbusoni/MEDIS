'''This code handles the relevant functionality of a Hawaii 2RG camera'''
import sys
sys.path.append('D:/dodkins/MEDIS/MEDIS')
import numpy as np
from params import ap, cp, tp, sp, iop
from Utils.plot_tools import loop_frames, quicklook_im, compare_images
# from Utils.misc import debug_program
# from Examples.get_photon_data import run
import Detector.readout as read
# import Detector.H2RG as H2RG
# import Detector.pipeline as pipe
# import matplotlib.pyplot as plt

sp.save_obs = False
sp.show_cube = False
sp.return_cube = True
sp.show_wframe = False
ap.companion=True
sp.num_processes = 1
ap.contrast = [0.01]
iop.date = '180407/'
iop.update(iop.date)
tp.detector = 'ideal'
tp.NCPA_type = 'Static'
tp.check_args()
num_exp = 1
ap.exposure_time = 0.01
ap.numframes = int(num_exp * ap.exposure_time / cp.frame_time)
tp.nwsamp = 1

datacube = []

#  ++++++++ No AO no Coron ++++++++
iop.hyperFile = iop.datadir+'/BinNoAoNoCoron.pkl'
tp.use_ao = False
tp.occulter_type = None
if __name__ == '__main__':
    hyper = read.get_integ_hypercube()
    image = hyper[0,0]
    datacube.append(image)
#  +++++++++++++++++++++++++++++++


#  ++++++++ Yes AO no Coron ++++++++
iop.hyperFile = iop.datadir+'/BinYesAoNoCoron.pkl'
tp.use_ao = True
tp.occulter_type = None
if __name__ == '__main__':
    hyper = read.get_integ_hypercube()
    image = hyper[0,0]
    datacube.append(image)
#  +++++++++++++++++++++++++++++++


#  ++++++++ Yes AO Yes Coron ++++++++
iop.hyperFile = iop.datadir+'/BinYesAoYesCoron.pkl'
tp.use_ao = True
tp.occulter_type = 'Solid'
if __name__ == '__main__':
    hyper = read.get_integ_hypercube()
    image = hyper[0,0]
    datacube.append(image)
#  +++++++++++++++++++++++++++++++


#  ++++++++ Long Integration ++++++++
iop.hyperFile = iop.datadir+'/BinYesAoYesCoron_long.pkl'
tp.use_ao = True
tp.occulter_type = 'Solid'
ap.exposure_time = 1.#0.001
ap.numframes = int(num_exp * ap.exposure_time / cp.frame_time)
if __name__ == '__main__':
    hyper = read.get_integ_hypercube()
    image = hyper[0,0] / 200
    datacube.append(image)
#  +++++++++++++++++++++++++++++++

if __name__ == '__main__':
    datacube = np.array(datacube)
    # print np.mean(datacube, axis=(1,2))
    annos = ['No AO', 'AO', 'AO + Coron.', 'Long Exp.']
    # datacube = datacube/10
    compare_images(datacube, logAmp = True, annos=annos, vmin=2e-6, vmax=0.01, title=r'$I$ (A.U.)')

