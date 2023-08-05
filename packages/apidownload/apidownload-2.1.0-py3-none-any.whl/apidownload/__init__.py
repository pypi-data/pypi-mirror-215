"""
Download the JSON contents of an API endpoint
"""
import json
import shutil
import sys
from pathlib import Path

import requests


class ApiDownload:
    """
    Class for downloading from the endpoints given in a file
    """

    DEFAULT_SETTINGS_FILE = Path('apidownload.json')

    def __init__(self, settings_path: str | None = None):
        if settings_path is None:
            self.settings_folder = Path()
            self.settings_file = self.DEFAULT_SETTINGS_FILE
        else:
            path = Path(settings_path)
            if path.is_dir():
                self.settings_folder = path
                self.settings_file = path / self.DEFAULT_SETTINGS_FILE
            else:
                self.settings_folder = path.parent
                self.settings_file = path

    def _fetch_endpoint(self, url: str, file: str, indent: int = 2):
        """
        Download the JSON data at url and save it in file
        """
        print('Updating ', file, sep='')
        try:
            request = requests.get(url, timeout=20)
        except requests.ConnectionError:
            print('\tCouldn\'t connect to', url, file=sys.stderr)
            return
        try:
            data = request.json()
        except requests.JSONDecodeError:
            print('\tInvalid JSON format returned', file=sys.stderr)
            return
        path = Path(file)
        if not path.is_absolute():
            path = self.settings_folder / path
        path.write_text(json.dumps(data, indent=indent))
        print('\tDone')

    def _create_settings_file(self):
        """
        Copy the example settings.json file into this directory
        """
        shutil.copyfile(
            Path(__file__).parent / 'apidownload.json',
            self.settings_file
        )
        print('Created', self.settings_file.absolute())

    def _check_endpoint(self, endpoint: dict):
        valid = True
        if 'url' not in endpoint:
            print('Missing "url" parameter:', endpoint)
            valid = False
        if 'file' not in endpoint:
            print('Missing "file" parameter:', endpoint)
            valid = False
        return valid

    def run(self):
        """
        Entry-point to program
        """
        if self.settings_file.exists():
            try:
                settings = json.loads(self.settings_file.read_text())
            except json.JSONDecodeError:
                print('Invalid JSON format:',
                      self.settings_file.absolute(), file=sys.stderr)
                return
            for endpoint in settings:
                if isinstance(endpoint, dict):
                    if self._check_endpoint(endpoint):
                        self._fetch_endpoint(**endpoint)
                else:
                    print('Invalid endpoint type:', endpoint, file=sys.stderr)
        else:
            self._create_settings_file()


if __name__ == '__main__':
    ApiDownload().run()
