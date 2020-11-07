import argparse
import data_collection

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collect mascot generation data')
    parser.add_argument('type', choices=['birds', 'adjectives'])
    args = parser.parse_args()
    collection_type = args.type
    if collection_type == 'birds':
        data_collection.get_birds_list()
    if collection_type == 'adjectives':
        data_collection.get_adjectives_list() 
