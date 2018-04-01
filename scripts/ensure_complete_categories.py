import sys

from noaa_json_utils import NoaaJsonUtils


json_fpath = sys.argv[1]

ju = NoaaJsonUtils(json_fpath=json_fpath)
ju.ensure_image_from_cats()
