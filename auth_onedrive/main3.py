import argparse
import pandas as pd

def read_file(file_path, file_type):
    """
    Reads a file based on its type and prints the contents.
    """
    try:
        if file_type == 'csv':
            data = pd.read_csv(file_path)
        elif file_type == 'tsv':
            data = pd.read_csv(file_path, sep='\t')
        elif file_type == 'excel':
            data = pd.read_excel(file_path, engine='openpyxl')
        else:
            raise ValueError("Unsupported file type. Supported types are: csv, tsv, excel")

        print(data)
    except Exception as e:
        print(f"Error reading the file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Read and display the contents of a file.")
    parser.add_argument('file_path', type=str, help="Path to the file.")
    parser.add_argument('file_type', type=str, help="Type of the file (csv, tsv, excel).")

    args = parser.parse_args()

    read_file(args.file_path, args.file_type)

if __name__ == '__main__':
    main()
