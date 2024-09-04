import argparse
import pandas as pd

# Define the source file for phrases to search
source = 'source.xlsx'

def read_file(file_path, file_type):
    """
    Reads a file based on its type and returns a pandas DataFrame.
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

        return data
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None

def search_phrases(data, column_name, phrases):
    """
    Searches for the phrases in a specified column of the DataFrame.
    Returns the index and content of the matching cells.
    """
    if column_name not in data.columns:
        print(f"Column '{column_name}' not found in the file.")
        return

    # Iterate through each phrase and search in the specified column
    for phrase in phrases:
        matches = data[data[column_name].str.contains(phrase, na=False, case=False)]

        if not matches.empty:
            for idx, row in matches.iterrows():
                print(f"Match found for '{phrase}' at index {idx}: {row[column_name]}")
        else:
            print(f"No matches found for '{phrase}' in column '{column_name}'.")

def get_phrases_to_search(source_file):
    """
    Reads the source file and returns a list of phrases from the 'address' column.
    """
    try:
        source_data = pd.read_excel(source_file, engine='openpyxl')

        if 'address' in source_data.columns:
            return source_data['address'].dropna().tolist()  # Drop empty values
        else:
            print(f"Column 'address' not found in the source file '{source_file}'.")
            return []
    except Exception as e:
        print(f"Error reading the source file: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Search phrases from the source file in the data file.")
    
    # Set default values for file_path and file_type
    parser.add_argument(
        'file_path', 
        nargs='?',  # This makes the argument optional
        default='data.xlsx',  # Default value if no argument is provided
        type=str, 
        help="Path to the data file to search (default: 'data.xlsx')."
    )
    parser.add_argument(
        'file_type', 
        nargs='?',  # This makes the argument optional
        default='excel',  # Default file type if no argument is provided
        type=str, 
        help="Type of the data file (csv, tsv, excel) (default: 'excel')."
    )
    
    args = parser.parse_args()

    # Read the data file
    data = read_file(args.file_path, args.file_type)

    if data is not None:
        # Get the list of phrases from the source file (source.xlsx)
        phrases_to_search = get_phrases_to_search(source)

        if phrases_to_search:
            # Search for the phrases in the 'address' column of the data
            search_phrases(data, 'address', phrases_to_search)
        else:
            print("No phrases to search for. The source file may be empty or incorrectly formatted.")
            
if __name__ == '__main__':
    main()
