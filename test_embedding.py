import unittest
from eth_types import Address32
from embedding import (
    BASIC_DATA_LEAF_KEY,
    CODE_HASH_LEAF_KEY,
    get_tree_key_for_basic_data,
    get_tree_key_for_code_hash,
)


class TestEmbedding(unittest.TestCase):
    def setUp(self):
        self.address = Address32(b"\x42" * 32)

    def test_get_tree_key_for_basic_data(self):
        result = get_tree_key_for_basic_data(self.address)
        self.assertEqual(len(result), 32)
        self.assertEqual(result[-1], BASIC_DATA_LEAF_KEY)
        print(result)

    def test_get_tree_key_for_code_hash(self):
        result = get_tree_key_for_code_hash(self.address)
        self.assertEqual(len(result), 32)
        self.assertEqual(result[-1], CODE_HASH_LEAF_KEY)


if __name__ == "__main__":
    unittest.main()
