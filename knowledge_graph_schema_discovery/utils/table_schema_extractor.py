import os
import pandas as pd
import json

class DataSchemaLoader:

    def __init__(self):
        self.data_folder_path = "../data"
        self.file_format = "csv"
    
    def load_schemas(self) -> str:

        schema_list = []
        for file_name in os.listdir(self.data_folder_path):
            if file_name.endswith(self.file_format):
                table_name = file_name.split(".")[0]
                schema_list.append({table_name: self.load_schema(file_name)})
        return json.dumps(schema_list)

    def load_schema(self, file_name: str) -> dict:
        
        file_path = os.path.join(self.data_folder_path, file_name)
        df = pd.read_csv(file_path)
        
        return df.columns.to_list()