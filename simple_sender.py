# pip install pywhatkit
import pywhatkit as kit
import pandas as pd
import time
from helper_functions import utils

CONTACTS_EXCEL_PATH = r"C:\Users\ofeks\OneDrive\Documents\Contacts for Wedding.xlsx"
EXCEL_SHEET_NAME = "Contacts - Henna"

CONTACTS_10COMM_PATH = r"C:\Users\ofeks\Desktop\Contacts_10comm_format.xlsx"

SEND_IMAGE = False
WEDDING_INV_PATH = r"C:\Users\ofeks\OneDrive\Temporary\Wedding invitation\Final_Wedding_Invitation.png"
HENNA_INV_PATH = r"C:\Users\ofeks\OneDrive\Temporary\Hina Invitation\Hina Invitation.png"

IGNORE_SENDER = False
SENDER = "יובל"

MESSAGE_TEST_TEXT = ""

# message type
is_approval_link_msg = False

# This should fit the row index in the excel file up to where messages should be sent...
# 1000 =~ infinity

test_case = 1000
SKIP_VALUE = 0


def hebrew_conv(text: str):
    return text[::-1]

def logger(text: str):
    print(text)
    f = open("logger.txt", 'a', encoding="utf-8")
    f.write(text + "\n")
    f.close()

def read_excel_file(input_path: str):
    try:
        df = pd.read_excel(input_path, sheet_name=EXCEL_SHEET_NAME)
        return df
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
        kit.sendwhats_image(phone_number,
                            text)
    time.sleep(3)

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

def create_msg(name: str, amount: int, nickname: str):
    if not pd.isnull(nickname):
         name = nickname

    # remove trailing spaces from name:
    name = utils.remove_trailing_spaces(name)

    if amount > 1:
        initial = f"{name} היקרים!"
        formality = "שהוזמנתם"
    else:                           # One person invitation
        initial = f"היי {name}!"
        formality = "שהוזמנת"

    MESSAGE_TEXT = f"""{initial}! אנחנו רק מזכירים {formality} לחתונה של יובל ואופק. 
                    לצפייה בהזמנה ואישור הגעה לאירוע לחצו על הלינק הבא. 
                    https://10comm.com/Invitation.php?token=8gsmZmrK 

                    אל דאגה! במידה ומשהו ישתנה תוכלו לעדכן אותנו שוב בקישור."""
    
    return MESSAGE_TEXT

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
        
        if active == SKIP_VALUE:
            logger(f"Skipped (index, name) = ({index},{hebrew_conv(name)}) becuase of reserved status.")
            continue

        # safety procution 
        if index > test_case:
            logger("Test case reached, run ended")
            break

        if not IGNORE_SENDER:
            if sender != SENDER:
                logger(f"skipped (index, name) = ({index},{hebrew_conv(name)}) because the sender did not match current sender.")
                continue    


        if send_approval_link_msg == "לא":
            logger(f"skipped (index, name) = ({index},{hebrew_conv(name)}) because thi should not receive approval link message.")
            continue

        elif send_approval_link_msg == "כן":
            text = create_msg(name, amount, nickname)
        else:
            raise ValueError(f"Unkown value - {send_approval_link_msg} for the following (index, name) = ({index},{name}).")


        phone_number = add_israel_country_code(phone_number)
        send(phone_number, text)
        logger(f"Message sent to (index, name) = ({index},{hebrew_conv(name)})")

def validate(df):
    """
    Checks that all numbers are in a valid string format
    """
    x = df['מספר'].apply(lambda x: isinstance(x, str))
    #print(x.to_markdown())
    return df['מספר'].apply(lambda x: isinstance(x, str)).all()

def remove_carriage(df):
    """
    removes excesive spaces...
    """
    df['מספר'] = df['מספר'].str.replace('_x000D_', '', regex=False)
    return df

if __name__ =="__main__":


    df = read_excel_file(CONTACTS_EXCEL_PATH)
    utils.remove_duplicate_phone_numbers(df, "מספר")
    df = utils.drop_duplicates(df)  

    if not validate(df):
        raise ValueError("Not all numbers are in a string format...")
    
    df = remove_carriage(df)

    res = utils.template_menu(["Send Messages",
                               "Convert Contacts excel to 10comm format"], "Select an option:")
    match res:
        case 0:
            iter_df(df)
        case 1:
            utils.Convert_to_10com(df, CONTACTS_10COMM_PATH)
        case _:
            raise ValueError("Check menu for errors...")