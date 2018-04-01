import json
import os
import unittest

from noaa_json_utils import NoaaJsonUtils


test_json_fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'test.json')


class TestJsonUtils(unittest.TestCase):
    def test_json_obj_init_only(self):
        with open(test_json_fpath) as f:
            json_object = json.load(f)

        ju = NoaaJsonUtils(json_object)

        self.assertEqual(json_object, ju.json_object)

    def test_json_fpath_init_only(self):
        with open(test_json_fpath) as f:
            json_object = json.load(f)

        ju = NoaaJsonUtils(json_fpath=test_json_fpath)

        self.assertEqual(json_object, ju.json_object)

    def test_invalid_init(self):
        self.assertRaises(AttributeError, NoaaJsonUtils)

    def test_get_item(self):
        with open(test_json_fpath) as f:
            json_object = json.load(f)

        ju = NoaaJsonUtils(json_fpath=test_json_fpath)
        self.assertEqual(json_object['images'], ju['images'])

    def test_set_item(self):
        ju = NoaaJsonUtils(json_fpath=test_json_fpath)
        ju['images'] = []
        self.assertEqual(ju['images'], ju.json_object['images'])

    def test_subtract(self):
        ju = NoaaJsonUtils(json_fpath=test_json_fpath)
        ju1 = NoaaJsonUtils(json_fpath=test_json_fpath)
        ju.images_subtract(ju1)


if __name__ == '__main__':
    unittest.main()
