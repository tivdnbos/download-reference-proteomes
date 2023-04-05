# UniProtKB Reference Proteome Downloader

This script downloads UniProtKB reference proteomes in FASTA format for a given proteome ID.

## Usage

`python proteome_downloader.py proteome_id1 proteome_id2 ...`

- `proteome_id`: The UniProtKB proteome identifier(s) to download.

## Installation

The script requires Python 3 and the following packages:

- requests
- argparse
- re

To install the packages, run the following command:

`pip install requests argparse re`


## Functionality

The script downloads UniProtKB reference proteomes in batches using the UniProt REST API. Each batch contains 500 sequences, and the script will download all batches of a single proteome and concatenate them into a single FASTA file. The file will be saved in the working directory with the name `proteome_id.fasta`.

## Example

Download the proteomes for `UP000005640` (_Homo sapiens_) and `UP000000625` (_Escherichia coli (strain K12)_):

`python proteome_downloader.py UP000005640 UP000002311`


This will create two files `UP000005640.fasta` and `UP000002311.fasta` in the working directory.
