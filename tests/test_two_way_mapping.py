from collections import defaultdict
from unittest import TestCase
from two_way_mapping import TwoWayMapping


class TwoWayMappingCase(TestCase):

    def assert_mapping(self, mapping):
        direct_reversed = defaultdict(set)
        for k, v in mapping._direct.items():
            for elem in v:
                direct_reversed[elem].add(k)
        self.assertEqual(len(direct_reversed), len(mapping._reverse))
        for k, v in direct_reversed.items():
            self.assertSetEqual(mapping._reverse[k], v)

    def test_clear(self):
        mapping = TwoWayMapping()
        mapping['mammals'] = 'dog'
        mapping['flowers'] = 'sunflower'
        mapping.clear()
        self.assert_mapping(mapping)
        self.assertEqual({}, mapping._direct)
        self.assertEqual({}, mapping._reverse)
        self.assertEqual({}, mapping.invert._direct)
        self.assertEqual({}, mapping.invert._reverse)

    def test_copy(self):
        mapping = TwoWayMapping()
        mapping['mammals'] = 'dog'
        mapping_copy = mapping.copy()
        mapping_copy['flowers'] = 'sunflower'
        self.assert_mapping(mapping)
        self.assert_mapping(mapping_copy)
        self.assertEqual(1, len(mapping._direct))
        self.assertEqual(1, len(mapping._reverse))
        self.assertEqual(2, len(mapping_copy._direct))
        self.assertEqual(2, len(mapping_copy._reverse))

    def test_two_way_mapping_one_to_one(self):
        mapping = TwoWayMapping()
        mapping['mammals'] = 'dog'
        mapping['flowers'] = 'sunflower'
        self.assert_mapping(mapping)

    def test_two_way_mapping_one_to_many(self):
        mapping = TwoWayMapping()
        mapping['mammals'] = 'dog'
        mapping['mammals'] = 'cat'
        self.assert_mapping(mapping)

    def test_two_way_mapping_many_to_many(self):
        mapping = TwoWayMapping()
        mapping['mammals'] = 'dog'
        mapping['mammals'] = 'cat'
        mapping['animals'] = 'dog'
        mapping['animals'] = 'cat'
        self.assert_mapping(mapping)
