import sqlite3
import pandas as pd  # This is to print the sql database in a 'pretty' way.
import time # To get time for email text write up


##########################################################################################################################################
######################################### This is the master function for the inventory project ##########################################
##########################################################################################################################################

def step_1():
    # This function prints the current output of the sqlite database called "inventory_db."
    # inventory_db is a persistent sql database that is created with the Inventory_DB_Initial_Table.py
    # It will ask the user what they want to do, and give them a few options

    conn = sqlite3.connect('inventory_db.db')
    cursor = conn.cursor()
    print('''

    ************************************************************
    *** Welcome to Ku0100's NOC Inventory Management System. ***
    *****   Contact: username@domain.com; (XXX) XXX-XXX    *****
    *****       Python Vers 3.6; Created 03.13.2017        *****
    ************************************************************

    ''')

    print('''
    Current Inventory
    -----------------

    ''')

    print(pd.read_sql_query('SELECT * FROM inventory_db', conn))
    print('\nPlease select an option from the list below:\n')
    print('1. Adjust count of current inventory.\n')
    print('2. Add device to inventory.\n')
    print('3. Remove device from inventory.\n')
    print('4. Create text to order more inventory.\n')
    print('5. Quit the program.\n')
    user_choice = input('> ')
    if int(user_choice) == 1:
        print('\nAdjust the count for which device?\n')
        user_device_choice = input('> ')
        adjust_count(user_device_choice)
    elif int(user_choice) == 2:
        print('\nWhat is the full name of the device you would like to add?\n')
        new_device = input('> ')
        while True:
            if str(new_device) == '':
                print('\nPlease enter a device name or type RETURN to go to return to the startup menu.\n')
                new_device = input('> ')
                if new_device.lower() == 'return':
                    step_1()
                else:
                    continue
            else:
                add_device_function(new_device)
    elif int(user_choice) == 3:
        remove_device_function()
    elif int(user_choice) == 4:
        order_inventory()
    elif int(user_choice) == 5:
        program_end()
    else:
        print('\nPlease choose a valid selection.\n')

##########################################################################################################################################
###################################### When the user wants to adjust the count of a specific device ######################################
##########################################################################################################################################

def adjust_count(user_device_choice):

    conn = sqlite3.connect('inventory_db.db')
    cursor = conn.cursor()

    for name in (str(user_device_choice)):
        # Check to see if device already exists in inventory_db
        cursor.execute('SELECT device_count FROM inventory_db WHERE device_name = ?', (str(user_device_choice),))
        device_exists = cursor.fetchone()
        # If device doesn't exist
        while device_exists is None:
            print('\nDevice %s is not currently in the inventory database. Would you like to add it? (y/n)\n' % (user_device_choice,))
            user_choice_yn = str(input('> '))
            if user_choice_yn.lower() in ['y','yes']:
                add_device_function(user_device_choice)
            elif user_choice_yn.lower() in ['n', 'no']:
                user_choice_master()
            else:
                print('\nPlease choose a valid selection.\n')
                continue
        # If device does exist
        else:
            for row in cursor.execute('SELECT * FROM inventory_db WHERE device_name = ?', (str(user_device_choice),)):
                update_row = cursor.fetchall()

            # print(update_row)
            print('\nWhat is the new count for device ' + str(user_device_choice) + '?\n')
            new_count = input('> ')

            cursor.execute('UPDATE inventory_db SET device_count = ? WHERE device_name = ?', (str(new_count), str(user_device_choice),))
            conn.commit()
            conn.close()

            print('\nDevice count has been updated to ' + str(new_count) + '.')
            user_choice_master()



    ############### TO DO: ###############
    # 1. Exception handling
    # 2. Add comments throughout

##########################################################################################################################################
#################################### When the user wants to add a new device to the inventory database ###################################
##########################################################################################################################################

def add_device_function(new_device):
    conn = sqlite3.connect('inventory_db.db')
    cursor = conn.cursor()

    for name in (str(new_device)):
        # Check to see if device already exists in inventory_db
        cursor.execute('SELECT device_count FROM inventory_db WHERE device_name = ?', (str(new_device),))
        device_exists = cursor.fetchone()
        # Device doesn't already exist in inventory_db
        while device_exists is None:
            print('\nWhat is the count of device %s you are adding?\n' % (str(new_device)))
            new_device_count = input('> ')

            cursor.execute('INSERT INTO inventory_db (device_name, device_count) VALUES (?, ?)', (str(new_device), str(new_device_count),))
            conn.commit()
            conn.close()
            print('\nDevice ' + str(new_device) + ' has been added to the inventory database with a count of ' + str(new_device_count) + '.')
            user_choice_master()
        # Device does already exist in inventory_db
        else:
            conn.close()
            print('\nDevice ' + str(new_device) + ' already exists in the inventory database.\n')
            print('Please select an option from the list below:\n')
            print('1. Adjust inventory count for %s.\n' % (str(new_device)))
            print('2. Return to startup menu.\n')
            print('3. Quit the program.\n')
            user_choice = input('> ')
            if int(user_choice) == 1:
                adjust_count(new_device)
            elif int(user_choice) == 2:
                step_1()
            elif int(user_choice) == 3:
                program_end()
            else:
                print('\nPlease choose a valid selection.\n')

    ############### TO DO: ###############
    # 1. Exception handling
    # 2. Add comments throughout

##########################################################################################################################################
################################## When the user wants to remove a new device from the inventory database ################################
##########################################################################################################################################

def remove_device_function():
    conn = sqlite3.connect('inventory_db.db')
    cursor = conn.cursor()

    print('\nWhat is the full name of the device you would like to remove?\n')
    remove_device = input('> ')
    # Check to see if device already exists in inventory_db
    cursor.execute('SELECT device_count FROM inventory_db WHERE device_name = ?', (str(remove_device),))
    device_exists = cursor.fetchone()
    # Device doesn't already exist in inventory_db
    while device_exists is not None:
        while True:
            print('\nPlease press ENTER to confirm deletion of ' + str(remove_device) + ' or any other key to cancel deletion.\n')
            delete_confirm = input('> ')
            if delete_confirm == '':
                cursor.execute('DELETE FROM inventory_db WHERE device_name = ?', (str(remove_device),))
                conn.commit()
                conn.close()
                user_choice_master()
            else:
                print('\nDeletion canceled.\n')
                print('Please select an option from the list below:\n')
                print('1. Delete a different device\n')
                print('2. Return to startup menu\n')
                print('3. Quit the program\n')
                user_choice = input('> ')
                if int(user_choice) == 1:
                    remove_device_function()
                elif int(user_choice) == 2:
                    step_1()
                elif int(user_choice) == 3:
                    program_end()
                else:
                    print('\nPlease choose a valid selection.\n')
    else:
        print('\nThis device does not currently exist in the inventory_db.\n')
        print('Please select an option from the list below:\n')
        print('1. Delete a different device\n')
        print('2. Return to startup menu\n')
        print('3. Quit the program\n')
        user_choice = input('> ')
        if int(user_choice) == 1:
            remove_device_function()
        elif int(user_choice) == 2:
            step_1()
        elif int(user_choice) == 3:
            program_end()
        else:
            print('\nPlease choose a valid selection.\n')

    ############### TO DO: ###############
    # 1. Exception handling
    # 2. Add comments throughout
    # 3. Ensure that user input is a valid device

##########################################################################################################################################
################################## When the user wants to order inventory, create text for email to send #################################
##########################################################################################################################################

def order_inventory():
    conn = sqlite3.connect('inventory_db.db')
    cursor = conn.cursor()
    print('\nWhat is the name of the device you need to stock?\n')
    order_device_name = input('> ')
    x = 1
    while x != 0:
        print('\nDo you have the TMS Code for this device? (y/n)\n')
        tms_available = str(input('> '))
        if tms_available.lower() in ['y', 'yes']:
            print('\nWhat is the TMS Code?\n')
            tms_code = input('> ')
            x = 0
        elif tms_available.lower() in ['n', 'no']:
            tms_code = 'N/A'
            x = 0
        else:
            print('\nPlease enter either yes or no.')
            x = 1
    while True:
        print('\nWhat number of inventory would you like to order for %s?\n' % str(order_device_name))
        order_device_num = input('> ')
        if order_device_num.isnumeric() == True:
            print('\nFinally, what is your full name [First Name Last Name]?\n')
            user_name = input('> ')
            print('\n***** Please use the following information when sending the request to the Warehouse team. *****\n')
            print('''

********************************************************************************************************
*********** PLEASE USE THE BELOW INFORMATION WHEN SENDING THE REQUEST TO THE WAREHOUSE TEAM ************
********************************************************************************************************

        To: inventoryMaster@domain.com

        Cc: personTwo@domain.com, personThree@domain.com

        Subject: NOC Inventory Procurement Request %s


        Inventory Master,



        The NOC basement storeroom is running low on a particular device. Would you please procure the following
        device(s) and amount(s)?

        Device: %s
        Count: %s
        TMS Code: %s



        Regards,


        %s

            ''' % (time.strftime('%m.%d.%Y'), str(order_device_name), str(order_device_num), str(tms_code), str(user_name)))
            user_choice_master()
        else:
            print('\nInput must be an integer.')
            continue

    ############### TO DO: ###############
    # 1. Exception handling
    # 2. Add comments throughout
    # 3. Allow adding multiple devices at once

##########################################################################################################################################
########################### This is a reference function to allow user to return to main menu or quit program ############################
##########################################################################################################################################

# This function is to clean up the code for the other functions
def user_choice_master():

    while True:
        print('\nWhat would you like to do now?\n')
        print('1. Return to startup menu\n')
        print('2. Quit the program\n')
        user_choice = input('> ')
        # while int(user_choice) == 1 or int(user_choice) == 2:
        if user_choice.isnumeric() == True and int(user_choice) < 3:
            if int(user_choice) == 1:
                step_1()
            elif int(user_choice) == 2:
                program_end()
        else:
            print('\nPlease choose a valid selection.\n')
            continue

##########################################################################################################################################
#################################### Another reference function that is called to quit the program #######################################
##########################################################################################################################################

# This function is called as an option to close the program. Will clean up code elsewhere
def program_end():

    print('\nThank you for using Ku0100\'s inventory tracker!\n')
    raise SystemExit

##########################################################################################################################################

step_1()
