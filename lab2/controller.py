import model
from model import Model
from view import View


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def run(self):
        while True:
            choice = self.show_menu()
            match choice:
                case '1':
                    self.add_item()
                case '2':
                    self.view_table()
                case '3':
                    self.update_item()
                case '4':
                    self.delete_task()
                case '5':
                    break

    def get_table(self) -> str:
        self.view.show_message("\nSelect table:")
        for index, table_name in enumerate(self.model.tables, start=1):
            self.view.show_message(f"{index}. {table_name}")
        return list(self.model.tables.keys())[int(input("Enter your choice: ")) - 1]

    def get_primary_key(self, table_name) -> (str, int):
        primary_key_name = self.model.tables[table_name].primary_key_name
        if not primary_key_name:
            self.view.show_message("Table has no primary key!")
            return "", -1
        item_id = self.view.get_item_id(primary_key_name)

        if not self.model.check_key_existance(table_name, item_id):
            print("The specified primary key doesn't exist")
            return "", -2
        return primary_key_name, item_id

    def get_foreign_keys(self, table_name):
        foreign_key_names = self.model.tables[table_name].foreign_key_names
        foreign_key_ids = []
        if foreign_key_names:
            foreign_key_ids = self.view.get_foreign_ids(foreign_key_names)
            for index, key in enumerate(foreign_key_ids):
                if not self.model.check_foreign_key_existance(foreign_key_names[index], key):
                    print("One or more foreign keys you entered do not exist.")
                    return []
        return foreign_key_ids

    def get_atributs(self, table_name):
        columns = self.model.tables[table_name].columns
        data_type_formating = self.model.data_type_formats
        column_names = [column.name for column in columns]
        column_data_types = [column.data_type for column in columns]

        return self.view.get_item_input(table_name, column_names, column_data_types, data_type_formating)

    def show_menu(self):
        self.view.show_message("\nMenu:")
        self.view.show_message("1. Add Item")
        self.view.show_message("2. View Table")
        self.view.show_message("3. Update Item")
        self.view.show_message("4. Delete Item")
        self.view.show_message("5. Quit")
        return input("Enter your choice: ")

    def add_item(self):
        table_name = self.get_table()

        foreign_key_ids = []
        if self.model.tables[table_name].foreign_key_names:
            foreign_key_ids = self.get_foreign_keys(table_name)
            if not foreign_key_ids:
                return

        inputs = self.get_atributs(table_name)

        if foreign_key_ids:
            atributes = tuple(foreign_key_ids) + inputs
        else:
            atributes = inputs

        self.model.add_item(table_name, atributes)

        self.view.show_message("Item added successfully!")

    def view_table(self):
        table_name = self.get_table()
        column_names = []
        if self.model.tables[table_name].primary_key_name:
            column_names = [self.model.tables[table_name].primary_key_name]
        for key in self.model.tables[table_name].foreign_key_names:
            column_names.append(key)
        for column_name in [column.name for column in self.model.tables[table_name].columns]:
            column_names.append(column_name)
        rows = self.model.get_all_from_table(table_name)

        self.view.show_rows(rows, column_names, table_name)

    def update_item(self):
        table_name = self.get_table()
        primary_key_name, item_id = self.get_primary_key(table_name)
        if item_id < 0:
            return

        foreign_key_ids = self.get_foreign_keys(table_name)

        inputs = self.get_atributs(table_name)

        if foreign_key_ids:
            atributes = tuple(foreign_key_ids) + inputs
        else:
            atributes = inputs

        self.model.update_item(table_name, atributes, item_id)

        self.view.show_message("Item updated successfully!")

    def delete_task(self):
        table_name = self.get_table()
        primary_key_name, item_id = self.get_primary_key(table_name)
        if item_id < 0:
            return

        self.view.show_message(self.model.delete_item(item_id, primary_key_name, table_name))