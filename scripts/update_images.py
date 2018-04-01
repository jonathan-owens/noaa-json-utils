from noaa_json_utils import NoaaJsonUtils

seq1_nwfsc_fpath = "/Volumes/Imagery/data/phase-1/phase1-annotations/nwfsc_seq1/original_nwfsc_seq1.mscoco.json"
full_nwfsc_fpath = "/Volumes/Imagery/data/nwfsc/actual_SH_1508_d20150917_1_fishcount_annotation_with_no_fish.mscoco.json"

full_nwfsc = NoaaJsonUtils(json_fpath=full_nwfsc_fpath)
seq1_nwfsc = NoaaJsonUtils(json_fpath=seq1_nwfsc_fpath)

for idx, image in enumerate(full_nwfsc['images']):
    if image.get('has_annots'):
        for idx_inner, sampled_image in enumerate(seq1_nwfsc['images']):
            if image['id'] == sampled_image['id']:
                seq1_nwfsc['images'][idx_inner] = full_nwfsc['images'][idx]

seq1_nwfsc.save()
