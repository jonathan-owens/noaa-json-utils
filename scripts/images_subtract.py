import sys

from noaa_json_utils import NoaaJsonUtils


full_fpath = sys.argv[1]
phase0_fpath = sys.argv[2]
phase1_fpath = sys.argv[3]
n_images_to_sample = int(sys.argv[4])

full = NoaaJsonUtils(json_fpath=full_fpath)
phase0 = NoaaJsonUtils(json_fpath=phase0_fpath)

full.images_subtract(phase0)
sampled = full.sample_random_images(n_images_to_sample=n_images_to_sample)

sampled.save(phase1_fpath)
