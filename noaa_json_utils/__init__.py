import json
import random


class NoaaJsonUtils:
    """
    The NoaaJsonUtils class is intended to add some facility functions for
    working with NOAA JSON objects, including addition and subtraction of JSON
    objects (or subsets thereof).
    """
    def __init__(self, json_object=None, json_fpath=None):
        """
        Create an instance of JsonUtils. The associated JSON object can
        either be specified directly, or, if not, and json_fpath is
        specified, then ``self.json_object`` will be loaded from
        ``json_fpath``.

        :param json_object: JSON-type dict to be associated with this instance.
        :type json_object: dict

        :param json_fpath: Filepath to save JSON object to. If
        ``json_object`` is not passed, this will be the location from which
        we try to load ``json_object``.
        :type json_fpath: str

        :raises AttributeError: If neither ``json_object`` nor ``json_fpath``
        are passed during initialization.
        """
        self.json_object = json_object
        self.json_fpath = json_fpath

        self.__image_index = {}
        self.__image_id_to_annots = {}

        if self.json_fpath and not self.json_object:
            with open(self.json_fpath) as json_file:
                self.json_object = json.load(json_file)
        elif not self.json_object and not self.json_fpath:
            raise AttributeError('Neither a json_object nor json_fpath was '
                                 'passed when attempting to create a '
                                 'JsonUtils instance, so no valid JSON object '
                                 'can be associated with it.')

        self.__build_index()

    def update_image_json(self, new_image):
        """

        :param new_image:
        :return:
        """
        try:
            self.__image_index[new_image['id']] = new_image
        except KeyError:
            print('[[ WARNING ]] That images does not exist')

    def __build_index(self):
        """
        Builds an index of the ``json_object`` that allows for quicker
        traversal and operations.

        These indexes allow us to quickly identify which annotations
        correspond to which image ID, so we can quickly get that information
        when performing additions and subtractions.

        :return: None
        """
        # Index mapping the image ID to the image ``dict``.
        for image in self.json_object['images']:
            self.__image_index[image['id']] = image

        # Index mapping the image ID to a list of annotation ``dict``s.
        for annot in self.json_object['annotations']:
            try:
                self.__image_id_to_annots[annot['image_id']].append(annot)
            except KeyError:
                self.__image_id_to_annots[annot['image_id']] = [annot]

    def __getitem__(self, item):
        """
        Allows [] to be used on a ``NoaaJsonUtils`` instance to directly access
        the associated JSON object.

        :param item:

        :return: The item-value corresponding to ``item``
        """
        return self.json_object[item]

    def __setitem__(self, key, value):
        """
        Allows [] to be used on a ``NoaaJsonUtils`` instance to directly modify
        the associated JSON dict.

        :param key:

        :param value:

        :return:
        """
        self.json_object[key] = value

    def images_subtract(self, other, modify=True):
        """
        One of the main sections in a NOAA JSON object is the ``images``
        section. This is a list of ``dicts`` containing various information
        about the images.

        This images subtract method is intended to allow one to subtract the
        images (and all of the other fields relating to those images) of one
        JSON from another.

        :param other: The other object to subtract from this one.
        :type other: NoaaJsonUtils

        :param modify: Whether or not to modify ``self``'s own JSON object
        :type modify: bool

        :return: The new NoaaJsonUtils object with the subtraction performed
        :rtype: NoaaJsonUtils
        """
        this_images_set = set(self.__image_index)
        other_images_set = set(other.__image_index)

        subtracted_images_set = this_images_set - other_images_set

        # Make copies of the old indexes so we can extract the data we need
        # out of them
        old_img_id_to_annots = self.__image_id_to_annots.copy()
        old_img_id_to_images = self.__image_index.copy()

        # Empty out the current indexes so we can rebuild them to contain
        # only the relevant indexes.
        new_image_index = {}
        new_image_id_to_annots = {}
        for image_id in subtracted_images_set:
            new_image_index[image_id] = old_img_id_to_images[image_id]
            try:
                new_image_id_to_annots[image_id] = old_img_id_to_annots[
                    image_id]
            # For the case when the image doesn't have any annotations
            except KeyError:
                continue

        # Now, rebuild the JSON. Some of the values don't change with
        # subtraction.
        new_json_object = {
            'categories': self.json_object['categories'],
            'licenses': self.json_object['licenses'],
            'info': self.json_object['info'],
            'images': [],
            'annotations': []
        }
        for image_id in subtracted_images_set:
            new_json_object['images'].append(new_image_index[image_id])
            try:
                new_json_object['annotations'].extend(new_image_id_to_annots[
                                                          image_id])
            # For the case when the image doesn't have any annotations
            except KeyError:
                continue

        if modify:
            self.json_object = new_json_object
            self.__image_id_to_annots = new_image_id_to_annots
            self.__image_index = new_image_index

        return NoaaJsonUtils(new_json_object)

    def sample_random_images(self, ratio=None, n_images_to_sample=None):
        """
        Sample  ``ratio * 100``% or ``n_images_to_sample`` random images from
        ``self.json_object['images]``.

        In addition to performing the sampling, it also pulls out the
        respective annotations that correspond to the sample image IDs. All
        other information in ``self.json_object`` is passed directly on to
        the sampled images returned.

        :param ratio: Fractional number of images to sample. Ratio is given
        preference. That is, if you specify both this and
        ``n_images_to_sample``, ``ratio`` will be used.
        :type ratio: float

        :param n_images_to_sample: The integer number of images to sample
        from the total population
        :type n_images_to_sample: int

        :return: NoaaJsonUtils containing the sampled images and annotations
        :rtype: NoaaJsonUtils
        """
        # Determine the integer number of images to sample
        if ratio:
            n_images_to_sample = int(ratio * len(self.json_object['images']))
        elif not n_images_to_sample:
            raise ValueError('[[ ERROR ]] You must either specify a ratio or '
                             'number of images to sample')

        # Pull out just the images from the JSON object and sample the
        # appropriate number
        sampled_images = random.sample(self.json_object['images'],
                                       n_images_to_sample)

        # Get the image IDs of the sampled images
        sampled_image_ids = sorted([int(image['id'])
                                    for image in sampled_images])

        # Populate the annotations corresponding to those images
        annotations = []
        for sampled_image_id in sampled_image_ids:
            try:
                annotations.extend(self.__image_id_to_annots[sampled_image_id])
            # For the case when the image doesn't have annotations
            except KeyError:
                continue

        sampled_json = {
            'categories': self.json_object['categories'],
            'licenses': self.json_object['licenses'],
            'info': self.json_object['info'],
            'images': sampled_images,
            'annotations': annotations
        }

        return NoaaJsonUtils(sampled_json)

    def shift_annotations(self, dx=0, dy=0):
        """
        Shift the annotations by `(dx, dy)`. This works on both `keypoints`
        and `bbox` annotations, the only two valid annotation types in MSCOCO.

        This overwrites the annotations stored in the JSON object and writes
        the changes to the file on disk.

        :param dx: x shift amount
        :type dx: int

        :param dy: y shift amount
        :type dy: int
        """
        for annot in self.json_object['annotations']:
            if annot.get('keypoints'):
                x, y, v = annot['keypoints']
                annot['keypoints'] = [
                    abs(x + dx),
                    abs(y + dy),
                    v
                ]
            elif annot.get('bbox'):
                x, y, w, h = annot['bbox']
                annot['bbox'] = [
                    abs(x + dx),
                    abs(y + dy),
                    w,
                    h
                ]
        self.save()

    def ensure_image_from_cats(self):
        """

        :return:
        """
        present_category_list = set([
            annot['category_id'] for annot in self.json_object['annotations']
        ])
        all_category_list = set([
            category['id'] for category in self.json_object['categories']
        ])

        print(all_category_list - present_category_list)

    def save(self, alt_fpath=None):
        """
        Save the JSON object to disk. Defaults to saving to
        ``self.json_fpath``, as long as it is defined. If ``alt_fpath`` is
        passed, then the JSON object is written to that location on disk.

        :param alt_fpath: Alternate location to dump the JSON object.
        :type alt_fpath: str

        :raises ValueError: If neither alt_fpath nor self.json_fpath are
        specified.
        """
        if alt_fpath:
            with open(alt_fpath, 'w') as out_file:
                json.dump(self.json_object, out_file, indent=4)
        elif self.json_fpath:
            with open(self.json_fpath, 'w') as out_file:
                json.dump(self.json_object, out_file, indent=4)
        else:
            raise ValueError('Cannot save JSON to file, since instance has no'
                             ' json_fpath and alt_fpath was not specified in '
                             'call to save.')
