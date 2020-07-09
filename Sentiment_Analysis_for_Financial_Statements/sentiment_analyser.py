import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests

from ratelimit import limits, sleep_and_retry


class SecAPI(object):
    SEC_CALL_LIMIT = {'calls': 10, 'seconds': 1}

    @staticmethod
    @sleep_and_retry
    # Dividing the call limit by half to avoid coming close to the limit
    @limits(calls=SEC_CALL_LIMIT['calls'] / 2, period=SEC_CALL_LIMIT['seconds'])
    def _call_sec(url):
        return requests.get(url)

    def get(self, url):
        return self._call_sec(url).text

    def get_sec_data(self, cik, doc_type, start=0, count=60):
        """
        function to pull filled 10-ks from the SEC for each company
        :param cik: cik number for certain stock
        :param doc_type: "10-k"
        :param start: years up to now
        :param count:
        :return: list of urls
        """
        rss_url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany' \
                  '&CIK={}&type={}&start={}&count={}&owner=exclude&output=atom' \
            .format(cik, doc_type, start, count)
        sec_data = self.get(rss_url)
        feed = BeautifulSoup(sec_data.encode('ascii'), 'xml').feed
        entries = [
            (
                entry.content.find('filing-href').getText(),
                entry.content.find('filing-type').getText(),
                entry.content.find('filing-date').getText())
            for entry in feed.find_all('entry', recursive=False)]

        return entries


def print_ten_k_data(ten_k_data, fields, field_length_limit=50):
    indentation = '  '

    print('[')
    for ten_k in ten_k_data:
        print_statement = '{}{{'.format(indentation)
        for field in fields:
            value = str(ten_k[field])

            # Show return lines in output
            if isinstance(value, str):
                value_str = '\'{}\''.format(value.replace('\n', '\\n'))
            else:
                value_str = str(value)

            # Cut off the string if it gets too long
            if len(value_str) > field_length_limit:
                value_str = value_str[:field_length_limit] + '...'

            print_statement += '\n{}{}: {}'.format(indentation * 2, field, value_str)

        print_statement += '},'
        print(print_statement)
    print(']')


def plot_similarities(similarities_list, dates, title, labels):
    assert len(similarities_list) == len(labels)

    plt.figure(1, figsize=(10, 7))
    for similarities, label in zip(similarities_list, labels):
        plt.title(title)
        plt.plot(dates, similarities, label=label)
        plt.legend()
        plt.xticks(rotation=90)

    plt.show()


