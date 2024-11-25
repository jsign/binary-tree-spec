class LeafNode:
    def __init__(self, key: bytes, value: bytes):
        self.key = key
        self.value = value


class InternalNode:
    def __init__(self):
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, key: bytes, value: bytes):
        if len(key) != 32:
            raise ValueError("key must be 32 bytes")
        if len(value) != 32:
            raise ValueError("value must be 32 bytes")

        key_bits = self._bytes_to_bits(key)
        if self.root is None:
            self.root = LeafNode(key, value)
            return

        self.root = self._insert_recursive(self.root, key_bits, key, value, 0)

    def _insert_recursive(self, node, key_bits, key, value, depth):
        if isinstance(node, LeafNode):
            if node.key == key:
                node.value = value
                return node
            existing_key_bits = self._bytes_to_bits(node.key)
            return self._split_leaf(
                node, key_bits, existing_key_bits, key, value, depth
            )

        bit = key_bits[depth] if depth < len(key_bits) else 0
        if bit == 0:
            node.left = self._insert_recursive(
                node.left, key_bits, key, value, depth + 1
            )
        else:
            node.right = self._insert_recursive(
                node.right, key_bits, key, value, depth + 1
            )
        return node

    def _split_leaf(self, leaf, key_bits, existing_key_bits, key, value, depth):
        if depth >= len(key_bits):
            raise Exception("depth is bigger than key length")

        if key_bits[depth] == existing_key_bits[depth]:
            new_internal = InternalNode()
            bit = key_bits[depth]
            if bit == 0:
                new_internal.left = self._split_leaf(
                    leaf, key_bits, existing_key_bits, key, value, depth + 1
                )
            else:
                new_internal.right = self._split_leaf(
                    leaf, key_bits, existing_key_bits, key, value, depth + 1
                )
            return new_internal
        else:
            new_internal = InternalNode()
            bit = key_bits[depth]
            if bit == 0:
                new_internal.left = LeafNode(key, value)
                new_internal.right = leaf
            else:
                new_internal.right = LeafNode(key, value)
                new_internal.left = leaf
            return new_internal

    def _bytes_to_bits(self, byte_data):
        bits = []
        for byte in byte_data:
            for i in range(8):
                bits.append((byte >> (7 - i)) & 1)
        return bits
