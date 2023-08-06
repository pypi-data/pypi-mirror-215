import argparse
from compare_packages.compare_packages import compare_packages


def main():
    parser = argparse.ArgumentParser(description='Compare package lists of two branches.')
    parser.add_argument('branch1', type=str, help='Name of the first branch')
    parser.add_argument('branch2', type=str, help='Name of the second branch')
    args = parser.parse_args()

    result = compare_packages(args.branch1, args.branch2)
    if result:
        print(result)
    else:
        print('Error occurred while getting package lists.')
    
    