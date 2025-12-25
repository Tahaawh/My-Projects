# name = "behnam"
# age = 23
# job = "programmer"
# print("My name is" +  name, "and I am" + str(age), "years old. I am a"+ job)
# print(f"my name is {name} and i'm {age} and i'm a {job}")

# def say_hello():
#     return "Hello World"

# print(say_hello())


# def counter_to_n(n: int):
#     ls = []
#     for i in range(n):
#         ls.append(i)
#     return ls,True


# print(counter_to_n(10))

# import datetime

# print(datetime.datetime.now().date().year)
# print(datetime.datetime.now().date().day)
# print(datetime.datetime.now().date().month)
# print(datetime.datetime.now().time().hour)
# print(datetime.datetime.now().time().minute)

# print(datetime.date(2021, 1, 1))
# # print(datetime.time(12, 30, 30))
# # print(datetime.datetime(2021, 1, 1, 12))


import datetime

# print((datetime.datetime.now().date()) + datetime.timedelta(weeks=2))
# print((datetime.datetime.now().date().strftime("%Y-%m-%d")) + datetime.timedelta(days=1))


# test ur self 1
# def calculate_born_year(year,age):
#     return year - age


# print(calculate_born_year(datetime.datetime.now().date().year,23))


# # test ur self 2
# def calculate_year_born(today,age:int):
#     today = datetime.datetime.strptime(today, "%Y-%m-%d")
#     return today.date().year - age


# print(calculate_year_born("2025-02-13",23))
##################################################
# from persiantools.jdatetime import JalaliDate


# # print(JalaliDate.today())
# # print(JalaliDate(datetime.datetime.now()))


# # print(JalaliDate.to_jalali(2020,1,1))
# print(JalaliDate(1395,10,10).to_gregorian())
##################################################
# name = "behnam"
# print(name[5:1:-2]) # [start:stop:step]
# print(name[::-1])
##################################################
# test ur self 4
# def palindrome_date(first_date):
#     for i in range((datetime.datetime.now().date().year - 2000) * 365):
#         if type(first_date) != str:
#             first_date = datetime.datetime.strftime(first_date, "%Y-%m-%d")
#         reverse_year = first_date.split("-")[0][::-1]  # 2001 -> 1002
#         concat_month_day = (
#             first_date.split("-")[1] + first_date.split("-")[2]
#         )  # 10.02 -> 1002
#         if reverse_year == concat_month_day:
#             print(f"{first_date} is a palindrome date")
#         first_date = datetime.datetime.strptime(first_date, "%Y-%m-%d").date()
#         first_date = first_date + datetime.timedelta(days=1)


# first_date = datetime.date(2000, 1, 1).strftime("%Y-%m-%d")

# palindrome_date(first_date)


#
# import datetime

# # print(datetime.datetime.now())
# print(datetime.date.today())

# print(datetime.datetime.fromtimestamp(0))


# def change_name():
#     name = input("please enter name : ")
#     return name

# name = "behnam"

# while True:
#     print(name)
#     name = change_name()

# data = {
#     "behnam": {"password": "1381", "data": {"grade": None, "email": None}},
#     "ali": {"password": "4321", "data": {"grade": None, "email": None}},
# }


# print(data["behnam"]["data"]["grade"])
#######################################
import time

# print(time.time())
# print(time.ctime())
# print(time.ctime(time.time()))


# start = time.perf_counter()
# start = 0
# for i in range(1,100000):
#     start +=1
# end = time.perf_counter()
# print(start - end)
#######################################
# print(time.localtime())

# start = time.perf_counter()
# time.sleep(1)
# end = time.perf_counter()
# print(end - start)

############################
import pandas as pd

# df = pd.DataFrame(
#     data={
#         "name": ["behnam", "ali", "sara"],
#         "age": [23, 28, 34],
#         "city": ["Tehran", "Mashhad", "Ahwaz"],
#     },
#     index=["person1", "person2", "person3"],
# )

# print(df)


dc = {"name":"behnam",
      "age" :23}

dc.pop("age")
print(dc)