# pip install pywhatkit
import pywhatkit as kit
import pandas as pd
import time
from helper_functions import utils

CONTACTS_EXCEL_PATH = r"C:\Users\ofeks\OneDrive\Documents\Contacts for Wedding.xlsx"
EXCEL_SHEET_NAME = "Contacts - Ilanit"

SINGLE_SHEET = False

CONTACTS_10COMM_PATH = r"C:\Users\ofeks\Desktop\Contacts_10comm_format.xlsx"

APPROVAL_EXCEL_10COMM_PATH = r"C:\Users\ofeks\Downloads\list_05-09-2024_20_29.csv"

SEND_IMAGE = False
WEDDING_INV_PATH = r"C:\Users\ofeks\OneDrive\Temporary\Wedding invitation\Final_Wedding_Invitation.png"
HENNA_INV_PATH = r"C:\Users\ofeks\OneDrive\Temporary\Hina Invitation\Hina Invitation.png"

IGNORE_SENDER = True
SENDER = "יובל"


MESSAGE_TEST_TEXT = ""

# message type
is_approval_link_msg = False

# This should fit the row index in the excel file up to where messages should be sent...
# 1000 =~ infinity

test_case = 1000
SKIP_VALUE = 0

def logger(text: str):
    print(text)
    f = open("logger.txt", 'a', encoding="utf-8")
    f.write(text + "\n")
    f.close()

def read_excel_file(input_path: str):
    try:
        if SINGLE_SHEET:
            df = pd.read_excel(input_path, sheet_name=EXCEL_SHEET_NAME)
            return df
        else:
            #excel_file = pd.ExcelFile(CONTACTS_EXCEL_PATH)

            # List to store all DataFrames
            df_list = []
            label_list = ["Contacts - Ofek",\
                          "Contacts - Yuval's Parents",\
                          "Contacts - Gal",\
                          "Contacts - Alon",\
                          "Contacts - Ilanit",\
                          "Contacts - Yuval"]

            # Iterate over each sheet name (label) and create a DataFrame
            for label in label_list:
                df = pd.read_excel(CONTACTS_EXCEL_PATH, sheet_name=label)
                df_list.append(df)

            return pd.concat(df_list, ignore_index=True)


    except Exception as e:
        logger(f"There was a problem reading the excel file...\n error was: {e}")
        raise Exception
    
def send(phone_number, text):

    #kit.sendwhatmsg_instantly(phone_number, message)
    if SEND_IMAGE:
        kit.sendwhats_image(phone_number,
                            WEDDING_INV_PATH,
                            text)
    else:
        kit.sendwhatmsg_instantly(phone_number,
                            text,
                            0)
    time.sleep(3)


def create_msg(name: str, amount: int, nickname: str):
    if not pd.isnull(nickname):
         name = nickname

    # remove trailing spaces from name:
    name = utils.remove_trailing_spaces(name)

    if amount > 1:
        initial = f"{name} היקרים!"
        formality = "שהוזמנתם"
        formality2 = "לראותכם!"
    else:                           # One person invitation
        initial = f"היי {name}!"
        formality = "שהוזמנת"
        formality2 = "לראותך!"

    msg_txt = f"""{initial}! אנחנו רק מזכירים {formality} לחתונה של יובל ואופק בתאריך 8/9/24 ביום ראשון. 
לחצ/י על הקישור לצפייה בהזמנה ואישור הגעה. 
https://10comm.com/Invitation.php?token=8gsmZmrK 

נשמח {formality2}"""
    
    return msg_txt

def iter_df(df: pd.DataFrame):

    for row in df.itertuples(name=None):
        print(row)
        index, \
            name, \
            phone_number, \
            amount, \
            nickname, \
            group, \
            sender, \
            send_approval_link_msg, \
            active, \
            more_info \
                = row

        # to match excel rows
        index = index + 2
        
        if active == SKIP_VALUE or index < 57:
            logger(f"Skipped (index, name) = ({index},{utils.hebrew_conv(name)}) becuase of reserved status.")
            continue

        # safety procution 
        if index > test_case:
            logger("Test case reached, run ended")
            break

        if not IGNORE_SENDER:
            if sender != SENDER:
                logger(f"skipped (index, name) = ({index},{utils.hebrew_conv(name)}) because the sender did not match current sender.")
                continue    


        if send_approval_link_msg == "לא":
            logger(f"skipped (index, name) = ({index},{utils.hebrew_conv(name)}) because thi should not receive approval link message.")
            continue

        elif send_approval_link_msg == "כן":
            text = create_msg(name, amount, nickname)
        else:
            raise ValueError(f"Unkown value - {send_approval_link_msg} for the following (index, name) = ({index},{name}).")


        phone_number = utils.add_israel_country_code(phone_number)
        send(phone_number, text)
        logger(f"Message sent to (index, name) = ({index},{utils.hebrew_conv(name)})")

def validate(df):
    """
    Checks that all numbers are in a valid string format
    """    
    # Apply the condition to check if each entry in 'מספר' is a string
    is_string = df['מספר'].apply(lambda x: isinstance(x, str))

    # Print the markdown of the entire condition check
    # print(is_string.to_markdown())

    # Filter rows where the condition is False
    false_rows = df[~is_string]

    # Print the rows where 'מספר' is not a string
    if not false_rows.empty:
        print("Rows where 'מספר' is not a string:")
        print(false_rows[['שם מלא','מספר','סוג','שולח את האסמאמס', 'שורה פעילה']].to_markdown())
    else:
        print("All rows in 'מספר' are strings.")

    # Return whether all rows in 'מספר' are strings
    return is_string.all()

def remove_carriage(df, column_name):
    """
    removes excesive spaces...
    """
    df[column_name] = df[column_name].str.replace('_x000D_', '', regex=False)
    return df

def print_df_stats(df: pd.DataFrame):
    total_rows = df.shape[0]
    print(f"Total number of rows: {total_rows}")

    # Calculate the sum of the 'כמות' column
    total_quantity_sum = df['כמות'].sum()
    print(f"Sum of the column 'כמות': {total_quantity_sum}")

if __name__ =="__main__":


    df = read_excel_file(CONTACTS_EXCEL_PATH)

    if not validate(df):
        raise ValueError("Not all numbers are in a string format...")

    utils.remove_duplicate_phone_numbers(df, "מספר")
    df = utils.drop_duplicates(df)  
    
    df = remove_carriage(df, 'מספר')
    df = remove_carriage(df, 'אישורי הגעה')

    print_df_stats(df)

    df = df[(df['שורה פעילה'] == 1) & (df['אישורי הגעה'] == 'כן')]
    
    print_df_stats(df)
    #print(df.columns)
    #print(df['מספר'].to_markdown())
    res = utils.template_menu(["Send Messages",
                               "Convert Contacts excel to 10comm format",
                               "Create approval Excel",
                               "Broadcast a message",
                               "Create an excel for iPLAN format"], "Select an option:")
    match res:
        case 0:
            iter_df(df)
        case 1:
            utils.Convert_to_10com(CONTACTS_10COMM_PATH)
        case 2:
            utils.Merge_Approvals(df, APPROVAL_EXCEL_10COMM_PATH)
        case 3:
            filtered_df = utils.filter_approval_Excel()
            utils.send_broadCastMessage(filtered_df)
        case 4:
            utils.filter_approval_Excel_for_iplan()
        case _:
            raise ValueError("Check menu for errors...")
        

        