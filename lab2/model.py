import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker, Mapper
from sqlalchemy import create_engine
from table_schemes import Base
import table_schemes
from sqlalchemy import exc

class RefColumn:
    def __int__(self):
        self.name = ""
        self.data_type = ""


class RefTable:
    def __int__(self):
        self.tableRefrece = None
        self.name = ""
        self.primary_key_name: str = ""
        self.foreign_key_names: list[str] = []
        self.columns: list[RefColumn] = []


class Model:
    def __init__(self):

        self.engine = create_engine(f"postgresql+psycopg2://postgres:{open('./secret', 'r').readlines()[0]}@localhost:5432/pyexample")
        self.session = sessionmaker(bind=self.engine)

        self.tables: dict[str, RefTable] = {}
        self.data_type_formats = {}
        self.create_tables()
        self.set_db_table_info()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

        for table_name, table_defenition in vars(table_schemes).items():

            if table_name.startswith('__') or table_name.endswith('__'):
                continue
            if type(table_defenition) is not sqlalchemy.orm.decl_api.DeclarativeAttributeIntercept:
                continue
            if table_name.count("Base") > 0:
                continue

            new_table = RefTable()
            new_table.name = table_name
            new_table.tableRefrece = table_defenition
            new_table.columns = []
            self.tables[table_name] = new_table

        self.data_type_formats["VARCHAR"] = r'.*'
        self.data_type_formats["INTEGER"] = r'^[0-9]+$'
        self.data_type_formats["DATE"] = r'^\d{4}-\d{2}-\d{2}$'

    def set_db_table_info(self):
        for table_name in self.tables.keys():
            mapper: Mapper = inspect(self.tables[table_name].tableRefrece)
            try:
                self.tables[table_name].primary_key_name = [column for column in mapper.columns if column.primary_key and not column.foreign_keys][0].name
            except IndexError:
                self.tables[table_name].primary_key_name = ""

            self.tables[table_name].foreign_key_names = [column.name.split('_')[-1] for column in mapper.columns if column.foreign_keys]

            for column in mapper.columns:
                if column.name is self.tables[table_name].primary_key_name or column.name.split('_')[-1] in self.tables[table_name].foreign_key_names:
                    continue
                new_column = RefColumn()
                new_column.name = column.name
                new_column.data_type = column.type

                self.tables[table_name].columns.append(new_column)

    def check_foreign_key_existance(self, key_name: str, key_value: int):
        r = []
        for table_name, table_info in self.tables.items():
            if table_info.primary_key_name != key_name:
                continue
            table = self.tables[table_name].tableRefrece

            mapper: Mapper = inspect(table)

            s = self.session()

            r = s.execute(s.query(mapper.primary_key[0])).all()

            s.close()

            break

        if (key_value,) in r:
            return True
        else:
            return False

    def check_key_existance(self, table, key: int):
        s = self.session()

        r = s.get(table, key)

        s.close()

        return False if r is None else True

    def add_item(self, table, atributes: tuple):
        s = self.session()

        new_item = table(*atributes)
        s.add(new_item)

        s.commit()
        s.close()

    def get_all_from_table(self, table):
        s = self.session()

        r = s.execute(s.query(table).limit(20))

        s.close()

        return r.all()

    def update_item(self, table, atributes: tuple, item_id: int):
        s = self.session()

        item = s.get(table, item_id)

        for index, colum in enumerate(self.tables[table.__tablename__].columns):
            setattr(item, colum.name, atributes[index])

        s.commit()
        s.close()

    def delete_item(self, table, item_id: int, primary_key_name: str):
        s = self.session()

        item = s.get(table, item_id)

        s.delete(item)
        try:
            s.commit()
        except (exc.IntegrityError, AssertionError):
            s.close()
            return f"Foreign key constraint violated! \nUnable to delete {table.__tablename__}:{primary_key_name}:{item_id}"
        s.close()
        return "Item deleted successfully!"
