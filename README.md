# kpdust

This is a simple Python script that analyzes the contents of your `.kdbx` file and generates a report of biggest entries/attachments. It uses the `pykeepass` library to read the `.kdbx` file and `tabulate` to format the output.

## Requirements

- Python 3.x
- pip

## Installation

1. Clone the repository:

```bash
git clone git@github.com:403-html/kpdust.git
cd kpdust
```

1. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the script with the path to your `.kdbx` file as an argument:

```bash
python kpdust.py /path/to/your/database.kdbx
```

Example output:

```sh
$ python3 kpdust.py sample.kdbx
Enter master password: 
KeePass DB: sample.kdbx (8.79 MB)
Total entries with attachments: 6
Total attachment size: 8.79 MB

Size         Count  Entry                  Group     Attachments
---------  -------  ---------------------  --------  ---------------------------------------------------
5.00 MB          1  Project Documentation  Work      project_design.bin (5.00 MB)
2.00 MB          1  Family Photos          Personal  family_photo.bin (2.00 MB)
1.00 MB          1  Client Presentation    Clients   presentation.bin (1.00 MB)
800.00 KB        2  Travel Documents       Personal  passport.bin (500.00 KB), insurance.bin (300.00 KB)
5.00 KB          1  Tax Information        Finance   tax_id.bin (5.00 KB)
2.00 KB          1  SSH Keys               Work      id_rsa.bin (2.00 KB)
```

## Options

- `-n` or `--entries`: Specify the number of entries to show (default: 10, from biggest to smallest).
- `-m` or `--min-size`: Specify the minimum attachment size to display (e.g. '100KB', default: 0 – show all).
- `-p` or `--password`: Provide the master password (omit to be prompted).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
