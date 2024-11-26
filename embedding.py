from typing import Sequence
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


def get_tree_key_for_code_chunk(address: Address32, chunk_id: int):
    return get_tree_key(
        address,
        (CODE_OFFSET + chunk_id) // STEM_NODE_WIDTH,
        (CODE_OFFSET + chunk_id) % STEM_NODE_WIDTH,
    )


PUSH_OFFSET = 95
PUSH1 = PUSH_OFFSET + 1
PUSH32 = PUSH_OFFSET + 32


def chunkify_code(code: bytes) -> Sequence[bytes32]:
    # Pad to multiple of 31 bytes
    if len(code) % 31 != 0:
        code += b"\\x00" * (31 - (len(code) % 31))
    # Figure out how much pushdata there is after+including each byte
    bytes_to_exec_data = [0] * (len(code) + 32)
    pos = 0
    while pos < len(code):
        if PUSH1 <= code[pos] <= PUSH32:
            pushdata_bytes = code[pos] - PUSH_OFFSET
        else:
            pushdata_bytes = 0
        pos += 1
        for x in range(pushdata_bytes):
            bytes_to_exec_data[pos + x] = pushdata_bytes - x
        pos += pushdata_bytes
    # Output chunks
    return [
        bytes32(bytes([min(bytes_to_exec_data[pos], 31)]) + code[pos : pos + 31])
        for pos in range(0, len(code), 31)
    ]
