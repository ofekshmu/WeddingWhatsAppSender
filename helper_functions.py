import re
import pandas as pd
import pywhatkit as kit
import time

APPROVAL_EXCEL_FACTORED = r"C:\Users\ofeks\Desktop\approval_excel.xlsx"

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
    def Convert_to_10com(output_filename: str):
        """
        Receives a df in a certain format,
        creates a new excel file with columns A and B
        A - Name
        B - Phone number
        """
        input_df = pd.read_excel(APPROVAL_EXCEL_FACTORED)

        print(f"Before: {len(input_df)}")
        input_df = input_df[input_df['סטטוס הגעה'].isna()]

        print(input_df['מספר'].to_markdown())
        print(f"After: {len(input_df)}")


        # Select columns A and B from the DataFrame
        selected_columns = input_df[['שם בקובץ המקורי', 'מספר']]
        print(selected_columns.to_markdown())
        
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

    @staticmethod
    def Merge_Approvals(df: pd.DataFrame, approval_excel_path: str):
        df_approvals = pd.read_csv(approval_excel_path)
        x = len(df_approvals)
        df_approvals = df_approvals.dropna(subset=['טלפון'])
        df_approvals = df_approvals[df_approvals['האם ברשימה'] != 'נמחק']
        utils.logger(f"removed {x - len(df_approvals)} blank columns")
        #print(df_approvals.to_markdown())
        utils.logger(f"Stats:\ndf length: {len(df)}\n10comm excel length")
        print(df[['מספר']].columns)
        print('test')
        df['מספר'] = df['מספר'].apply(lambda x: '0' + x[4:6] + '-' + x[6:] if x[:4] == '+972' and len(x) == 13\
                                                     else 'BAD NUMBER FORMAT')
        print(df['מספר'].to_markdown())
        merged_df = pd.merge(df[['שם מלא', 'מספר', 'כמות', 'סוג']], 
                             df_approvals[['שם מלא', 'טלפון', 'סטטוס הגעה']], left_on='מספר', right_on='טלפון', how='outer')
        merged_df.drop('טלפון', axis=1, inplace=True)
        merged_df.rename(columns={'שם מלא_x': 'שם בקובץ המקורי', 'שם מלא_y': 'שם כפי שהוזן במערכת אישורי הגעה'}, inplace=True)
        #merged_df = merged_df[merged_df['סטטוס הגעה'] != 'לא ידוע']
        print(merged_df.to_markdown())
        merged_df.to_excel(APPROVAL_EXCEL_FACTORED, index=False)
        
    @staticmethod
    def filter_approval_Excel():
        """_summary_
        """
        
        approval_df = pd.read_excel(APPROVAL_EXCEL_FACTORED)
        initial_values = len(approval_df)
        


        if True:
            approval_df = approval_df[(approval_df['סוג'] == 'צבא -אופק') |
                                      (approval_df['סוג'] == 'חברים לימודים אופק') |
                                      (approval_df['סוג'] == "בצ'אטה")]
            
            approval_df['סטטוס הגעה'] = approval_df['סטטוס הגעה'].astype(str)

            approval_df = approval_df[approval_df['סטטוס הגעה'].str.isdigit() ]

        utils.logger(f"The size of the data frame was reduced by {initial_values - len(approval_df)}\n\
The original size was {initial_values}\n\
The current size in {len(approval_df)}")
        
        print(approval_df.to_markdown())
        
        return approval_df
    
    @staticmethod
    def hebrew_conv(text: str):
        return text[::-1]
  
    @staticmethod
    def send(phone_number, text):

        kit.sendwhatmsg_instantly(phone_number,
                            text,
                            0)
        time.sleep(3)
    
    @staticmethod
    def add_israel_country_code(phone_number):
        """
        This function takes a phone number without a country code and adds Israel's country code (+972) to it.
        
        Parameters:
        phone_number (str): The phone number without the country code.

        Returns:
        str: The phone number with Israel's country code added.
        """
        israel_country_code = "+972"
        
        # Remove any leading zero from the phone number
        if phone_number.startswith("0"):
            phone_number = phone_number[1:]
        
            # Combine the country code with the phone number
            phone_number = israel_country_code + phone_number
        
        return phone_number    
    
    @staticmethod
    def send_broadCastMessage(filtered_df):
        text = f"""היי!
איזה כיף! אישרת הגעה לאירוע שלנו!
פתחנו קבוצת טרמפים עבור מי שאולי מסתבך להגיע וגם עבור מי שיכול לעזור בהגעה,

https://chat.whatsapp.com/EoqStFuFNGDGH0RNMw5cwN"""
        
        for index, row in filtered_df.iterrows():
            phone_number = row['מספר']
            index = row.index
            name = row['שם בקובץ המקורי'] + " | " + row['שם כפי שהוזן במערכת אישורי הגעה']
        
        
            phone_number = utils.add_israel_country_code(phone_number)
            utils.send(phone_number, text)
            utils.logger(f"Message sent to (index, name) = ({index},{utils.hebrew_conv(name)})")

    @staticmethod
    def filter_approval_Excel_for_iplan():

        approval_df = pd.read_excel(APPROVAL_EXCEL_FACTORED)
        initial_values = len(approval_df)
        
        

        if True:
            approval_df['סטטוס הגעה'] = approval_df['סטטוס הגעה'].astype(str)

            approval_df = approval_df[approval_df['סטטוס הגעה'].str.isdigit()]

        approval_df['סטטוס הגעה'] = approval_df['סטטוס הגעה'].astype(int)
        approval_df.drop('כמות', axis=1, inplace=True)

        utils.logger(f"The size of the data frame was reduced by {initial_values - len(approval_df)}\n\
The original size was {initial_values}\n\
The current size in {len(approval_df)}\n\
Guests sum is: {approval_df['סטטוס הגעה'].sum()}")
        
        from datetime import datetime

        # Get the current date and time
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Add the current date and time to the file name
        date = f"_{current_time}"
        approval_df.to_excel(r"C:\Users\ofeks\OneDrive\Temporary\Whatsapp sender\outputs\iPlanGuests_" + date + ".xls", index=False, header=False, engine='openpyxl')