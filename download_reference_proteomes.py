import argparse
import requests
from requests.adapters import HTTPAdapter, Retry
import re

def download_proteome(proteome_id):
    """
    Download UniProtKB reference proteome in fasta format for a given proteome ID.
    :param proteome_id: str, UniProtKB proteome identifier
    :return: None
    """

    re_next_link = re.compile(r'<(.+)>; rel="next"')
    retries = Retry(total=5, backoff_factor=0.25, status_forcelist=[500, 502, 503, 504])
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retries))

    def get_next_link(headers):
        if "Link" in headers:
            match = re_next_link.match(headers["Link"])
            if match:
                return match.group(1)

    def get_batch(batch_url):
        while batch_url:
            response = session.get(batch_url)
            response.raise_for_status()

            yield response
            batch_url = get_next_link(response.headers)

    # set the base URL for UniProtKB proteome downloads
    url = "https://rest.uniprot.org/uniprotkb/stream?download=true&format=fasta&query=(proteome:{})&size=500".format(proteome_id)

    # make the download request and write the response content to a file
    progress = 0
    with open((proteome_id + ".fasta"), "w") as out_f:
        for batch in get_batch(url):
            lines = batch.text.splitlines()
            if not progress:
                print(lines[0], file=out_f)
            for line in lines[1:]:
                print(line, file=out_f)
            progress += len(lines[1:])

    print(f"Downloaded proteome {proteome_id}")

if __name__ == '__main__':
    # create an argparse parser for command line arguments
    parser = argparse.ArgumentParser(description="Download UniProtKB reference proteome in fasta format for given proteome IDs.")
    parser.add_argument("proteome_ids", nargs="+", type=str, help="UniProtKB proteome identifiers") # nargs="+" argument for parser.add_argument() allows passing multiple proteome IDs as command line arguments.

    # parse command line arguments
    args = parser.parse_args()

    # download the proteomes
    for proteome_id in args.proteome_ids:
        download_proteome(proteome_id)

