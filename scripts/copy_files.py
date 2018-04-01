import os
from shutil import copyfile
import sys

from noaa_json_utils import NoaaJsonUtils

json_fpath = sys.argv[1]
input_dir = sys.argv[2]
output_dir = sys.argv[3]

ju = NoaaJsonUtils(json_fpath=json_fpath)

# Copy from aretha
# for sampled_image_fp in sampled_image_fps:
#     full_image_fp = os.path.join(image_copy_dir, sampled_image_fp + '.png')
#     os.system('touch %s' % full_image_fp)
# os.system('scp jonathan.owens@aretha.kitware.com:/data/dawkins/'
#           'habcam_data/2015_Habcam_photos/%s.png %s'
#           % (sampled_image_fp, sys.argv[4]))


for image in ju['images']:
    src_fpath = os.path.join(input_dir, image['file_name'])
    dest_fpath = os.path.join(output_dir, image['file_name'])
    copyfile(src_fpath, dest_fpath)
