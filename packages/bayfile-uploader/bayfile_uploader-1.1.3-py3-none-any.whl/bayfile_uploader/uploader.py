from requests import post
from json import loads
from os import path
import click
import sys


url = 'https://api.bayfiles.com/upload'


def upload_file(file_name: str) -> None:
    with open(file_name, 'rb') as f:
        response = post(url, files={'file': f})
        json_data = loads(response.text)
        if response.status_code == 200:
            print(json_data['data']['file']['url']['full'])
        else:
            print(json_data['error']['message'], file_name, file=sys.stderr)


@click.command()
@click.option(
        '--file', 
        prompt='Enter the file you want to upload', 
        help='The file you wanto to upload', 
        type=click.File('r')
)
def main(file):
    if path.exists(file.name):
        upload_file(file.name)
    else:
        print(f'File not found: {file}', file=sys.stderr)


if __name__ == '__main__':
    main()
