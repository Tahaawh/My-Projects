# alt shift f
import datetime
import os
import json

# r
# w
# a


def delete_acc(username):
    with open("data.json", "r") as myfile:
        result = json.load(myfile)
        result.pop(username)
    with open("data.json", "w") as myfile:
        json.dump(result, myfile)
    return f"{username} deleted !"


def submit_ticket(username: str, message: str):
    with open("data.json", "r") as myfile:
        data = json.load(myfile)
        ticket_data = data[username]["ticket"]
        if ticket_data == None:
            outer_list = []
            listed_ticket = [message, "user"]
            outer_list.append(listed_ticket)
            data[username]["ticket"] = outer_list
        else:
            ticket_data.append([message, "user"])
            data[username]["ticket"] = ticket_data

    # dump the data to the file (rewrite the file)
    with open("data.json", "w") as myfile:
        json.dump(data, myfile)

    return "your ticket has been submitted successfully"


def edit_profile(username: str):
    with open("data.json", "r") as myfile:
        all_data = json.load(myfile)
        if username in all_data.keys():
            data = all_data[username]["data"]
            grade, email = input("please enter grade : "), input(
                "please enter email : "
            )
            data["grade"] = grade
            data["email"] = email

    # dump the data to the file (rewrite the file)
    with open("data.json", "w") as myfile:
        json.dump(all_data, myfile)


def create_json_file():
    if not os.path.exists("data.json"):
        with open("data.json", "w") as myfile:
            json.dump({}, myfile)


def login_user(username: str, password: str, all_username: list, all_password: list):
    # for every_user in zip(all_username, all_password):
    #     if username == every_user[0] and password == every_user[1]:
    #         return f"Welcome {username}", True
    # else:
    #     return "Invalid username or password", False
    with open("data.json", "r") as myfile:
        data = json.load(myfile)
        if username in data.keys() and password == data[username]["password"]:
            return f"Welcome {username}", True
        else:
            return "Invalid username or password", False


def signup_user(username: str, password: str, all_username: list, all_password: list):
    # all_username.append(username)
    # all_password.append(password)
    with open("data.json", "r") as myfile:
        data = json.load(myfile)  # {}
        data[username] = {
            "password": password,
            "ticket": None,
            "data": {"grade": None, "email": None},
        }

    with open("data.json", "w") as myfile:
        json.dump(data, myfile)
    return f"User {username} has been created successfully"


def set_time_exam(new_time: str, time_exam):
    print(time_exam)
    if ":" in new_time:
        time_splited = new_time.split(":")  # ["12","30"]
        time_exam = datetime.time(int(time_splited[0]), int(time_splited[1]))
        return time_exam


def set_date_exam(new_date: str, date_exam):
    print(date_exam)
    if "-" in new_date and "/" in new_date:
        return "invalid date ..."
    if "-" in new_date:
        date_splited = new_date.split("-")
        date_exam = datetime.date(
            int(date_splited[0]), int(date_splited[1]), int(date_splited[2])
        )
        return date_exam
    elif "/" in new_date:
        date_splited = new_date.split("/")  # ["2025","2","28"]
        date_exam = datetime.date(
            int(date_splited[0]), int(date_splited[1]), int(date_splited[2])
        )
        return date_exam


def show_and_check_datetime(date_exam: datetime.date, time_exam: datetime.time):
    # print(datetime.datetime.now())
    print(
        datetime.datetime(
            date_exam.year,
            date_exam.month,
            date_exam.day,
            time_exam.hour,
            time_exam.minute,
            time_exam.second,
        )
        - datetime.datetime.now()
    )
