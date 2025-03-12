import pandas as pd

class ExcelReader:
    def read_excel(self, file_path, filters=None, exact_match=True):
        # Read the Excel file
        df = pd.read_excel(file_path, engine='openpyxl')
        
        # Apply custom filters to the DataFrame if any
        if filters:
            for column, values in filters.items():
                if isinstance(values, list):
                    if exact_match:
                        df = df[df[column].isin(values)]
                    else:
                        # Ensure the column is of string type before using .str.contains
                        df = df[df[column].astype(str).str.contains('|'.join(values), case=False, na=False)]
                else:
                    if exact_match:
                        df = df[df[column] == values]
                    else:
                        # Ensure the column is of string type before using .str.contains
                        df = df[df[column].astype(str).str.contains(values, case=False, na=False)]
        

        
        return df
    
    def filter_df(self, df, filters,exact_match=True):
        for column, values in filters.items():
            if isinstance(values, list):
                if exact_match:
                    df = df[df[column].isin(values)]
                else:
                    # Ensure the column is of string type before using .str.contains
                    df = df[df[column].astype(str).str.contains('|'.join(values), case=False, na=False)]
            else:
                if exact_match:
                    df = df[df[column] == values]
                else:
                    # Ensure the column is of string type before using .str.contains
                    df = df[df[column].astype(str).str.contains(values, case=False, na=False)]
        return df