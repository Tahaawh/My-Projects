from menus import *
from defs import *
from pyfiglet import figlet_format
import datetime
import time


all_username = []
all_password = []
date_exam = datetime.datetime.fromtimestamp(0).date()  # 1970/1/1
time_exam = datetime.datetime.fromtimestamp(0).time()  # 3:30:00
while True:
    create_json_file()
    selection = menu_start()
    if selection == 1:
        selection_admin = menu_admin()
        if selection_admin == 1:
            message = input("Date or Time or both ? : ")
            if message == "time":
                new_time = input("please enter your new time\n( e.g : 12:30 ) : ")
                time_exam = set_time_exam(new_time, time_exam)
            elif message == "date":
                new_date = input(
                    "please enter the new date \n (e.g =>  2012-12-10 2012/12/10 ) : "
                )  # 2025/2/28
                date_exam = set_date_exam(new_date, date_exam)
            elif message == "both":
                pass
        elif selection_admin == 2:
            pass
        elif selection_admin == 3:
            username = input("please enter the username to edit : ")
            edit_profile(username)
        elif selection_admin == 4:
            pass
        elif selection_admin == 5:
            pass
    elif selection == 2:
        selection_auth = menu_authentication()
        if selection_auth == 1:
            username = input("please enter your username to signup : ")
            password = input("please enter your password : ")
            result = login_user(username, password, all_username, all_password)
            if result[1] == True:
                time.sleep(1.5)
                print(figlet_format(result[0]))
                selection_student = menu_student()
                if selection_student == 1:
                    show_and_check_datetime(date_exam,time_exam)
                elif selection_student == 2:
                    pass
                elif selection_student == 3:
                    pass
                elif selection_student == 4:
                    new_message = input("please enter your message : ")
                    print(submit_ticket(username,new_message))
                elif selection_student == 5:
                    (delete_acc(username))
                    
            else:
                print(result[0])
        elif selection_auth == 2:
            username = input("please enter your username to signup : ")
            password = input("please enter your password : ")
            print(signup_user(username, password, all_username, all_password))
        # selection_user = menu_student()
