import argparse
import data_collection
import generate

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collect mascot generation data')
    subparsers = parser.add_subparsers(help='sub-command help', dest='subparser_name')

    collect_parser = subparsers.add_parser('collect')

    generate_parser = subparsers.add_parser('gen')
    generate_parser.add_argument('type', choices=['birds', 'veggies',
        'fruits'], help='type of object to generate')
    generate_parser.add_argument('--count', '-c', type=int, default=1)
    generate_parser.add_argument('--max-adj-syllables', '-a', type=int)
    generate_parser.add_argument('--max-noun-syllables', '-n', type=int)
    generate_parser.add_argument('--max-total-syllables', '-t', type=int)
    generate_parser.add_argument('--adj-percentiles', '-A', nargs=2, type=float)
    generate_parser.add_argument('--noun-percentiles', '-N', nargs=2, type=float)

    args = parser.parse_args()

    if (args.subparser_name == 'collect'):
        data_collection.collect_all_data()
        print('Completed collecting data!')

    if (args.subparser_name == 'gen'):
        generate_args = dict(
            noun=args.type,
            noun_frequency_percentile_range=args.noun_percentiles,
            adjective_frequency_percentile_range=args.adj_percentiles,
            max_adjective_syllable_count=args.max_adj_syllables,
            max_noun_syllable_count=args.max_noun_syllables,
            max_total_syllable_count=args.max_total_syllables
        )
        results = [
            generate.generate(**{
                k: v for k,v in
                generate_args.items()
                if v is not None
            })
            for i in range(args.count)
        ]
        print("\n".join(results))
