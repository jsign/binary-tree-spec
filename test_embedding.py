import unittest
from eth_types import Address32
from embedding import (
    BASIC_DATA_LEAF_KEY,
    CODE_HASH_LEAF_KEY,
    HEADER_STORAGE_OFFSET,
    get_tree_key_for_basic_data,
    get_tree_key_for_code_hash,
    get_tree_key_for_storage_slot,
    get_tree_key_for_code_chunk,
)


class TestEmbedding(unittest.TestCase):
    def setUp(self):
        self.address = Address32(b"\x42" * 32)

    def test_get_tree_key_for_basic_data(self):
        result = get_tree_key_for_basic_data(self.address)
        self.assertEqual(len(result), 32)
        self.assertEqual(result[-1], BASIC_DATA_LEAF_KEY)

    def test_get_tree_key_for_code_hash(self):
        result = get_tree_key_for_code_hash(self.address)
        self.assertEqual(len(result), 32)
        self.assertEqual(result[-1], CODE_HASH_LEAF_KEY)

    def test_get_tree_key_for_storage_slot_below_threshold(self):
        # In header
        keys = [
            get_tree_key_for_storage_slot(self.address, storage_key)
            for storage_key in range(HEADER_STORAGE_OFFSET)
        ]
        # All storage slots above live in the header so should have the same stem.
        stems = [key[:31] for key in keys]
        self.assertEqual(len(set(stems)), 1)
        for i, key in enumerate(keys):
            self.assertEqual(key[31], i + 64)

        # Check that a storage slot outside of the header has a different key.
        storage_slot = 64
        result = get_tree_key_for_storage_slot(self.address, storage_slot)
        self.assertNotEqual(keys[0], result)

    def test_get_tree_key_for_code_chunk(self):
        keys = [
            get_tree_key_for_code_chunk(self.address, chunk_id)
            for chunk_id in range(128)
        ]
        # All code-chunks above live in the header so should have the same stem.
        stems = [key[:31] for key in keys]
        self.assertEqual(len(set(stems)), 1)
        for i, key in enumerate(keys):
            self.assertEqual(key[31], i + 128)

        # Check that a code-chunk outside of the header has a different key.
        chunk_id = 256
        result = get_tree_key_for_code_chunk(self.address, chunk_id)
        self.assertNotEqual(keys[0], result)


if __name__ == "__main__":
    unittest.main()
