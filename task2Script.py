import pandas as pd
from datetime import datetime

filePath = './Humidity Dataset.csv'

def main():
    # ensure RowID's are consistent
    print("Checking column: RowID")
    check_RowID()
    print("Done")

    # ensure stamp values are consistent
    print("Checking column: stamp")
    check_stamp()
    print("Done")

    # ensure datetime values are consistent
    print("Checking column: datetime")
    check_datetime()
    print("Done")

    # ensure hum values are consistent
    print("Checking column: hum")
    check_hum()
    print("Done")


# function to check if value is decimal
def check_decimal(dec):
    try:
        float(dec)
    except ValueError:
        return False
    if float(dec) == 0:
        return False
    return True

# function to check if value is integer
def check_int(num):
    try:
        int(num)
    except ValueError:
        return False
    if int(num) == 0:
        return False
    return True

# function to check if value is in datetime format
def check_time(var):
    try:
        datetime.strptime(var, '%Y/%m/%d %H:%M:%S')
    except ValueError:
        return False
    return True

def check_RowID():
    # check rowID values are unique integers (will also find missing rows)
    df = pd.read_csv(filePath) # reload csv

    errors = {"valueError":{}, "duplicate":{}}
    testList = []
    # find errors
    for index, val in enumerate(df['rowID']):
        i = index + 2 # nessesary because index starts from 0 refering to Spreadsheet software row 2, meaning that the indexes here are 2 less than in the spreadsheet software
        if val in testList:
            errors["duplicate"][i] = val
        if not check_int(val):
            errors["valueError"][i] = val
        testList.append(val)
    # case if no errors
    if len(errors["duplicate"]) == 0 and len(errors["valueError"]) == 0:
        return
    else:
        # print value errors
        if len(errors["valueError"]) > 0:
            print("RowID Value errors:")
            for error in errors["valueError"]:
                print(f"Row: {error}, Value: {errors['valueError'][error]}")
        # print duplicate value errors
        if len(errors["duplicate"]) > 0:
            print("RowID Value errors:")
            for error in errors["duplicate"]:
                print(f"Row: {error}, Value: {errors['duplicate'][error]}")
        print("Please first fix these errors")
        input("Then press Enter to continue...")
        check_RowID() # Ensure errors are fixed before continuing

def check_stamp():
    # check stamp values are all integers
    df = pd.read_csv(filePath) # reload csv
    errors = {"valueError":{}}
    # find errors
    for index, val in enumerate(df['stamp']):
        i = index + 2 # nessesary because index starts from 0 refering to Spreadsheet software row 2, meaning that the indexes here are 2 less than in the spreadsheet software
        if not check_int(val):
            errors["valueError"][i] = val
    # case if no errors
    if len(errors["valueError"]) == 0:
        return
    else:
        # print value errors
        if len(errors["valueError"]) > 0:
            print("stamp Value errors:")
            for error in errors["valueError"]:
                print(f"Row: {error}, Value: {errors['valueError'][error]}")
        print("Please first fix these errors")
        input("Then press Enter to continue...")
        check_stamp() # Ensure errors are fixed before continuing

def check_datetime():
    # check datetime values are consecutive time values in correct format
    df = pd.read_csv(filePath) # reload csv
    errors = {"valueError":{}}
    # find errors
    for index, val in enumerate(df['datetime']):
        i = index + 2 # nessesary because index starts from 0 refering to Spreadsheet software row 2, meaning that the indexes here are 2 less than in the spreadsheet software
        val = val.lstrip(' ') # remove white space at beggining
        if not check_time(str(val)):
            errors["valueError"][i] = val
    # case if no errors
    if len(errors["valueError"]) == 0:
        return
    else:
        # print value errors
        if len(errors["valueError"]) > 0:
            print("datetime Value errors:")
            for error in errors["valueError"]:
                print(f"Row: {error}, Value: {errors['valueError'][error]}")
        print("Please first fix these errors")
        input("Then press Enter to continue...")
        check_datetime() # Ensure errors are fixed before continuing

def check_hum():
    #  check hum vales are decimals (1dp)
    df = pd.read_csv(filePath) # reload csv
    errors = {"valueError":{}}
    # find errors
    for index, val in enumerate(df['hum']):
        i = index + 2 # nessesary because index starts from 0 refering to Spreadsheet software row 2, meaning that the indexes here are 2 less than in the spreadsheet software
        if not check_decimal(val):
            errors["valueError"][i] = val
    # case if no errors
    if len(errors["valueError"]) == 0:
        return
    else:
        # print value errors
        if len(errors["valueError"]) > 0:
            print("hum Value errors:")
            for error in errors["valueError"]:
                print(f"Row: {error}, Value: {errors['valueError'][error]}")
        print("Please first fix these errors")
        input("Then press Enter to continue...")
        check_hum() # Ensure errors are fixed before continuing

main() # begin validation
