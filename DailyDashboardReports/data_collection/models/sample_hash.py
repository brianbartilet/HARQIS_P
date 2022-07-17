from Core.web import *


class DtoHashObject(JsonObject):

    def __eq__(self, other):
        return self.test_case_id == other.test_case_id

    def __hash__(self):
        return hash((
            'id', self.id,
            'data', self.data,

        ))

    id = str
    test_case_id = str
    data = dict
    test_runs = []


class DtoQTestRun(DtoHashObject):
    test_case_id = str
