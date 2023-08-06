# compare_packages

A shared library for comparing binary packages of two branches obtained from the public REST API https://rdb.altlinux.org/api/

This library gets the names of the two branches into the console, compares them and outputs:
- all packages that are in the 1st, but not in the 2nd
- all packages that are in the 2nd, but they are not in the 1st
- all packages whose version-release is greater in the 1st than in the 2nd

## Installing

1. Make sure you have Python and pip (Python package manager) installed. If you are using Python version 3.4 and higher, then pip should already be installed. If not, you can install it by running the command in the terminal:

python -m ensurepip --default-pip

2. Open the terminal and run the command:

pip install compare_packages

3. To run it, you need to run the command in the terminal:

compare_packages <first branch> <second branch>

