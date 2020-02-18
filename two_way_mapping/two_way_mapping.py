from collections import defaultdict


class TwoWayMapping(object):

    def __init__(self):
        self._direct = defaultdict(set)
        self._reverse = defaultdict(set)
        self.invert = TwoWayMapping.__new__(TwoWayMapping)
        self.invert._direct = self._reverse
        self.invert._reverse = self._direct

    def clear(self):
        self._direct = defaultdict(set)
        self._reverse = defaultdict(set)

    def copy(self):
        new_mapping = TwoWayMapping()
        new_mapping._direct = self._direct.copy()
        new_mapping._reverse = self._reverse.copy()

    def get(self, key, default=None):
        return self._direct.get(key, default)

    def pop(self, key, default=None):
        values = self._direct.get(key, set())
        return_values = values or default
        self._direct.pop(key, None)
        for value in values:
            self._reverse[value].discard(key)
            if not self._reverse[value]:
                del self._reverse[value]
        return return_values

    def __getitem__(self, item):
        if item in self._direct:
            return self._direct[item]
        else:
            return None

    def __setitem__(self, key, value):
        self._direct[key].add(value)
        self._reverse[value].add(key)

    def __delitem__(self, key):
        values = self._direct[key]
        del self._direct[key]
        for value in values:
            self._reverse[value].discard(key)
            if not self._reverse[value]:
                del self._reverse[value]
