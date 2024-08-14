# pip install pywhatkit
import pywhatkit as kit
import pandas as pd
import time
from helper_functions import utils

input_path = r"C:\Users\ofeks\OneDrive\Documents\Contacts for Wedding.xlsx"
image_path = r"C:\Users\ofeks\OneDrive\Temporary\Wedding invitation\Final_Wedding_Invitation.png"
sheet_name = "Contacts - Ilanit"
current_sender = "אילנית"

# message type
is_approval_link_msg = False

# leave it as "" in operational mode
test_text = ""
#"נבחרתם להיות בקבוצת המדגם של הזמנת החתונה שלנו!, הזמנה זו נשלחה כדי לבדוק את תקינות מנגנון השליחה שלנו, לאחר סיום והצלחת הבדיקה, תקבלו אחת נוספת.. \n"

# This should fit the row index in the excel file up to where messages should be sent...
# 1000 =~ infinity

test_case = 1000
RESERVED_INDICATION = 0


def hebrew_conv(text: str):
    return text[::-1]

def logger(text: str):
    print(text)
    f = open("logger.txt", 'a', encoding="utf-8")
    f.write(text + "\n")
    f.close()

def read_excel_file():
    try:
        df = pd.read_excel(input_path, sheet_name=sheet_name)
        return df
    except Exception as e:
        logger(f"There was a problem reading the excel file...\n error was: {e}")
        raise Exception
    
def send(phone_number, text):

    #kit.sendwhatmsg_instantly(phone_number, message)
    kit.sendwhats_image(phone_number,
                        image_path,
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

def create_msg(name: str, amount: int, nickname: str, is_approval_link_msg: bool):
    if not pd.isnull(nickname):
         name = nickname

    # remove trailing spaces from name:
    name = utils.remove_trailing_spaces(name)

    if is_approval_link_msg:
        #TODO: degine the approval message
        text = test_text + 'משפחה וחברים יקרים! הנכם מוזמנים לחתונה של יובל ואופק. לצפייה בהזמנה ואישור הגעה לאירוע לחצו על הלינק הבא.  https://10comm.com/Invitation.php?token=8gsmZmrK'
        text = 'test_msg'
    else:

        if amount > 1:
            intro = f"{name} היקרים!"
            first_counter = "להזמינכם"
            second_counter = "לראותכם"
        else:
            intro = f"היי {name}!"
            first_counter = "להזמינך"
            second_counter = "לראותך"


        text = test_text + f"{intro}\nאנו מתרגשים {first_counter} לאירוע החתונה שלנו שייערך בתאריך ה-08.09.24 בכפר אירועים 'קולוניה', רחובות. \nנשמח {second_counter}!"

    return text


def iter_df(df: pd.DataFrame):

    for row in df.itertuples(name=None):
        print(row)
        index, name, phone_number, amount, nickname, type, sender, send_approval_link_msg, reserved = row

        # to match excel rows
        index = index + 2
        
        if reserved == RESERVED_INDICATION:
            logger(f"Skipped (index, name) = ({index},{hebrew_conv(name)}) becuase of reserved status.")
            continue

        # safety procution 
        if index > test_case:
            logger("Test case reached, run ended")
            break

        if sender != current_sender:
            logger(f"skipped (index, name) = ({index},{hebrew_conv(name)}) because the sender did not match current sender.")
            continue

        if is_approval_link_msg:
            # message will be changed
            # only prticipants with the relevant config will receive it
            if send_approval_link_msg == "לא":
                logger(f"skipped (index, name) = ({index},{hebrew_conv(name)}) because thi should not receive approval link message.")
                continue

            elif send_approval_link_msg == "כן":
                text = create_msg(name, amount, nickname, is_approval_link_msg)
            else:
                raise ValueError(f"Unkown value - {send_approval_link_msg} for the following (index, name) = ({index},{name}).")
        else:
            text = create_msg(name, amount, nickname, is_approval_link_msg)

        phone_number = add_israel_country_code(phone_number)
        send(phone_number,text)
        logger(f"Message sent to (index, name) = ({index},{hebrew_conv(name)})")

def validate(df):
    """
    
    """
    x = df['מספר'].apply(lambda x: isinstance(x, str))
    print(x.to_markdown())
    return df['מספר'].apply(lambda x: isinstance(x, str)).all()

def remove_carriage(df):
    df['מספר'] = df['מספר'].str.replace('_x000D_', '', regex=False)
    return df

if __name__ =="__main__":
    df = read_excel_file()
    print(df.to_markdown())
    #print(df.columns)
    if not validate(df):
        raise ValueError("Not all numbers are in a string format...")
    
    df = remove_carriage(df)
    #print(df.to_markdown())

    iter_df(df)