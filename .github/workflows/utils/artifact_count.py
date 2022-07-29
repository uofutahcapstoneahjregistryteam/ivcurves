import argparse
import requests


def get_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='The artifacts URL of the GitHub workflow run.')
    return parser


if __name__ == '__main__':
    args = get_argparser().parse_args()
    res = requests.get(args.url)
    print(res.json())
    print(res.json()['total_count'])

