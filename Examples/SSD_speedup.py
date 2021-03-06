'''Apparently cannot communicate between queues on Windows. This may work on U(/Li)nux'''
import sys, os

sys.path.append('D:/dodkins/MEDIS/MEDIS')
import glob
import numpy as np
# np.set_printoptions(threshold=np.inf)
import cPickle as pickle
import multiprocessing
import time
from functools import partial
import matplotlib.pylab as plt
from params import ap, cp, tp, mp, sp
# import Detector.analysis as ana
import Detector.readout as read
import Detector.pipeline as pipe
# import Detector.temporal as temp
import Detector.spectral as spec
from Detector.distribution import gaussian, poisson, MR, gaussian2
from scipy.optimize import curve_fit
from Utils.plot_tools import view_datacube, quicklook_im, loop_frames
import Utils.misc as misc
import medis.Detector.get_photon_data as gpd
from Utils.misc import debprint
import traceback
import itertools

# os.system("taskset -p 0xfffff %d" % os.getpid())
ap.companion = True
ap.contrast = [0.005,0.001,0.0025,0.01]#[0.1,0.1]
ap.lods = [[0.5,-0.5],[-1.0,1.0],[2.0,-2.0],[-3.0,3.0]]
ap.numframes = 2000
tp.detector = 'MKIDs'  #
sp.save_obs = True
mp.date = '180402/'
mp.datadir = os.path.join(mp.rootdir, mp.data, mp.date)
sp.show_cube = False
sp.return_cube = False
cp.vary_r0 = False
tp.occulter_type = '8TH_ORDER'  #
tp.satelite_speck = True
tp.NCPA_type = 'Static'
tp.nwsamp = 8
tp.speck_peakIs = [0.01, 0.0025]
tp.speck_phases = [np.pi / 2.,np.pi / 2.]
tp.speck_locs = [[50, 50], [100,100]]
sp.show_wframe = False  # 'continuous'
tp.piston_error = True
if sp.show_wframe == 'continuous':
    sp.fig = plt.figure()

ints = np.empty(0)
times = np.empty(0)
max_photons = 5e7  # 5e7 appears to be the max Pool can handle irrespective of machine capability?
# ap.numframes=200
num_chunks = int(ap.star_photons * ap.numframes / max_photons)
if num_chunks < 1:
    num_chunks = 1
print num_chunks

# ap.numframes = int(max_photons/ap.star_photons)

# num_chunks=1
bin_time = 2e-3  # 10e-3
num_ints = int(cp.frame_time * ap.numframes / bin_time)
# ylocs = range(35, 45)
# xlocs = range(85, 95)
xlocs = range(0, 129)  # range(0,128)#65
ylocs = range(0, 129)  # range(0,128)#85
occultdirs = ['mask', 'nomask']
# mp.obsfile = occultdirs[0] + '/' + 'r0varyObsfile_piston_colors.h5'
LCmapFile = os.path.join(mp.rootdir,mp.proc_dir, mp.date, 'LCvaryR0_piston_colors.pkl')
IratioFile = os.path.join(mp.rootdir, mp.proc_dir, mp.date,'IrvaryR0_piston_colors.pkl')#Iratio4040_6chunk.pkl'
# calibFile  = os.path.join(mp.rootdir,mp.proc_dir, mp.date, occultdirs[0],'calibframes.pkl')

# tp.LCmap = np.zeros((len(xlocs), len(ylocs), num_ints))


# def make_LC_map(num_chunks, max_photons, xlocs, ylocs, bin_time, LCmapFile):
#     LCmap = np.zeros((len(xlocs),len(ylocs),num_chunks*num_ints))
#     for i in range(num_chunks):
#
#         start = i*max_photons
#         # print start, start+max_photons
#         packets = pipe.read_obs(max_photons=max_photons,start=start)
#
#         # newpackets = pipe.isolate_interval(packets,[0,0.1])
#         # print np.shape(newpackets)
#         # cube = pipe.arange_into_cube(newpackets)
#         # image = pipe.make_intensity_map(cube)
#         # image = pipe.make_intensity_map_packets(packets)
#         # # loop_frames
#         # quicklook_im(image)
#         # print image[58,67]
#
#         # xloc, yloc = 58., 67.
#         # xloc, yloc = 60., 60.
#         # xloc, yloc = 60., 60.
#
#         for ix, xloc in enumerate(xlocs):
#             for iy, yloc in enumerate(ylocs):
#                 LC = pipe.get_lightcurve(packets,xloc,yloc, i*cp.frame_time*ap.numframes,bin_time=bin_time)
#                 # print LC['intensity']
#                 LCmap[ix,iy,i*num_ints:(i+1)*num_ints] = LC['intensity']
#                 if (ix*len(ylocs) + iy)%10==0: misc.progressBar(value = (ix*len(ylocs) + iy), endvalue=len(xlocs)*len(ylocs))
#     with open(LCmapFile, 'wb') as handle:
#         pickle.dump(LCmap, handle, protocol=pickle.HIGHEST_PROTOCOL)


def save_LCmap(LCmap):
    with open(LCmapFile, 'wb') as handle:
        pickle.dump(LCmap, handle, protocol=pickle.HIGHEST_PROTOCOL)

def plot_SSD_color(xlocs, ylocs, LCmapFile, inspect=False):
    with open(LCmapFile, 'rb') as handle:
        LCmaps = pickle.load(handle)

    assert len(LCmaps.shape) == 4
    if os.path.isfile(IratioFile):
        with open(IratioFile, 'rb') as handle:
            total_maps, median_maps, interval_maps, Iratios, mIratios = pickle.load(handle)
        print np.shape(Iratios)
    else:
        total_maps, median_maps, interval_maps, Iratios, mIratios = [], [], [], [], []
        for LCmap in LCmaps:
            print np.shape(LCmap)

            # yinspect = range(35,45)
            # xinspect = range(85,95)
            yinspect = range(62,68)
            xinspect = range(62,68)
            # xinspect = range(95,102)
            # yinspect = range(26,36)

            total_map = np.sum(LCmap, axis=2)
            median_map = np.median(LCmap, axis=2)
            interval_map = np.sum(LCmap[:, :, :100], axis=2)

            if inspect:
                plt.imshow(median_map[yinspect[0]:yinspect[-1],xinspect[0]:xinspect[-1]])
                plt.show()

            Ic, Is, Iratio, mIratio = get_Iratio(LCmap, xlocs, ylocs, xinspect, yinspect, inspect)

            # quicklook_im(total_map, logAmp=True, show=False, vmin=1)
            # quicklook_im(median_map, logAmp=True, show=False, vmin=1)
            # quicklook_im(interval_map, logAmp=True, show=True, vmin=1)
            # quicklook_im(np.abs(Ic) + 1e-3, logAmp=True, show=False, vmin=1)  # , vmax=25)#
            # quicklook_im(Is, logAmp=True, show=False, vmin=1)  # ,vmax=5,)#
            # quicklook_im(Iratio, logAmp=True, show=False, vmin=1)  # ,vmax=25,)#
            # quicklook_im(mIratio, logAmp=True, show=False, vmin=1)  # , vmax=5,)#
            # quicklook_im(mIratio * Iratio, logAmp=True, show=False, vmin=1)  # , vmax=500,)#
            # plt.show()

            total_maps.append(total_map)
            median_maps.append(median_map)
            interval_maps.append(interval_map)
            Iratios.append(Iratio)
            mIratios.append(mIratio)


    with open(IratioFile, 'wb') as handle:
        pickle.dump([total_maps, median_maps, interval_maps, Iratios, mIratios], handle, protocol=pickle.HIGHEST_PROTOCOL)

    images = np.array([total_maps, median_maps, interval_maps, Iratios])

    return images



def get_Iratio(LCmap, xlocs, ylocs, xinspect, yinspect, inspect):
    Iratio = np.zeros((len(xlocs), len(ylocs)))
    Ic = np.zeros((len(xlocs), len(ylocs)))
    Is = np.zeros((len(xlocs), len(ylocs)))
    mIratio = np.zeros((len(xlocs), len(ylocs)))
    for ix, xloc in enumerate(xlocs):
        for iy, yloc in enumerate(ylocs):
            if (ix * len(ylocs) + iy) % 100 == 0: misc.progressBar(value=(ix * len(ylocs) + iy),
                                                                   endvalue=len(xlocs) * len(ylocs))
            ints = LCmap[ix, iy]

            ID = pipe.get_intensity_dist(ints)
            bincent = (ID['binsS'] + np.roll(ID['binsS'], 1)) / 2.
            bincent = np.array(bincent)[1:]

            guessIc = np.mean(ints) * 0.7
            guessIs = np.mean(ints) * 0.3

            Imean = np.mean(ints)
            Istd = np.std(ints)
            Ic[ix, iy] = np.sqrt(Imean ** 2 - Istd ** 2)
            Is[ix, iy] = Imean - Ic[ix, iy]
            Iratio[ix, iy] = Ic[ix, iy] / Is[ix, iy]
            m = (np.sum(ints) - (Ic[ix, iy] + Ic[ix, iy])) / (
                np.sqrt(Is[ix, iy] ** 2 + 2 * Ic[ix, iy] + Is[ix, iy]) * len(ints))
            mIratio[ix, iy] = m ** -1 * (Iratio[ix, iy])
            if inspect == True and xloc in yinspect and yloc in xinspect:
                plt.figure()
                plt.plot(ints)
                print xloc, yloc
                plt.figure()
                plt.step(bincent, ID['histS'])
                plt.plot(bincent, MR(bincent, Ic[ix, iy], Is[ix, iy]), 'r--')
                print Imean, Istd, Ic[ix, iy], Is[ix, iy], Iratio[ix, iy]
                try:
                    popt, _ = curve_fit(MR, bincent, ID['histS'], p0=[guessIc, guessIs])
                    Ic[ix, iy] = popt[0]
                    Is[ix, iy] = popt[1]
                    Iratio[ix, iy] = popt[0] / popt[1]
                    m = (np.sum(ints) - (popt[0] + popt[0])) / (
                        np.sqrt(popt[1] ** 2 + 2 * popt[0] + popt[1]) * len(ints))
                    mIratio[ix, iy] = m ** -1 * (Iratio[ix, iy])
                    plt.plot(bincent, MR(bincent, *popt), 'b--')
                    print popt, popt[0] / popt[1]
                except RuntimeError:
                    pass

                plt.show()

    return Ic, Is, Iratio, mIratio

def plot_SSD(xlocs, ylocs, LCmapFile, inspect=False):
    with open(LCmapFile, 'rb') as handle:
        LCmap = pickle.load(handle)

    assert len(LCmap.shape) != 4

    LCmap = LCmap[:, :, :]

    print np.shape(LCmap)

    # yinspect = range(35,45)
    # xinspect = range(85,95)
    yinspect = range(62,68)
    xinspect = range(62, 68)
    # xinspect = range(95,102)
    # yinspect = range(26,36)

    total_map = np.sum(LCmap, axis=2)
    median_map = np.median(LCmap, axis=2)
    interval_map = np.sum(LCmap[:, :, :100], axis=2)

    if inspect:
        plt.imshow(median_map[yinspect[0]:yinspect[-1],xinspect[0]:xinspect[-1]])
        plt.show()

    quicklook_im(total_map, logAmp=True, show=False)
    quicklook_im(median_map, logAmp=True, show=False)
    quicklook_im(interval_map, logAmp=True, show=True)

    if os.path.isfile(IratioFile):
        with open(IratioFile, 'rb') as handle:
            Ic, Is, Iratio, mIratio = pickle.load(handle)
        print np.shape(Iratio)
    else:
        Ic, Is, Iratio, mIratio = get_Iratio(LCmap, xlocs, ylocs, xinspect, yinspect, inspect)
        with open(IratioFile, 'wb') as handle:
            pickle.dump([Ic, Is, Iratio, mIratio], handle, protocol=pickle.HIGHEST_PROTOCOL)

    quicklook_im(np.abs(Ic) + 1e-3, logAmp=True, show=False)  # , vmax=25)#
    quicklook_im(Is, logAmp=True, show=False)  # ,vmax=5,)#
    quicklook_im(Iratio, logAmp=True, show=False)  # ,vmax=25,)#
    quicklook_im(mIratio, logAmp=True, show=False)  # , vmax=5,)#
    quicklook_im(mIratio * Iratio, logAmp=True, show=False)  # , vmax=500,)#
    plt.show()

    return total_map, median_map, interval_map, Iratio, mIratio


def mp_worker(idx, packets):
    ints = get_LCmap_multi(idx, packets)
    return ints


def run():
    packets = pipe.read_obs(max_photons=max_photons)
    print packets[:50], packets.shape
    # tp.packets = packets

    print sp.num_processes, 'NUM_PROCESSES'
    p = multiprocessing.Pool(sp.num_processes)
    LCmap = np.zeros((len(xlocs), len(ylocs), num_ints))
    print num_ints, num_chunks
    for i in range(num_chunks):
        packets_chunk = packets[i * max_photons:(i + 1) * max_photons]
        print debprint((i, packets_chunk.shape))
        prod_x = partial(mp_worker, packets=packets_chunk)  # prod_x has only one argument x (y is fixed to 10)
        # idxs = range(tp.grid_size**2)
        idxs = range(len(xlocs) * len(ylocs))
        print debprint(idxs)
        LClist = p.map(prod_x, idxs)
        # LClist = mp_worker(idxs[0])
        # LClist = p.map(mp_worker, idxs)

        # LClist = []
        # for idx in idxs:
        #     ints = p.apply_async(mp_worker, (idx, packets)).get()
        #     print ints
        #     LClist.append(ints)
        # print LClist
        binned_chunk = num_ints / num_chunks
        print debprint((len(LClist[0]), binned_chunk))
        for idx in idxs:
            ix = idx / len(xlocs)
            iy = idx % len(xlocs)
            LCmap[ix, iy, i * binned_chunk:(i + 1) * binned_chunk] = LClist[idx]

    plt.imshow(LCmap[:, :, 0])
    plt.show()
    return LCmap


def get_LCmap_multi(idx, packets):
    # ix = idx/tp.grid_size
    # iy = idx%tp.grid_size
    ix = idx / len(xlocs)
    iy = idx % len(xlocs)
    # print ix, iy
    xloc = xlocs[ix]
    yloc = ylocs[iy]
    # print xloc, yloc
    # print tp.packets
    # print np.shape(packets), packets[:5]
    start = packets[0, 2]
    end = packets[-1, 2]
    # print start, end

    time0 = time.time()
    LC = pipe.get_lightcurve(packets, xloc, yloc, start, end + cp.frame_time, bin_time=bin_time)
    # print LC['intensity']
    time1 = time.time()
    print 'time for LC', time1 - time0
    # tp.LCmap[ix, iy] = LC['intensity']
    # if (ix * len(ylocs) + iy) % 10 == 0: misc.progressBar(value=(ix * len(ylocs) + iy),
    #                                                       endvalue=len(xlocs) * len(ylocs))
    return LC['intensity']


sentinel = None


def LCmap_worker(inqueue, output, packqueue):
# def LCmap_worker(inqueue, output, packets):
    try:
        # idx = inqueue.get()
        for idx in iter(inqueue.get, sentinel):
            # print inqueue.qsize(), output.qsize()  # , packqueue.qsize()
            ix = idx / len(xlocs)
            iy = idx % len(xlocs)
            xloc = xlocs[ix]
            yloc = ylocs[iy]
            # print inqueue.qsize(), output.qsize(), packqueue.qsize(),  'line305 3queues'
            packets = packqueue.get()
            # print inqueue.qsize(), output.qsize(), packqueue.qsize(), 'line307 3queues'
            start = 0#packets[0, 0]
            end = ap.numframes * cp.frame_time#packets[-1, 0]
            # print packets[:5],
            # print packets[-5:],
            # print np.shape(packets)
            # print start, end, 'start end'
            # print ix, iy, inqueue.qsize(), output.qsize(), packqueue.qsize()
            # time0 = time.time()
            LC = pipe.get_lightcurve(packets, xloc, yloc, start, end + cp.frame_time, bin_time=bin_time)
            # LC = pipe.get_lightcurve(packets, xloc, yloc, start, end + cp.frame_time, bin_time=bin_time, speed_up=False)
            # print LC['intensity'], len(LC['intensity'])
            # time1 = time.time()
            # print 'time', time1 - time0
            # tp.LCmap[ix, iy] = LC['intensity']
            # if (ix * len(ylocs) + iy) % 10 == 0: misc.progressBar(value=(ix * len(ylocs) + iy),
            #                                                       endvalue=len(xlocs) * len(ylocs))
            # return LC['intensity']
            output.put(LC['intensity'])
            # packqueue.put(newpackets)
    except Exception as e:
        # print ' **** Caught Exception ****'
        traceback.print_exc()
        raise e

def LCmap_speedup_colors():
    allpackets = pipe.read_obs()
    # packets = packets[:,2:]

    phases = allpackets[:, 1] - allpackets[:, 0]
    # packets = np.vstack((phases,packets[:,2:]))
    print phases[:50]
    print np.shape(allpackets)
    wsamples = np.linspace(tp.band[0], tp.band[1], tp.nwsamp)
    print wsamples

    phasebins = spec.phase_cal(wsamples)
    print phasebins
    binnedphase = np.digitize(phases,phasebins)
    print binnedphase[:20]
    LCmaps = np.zeros((len(phasebins), len(xlocs), len(ylocs), num_ints))
    for col in range(len(phasebins)):
        locs = np.where(binnedphase == col)[0]
        packets = allpackets[locs]
        # cube = pipe.arange_into_cube(packets)
        # image = pipe.make_intensity_map(cube)
        # quicklook_im(image)
        print 'Sorting packets (takes a while)'
        ind = np.lexsort((packets[:, 3], packets[:, 4]))
        packets = packets[ind]

        print packets.shape, sp.num_processes
        # exit()
        LCmap = np.zeros((len(xlocs), len(ylocs), num_ints))
        # for i in range(num_chunks):
        #     packets_chunk = packets[i * max_photons:(i + 1) * max_photons]
        output = multiprocessing.Queue()
        inqueue = multiprocessing.Queue()
        packqueue = multiprocessing.Queue()
        jobs = []

        for i in range(sp.num_processes):
            p = multiprocessing.Process(target=LCmap_worker, args=(inqueue, output, packqueue))
            jobs.append(p)
            p.start()
            # print 'ip', i
        for idx in range(len(xlocs) * len(ylocs)):
            # print 'idx', idx
            inqueue.put(idx)
        lower=0
        # for ix, iy in zip(xlocs,ylocs):
        for ix, iy in list(itertools.product(xlocs, ylocs)):
            print ix, iy, 'ix iy'#'idx', idx
            # print inqueue.qsize(), output.qsize(), packqueue.qsize(), ' 3queues'
            diff = 0
            span = lower
            while diff == 0:
                diff = packets[span,3] - iy
                span += 1
                if span == len(packets):
                    break
            # print 'lower and span', lower, span
            upper = span -1
            packets_chunk = packets[lower:upper]
            lower=upper
            packqueue.put(packets_chunk)
            LClist = output.get()
            # if ix == 1 and iy == 1:
            #     exit()
            # print LClist, 'LClist'
            # binned_chunk = num_ints / num_chunks
            # print debprint((len(LClist[0]), binned_chunk))
            # for idx in idxs:
            # ix = idx / len(xlocs)
            # iy = idx % len(xlocs)
            # LCmap[ix, iy, i * binned_chunk:(i + 1) * binned_chunk] = LClist  # [idx]
            LCmap[ix, iy] = LClist  # [idx]
            # print LClist
        print inqueue.qsize(), output.qsize(), packqueue.qsize(),  'line380 3queues'
        output.put(None)
        # packqueue.put(None)
        print inqueue.qsize(), output.qsize(), packqueue.qsize(),  'line383 3queues'
        for i in range(sp.num_processes):
            # Send the sentinal to tell Simulation to end
            inqueue.put(sentinel)
            print 'second i', i
            print 'line 205', tp.detector
            print inqueue.qsize(), output.qsize(), packqueue.qsize(), 'line389 3queues'
        for i, p in enumerate(jobs):
            p.join()
            print 'third i', i

        print col, type(col)
        LCmaps[col] = LCmap
    return LCmaps

def LCmap_speedup():
    packets = pipe.read_obs()
    packets = packets[:,2:]
    print 'Sorting packets (takes a while)'
    ind = np.lexsort((packets[:, 1], packets[:, 2]))
    packets = packets[ind]

    print packets.shape, sp.num_processes
    # exit()
    LCmap = np.zeros((len(xlocs), len(ylocs), num_ints))
    # for i in range(num_chunks):
    #     packets_chunk = packets[i * max_photons:(i + 1) * max_photons]
    output = multiprocessing.Queue()
    inqueue = multiprocessing.Queue()
    packqueue = multiprocessing.Queue()
    jobs = []

    for i in range(sp.num_processes):
        p = multiprocessing.Process(target=LCmap_worker, args=(inqueue, output, packqueue))
        jobs.append(p)
        p.start()
        # print 'ip', i
    for idx in range(len(xlocs) * len(ylocs)):
        # print 'idx', idx
        inqueue.put(idx)
    lower=0
    # for ix, iy in zip(xlocs,ylocs):
    for ix, iy in list(itertools.product(xlocs, ylocs)):
        print ix, iy, 'ix iy'#'idx', idx
        # print inqueue.qsize(), output.qsize(), packqueue.qsize(), ' 3queues'
        diff = 0
        span = lower
        while diff == 0:
            # print diff, packets[span,1], iy,  span
            diff = packets[span,1] - iy
            span += 1
            if span == ap.star_photons*ap.numframes:
                break
        print 'lower and span', lower, span
        upper = span -1
        packets_chunk = packets[lower:upper]
        lower=upper
        packqueue.put(packets_chunk)
        LClist = output.get()
        # if ix == 1 and iy == 1:
        #     exit()
        # print LClist, 'LClist'
        # binned_chunk = num_ints / num_chunks
        # print debprint((len(LClist[0]), binned_chunk))
        # for idx in idxs:
        # ix = idx / len(xlocs)
        # iy = idx % len(xlocs)
        # LCmap[ix, iy, i * binned_chunk:(i + 1) * binned_chunk] = LClist  # [idx]
        LCmap[ix, iy] = LClist  # [idx]
    print inqueue.qsize(), output.qsize(), packqueue.qsize(),  'line380 3queues'
    output.put(None)
    # packqueue.put(None)
    print inqueue.qsize(), output.qsize(), packqueue.qsize(),  'line383 3queues'
    for i in range(sp.num_processes):
        # Send the sentinal to tell Simulation to end
        inqueue.put(sentinel)
        print 'second i', i
        print 'line 205', tp.detector
        print inqueue.qsize(), output.qsize(), packqueue.qsize(), 'line389 3queues'
    for i, p in enumerate(jobs):
        p.join()
        print 'third i', i

    return LCmap
    # pipe.get_lightcurve_2d(packets, xlocs, ylocs, start, end+cp.frame_time, bin_time=bin_time)




if __name__ == '__main__':
    sp.num_processes = 45
    if not os.path.isfile(mp.datadir + mp.obsfile):
        print '********** Making obsfile ***********'
        begin = time.time()
        gpd.run()
        end = time.time()
        print 'Time elapsed: ', end - begin
        print '*************************************'

    if not os.path.isfile(LCmapFile):
        sp.num_processes = 35
        print '********** Making LightCurve file ***********'
        begin = time.time()
        # LCmap = LCmap_speedup()
        LCmaps = LCmap_speedup_colors()
        end = time.time()
        save_LCmap(LCmaps)
        print 'Time elapsed: ', end - begin
        print '*********************************************'

    # images = plot_SSD(xlocs, ylocs, LCmapFile, inspect=False)
    images = plot_SSD_color(xlocs, ylocs, LCmapFile, inspect=False)

    for i in range(tp.nwsamp):
        # print np.argwhere(np.isnan(images[3,i])),np.nanmean(images[3,i])
        # images[3,i][np.argwhere(np.isnan(images[3,i]))] = np.nanmean(images[3,i])
        nan_mask = np.isnan(images[3,i])
        # images[3,i][nan_mask]=np.nanmean(images[3,i])
        print np.nanstd(images[3,i])
        images[3, i][nan_mask] = np.random.normal(0, np.nanstd(images[3,i]), size=np.count_nonzero(nan_mask))

        zero_mask = images[1, i] == 0
        images[1, i][zero_mask] = np.random.normal(0, np.nanstd(images[1, i]), size=np.count_nonzero(zero_mask))
    nphotons = np.sum(images[0],axis=(1,2))
    print nphotons
    print images[3].shape

    # print np.nansum(images[3])
    images[1] = images[1] * nphotons.reshape(tp.nwsamp,1,1) / np.sum(images[1],axis=(1,2)).reshape(tp.nwsamp,1,1)
    images[2] = images[2] * nphotons.reshape(tp.nwsamp,1,1) / np.sum(images[2],axis=(1,2)).reshape(tp.nwsamp,1,1)
    # images[3] = images[3] * nphotons.reshape(tp.nwsamp,1,1) / np.sum(images[3],axis=(1,2)).reshape(tp.nwsamp,1,1)
    print np.sum(images[0],axis=(1,2))
    print np.sum(images[1],axis=(1,2))
    print np.sum(images[2],axis=(1,2))
    print np.sum(images[3],axis=(1,2))

    # for image in images[3:]:
    #     print np.shape(image)
    #     for imag in image:
    #         quicklook_im(imag, logAmp=False, show=True, vmin= 1)
    #         # print image[::50]

    wsamples = np.linspace(tp.band[0], tp.band[1], tp.nwsamp)
    scale_list = tp.band[0] / wsamples
    print wsamples, tp.band, scale_list
    from Detector.analysis import make_SNR_plot, make_cont_plot
    from vip_hci import pca
    SDIs = []

    for i in range(4):
        SDI = pca.pca(images[i], angle_list=np.zeros((len(images[i]))), scale_list=scale_list[::-1]**-1,
                               mask_center_px=None)
        SDIs.append(SDI)
    SDIs = np.array(SDIs)
    all_curves = np.vstack((images[:,0], SDIs))
    for i in range(len(all_curves)):
        quicklook_im(all_curves[i], vmin=1)
    # make_cont_plot(SDIs, ['Stack', 'Med', 'Short', 'Ratio'])
    # make_cont_plot(images[:,0], ['Stack', 'Med', 'Short', 'Ratio'])
    make_cont_plot(all_curves, ['J-Stack', 'J-Median', 'J-Lucky', 'J-SSD', 'SDI-Stack', 'SDI-Median', 'SDI-Lucky', 'SDI-SSD'])# norms = [1,2000,20,1,1,2000,20,1]
    plt.show()
    # mp.obsfile = occultdirs[1] + '/' + 'r0varyObsfile_piston_colors.h5'
    # LCmapFile = os.path.join(mp.rootdir, mp.proc_dir, mp.date, occultdirs[1], 'LCvaryR0_piston_colors.pkl')
    # IratioFile = os.path.join(mp.rootdir, mp.proc_dir, mp.date, occultdirs[1], 'IrvaryR0_piston_colors.pkl')
    #
    # if not os.path.isfile(mp.datadir + mp.obsfile):
    #     sp.num_processes = 20
    #     tp.occulter_type = None
    #     gpd.run()
    #     LCmap = LCmap_speedup()
    #     save_LCmap(LCmap)
    # images = plot_LC_map(xlocs, ylocs, LCmapFile, inspect=True)
# #     # print end-begin
#
# # make_LC_map(num_chunks, max_photons, xlocs, ylocs, bin_time, LCmapFile)
#
#     labels = ['total_map','median','interval_map','Iratio','mIratio']
#     import Detector.analysis as ana
#     ana.make_cont_plot(images,labels)

# max_photons=1.5e8
# packets = pipe.read_obs(max_photons=max_photons,start=0)
# # image = pipe.make_intensity_map_packets(packets)
# # quicklook_im(image)
# for xloc in range(30,96,4):
#     for yloc in [61,62]:#range(0,120,20):#range(65,70,1):
#         # xloc, yloc = 58, 27
#         print xloc, yloc

#         LC = pipe.get_lightcurve(packets,xloc,yloc)
#         print sum(LC['intensity'])
#         plt.plot(LC['time'][:-1], LC['intensity'])

#         ID = pipe.get_intensity_dist(LC['intensity'])
#         plt.figure()
#         plt.plot(ID['binsS'][:-1], ID['histS'])
#         plt.show()


