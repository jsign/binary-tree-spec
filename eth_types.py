class Address(bytes):
    def __new__(cls, value):
        if len(value) != 20:
            raise ValueError("address must be exactly 20 bytes long")
        return super().__new__(cls, value)


class Address32(bytes):
    def __new__(cls, value):
        if len(value) != 32:
            raise ValueError("address must be exactly 32 bytes long")
        return super().__new__(cls, value)


class bytes32(bytes):
    def __new__(cls, value):
        if len(value) != 32:
            raise ValueError("blob must be exactly 32 bytes long")
        return super().__new__(cls, value)
