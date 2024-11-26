import unittest
from tree import BinaryTree, StemNode


def get_height(node):
    if node is None:
        return 0
    if isinstance(node, StemNode):
        return 1
    return 1 + max(get_height(node.left), get_height(node.right))


class TestBinaryTree(unittest.TestCase):
    def test_single_entry(self):
        tree = BinaryTree()
        tree.insert(b"\x00" * 32, b"\x01" * 32)
        self.assertEqual(get_height(tree.root), 1)

    def test_two_entries_diff_first_bit(self):
        tree = BinaryTree()
        tree.insert(b"\x00" * 32, b"\x01" * 32)
        tree.insert(b"\x80" + b"\x00" * 31, b"\x02" * 32)
        self.assertEqual(get_height(tree.root), 2)

    def test_one_stem_colocated_values(self):
        tree = BinaryTree()
        tree.insert(b"\x00" * 31 + b"\x03", b"\x01" * 32)
        tree.insert(b"\x00" * 31 + b"\x04", b"\x02" * 32)
        tree.insert(b"\x00" * 31 + b"\x09", b"\x03" * 32)
        tree.insert(b"\x00" * 31 + b"\xFF", b"\x04" * 32)
        self.assertEqual(get_height(tree.root), 1)

    def test_two_stem_colocated_values(self):
        tree = BinaryTree()
        # stem: 0...0
        tree.insert(b"\x00" * 31 + b"\x03", b"\x01" * 32)
        tree.insert(b"\x00" * 31 + b"\x04", b"\x02" * 32)
        # stem: 10...0
        tree.insert(b"\x80" * 31 + b"\x03", b"\x01" * 32)
        tree.insert(b"\x80" * 31 + b"\x04", b"\x02" * 32)
        self.assertEqual(get_height(tree.root), 2)

    def test_two_keys_match_first_42_bits(self):
        tree = BinaryTree()
        # key1 and key 2 have the same prefix of 42 bits (b0*42+b1+b1) and differ after.
        key1 = b"\x00" * 5 + b"\xC0" * 27
        key2 = b"\x00" * 5 + b"\xE0" + b"\x00" * 26
        tree.insert(key1, b"\x01" * 32)
        tree.insert(key2, b"\x02" * 32)
        self.assertEqual(get_height(tree.root), 1 + 42 + 1)

    def test_insert_duplicate_key(self):
        tree = BinaryTree()
        tree.insert(b"\x01" * 32, b"\x01" * 32)
        tree.insert(b"\x01" * 32, b"\x02" * 32)
        self.assertEqual(get_height(tree.root), 1)
        # Verify that the value is updated
        self.assertEqual(tree.root.values[1], b"\x02" * 32)

    def test_large_number_of_entries(self):
        tree = BinaryTree()
        for i in range(1 << 8):
            key = i.to_bytes(1, byteorder="little") + b"\x00" * 31
            tree.insert(key, b"\xFF" * 32)
        self.assertEqual(get_height(tree.root), 1 + 8)

    def test_merkleize_multiple_entries(self):
        tree = BinaryTree()
        keys = [
            b"\x00" * 32,
            b"\x80" + b"\x00" * 31,
            b"\x01" + b"\x00" * 31,
            b"\x81" + b"\x00" * 31,
        ]
        for i, key in enumerate(keys, start=1):
            tree.insert(key, i.to_bytes(32, byteorder="little"))
        got = tree.merkleize()
        expected = "e27e0e85876a24c51d16cf81d7e4d7e9d7aebe538eeaaef48e1bf3a843ea398d"
        self.assertEqual(bytes.hex(got), expected)


if __name__ == "__main__":
    unittest.main()
