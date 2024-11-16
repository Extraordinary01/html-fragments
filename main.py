import argparse

from msg_split import split_message


MAX_LEN = 4096


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-len', type=int)
    parser.add_argument('file', type=str)
    args = parser.parse_args()
    max_len = args.max_len or MAX_LEN
    file = args.file
    with open(file, 'r') as f:
        source = f.read()

    fragments = split_message(source, max_len)
    number_of_fragments = 0
    for fragment in fragments:
        number_of_fragments += 1
        print(f'--fragment #{number_of_fragments}: {len(fragment)} chars--')
        print(fragment)
