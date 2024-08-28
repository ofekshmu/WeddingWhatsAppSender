import re
import pandas as pd

class utils:

    @staticmethod
    def logger(text: str):
        print(text)
        f = open("logger.txt", 'a', encoding="utf-8")
        f.write(text + "\n")
        f.close()

    @staticmethod
    def remove_trailing_spaces(st: str) -> str:
        initial_val = st
        if st[-1] == " ":
            return utils.remove_trailing_spaces(st[:-1])
        if st[0] == " ":
            return utils.remove_trailing_spaces(st[1:])
        if len(st) == 0:
            raise ValueError(f"Something is wrong with either the function of the input: initial value is ({initial_val})")
        return st

# print(utils.remove_trailing_spaces("12 1234 14 4") == "12 1234 14 4")
# print(utils.remove_trailing_spaces("12 1234 14 ") == "12 1234 14")
# print(utils.remove_trailing_spaces("   1234 14 4") == "1234 14 4")
# print(utils.remove_trailing_spaces(" 12 1234       ") == "12 1234")
# print(utils.remove_trailing_spaces(" אילנית") == "אילנית")


    @staticmethod
    def normalize_to_international(phone_number):
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone_number)
        
        # Check if the number starts with the Israeli country code (972)
        if digits.startswith('972'):
            return f'+{digits}'
        elif digits.startswith('0'):
            # Local number, assume Israeli and convert to international format
            return f'+972{digits[1:]}'
        else:
            # If it does not start with '0' or '972', assume it's already in international format
            # Add international prefix if necessary, e.g., + or leading '0'
            raise ValueError("This case should not happen")
            return f'+{digits}'
    
    @staticmethod
    def remove_duplicate_phone_numbers(df, phone_column):
        # Normalize the phone numbers
        df[phone_column] = df[phone_column].apply(utils.normalize_to_international)
        
        
    @staticmethod
    def drop_duplicates(df):
        # Identify duplicates
        duplicates = df[df.duplicated(subset='מספר', keep=False)]
        
        # Print the duplicates
        if not duplicates.empty:
            print("Dropped duplicates:")
            print(duplicates[['שם מלא','מספר','שולח את האסמאמס']])
        else:
            print("No duplicates found.")
        
        # Drop duplicates based on the normalized phone number
        return df.drop_duplicates(subset='מספר')
    
    @staticmethod
    def Convert_to_10com(df: pd.DataFrame, output_filename: str):
        """
        Receives a df in a certain format,
        creates a new excel file with columns A and B
        A - Name
        B - Phone number
        """
        # Select columns A and B from the DataFrame
        selected_columns = df[['כינוי', 'מספר']]
        
        # Write the selected columns to a new Excel file
        selected_columns.to_excel(output_filename, index=False)
        utils.logger(f"Done!\nFile saved here: {output_filename}")

    @staticmethod
    def template_menu(options: list[str], msg: str = "Choose one of the following:\n", sort: bool = False) -> int:
        """
        The function creates a template menu that is printed out for the user.
        Inputs are @options - a list of strings containing different options.
                   @msg - str with a menu message
        return a numbers from 0 to len(options) - 1 representing the chosen option.
        if input does not match a valid option, the function asks for a valid one.
        """
        if sort:
            options = sorted(options)

        utils.logger(msg + '\n')
        utils.pretty_print([f"{str(i) + ' -> ':6s}{x}" for i, x in enumerate(options, start=0)])

        while True:
            x = input()
            if not x.isnumeric():
                continue
            x = int(x)
            if x < 0 or x >= len(options):
                continue
            return x
        
    @staticmethod
    def pretty_print(lst: list, const: int = 6) -> None:
        """
        The function prints the given list in a rectangle shaped pattern.
        The elements are indexed from 0 to n - 1.
        The rectangle is set to have a maximun of @const elements per column.
        """
        n = len(lst)
        m = 1 + n // const
        for i in range(0, const):
            for j in range(0, m):
                index = i + const*j
                if index >= len(lst):
                    break
                print(f"{lst[i + const*j]:27s}", end="")
            print()