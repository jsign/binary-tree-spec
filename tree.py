from blake3 import blake3


class StemNode:
    def __init__(self, stem: bytes):
        assert len(stem) == 31, "stem must be 31 bytes"
        self.stem = stem
        self.left = None
        self.right = None


class InternalNode:
    def __init__(self):
        self.left = None
        self.right = None


class LeafNode:
    def __init__(self, value: bytes):
        assert len(value) == 32, "value must be 32 bytes"
        self.value = value


class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, key: bytes, value: bytes):
        assert len(key) == 32, "key must be 32 bytes"
        assert len(value) == 32, "value must be 32 bytes"
        stem = key[:31]
        subindex = key[31:]

        self.root = self._insert(self.root, stem, subindex, value, 0)

    def _insert(self, node, stem, subindex, value, depth):
        assert depth < 248, "depth must be less than 248"

        subindex_bits = self._bytes_to_bits(subindex)
        if node is None:
            node = StemNode(stem)
            self._insert_stem_subtree(node, subindex_bits, value)
            return node

        stem_bits = self._bytes_to_bits(stem)
        if isinstance(node, StemNode):
            if node.stem == stem:
                self._insert_stem_subtree(
                    node,
                    subindex,
                    value,
                )
                return node
            existing_stem_bits = self._bytes_to_bits(node.stem)
            return self._split_leaf(
                node, stem_bits, existing_stem_bits, subindex, value, depth
            )

        bit = stem_bits[depth]
        if bit == 0:
            node.left = self._insert(node.left, stem, subindex, value, depth + 1)
        else:
            node.right = self._insert(node.right, stem, subindex, value, depth + 1)
        return node

    def _insert_stem_subtree(self, node, subindex_bits, value):
        if len(subindex_bits) == 1:
            if subindex_bits[0] == 0:
                node.left = LeafNode(value)
            else:
                node.right = LeafNode(value)
            return
        if subindex_bits[0] == 0:
            if node.left is None:
                node.left = InternalNode()
            self._insert_stem_subtree(node.left, subindex_bits[1:], value)
        else:
            if node.right is None:
                node.right = InternalNode()
            self._insert_stem_subtree(node.right, subindex_bits[1:], value)

    def _split_leaf(self, leaf, stem_bits, existing_stem_bits, subindex, value, depth):
        if stem_bits[depth] == existing_stem_bits[depth]:
            new_internal = InternalNode()
            bit = stem_bits[depth]
            if bit == 0:
                new_internal.left = self._split_leaf(
                    leaf, stem_bits, existing_stem_bits, subindex, value, depth + 1
                )
            else:
                new_internal.right = self._split_leaf(
                    leaf, stem_bits, existing_stem_bits, subindex, value, depth + 1
                )
            return new_internal
        else:
            new_internal = InternalNode()
            bit = stem_bits[depth]
            stem = self._bits_to_bytes(stem_bits)
            if bit == 0:
                new_internal.left = StemNode(stem)
                self._insert_stem_subtree(new_internal.left, subindex, value)
                new_internal.right = leaf
            else:
                new_internal.right = StemNode(stem)
                self._insert_stem_subtree(new_internal.right, subindex, value)
                new_internal.left = leaf
            return new_internal

    def _bytes_to_bits(self, byte_data):
        bits = []
        for byte in byte_data:
            for i in range(8):
                bits.append((byte >> (7 - i)) & 1)
        return bits

    def _bits_to_bytes(self, bits):
        byte_data = bytearray()
        for i in range(0, len(bits), 8):
            byte = 0
            for j in range(8):
                byte |= bits[i + j] << (7 - j)
            byte_data.append(byte)
        return bytes(byte_data)

    def _hash(self, data):
        return blake3(data).digest()

    def merkelize(self):
        def _merkelize(node):
            if node is None:
                return b"\x00" * 32
            if isinstance(node, InternalNode):
                left_hash = _merkelize(node.left)
                right_hash = _merkelize(node.right)
                return self._hash(left_hash + right_hash)
            if isinstance(node, StemNode):
                left_hash = _merkelize(node.left)
                right_hash = _merkelize(node.right)
                return self._hash(node.stem + self._hash(left_hash + right_hash))

            return node.value

        return _merkelize(self.root)
