import pandas as pd
from datetime import datetime
import time

filePath = './Humidity Dataset.csv'

def main():
    # ensure RowID's are consistent
    print("Checking column: RowID")
    check_RowID()
    print("__________________________________")

    # ensure stamp values are consistent
    print("Checking column: stamp")
    check_stamp()
    print("__________________________________")

    # ensure datetime values are consistent
    print("Checking column: datetime")
    check_datetime()
    print("__________________________________")

    # ensure hum values are consistent
    print("Checking column: hum")
    check_hum()
    print("__________________________________")


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

def check_timestamp(date, timestamp): #! Checks whether the date converted to a timestamp is equal to the matching timestamp value
    if (not check_int(timestamp)): # If the timestamp is misformatted, can't compare
        return True

    dateTimestamp = time.mktime(time.strptime(date, '%Y/%m/%d %H:%M:%S')) # Converts the timestamp string into a time object and then into a timestamp
    
    return dateTimestamp != float(timestamp) # If they aren't equal, return False meaning error

def check_RowID():
    # check rowID values are unique integers (will also find missing rows)
    df = pd.read_csv(filePath)  # reload csv
    previousID = 0 # The ID of the previous row, checking for missing rows

    errors = {"valueError":{}, "duplicate":{}, "missingRows": {}}
    testList = []
    # find errors
    for index, val in enumerate(df['rowID']):
        i = index + 2 # nessesary because index starts from 0 refering to Spreadsheet software row 2, meaning that the indexes here are 2 less than in the spreadsheet software
        if val in testList:
            errors["duplicate"][i] = val
        if not check_int(val):
            errors["valueError"][i] = val
        else:
            if (int(val) - previousID > 2000):
                errors["missingRows"][i] = val
            previousID = int(val)

        testList.append(val)

    # case if no errors
    if len(errors["duplicate"]) == 0 and len(errors["valueError"]) == 0 and len(errors["missingRows"]) == 0:
        return
    else:
        # print value errors
        if len(errors["valueError"]) > 0:
            print("RowID Value errors:")
            for error in errors["valueError"]:
                print(f"\tRow: {error}, Value: {errors['valueError'][error]}")
            print()
        # print duplicate value errors
        if len(errors["duplicate"]) > 0:
            print("RowID Value errors:")
            for error in errors["duplicate"]:
                print(f"\tRow: {error}, Value: {errors['duplicate'][error]}")
            print()

        # print duplicate value errors
        if len(errors["missingRows"]) > 0:
            print("Missing Rows: ")
            for error in errors["missingRows"]:
                print(f"\tRow: {error}, Value: {errors['missingRows'][error]}")
            print()

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
                print(f"\tRow: {error}, Value: {errors['valueError'][error]}")
            print()

def check_datetime():
    # check datetime values are consecutive time values in correct format
    df = pd.read_csv(filePath) # reload csv
    errors = {"valueError":{},"duplicate":{}, "inconsistencies": {}}
    testList = []
    # find errors
    for index, val in enumerate(df['datetime']):
        i = index + 2 # nessesary because index starts from 0 refering to Spreadsheet software row 2, meaning that the indexes here are 2 less than in the spreadsheet software
        val = val.lstrip(' ') # remove white space at beggining
        if not check_time(str(val)):
            errors["valueError"][i] = val
        elif not check_timestamp(str(val), df['stamp'][index]): # If the date is not misformatted, we can compare it with the timestamp
            errors["inconsistencies"][i] = val
        if val in testList:
            errors["duplicate"][i] = val
        testList.append(val)
    # case if no errors
    if len(errors["valueError"]) == 0 and len(errors["duplicate"]) == 0:
        return
    else:
        # print value errors
        if len(errors["valueError"]) > 0:
            print("datetime Value errors:")
            for error in errors["valueError"]:
                print(f"\tRow: {error}, Value: {errors['valueError'][error]}")
            print()
        # print duplicate errors
        if len(errors["duplicate"]) > 0:
            print("datetime Duplicate errors:")
            for error in errors["duplicate"]:
                print(f"\tRow: {error}, Value: {errors['duplicate'][error]}")
            print()

        # print inconsistency errors
        if len(errors["inconsistencies"]) > 0:
            print("datetime Inconsistency errors:")
            for error in errors["inconsistencies"]:
                print(f"\tRow: {error}, Value: {errors['inconsistencies'][error]}")
            print()

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
                print(f"\tRow: {error}, Value: {errors['valueError'][error]}")
            print()

main() # begin validation
