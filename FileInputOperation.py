import os
import re
import pandas as pd

def capture_and_replace_quotes(input_string):
    # Find all substrings between single quotes
    quoted_strings = re.findall(r"'(.*?)'", input_string)

    # Replace colons with commas in the quoted strings
    modified_strings = [s.replace(';', ',') if ';' in s else s for s in quoted_strings]

    # Replace the original quoted strings with the modified ones in the input string
    for original, modified in zip(quoted_strings, modified_strings):
        input_string = input_string.replace(f"'{original}'", f"'{modified}'")

    return input_string

class FileInputOperation:

    def __init__(self, input_directory):
        self.input_dir = input_directory

    def get_files(self, extensions, exclude_extension):
        file_list = []
        for root, dirs, files in os.walk(self.input_dir):
            for file in files:
                if len(exclude_extension) > 0 and len(extensions) == 0:
                    if not any(file.lower().endswith(ext.lower()) for ext in exclude_extension):
                        file_list.append(os.path.join(root, file))
                elif len(extensions) > 0 and len(exclude_extension) == 0:
                    if any(file.lower().endswith(ext.lower()) for ext in extensions):
                        file_list.append(os.path.join(root, file))

                elif len(extensions) == 0 and len(exclude_extension) == 0:
                    file_list.append(os.path.join(root, file))

                else:
                    raise ValueError("only provide exclude or include not in both in config files ")
        return file_list

    @staticmethod
    # def get_file_content(file):
    #     with open(file, 'r', errors="ignore") as fr:
    #         return fr.read()
    def get_file_content(file):
        with open(file, 'r', errors="ignore") as fr:
            # Create a list of lines that don't start with '#', then join them
            lines = [line for line in fr if not line.strip().startswith('#')]
            return "".join(lines)

    @staticmethod
    def get_csv_file_content(file):
        with open(file, 'r', newline='') as csvfile:
            reader = pd.read_csv(file)

        return reader

    @staticmethod
    def remove_comment(sql):
        # Use regex to remove comments
        updated_sql = sql
        # This pattern matches both single-line and multi-line comments
        # pattern = r'#.*?$|--.*?$|/\*.*?\*/'
        pattern = r'/\*.*?\*/'
        del_pattern = r'\b(delete|del)\b\s+from'
        updated_sql = re.sub(pattern, '', updated_sql, flags=re.DOTALL | re.MULTILINE)
        updated_sql = re.sub('--.*', '', updated_sql, flags=re.IGNORECASE)
        # updated_sql = re.sub('#.*', '', updated_sql, flags=re.IGNORECASE)
        updated_sql = re.sub(del_pattern, 'delete', updated_sql, flags=re.IGNORECASE)
        updated_sql = re.sub("\'\s*;\s*\'", ',', updated_sql, flags=re.DOTALL | re.IGNORECASE | re.MULTILINE)
        updated_sql = capture_and_replace_quotes(updated_sql)
        updated_sql = updated_sql.replace('"', '')
        updated_sql = re.sub('(\s+\.|\.\s+)', '.', updated_sql, flags=re.DOTALL | re.IGNORECASE | re.MULTILINE)
        return updated_sql

    @staticmethod
    def remove_sql_functions(content):
        stack = []
        new_content = ''
        last_idx = 0

        for match in re.finditer(r'(CAST|COALESCE|EXTRACT|LEADING|SUBSTRING|TRIM|OPENQUERY)\s*\(', content, flags=re.IGNORECASE):
            function_name = match.group(1).lower()
            start_index = match.start()
            stack.append(start_index)
            new_content += content[last_idx:start_index]
            idx = match.end()
            depth = 1
            while depth > 0 and idx < len(content):
                if content[idx] == '(':
                    depth += 1
                elif content[idx] == ')':
                    depth -= 1
                idx += 1

            last_idx = idx

            if depth == 0:
                new_content += ' '
            else:
                new_content += content[start_index:idx]

        new_content += content[last_idx:]
        return new_content
