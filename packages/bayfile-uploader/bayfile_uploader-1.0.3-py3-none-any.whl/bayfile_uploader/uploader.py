from requests import post
from json import loads
import sys
from os import path


url = 'https://api.bayfiles.com/upload'


def upload_file(file_name: str) -> None:
    with open(file_name, 'rb') as f:
        response = post(url, files={'file': f})
        json_data = loads(response.text)
        if response.status_code == 200:
            print(json_data['data']['file']['url']['full'])
        else:
            print(json_data['error']['message'], file_name)


def main():
    if len(sys.argv) > 1:
        file = sys.argv[1]
        if path.exists(file):
            upload_file(sys.argv[1])
        else:
            print(f'Invalid file: {file}')

    else:
        print('missing parameter for file.')


if __name__ == '__main__':
    main()
