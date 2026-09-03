import configparser
import pandas as pd
import re
from SqlParser import SqlParser


class helper:
    config_path = r'configuration.cfg'

    def __init__(self):
        self.sql_dict = {}

    @staticmethod
    def get_cte_table_lst(content):

        with_dict = []
        for cte_table in re.compile(r'(?:with|\,)\s*([\w.-]+)\s+(?:as\s*(\()?|\()', re.IGNORECASE | re.DOTALL).finditer(
                content):
            cte_table = cte_table.group(1)
            with_dict.append(cte_table)

        return with_dict

    @staticmethod
    def get_config(config_path):
        config = configparser.RawConfigParser()
        config.read(config_path)
        sections = config.sections()
        get_config = {}
        for section in sections:
            get_config[section] = dict(config.items(section))
        return get_config

    @staticmethod
    def get_volatile_table_lst(file, content):
        sql_parser_obj = SqlParser(file, content)
        volatile_dict = []
        for query in content.split(';'):
            for i in sql_parser_obj.create_volatile_pattern.finditer(query):
                create_table = i.group(1)
                volatile_dict.append(create_table)
        return volatile_dict

    @staticmethod
    def creating_df(source_dict, target_dict, final_df, db_name, db_schema, db_database):

        # CORRECTED: Use the desired final column names from the beginning.
        source_cols = ["file_name", "sourcerow_num", "source_type", "source_database", "source_schema", "source_table"]
        target_cols = ["file_name", "targetrow_num", "target_type", "target_database", "target_schema", "target_table"]

        df = pd.DataFrame(source_dict, columns=source_cols)
        df1 = pd.DataFrame(target_dict, columns=target_cols)

        result_df = None

        if not df.empty and not df1.empty:
            # The merge now works perfectly with no conflicting column names.
            result_df = pd.merge(df, df1, on="file_name")
            result_df.drop_duplicates(inplace=True)

        elif not df1.empty:
            result_df = df1.copy()

        elif not df.empty:
            result_df = df.copy()

        elif df.empty and df1.empty:
            return final_df

        result_df['DB_Object_database'] = db_database
        result_df['DB_Object_schema'] = db_schema
        result_df['DB_Object_table'] = db_name

        if final_df is not None:
            final_df = pd.concat([final_df, result_df], ignore_index=True)
        else:
            # CORRECTED: Define the full list of final, correctly named columns.
            columns = [
                'file_name', "DB_Object_database", 'DB_Object_schema', 'DB_Object_table',
                'sourcerow_num', 'source_type', 'source_database', 'source_schema', 'source_table',
                'targetrow_num', 'target_type', 'target_database', 'target_schema', 'target_table'
            ]
            # Create a dataframe with only the columns present in result_df to avoid errors.
            final_df = pd.DataFrame(columns=[col for col in columns if col in result_df.columns])
            final_df = pd.concat([final_df, result_df], ignore_index=True)

        return final_df

    def resolve_dynamic_sql(self, file_content):
        re_fetch_sql_in_var = re.compile(r'set\s+(\w+)\s*=\s+(.*?);', flags=re.IGNORECASE)
        for var_with_value in re_fetch_sql_in_var.finditer(file_content):

            variable = var_with_value.group(1)
            variable_value = var_with_value.group(2).strip().replace("'", '')

            if variable_value.lower() == 'null':
                continue

            if '||' not in variable_value and self.sql_dict.get(variable) is None:
                self.sql_dict[variable] = variable_value

            if "||" in variable_value:
                variable_value_lst = variable_value.split('||')
                for i, value in enumerate(variable_value_lst):
                    if "'" not in value:
                        value = value.strip()
                        if self.sql_dict.get(value) is not None:
                            variable_value_lst[i] = self.sql_dict[value]

                updated_value = "".join(variable_value_lst)

                self.sql_dict[variable] = updated_value

    def process_dynamic_sql(self, content):
        splited_content = content.split('||')
        for i, value in enumerate(splited_content):
            if "'" not in value:
                value = value.strip().replace(':', '').replace("'", "")
                if self.sql_dict.get(value) is not None:
                    splited_content[i] = self.sql_dict[value]

        updated_splited = [i.strip().replace("'", '') for i in splited_content]

        updated_value = "".join(updated_splited)

        return updated_value

    @staticmethod
    def clean_up_dictionary(input_dict):
        cleaned_dict = {}
        for key, value in input_dict.items():
            cleaned_value = value.replace("'", "").strip()
            cleaned_dict[key] = cleaned_value
        return cleaned_dict

    @staticmethod
    def separate_schema_table(data_entity):
        if not data_entity:
            return None, 'defaultdatabase', 'defaultschema', None

        database = 'defaultdatabase'
        schema = 'defaultschema'
        table = None

        # Split and strip the input
        parts = [part.strip() for part in data_entity.strip().split('.')]

        if len(parts) == 1:
            table = parts[0]
        elif len(parts) == 2:
            schema, table = parts
        elif len(parts) == 3:
            database, schema, table = parts

        concatenated_data_entity = f"{database}.{schema}.{table}" if table else None

        return database, schema, table

    @staticmethod
    def process_db_object(sql_parser_obj, object_type):

        """Generalized method to process different database object types."""
        object_table = object_schema = object_database = None

        object_patterns = {
            'procedure': sql_parser_obj.process_procedure_pattern,
            'macro': sql_parser_obj.process_macro_pattern_return,
            'view': sql_parser_obj.process_view_pattern,
            'function': sql_parser_obj.process_function_call_pattern,
            'package': sql_parser_obj.process_package_pattern,
        }

        if object_type in object_patterns:
            # The method now returns a tuple (name, line_number)
            result_tuple = object_patterns[object_type]()
            print(result_tuple)

            # Check if the tuple and its first element (the name) are not None
            if result_tuple and result_tuple[0]:
                db_object_name = result_tuple[0]  # Extract the name from the tuple

                # Replace redundant spaces or periods around dots
                db_object_name = re.sub(r"\.\s+|\s+\.", ".", db_object_name)
                db_object_parts = db_object_name.split('.')

                if len(db_object_parts) == 3:
                    object_database, object_schema, object_table = db_object_parts
                elif len(db_object_parts) == 2:
                    object_schema, object_table = db_object_parts
                elif len(db_object_parts) == 1:
                    object_table = db_object_parts[0]

        return object_database, object_schema, object_table

    def get_db_object_name(self, file, content):
        config = helper.get_config(helper.config_path)
        db_object = config['FILE']['db_object'].lower() if 'db_object' in config['FILE'] else None
        sql_parser_obj = SqlParser(file, content)

        # Process based on db_object type
        if db_object:
            return self.process_db_object(sql_parser_obj, db_object)

        # Fallback logic if db_object is not specified
        else:
            for object_type in ['procedure', 'macro', 'view', 'function', 'package']:
                db_object_info = self.process_db_object(sql_parser_obj, object_type)
                if any(db_object_info):
                    return db_object_info

        return None, None, None
