class Stats:

    def __init__(self):
        self.access_count = {}  # Dictionary to store access counts
        self.join_degree_count = {}  # Dictionary to store join degree counts
        self.join_degree_value = {}  # Dictionary to store join degree counts
        self.combine_join_count = {}  # Dictionary to store combined join counts
        self.incoming_entities_value = {}  # Dictionary to store incoming entities
        self.incoming_entities_count = {}  # Dictionary to store incoming entities
        self.outgoing_entities_value = {}  # Dictionary to store outgoing entities
        self.outgoing_entities_count = {}  # Dictionary to store outgoing entities

    def driver(self, stat_table_lst, entity_lst):   #
        self.get_access_count(stat_table_lst)
        self.get_join_degree_count(stat_table_lst)
        self.get_combine_join_count(stat_table_lst)
        self.get_join_degree_count_length()
        self.get_incoming_entities_value(stat_table_lst, entity_lst)
        self.get_incoming_entities_count()
        self.get_outgoing_entities_value(stat_table_lst, entity_lst)
        self.get_outgoing_entities_count()

    def get_access_count(self, stat_table_lst):

        for table_name in stat_table_lst:
            if table_name in self.access_count:
                self.access_count[table_name] += 1
            else:
                self.access_count[table_name] = 1

    def get_join_degree_count(self, stat_table_lst):
        for elem in stat_table_lst:
            copy_table_lst = stat_table_lst.copy()
            copy_table_lst.remove(elem)
            if elem in self.join_degree_value:
                self.join_degree_value[elem].update(copy_table_lst)
            else:
                self.join_degree_value[elem] = set(copy_table_lst)

    def get_combine_join_count(self, stat_table_lst):
        for elem in stat_table_lst:
            self.combine_join_count[elem] = self.combine_join_count.get(elem, 0) + len(stat_table_lst) - 1

    def get_join_degree_count_length(self):
        self.join_degree_count = {key: len(value) for key, value in self.join_degree_value.items()}

    def get_incoming_entities_count(self):
        self.incoming_entities_count = {key: len(value) for key, value in self.incoming_entities_value.items()}

    def get_outgoing_entities_count(self):
        self.outgoing_entities_count = {key: len(value) for key, value in self.outgoing_entities_value.items()}

    def get_incoming_entities_value(self, stat_table_lst: list, entities_lst: list):
        for table in entities_lst:
            if table in self.incoming_entities_value:
                self.incoming_entities_value[table].update(stat_table_lst)

            else:
                self.incoming_entities_value[table] = set(stat_table_lst)

    def get_outgoing_entities_value(self, stat_table_lst, entities_lst):
        for table in stat_table_lst:
            if table in self.outgoing_entities_value:
                self.outgoing_entities_value[table].update(entities_lst)

            else:
                self.outgoing_entities_value[table] = set(entities_lst)
