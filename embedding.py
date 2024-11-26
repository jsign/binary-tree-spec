import blake3

from eth_types import Address, Address32, bytes32

BASIC_DATA_LEAF_KEY = 0
CODE_HASH_LEAF_KEY = 1
HEADER_STORAGE_OFFSET = 64
CODE_OFFSET = 128
STEM_NODE_WIDTH = 256
MAIN_STORAGE_OFFSET = 256


def old_style_address_to_address32(address: Address) -> Address32:
    return Address32(b"\\x00" * 12 + address)


def tree_hash(inp: bytes) -> bytes32:
    return bytes32(blake3.blake3(inp).digest())


def get_tree_key(address: Address32, tree_index: int, sub_index: int):
    # Assumes STEM_NODE_WIDTH = 256
    return tree_hash(address + tree_index.to_bytes(32, "little"))[:31] + bytes(
        [sub_index]
    )


def get_tree_key_for_basic_data(address: Address32):
    return get_tree_key(address, 0, BASIC_DATA_LEAF_KEY)


def get_tree_key_for_code_hash(address: Address32):
    return get_tree_key(address, 0, CODE_HASH_LEAF_KEY)
