import re
import regex

class SqlParser:
    From_pattern = re.compile(
        r'(\bFROM)\s+(([\w\&\.\-\<\>\$\#\@\{\}]+(?:\.\w+)?)(?:\s+(?:as\s+)?\w+)?\s*(?:\s*,\s*([\w\&\.\-\<\>\$\#\@\{\}]+(?:\.\w\$+)?)(?:\s+(?:as\s+)?\w+)?)*)',
        flags=re.IGNORECASE)
    update_5th_pattern = regex.compile(
        r'\b(update)\s+(\w+)\s+from\s+(\((?:[^()]++|(?R))*\)\s+(?:as\s+)?\w+)((\s*,\s*(?:\((?:[^()]++|(?R))*\)|[\w\&\.\-\$\#\{\}]+)\s+(as\s+)?\w+)+)',
        flags=re.IGNORECASE)
    update_pattern = re.compile(
        r'\b(update)\s+\w+\s+(FROM)\s+(([\w\&\.\-\<\>\$\#\@\{\}]+(?:\.\w+)?)(?:\s+(?:as\s+)?\w+)?\s*(?:\s*,\s*([\w\&\.\-\<\>\$\#\@\{\}]+(?:\.\w\$+)?)(?:\s+(?:as\s+)?\w+)?)*)',
        flags=re.IGNORECASE)
    update_2nd_pattern = re.compile(
        r'(\b(update)\s+\w+\s+from\s+([\w\&\.\-\$\@\{\}]+\s+\w+))\s+((inner|full|right|left)\s+(outer\s+)?join\s+([\w\&\.\-\$\{\}]+)\s+\w+)+',
        flags=re.IGNORECASE)
    update_3nd_pattern = re.compile(
        r'(\bUPDATE)\s+([\w\&\.\-\<\>\$\#\@\{\}]+)(?:\s+(?:as\s+)?\w+)?(?:\s+([\w\&\.\-\<\>\$\#\@\{\}]+))?\s+(SET|from)',
        flags=re.IGNORECASE)
    update_delete_comma_separated = re.compile(
        r'\b(update)\s+[\w\_\.]+\s+from\s+([\w\&\.\-\<\>\$\#\@\{\}]+)\s+\w+\s*,\s*\(', flags=re.IGNORECASE)
    create_Table_pattern = re.compile(
        r'create\s+(?:or\s+replace\s+)?(?:set|multiset|global)?\s*(?:table)\s+(?:if)?\s*(?:not)?\s*(?:exists)?\s*([\w\&\.\-\<\>\$\#\@\{\}]+)',
        flags=re.IGNORECASE)
    create_View_pattern = re.compile(
        r'create\s+(?:or\s+replace\s+)?(?:set|multiset|global)?\s*(?:view)\s+(?:if)?\s*(?:not)?\s*(?:exists)?\s*([\w\&\.\-\<\>\$\#\@\{\}]+)',
        flags=re.IGNORECASE)
    create_External_Table_pattern = re.compile(
        r'create\s+(?:or\s+replace\s+)?(?:WRITABLE\s+)?(?:external)\s+(?:web\s+)?(?:table)\s+(?:if)?\s*(?:not)?\s*(?:exists)?\s*([\w\&\.\-\<\>\$\#\@\{\}]+)',
        flags=re.IGNORECASE)
    create_External_View_pattern = re.compile(
        r'create\s+(?:or\s+replace\s+)?(?:WRITABLE\s+)?(?:external)\s+(?:web\s+)?(?:view)\s+(?:if)?\s*(?:not)?\s*(?:exists)?\s*([\w\&\.\-\<\>\$\#\@\{\}]+)',
        flags=re.IGNORECASE)
    insert_pattern = re.compile(r'\b(?:insert|ins)\s+(?:into|overwrite)?\s*(?:table)?\s*([\w\.\-\<\>\$\@\#\{\}\\]+)',
                                flags=re.IGNORECASE)
    function_pattern = re.compile(r'(CREATE\s+or\s+replace|CREATE|REPLACE)\s+(?:EDITIONABLE|NONEDITIONABLE)?\s*function\s+(([\w&.\-<>$#@{}]+)\s*\n?\s*([\w&.\-<>$#@{}]+))',flags=re.IGNORECASE)
    package_pattern = re.compile(r'(CREATE\s+or\s+replace|CREATE|REPLACE)\s+(?:EDITIONABLE|NONEDITIONABLE)?\s*package\s+(?:BODY)?\s*(([\w&.\-<>$#@{}]+)\s*\n?\s*([\w&.\-<>$#@{}]+))',flags=re.IGNORECASE)
    macro_pattern = re.compile(r'(?:CREATE\s+or\s+replace|CREATE|REPLACE)\s+(?:EDITIONABLE|NONEDITIONABLE)?\s*macro\s+(([\w&.\-<>$#@{}]+)\s*\n?\s*([\w&.\-<>$#@{}]+))',flags=re.IGNORECASE)
    truncate_pattern = re.compile(r'truncate\s+table\s+([\w\&\.\-\<\>\$\#\@\{\}]+)', flags=re.IGNORECASE)
    merge_pattern = re.compile(r'merge\s+into\s+([\w\&\.\-\<\>\$\@\#\@\{\}]+)', flags=re.IGNORECASE)
    join_pattern = re.compile(r'((inner|right|left|full|cross)\s+)?(outer\s+)?\bjoin\s+([\w\&\.\-\<\>\$\#\@\{\}]+)',
                              flags=re.IGNORECASE)
    delete_pattern = re.compile(r'(\bdelete|\bdel)\s+([\w\&\.\-\<\>\$\#\@\{\}]+)', flags=re.IGNORECASE)
    alter_pattern = re.compile(r'(?:alter)\s+(?:table)\s+([\w\&\.\-\<\>\$\#\@\{\}]+)', flags=re.IGNORECASE)
    drop_table_patter = re.compile(r'drop\s+table\s+(?:if)?\s*(?:not)?\s*(?:exists)?\s*([\w\&\.\-\<\>\$\#\@\{\}]+)',
                                   flags=re.IGNORECASE | re.DOTALL)
    re_procedure = re.compile(r"(?:CREATE\s+OR\s+REPLACE|CREATE|REPLACE)\s+(?:EDITIONABLE|NONEDITIONABLE)?\s*PROCEDURE\s+(([\w&.\-<>$#@{}]+)\s*\n?\s*([\w&.\-<>$#@{}]+))", flags=re.IGNORECASE | re.DOTALL)
    re_macro = re.compile(r"(?:CREATE\s+or\s+replace|CREATE|REPLACE)\s+(?:EDITIONABLE|NONEDITIONABLE)?\s*macro\s+(([\w&.\-<>$#@{}]+)\s*\n?\s*([\w&.\-<>$#@{}]+))",
                          flags=re.IGNORECASE | re.DOTALL)
    re_view = re.compile(r"(CREATE\s+or\s+replace|CREATE|REPLACE)\s+(?:FORCE)?\s*(?:recursive|temporary|MATERIALIZED|EDITIONABLE|NONEDITIONABLE)?\s*(view)\s+([\w.\-<>$#{}]+)",
                         flags=re.IGNORECASE | re.DOTALL)
    load_data = re.compile(r"load\s+data\s+inpath\s+([\w\&\.\'\-\<\>\\\/\$\#\@\{\}]+)", flags=re.IGNORECASE | re.DOTALL)
    into_table = re.compile(r"into\s*table\s*([\w\&\.\'\-\<\>\\\/\$\#\@\{\}]+)")
    describe = re.compile(r"\bdescribe|desc\s+(?:formatted)?\s*([\w\&\.\-\<\>\$\#\@\{\}]+)")
    show_table = re.compile(r"\bshow\s+table\s+stats\s*([\w\&\.\-\<\>\$\#\@\{\}]+)")
    msck_repair_table = re.compile(r"\bmsck\s+repair\s+table\s*([\w\&\.\-\<\>\$\#\@\{\}]+)")
    function_call_pattern = re.compile(r'function\s+([\w\.\-\<\>\$\@\#\{\}\\]+)', flags=re.IGNORECASE)
    create_volatile_pattern = re.compile(
        r'create\s+(?:or\s+replace\s+)?(?:set|multiset|volatile|temporary|temp|global)?\s*(?:temporary|volatile|temp)\s+(?:table)(?:\s+if\s+not\s+exists\s*)?\s*([\w\.\-\<\>\$\#\{\}]+)',
        flags=re.IGNORECASE)
    create_volatile_View_pattern = re.compile(
        r'create\s+(?:or\s+replace\s+)?(?:set|multiset|volatile|temporary|temp|global)?\s*(?:temporary|volatile|temp)\s+(?:view)(?:\s+if\s+not\s+exists\s*)?\s*([\w\.\-\<\>\$\#\{\}]+)',
        flags=re.IGNORECASE)

    def __init__(self, file, content, line_offset=0):
        content = re.sub(r'delete\s+from', 'delete ', content, flags=re.I)
        self.content = content
        self.file = file
        self.line_offset = line_offset

    @staticmethod
    def sepreate_schema_table(dataentity):
        """
        Parses a data entity string into its database, schema, and table components.
        """
        try:
            # Set default values
            table = None
            schema = 'defaultschema'
            database = 'defaultdatabase'

            dataentity_split = dataentity.strip().split('.')
            num_parts = len(dataentity_split)

            if num_parts == 4:
                # Handles 'db_part1.db_part2.schema.table'
                # Concatenates the first two parts for the database name
                database = f"{dataentity_split[0].strip()}.{dataentity_split[1].strip()}"
                schema = dataentity_split[2].strip()
                table = dataentity_split[3].strip()
            elif num_parts == 3:
                # Handles 'database.schema.table'
                database = dataentity_split[0].strip()
                schema = dataentity_split[1].strip()
                table = dataentity_split[2].strip()
            elif num_parts == 2:
                # Handles 'schema.table'
                schema = dataentity_split[0].strip()
                table = dataentity_split[1].strip()
            elif num_parts == 1:
                # Handles 'table'
                table = dataentity_split[0].strip()

            return database, schema, table
        except Exception as e:
            # In case of an unexpected error (e.g., non-string input)
            print(f"An error occurred: {e}")
            return None, None, None

    def process_update_5th_pattern(self, source_lst, target_lst):
        update_source_lst = []
        update_target_lst = []
        for i in self.update_5th_pattern.finditer(self.content):
            alias = i.group(2).strip()
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            for table_name in i.group(4).strip().split(","):
                if table_name != "":
                    from_table_alias = table_name.strip().split()
                    if alias == from_table_alias[1]:
                        database, schema, table = self.sepreate_schema_table(from_table_alias[0])
                        target_lst.append([self.file, line_number, i.group(1), database, schema, table])
                        update_target_lst.append(from_table_alias[0])
                    else:
                        database, schema, table = self.sepreate_schema_table(from_table_alias[0])
                        source_lst.append([self.file, line_number, 'from', database, schema, table])
                        update_source_lst.append(from_table_alias[0])
        return update_source_lst, update_target_lst

    def process_update_delete_comma_separated(self, source_lst, target_lst):
        update_lst = []
        for i in self.update_delete_comma_separated.finditer(self.content):
            update_table = i.group(2)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            update_lst.append(update_table)
            database, schema, table = self.sepreate_schema_table(update_table)
            target_lst.append([self.file, line_number, i.group(1), database, schema, table])
            self.content = self.content.replace(i.group(0), '')
        return update_lst

    def process_update_pattern(self, source_lst: list, target_lst):
        update_source_lst = []
        update_target_lst = []
        for i in self.update_pattern.finditer(self.content):
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            database, schema, table = self.sepreate_schema_table(i.group(4))
            target_lst.append([self.file, line_number, i.group(1), database, schema, table])
            update_target_lst.append(i.group(4))
            for table_name in i.group(3).strip().split(",")[1:]:
                from_table = table_name.split()[0]
                database, schema, table = self.sepreate_schema_table(from_table)
                source_lst.append([self.file, line_number, 'from', database, schema, table])
                update_source_lst.append(from_table)
            self.content = self.content.replace(i.group(0), '')
        return update_source_lst, update_target_lst

    def process_update_2nd_pattern(self, source_lst, target_lst):
        update_lst = []
        for i in self.update_2nd_pattern.finditer(self.content):
            update_table = i.group(3).split()[0]
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            database, schema, table = self.sepreate_schema_table(update_table)
            update_lst.append(update_table)
            target_lst.append([self.file, line_number, i.group(2), database, schema, table])
            self.content = self.content.replace(i.group(2), '')
        return update_lst

    def process_view_patterns(self, source_lst, target_lst):
        for i in self.re_view.finditer(self.content):
            view_table = i.group(3)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            database, schema, table = self.sepreate_schema_table(view_table)
            target_lst.append([self.file, line_number, 'create_view', database, schema, table])

    def process_update_3nd_pattern(self, source_lst, target_lst):
        update_lst = []
        for i in self.update_3nd_pattern.finditer(self.content):
            update_table = i.group(2)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            temp_source_lst, update_pattern_dict = self.extract_missing_dataentity_from_regex(self.file, self.content)
            if update_pattern_dict.get(update_table):
                update_table = update_pattern_dict[update_table]
            database, schema, table = self.sepreate_schema_table(update_table)
            update_lst.append(update_table)
            target_lst.append([self.file, line_number, i.group(1), database, schema, table])
        return update_lst

    def process_show_table(self, source_lst, target_lst):
        for i in self.show_table.finditer(self.content):
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            database, schema, table = self.sepreate_schema_table(i.group(1))
            source_lst.append([self.file, line_number, 'show_table', database, schema, table])
        return source_lst

    def process_describe_table(self, source_lst, target_lst):
        for i in self.describe.finditer(self.content):
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            database, schema, table = self.sepreate_schema_table(i.group(1))
            source_lst.append([self.file, line_number, 'describe_table', database, schema, table])
        return source_lst

    def process_msck_table(self, source_lst, target_lst):
        for i in self.msck_repair_table.finditer(self.content):
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            database, schema, table = self.sepreate_schema_table(i.group(1))
            source_lst.append([self.file, line_number, 'msck_table', database, schema, table])
        return source_lst

    def process_From_pattern(self, source_lst, target_lst):
        from_lst = []
        for i in self.From_pattern.finditer(self.content):
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            if ',' in i.group(2):
                data = i.group(2).split(",")
                for tablename in data:
                    from_table = tablename.strip().split()[0]
                    from_lst.append(from_table)
                    database, schema, table = self.sepreate_schema_table(from_table)
                    # print(table)
                    source_lst.append([self.file, line_number, 'from', database, schema, table])
            else:
                from_table = i.group(2).strip().split()[0]
                # print(from_table)
                from_lst.append(from_table)
                database, schema, table = self.sepreate_schema_table(from_table)
                print(table)
                source_lst.append([self.file, line_number, 'from', database, schema, table])
        return from_lst

    def process_join_pattern(self, source_lst, target_lst):
        join_lst = []
        for i in self.join_pattern.finditer(self.content):
            join_table = i.group(4)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            join_lst.append(join_table)
            database, schema, table = self.sepreate_schema_table(join_table)
            source_lst.append([self.file, line_number, 'join', database, schema, table])
        return join_lst

    def process_volatile_pattern(self, source_lst, target_lst):
        for i in self.create_volatile_pattern.finditer(self.content):
            volatile_table = i.group(1)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            database, schema, table = self.sepreate_schema_table(volatile_table)
            target_lst.append([self.file, line_number, 'Volatile-table', database, schema, table])

    def process_drop_pattern(self, source_lst, target_lst):
        drop_lst = []
        for i in self.drop_table_patter.finditer(self.content):
            drop_table = i.group(1)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            drop_lst.append(drop_table)
            database, schema, table = self.sepreate_schema_table(drop_table)
            target_lst.append([self.file, line_number, 'drop table', database, schema, table])
        return drop_lst

    def process_merge_pattern(self, source_lst, target_lst):
        merge_table_lst = []
        for i in self.merge_pattern.finditer(self.content):
            merge_table = i.group(1)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            merge_table_lst.append(merge_table)
            database, schema, table = self.sepreate_schema_table(merge_table)
            target_lst.append([self.file, line_number, 'merge', database, schema, table])
        return merge_table_lst

    def process_create_Table_pattern(self, source_lst, target_lst):
        for i in self.create_Table_pattern.finditer(self.content):
            create_table = i.group(1)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            database, schema, table = self.sepreate_schema_table(create_table)
            target_lst.append([self.file, line_number, 'create_table', database, schema, table])

    def process_macro_pattern(self, source_lst, target_lst):
        for i in self.macro_pattern.finditer(self.content):
            macro_table = i.group(1)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            database, schema, table = self.sepreate_schema_table(macro_table)
            target_lst.append([self.file, line_number, 'macro', database, schema, table])

    def process_create_View_pattern(self, source_lst, target_lst):
        for i in self.create_View_pattern.finditer(self.content):
            create_table = i.group(1)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            database, schema, table = self.sepreate_schema_table(create_table)
            target_lst.append([self.file, line_number, 'create_view', database, schema, table])

    def process_create_volatile_view_pattern(self, source_lst, target_lst):
        for i in self.create_volatile_View_pattern.finditer(self.content):
            create_table = i.group(1)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            database, schema, table = self.sepreate_schema_table(create_table)
            target_lst.append([self.file, line_number, 'volatile_view', database, schema, table])

    def process_create_external_table_pattern(self, source_lst, target_lst):
        for i in self.create_External_Table_pattern.finditer(self.content):
            create_table = i.group(1)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            database, schema, table = self.sepreate_schema_table(create_table)
            target_lst.append([self.file, line_number, 'external_table', database, schema, table])

    def process_create_external_view_pattern(self, source_lst, target_lst):
        for i in self.create_External_View_pattern.finditer(self.content):
            create_table = i.group(1)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            database, schema, table = self.sepreate_schema_table(create_table)
            target_lst.append([self.file, line_number, 'external_view', database, schema, table])

    def process_load_data(self, source_lst, target_lst):
        for i in self.load_data.finditer(self.content):
            file = i.group(1)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            database, schema, table = self.sepreate_schema_table(file)
            source_lst.append([self.file, line_number, 'source_load_table', database, schema, table])
        for target_table_match in self.into_table.finditer(self.content):
            target_table = target_table_match.group(1)
            line_number = self.line_offset + self.content.count('\n', 0, target_table_match.start()) + 1
            database, schema, table = self.sepreate_schema_table(target_table)
            target_lst.append([self.file, line_number, 'target_load_table', database, schema, table])

    def process_function_pattern(self, source_lst, target_lst):
        for i in self.function_pattern.finditer(self.content):
            function_name = i.group(1)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            database, schema, table = self.sepreate_schema_table(function_name)
            target_lst.append([self.file, line_number, 'function', database, schema, table])

    def process_function_call_pattern(self):
        for i in self.function_call_pattern.finditer(self.content):
            function_table = i.group(1)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            return function_table, line_number
        return None, None

    def process_package_pattern(self):
        for i in self.package_pattern.finditer(self.content):
            package_table = i.group(2)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            return package_table, line_number
        return None, None

    def process_insert_pattern(self, source_lst, target_lst):
        insert_lst = []
        for i in self.insert_pattern.finditer(self.content):
            insert_table = i.group(1)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            insert_lst.append(insert_table)
            database, schema, table = self.sepreate_schema_table(insert_table)
            target_lst.append([self.file, line_number, 'insert', database, schema, table])
        return insert_lst

    def process_truncate_pattern(self, source_lst, target_lst):
        for i in self.truncate_pattern.finditer(self.content):
            truncate_table = i.group(1)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            database, schema, table = self.sepreate_schema_table(truncate_table)
            target_lst.append([self.file, line_number, 'truncate_table', database, schema, table])

    def process_delete_pattern(self, source_lst, target_lst):
        for i in self.delete_pattern.finditer(self.content):
            delete_table = i.group(2)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            database, schema, table = self.sepreate_schema_table(delete_table)
            target_lst.append([self.file, line_number, 'delete_table', database, schema, table])

    def process_alter_pattern(self, source_lst, target_lst):
        for i in self.alter_pattern.finditer(self.content):
            alter_table = i.group(1)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            database, schema, table = self.sepreate_schema_table(alter_table)
            target_lst.append([self.file, line_number, 'alter', database, schema, table])

    def process_procedure_pattern(self):
        for i in self.re_procedure.finditer(self.content):
            procedure_table = i.group(1)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            return procedure_table, line_number
        return None, None

    def process_macro_pattern_return(self):
        for i in self.re_macro.finditer(self.content):
            macro_table = i.group(2)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            return macro_table, line_number
        return None, None

    def process_view_pattern(self):
        for i in self.re_view.finditer(self.content):
            view_table = i.group(3)
            line_number = self.line_offset + self.content.count('\n', 0, i.start()) + 1
            return view_table, line_number
        return None, None

    def extract_missing_dataentity_from_regex(self, file, content):
        stack = []
        table_list = []
        update_pattern_dict = {}
        for match in re.finditer(r'\(\s*(select|sel)', content, re.IGNORECASE | re.DOTALL):
            start_index = match.start()
            line_number = self.line_offset + content.count('\n', 0, start_index) + 1
            for idx, char in enumerate(content[start_index:], start=start_index):
                if char == '(':
                    stack.append(idx)
                elif char == ')':
                    if stack:
                        stack.pop()
                        if not stack:
                            following_content = content[idx:]
                            second_regex_pattern = re.compile(rf'^\)\s*\w+(\s*,\s*([\w&\.<>\$\#@-]+)(\s+\w+)?)+', flags=re.IGNORECASE)
                            second_match = re.search(second_regex_pattern, following_content)
                            if second_match:
                                second_match_content = second_match.group(0)
                                second_match_content = re.sub(r'\)\s*[\w\.\-]+\s*(,)?', '', second_match_content)
                                if second_match_content:
                                    values = second_match_content.strip().split(',')
                                    for value in values:
                                        table_name_with_alias = value.strip().split()
                                        try:
                                            if len(table_name_with_alias) >= 1:
                                                table_name = table_name_with_alias[0]
                                                database, schema, table = self.sepreate_schema_table(table_name)
                                                table_list.append([file, line_number, 'from', database, schema, table])
                                                if len(table_name_with_alias) == 2:
                                                    alias = table_name_with_alias[1]
                                                    update_pattern_dict[alias] = table_name
                                        except Exception as e:
                                            print(e)
                            break
        return table_list, update_pattern_dict

    def parse_sql(self, source_lst: list, target_lst: list):
        from_table_lst = self.process_From_pattern(source_lst, target_lst)
        # print(source_lst)
        fifth_update_source_lst, fifth_update_target_lst = self.process_update_5th_pattern(source_lst, target_lst)
        update_source_lst, update_target_lst = self.process_update_pattern(source_lst, target_lst)
        second_update_lst = self.process_update_2nd_pattern(source_lst, target_lst)
        third_update_lst = self.process_update_3nd_pattern(source_lst, target_lst)
        update_del_lst = self.process_update_delete_comma_separated(source_lst, target_lst)
        self.process_create_Table_pattern(source_lst, target_lst)
        self.process_macro_pattern(source_lst, target_lst)
        self.process_create_View_pattern(source_lst, target_lst)
        self.process_create_external_table_pattern(source_lst, target_lst)
        self.process_create_external_view_pattern(source_lst, target_lst)
        self.process_create_volatile_view_pattern(source_lst, target_lst)
        insert_pattern_lst = self.process_insert_pattern(source_lst, target_lst)
        self.process_truncate_pattern(source_lst, target_lst)
        merge_pattern_lst = self.process_merge_pattern(source_lst, target_lst)
        join_table_lst = self.process_join_pattern(source_lst, target_lst)
        self.process_delete_pattern(source_lst, target_lst)
        self.process_alter_pattern(source_lst, target_lst)
        self.process_drop_pattern(source_lst, target_lst)
        self.process_load_data(source_lst, target_lst)
        self.process_msck_table(source_lst, target_lst)
        self.process_show_table(source_lst, target_lst)
        self.process_volatile_pattern(source_lst, target_lst)

        stat_table_lst = from_table_lst + join_table_lst + fifth_update_source_lst + update_source_lst
        incoming_entitty_lst = update_target_lst + update_del_lst + fifth_update_target_lst + second_update_lst + third_update_lst + insert_pattern_lst + merge_pattern_lst

        return source_lst, target_lst, stat_table_lst, incoming_entitty_lst
