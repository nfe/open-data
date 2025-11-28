import pandas as pd
import json

def read_and_convert_to_json(file_path):
    """
    Reads data from all sheets in the PGE_CodigosSIAFImunicipios.xls file,
    consolidates it, and converts it to a JSON string with specific headers.

    Args:
        file_path (str): The path to the Excel file.

    Returns:
        str: A JSON string representing the consolidated data.
    """
    try:
        all_sheets_df = pd.read_excel(file_path, sheet_name=None, header=2)
        consolidated_df = pd.concat(all_sheets_df.values(), ignore_index=True)
        
        # Assuming the Excel file has at least 3 columns that you want to rename.
        # If there are more columns, you might want to select specific ones.
        # For now, we'll rename the first three.
        current_columns = consolidated_df.columns.tolist()
        rename_mapping = {
            current_columns[0]: 'id',
            current_columns[1]: 'name',
            current_columns[2]: 'state'
        }
        consolidated_df.rename(columns=rename_mapping, inplace=True)

        # If you only want these three columns in your final JSON:
        consolidated_df = consolidated_df[['id', 'name', 'state']]

        # Convert DataFrame to a list of dictionaries and then to a JSON string
        json_data = consolidated_df.to_json(orient='records', indent=4)
        return json_data
    except FileNotFoundError:
        print(f"Error: The file was not found at {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    file_to_read = "raw/localities/bra/siafi/pge_siafi.xls"
    output_filename = "raw/localities/bra/siafi/cities.json"
    json_output = read_and_convert_to_json(file_to_read)
    if json_output is not None:
        with open(output_filename, 'w') as f:
            f.write(json_output)
        print(f"Data successfully saved to {output_filename}")
