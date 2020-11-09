import argparse
import data_collection

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collect mascot generation data')
    subparsers = parser.add_subparsers(help='sub-command help', dest='subparser_name')

    collect_parser = subparsers.add_parser('collect')

    generate_parser = subparsers.add_parser('gen')
    generate_parser.add_argument('type', choices=['birds', 'veggies', 'fruits'])

    args = parser.parse_args()

    if (args.subparser_name == 'collect'):
        data_collection.collect_all_data()
        print('Completed collecting data!')

    if (args.subparser_name == 'gen'):
        generated_result = data_collection.generate(noun=args.type)
        print(generated_result)
