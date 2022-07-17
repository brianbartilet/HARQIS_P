from Workflows.finance import *


class UnitTests(TestCase):

    def test_generate_collection_selling_standard_lo(self):
        generate_collection_selling('EchoMTG',
                                    'GoogleAPIsSheet',
                                    'x35 USD',
                                    35,
                                    'standard',
                                    15)

    def test_generate_collection_selling_standard_hi(self):
        generate_collection_selling('EchoMTG',
                                    'GoogleAPIsSheet',
                                    'x37 USD',
                                    37,
                                    'standard',
                                    -1000,
                                    15)

    def test_generate_collection_selling_penny(self):
        generate_collection_selling('EchoMTG',
                                    'GoogleAPIsSheet',
                                    'x30 USD',
                                    30,
                                    'penny',
                                    None)

    def test_generate_collection_buylist(self):
        generate_collection_buylist('EchoMTG',
                                    'GoogleAPIsSheet',
                                    'MY WISHLIST',
                                    25878)
