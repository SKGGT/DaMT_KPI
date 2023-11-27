from re import match
import datetime


class View:
    @staticmethod
    def show_rows(table_name: str, rows: list[str]):
        print(f"{table_name}:")
        for row in rows:
            for index, column in enumerate(row):
                print(f"{column}")

    @staticmethod
    def get_item_input(table_name, column_names, data_type_names, data_type_formating):
        def validate_date(date_string):
            try:
                datetime.date.fromisoformat(date_string)
                return True
            except ValueError:
                print("Incorrect data format, should be YYYY-MM-DD")
                return False

        inputs = []

        for i, column in enumerate(column_names, start=0):
            while True:
                input_string = input(f"Enter {table_name} {column}: ")

                if data_type_names[i] == 'DATE' and not validate_date(input_string):
                    input_string = ""

                if match(data_type_formating[data_type_names[i]], input_string) is None:
                    if data_type_names[i] != 'DATE':
                        print(
                            f"The value you entered doesn't conform to the column's data type '{data_type_names[i]}'!")
                    continue
                break

            if not input_string.isnumeric():
                inputs.append(input_string)
            else:
                inputs.append(int(input_string))

        return tuple(inputs)

    @staticmethod
    def get_item_id(key_name) -> int:
        return int(input(f"Enter {key_name}: "))

    @staticmethod
    def get_foreign_ids(key_names) -> list[int]:
        print("Enter foreign keys:")
        inputs = []
        for key_name in key_names:
            while True:
                input_string = input(f"Enter {key_name}: ")
                if not input_string.isnumeric():
                    print("The key's value has to be an integer")
                    continue
                inputs.append(int(input_string))
                break
        return inputs

    @staticmethod
    def get_simple_input(prompt: str) -> str:
        return input(prompt)

    @staticmethod
    def show_message(message):
        print(message)
