from model import Model, RefTable
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

    def get_table(self) -> RefTable:
        self.view.show_message("\nSelect table:")
        for index, table_name in enumerate(self.model.tables, start=1):
            self.view.show_message(f"{index}. {table_name}")
        return self.model.tables[list(self.model.tables.keys())[int(self.view.get_simple_input("Enter your choice: ")) - 1]]

    def get_primary_key(self, table: RefTable) -> (str, int):
        primary_key_name = table.primary_key_name
        if not primary_key_name:
            self.view.show_message("Table has no primary key!")
            return "", -1
        item_id = self.view.get_item_id(primary_key_name)

        if not self.model.check_key_existance(table.tableRefrece, item_id):
            print("The specified primary key doesn't exist")
            return "", -2
        return primary_key_name, item_id

    def get_foreign_keys(self, table: RefTable):
        foreign_key_names = table.foreign_key_names
        foreign_key_ids = []
        if foreign_key_names:
            foreign_key_ids = self.view.get_foreign_ids(foreign_key_names)
            for index, key in enumerate(foreign_key_ids):
                if not self.model.check_foreign_key_existance(foreign_key_names[index], key):
                    print("One or more foreign keys you entered do not exist.")
                    return []
        return foreign_key_ids

    def get_atributs(self, table: RefTable):
        columns = table.columns
        data_type_formating = self.model.data_type_formats
        column_names = [column.name for column in columns]
        column_data_types = [str(column.data_type) for column in columns]

        return self.view.get_item_input(table.name, column_names, column_data_types, data_type_formating)

    def show_menu(self):
        self.view.show_message("\nMenu:")
        self.view.show_message("1. Add Item")
        self.view.show_message("2. View Table")
        self.view.show_message("3. Update Item")
        self.view.show_message("4. Delete Item")
        self.view.show_message("5. Quit")
        return self.view.get_simple_input("Enter your choice: ")

    def add_item(self):
        table: RefTable = self.get_table()

        foreign_key_ids = []
        if table.foreign_key_names:
            foreign_key_ids = self.get_foreign_keys(table)
            if not foreign_key_ids:
                return

        inputs = self.get_atributs(table)

        if foreign_key_ids:
            atributes = tuple(foreign_key_ids) + inputs
        else:
            atributes = inputs

        self.model.add_item(table.tableRefrece, atributes)

        self.view.show_message("Item added successfully!")

    def view_table(self):
        table: RefTable = self.get_table()
        column_names = []
        if table.primary_key_name:
            column_names = [table.primary_key_name]
        if table.foreign_key_names:
            column_names.extend(table.foreign_key_names)
        for column in table.columns:
            column_names.append(column.name)
        rows = self.model.get_all_from_table(table.tableRefrece)

        self.view.show_rows(table.name, rows)

    def update_item(self):
        table: RefTable = self.get_table()
        primary_key_name, item_id = self.get_primary_key(table)
        if item_id < 0:
            return

        foreign_key_ids = self.get_foreign_keys(table)

        inputs = self.get_atributs(table)

        if foreign_key_ids:
            atributes = tuple(foreign_key_ids) + inputs
        else:
            atributes = inputs

        self.model.update_item(table.tableRefrece, atributes, item_id)

        self.view.show_message("Item updated successfully!")

    def delete_task(self):
        table: RefTable = self.get_table()
        primary_key_name, item_id = self.get_primary_key(table)
        if item_id < 0:
            return

        self.view.show_message(self.model.delete_item(table.tableRefrece, item_id, primary_key_name))
