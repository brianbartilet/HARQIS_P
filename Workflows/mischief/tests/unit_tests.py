from Workflows.mischief import *


class UnitTests(TestCase):

    def test_create_proxies(self):
        path = 'C:\\Bin.Deploy\\Notes\\MTG\\2021'
        output = 'C:\\Bin.Deploy\\Notes\\MTG\\proxies.txt'
        generate_proxies_mapping(path, output)
