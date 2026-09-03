from FileInputOperation import FileInputOperation
from SqlParser import SqlParser
from helper import helper
from stats import Stats
import pandas as pd
import os
import datetime
import re

config = helper.get_config(helper.config_path)

input_dir = config['global']['input_dir']
output_dir = config['global']['output_dir']
input_stats = config['global']['stats']
allowed_extensions = config['global']['include_extension']
not_allowed_extensions = config['global']['exclude_extension']
process_file_count = int(config['FILE']['process_file_count']) if config['FILE']['process_file_count'] else None
csv_sql_column = config['csv_prerequisite']['column_to_extract']
csv_sql_index_column = config['csv_prerequisite']['column_index']

now = datetime.datetime.now()
date_string = now.strftime("%Y%m%d_%H%M%S")

include_extension = [ext.strip() for ext in allowed_extensions.split(',') if ext]
exclude_extension = [ext.strip() for ext in not_allowed_extensions.split(',') if ext]

db_names = []


def process_files():
    obj = FileInputOperation(input_dir)
    file_lst = obj.get_files(include_extension, exclude_extension)

    stat = Stats()
    counter = 0
    file_counter = 0
    final_df = None
    for index, file in enumerate(file_lst):
        print(f"Processing file: {os.path.basename(file)}")
        counter += 1
        try:
            if file.endswith('.csv'):
                final_df = process_csv_file(stat, obj, file, final_df, csv_sql_column, csv_sql_index_column)
            else:
                final_df = process_comprehensive_file(stat, obj, file, final_df)
        except Exception as e:
            print(f"Error processing file {file}: {e}")

        if process_file_count and counter >= process_file_count:
            if final_df is not None and not final_df.empty:
                save_dataframe(final_df, file_counter)
            file_counter += 1
            counter = 0
            final_df = None

    if final_df is not None and not final_df.empty:
        save_dataframe(final_df, file_counter)

    if input_stats.lower() == 'true':
        stats_df = pd.DataFrame({
            'Join_Count': stat.combine_join_count,
            'Join_Degree': stat.join_degree_count,
            'Access_Count': stat.access_count,
            'Incoming_Entities': stat.incoming_entities_count,
            'Outgoing_Entities': stat.outgoing_entities_count
        })
        stats_df.to_csv(os.path.join(output_dir, f'statistics_{date_string}.csv'), index=True)


def save_dataframe(df, file_counter):
    df = df.apply(lambda col: col.map(lambda x: x.lower() if isinstance(x, str) else x))
    df = df.drop_duplicates()
    output_file = os.path.join(output_dir, f'Source_Target_{file_counter}_{date_string}.csv')
    # Check if file exists to determine if we need to write headers
    header = not os.path.isfile(output_file)
    df.to_csv(output_file, mode='a', index=False, header=header)


def process_csv_file(stat, obj, file, final_df, key, key_id):
    csv_reader = obj.get_csv_file_content(file)
    for index, row in csv_reader.iterrows():
        query = row.get(key)
        if not query or not isinstance(query, str):
            continue
        query_id = row.get(key_id, None)
        cte_table_list = helper.get_cte_table_lst(query)
        volatile_table_list = helper.get_volatile_table_lst(file, query)
        final_df = process_query(file, query, final_df, stat, query_id, None, None, cte_table_list, volatile_table_list)
    return final_df


def process_comprehensive_file(stat, obj, file, final_df):
    file_content = obj.get_file_content(file)

    filtered_content = obj.remove_comment(file_content)
    filtered_content = obj.remove_sql_functions(filtered_content) # Be cautious with this line

    try:
        db_database, db_schema, db_name = helper().get_db_object_name(file, filtered_content)
        if db_name:
            db_names.append([file, f'{db_schema}.{db_name}'])
    except Exception as e:
        print(f"Could not get DB object name from {file}: {e}")
        db_database = db_schema = db_name = None

    cte_table_list = helper.get_cte_table_lst(filtered_content)
    volatile_table_list = helper.get_volatile_table_lst(file, filtered_content)

    char_offset = 0
    for query in filtered_content.split(';'):
        if not query.strip():
            char_offset += len(query) + 1
            continue

        line_offset = filtered_content.count('\n', 0, char_offset)
        final_df = process_query(file, query, final_df, stat, db_name, db_schema, db_database, cte_table_list,
                                 volatile_table_list, line_offset=line_offset)
        char_offset += len(query) + 1

    return final_df


def process_query(file, query, final_df, stat, query_id, db_schema, db_database, cte_table_list, volatile_table_list,
                  line_offset=0):

    # print(query)
    sqlParser_obj = SqlParser(file, query, line_offset=line_offset)
    source_lst, target_lst, stat_table_lst, incoming_entities_lst = sqlParser_obj.parse_sql([], [])
    print(source_lst)
    source_lst = [inner_list for inner_list in source_lst if inner_list[5] and inner_list[5] not in cte_table_list]
    target_lst = [inner_list for inner_list in target_lst if inner_list[5] and inner_list[5] not in cte_table_list]

    source_lst = [[
                      inner_list[0], inner_list[1], 'volatile-' + inner_list[2],
                      inner_list[3], inner_list[4], inner_list[5]
                  ] if inner_list[5] in volatile_table_list else inner_list for inner_list in source_lst]

    target_lst = [[
                      inner_list[0], inner_list[1], 'volatile-' + inner_list[2],
                      inner_list[3], inner_list[4], inner_list[5]
                  ] if inner_list[5] in volatile_table_list else inner_list for inner_list in target_lst]

    if stat_table_lst:
        stat.driver(stat_table_lst, incoming_entities_lst)

    return helper.creating_df(source_lst, target_lst, final_df, query_id, db_schema, db_database)


if __name__ == '__main__':
    process_files()
