import psycopg2 as psycopg2
import table_schemes


class column:
    def __int__(self):
        self.name = ""
        self.data_type = ""


class table:
    def __int__(self):
        self.name = ""
        self.primary_key_name: str = ""
        self.foreign_key_names: list[str] = []
        self.columns: list[column] = []

    def get_data_type(self, column_name: str = "", column_index: int = -1):
        assert (column_name != "") != (column_index != -1), "need to specify either column's name or index!"
        if column_name:
            try:
                return self.columns[[column.name for column in self.columns].index(column_name)].data_type
            except ValueError:
                raise ValueError("The specified column name doesn't exist")
        elif column_index:
            try:
                return self.columns[column_index].data_type
            except IndexError:
                raise IndexError("The specified column index doesn't exist")


class Model:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password=f"{open('./secret', 'r').readlines()[0]}",
            host='localhost',
            port=5432
        )
        self.tables: dict[str, table] = {}
        self.data_type_formats = {}
        self.create_tables()
        self.set_db_table_info()

    def create_tables(self):
        c = self.conn.cursor()

        for table_name, table_defenition in vars(table_schemes).items():
            if table_name.startswith('__') or table_name.endswith('__'):
                continue
            new_table = table()
            new_table.name = table_name
            new_table.columns = []
            self.tables[table_name] = new_table

            c.execute(table_defenition)

            # Check if the table exists
            c.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')")
            table_exists = c.fetchone()[0]

            if not table_exists:
                # Table does not exist, so create it
                c.execute(table_defenition.replace('IF NOT EXISTS ', ''))

        self.data_type_formats["character varying"] = r'.*'
        self.data_type_formats["integer"] = r'^[0-9]+$'
        self.data_type_formats["date"] = r'^\d{4}-\d{2}-\d{2}$'

        self.conn.commit()

    def set_db_table_info(self):
        c = self.conn.cursor()

        for table_name in self.tables.keys():
            c.execute(
                f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE WHERE TABLE_NAME  = N'{table_name}'")
            key = c.fetchall()
            if not key or not key[0]:
                key = ''
            else:
                key = key[0][0]
            self.tables[table_name].primary_key_name = key

            c.execute(
                f"SELECT COLUMN_NAME FROM information_schema.key_column_usage WHERE TABLE_NAME  = N'{table_name}'")
            keys = c.fetchall()
            if key:
                keys.remove((key,))
            normal_keys = []
            for key in keys:
                normal_keys.append(key[0])

            self.tables[table_name].foreign_key_names = normal_keys

            c.execute(
                f"SELECT COLUMN_NAME, DATA_TYPE FROM information_schema.COLUMNS WHERE TABLE_NAME  = N'{table_name}'")
            columns = c.fetchall()

            for column_info in columns:
                if column_info[0] == self.tables[table_name].primary_key_name or column_info[0] in self.tables[table_name].foreign_key_names:
                    continue
                new_column = column()
                new_column.name, new_column.data_type = tuple(column_info)

                self.tables[table_name].columns.append(new_column)

    def check_foreign_key_existance(self, key_name, key_value):
        c = self.conn.cursor()

        c.execute(f"SELECT table_name FROM information_schema.CONSTRAINT_COLUMN_USAGE WHERE column_name='{key_name}'")

        table_name = c.fetchall()
        if not table_name or not table_name[0]:
            return False
        table_name = table_name[0][0]

        c.execute(f'SELECT "{key_name}" FROM "{table_name}"')

        if (key_value,) in c.fetchall():
            return True
        else:
            return False

    def check_key_existance(self, table_name: str, key: int):
        c = self.conn.cursor()

        c.execute(f'SELECT * FROM "{table_name}" WHERE "{self.tables[table_name].primary_key_name}"={key}')

        return True if c.fetchall() != [] else False

    def add_item(self, table_name: str, atributes: tuple):
        column_names = self.tables[table_name].foreign_key_names
        for column_name in [column.name for column in self.tables[table_name].columns]:
            column_names.append(column_name)

        c = self.conn.cursor()
        c.execute(
            f"""INSERT INTO "{table_name}" {str(tuple(column_names)).replace("'", '"')} VALUES {str(('%s',) * len(atributes)).replace("'", '')}""",
            atributes)

        self.conn.commit()

    def get_all_from_table(self, table_name: str):
        c = self.conn.cursor()

        c.execute(f'SELECT * FROM "{table_name}"')

        return c.fetchall()

    def update_item(self, table_name: str, atributes: tuple, item_id: int):
        column_names = [column.name for column in self.tables[table_name].columns]
        primary_key_name = self.tables[table_name].primary_key_name

        c = self.conn.cursor()

        c.execute(
            f"""UPDATE "{table_name}" SET {str(tuple([f'"{column}"=%s' for column in column_names]))[1:-1].replace("'", '')} WHERE "{primary_key_name}"={item_id}""",
            atributes)

        self.conn.commit()

    def delete_item(self, item_id, primary_key_name, table_name):
        c = self.conn.cursor()
        c.execute(f'DELETE FROM "{table_name}" WHERE "{primary_key_name}"={item_id}')
        self.conn.commit()
