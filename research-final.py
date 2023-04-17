import time
import eclipsr as ecl
import eleanor
import numpy as np
from astroquery.mast import Observations

with open('data.dat', 'r') as f:
    temp_data = f.read()
    tic_list = [int(i) for i in temp_data.split()]

candidates = []
start_time = time.time()
for i in range(46076, 47299):
    obsTable = Observations.query_criteria(provenance_name="GSFC-eleanor-lite", target_name=str(tic_list[i]), sequence_number=3)
    data = Observations.get_product_list(obsTable)
    Observations.download_products(data, download_dir='E:\\Coding\\PyCharm Python Projects\\light curve testing 2')

    target_data = eleanor.TargetData(eleanor.Source(fn='hlsp_gsfc-eleanor-lite_tess_ffi_s0003-0000000' + str(tic_list[i]) + '_tess_v1.0_lc.fits', fn_dir='E:\\Coding\\PyCharm Python Projects\\light curve testing 2\\mastDownload\\HLSP\\hlsp_gsfc-eleanor-lite_tess_ffi_s0003-0000000' + str(tic_list[i]) + '_tess_v1.0_lc'))

    # plt.plot(target_data.time[q], target_data.corr_flux[q]/np.nanmedian(target_data.corr_flux[q]), 'g')
    # plt.show()

    lc = target_data.to_lightkurve()
    lc = lc.normalize()

    times = lc.time.value
    signal = lc.flux.value

    try:
        times, signal = ecl.utility.ingest_signal(times, signal, tess_sectors=False)
        t_0, period, score, sine_like, wide, n_kernel, width_stats, depth_stats = ecl.find_eclipses(times, signal, mode=1, tess_sectors=False)
    except:
        continue

    if score >= 0.36:
        T = np.linspace(0.5, 27, 15000)
        bls = lc.to_periodogram(method='bls', period=T)
        if bls.max_power > 3500:
            candidates.append(tic_list[i])

            with open('candidates.dat', 'a') as f:
                f.write(str(tic_list[i]) + '\n')

end_time = time.time()
tot_time = end_time - start_time

print(tot_time)
print(candidates)

