# binary-tree-spec

This repository contains a minimal Python implementation for [EIP-7864](https://github.com/ethereum/EIPs/pull/9257) ([discussion thread](https://ethereum-magicians.org/t/eip-7864-ethereum-state-using-a-unified-binary-tree/22611)).

## Project Structure

- `tree.py`: Contains the implementation of the `BinaryTree` class.
- `embedding.py`: Contains the implementation accounts encoding into the tree.

## Running Tests

To run the tests, you can use the following command:

```sh
python -m unittest discover
```

This will discover and run all the tests in the `test_tree.py` file.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.
