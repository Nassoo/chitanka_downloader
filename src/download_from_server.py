import os

import requests
import json
import logging

from helpers.powermanagement import long_running
from src.get_urls import GetContent

IP = 'http://127.0.0.1:8000/'


class DownloadFiles(GetContent):
    def __init__(self):
        super().__init__()
        self.urls_to_download = {}
        self.user_urls = json.load(open('user_data/user_files.json', 'r', encoding='utf-8'))
        self.user_series = json.load(open('user_data/user_series.json', 'r', encoding='utf-8'))
        self.output_dir = "../Читанка" if self.filenames == 'кирилица' else 'Chitanka'  # self.get_directory()
        self.file_type = '.fb2.zip'
        self.download_progress = 0
        self.update = True

    @long_running
    def download(self):
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.info('Starting download')
        for key in self.urls_to_download.keys():
            try:
                self.download_progress += 1
                short_name, path = self.urls_to_download[key][1:3]
                url = IP + key + '-' + short_name + self.file_type
                dir_name = os.path.join(self.output_dir, '/'.join(path.split('/')[:-1]))
                file_name = path.split('/')[-1] + self.file_type
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
                try:
                    head = requests.head(url).headers['Location']
                    r = requests.get(IP + head)
                except KeyError as e:
                    try:
                        ext = '.sfb.zip'
                        head = requests.head(IP + key + '-' + short_name + ext).headers['location']
                        head = head.replace(ext, self.file_type)
                        r = requests.get(IP + head)
                        logging.exception(f'{e}\n    {key}: {url} [SUCCESS form localhost with link to .sfb.zip]',
                                          exc_info=False)
                    except KeyError as e:
                        # TODO: add ?please
                        url = 'https://chitanka.info/' + key + '-' + short_name + self.file_type
                        r = requests.get(url)
                        logging.exception(f'{e}\n    {key}: {url} [SUCCESS form chitanka.info]', exc_info=False)
                # try:
                #     head = requests.head(url).headers['Location']
                #     r = requests.get(IP + head)
                # except requests.exceptions.MissingSchema as e:
                #     r = requests.get(url)
                #     url_fixed = r.url.replace('book/%5C', '').replace('text/%5C', '')
                #     r = requests.get(url_fixed)
                #     logging.exception(f'{e}\n    {key}: {url} [SUCCESS form localhost]', exc_info=False)

                with open(os.path.join(dir_name, file_name), 'wb') as f:
                    f.write(r.content)

                # TODO: Move it to get_new_urls(), so it can't delete accidentally duplicated files?
                if self.update and key in self.user_urls and self.user_urls[key][2] != self.urls_to_download[key][2]:
                    os.remove(os.path.join(self.output_dir, self.user_urls[key][2] + self.file_type))

                self.user_urls[key] = self.urls_to_download[key]
                self.user_series.pop(key, None)

            except Exception as e:
                logging.exception(f'{e} \n    {key} [FAIL]')

        # TODO: add an option to save the progress after each iteration
        self.save_urls()
        logging.info('End of download')

    def save_urls(self):
        with open("./user_data/user_files.json", "w", encoding='utf-8') as f:
            json.dump(self.user_urls, f, ensure_ascii=False, indent=4)
        with open("./user_data/user_series.json", "w", encoding='utf-8') as f:
            json.dump(self.user_series, f, ensure_ascii=False, indent=4)

    def get_new_urls(self):
        if self.update:
            self.urls_to_download = {k: v for k, v in self.urls.items()
                                     if k not in self.user_urls.keys()
                                     or self.user_urls[k][3] < v[3]
                                     or self.user_urls[k][2] != v[2]}
        else:
            self.urls_to_download = self.urls
