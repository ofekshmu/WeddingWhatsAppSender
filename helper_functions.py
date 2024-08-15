import re

class utils:

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
            print(duplicates[['שם מלא','מספר']])
        else:
            print("No duplicates found.")
        
        # Drop duplicates based on the normalized phone number
        return df.drop_duplicates(subset='מספר')