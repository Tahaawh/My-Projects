def menu_start():
    print("1 -  admin")
    print("2 -  student")
    selection = int(input("please enter your selection : "))
    return selection


def menu_authentication():
    print("1 - login")
    print("2 - signup")
    selection = int(input("please enter your selection : "))
    return selection


def menu_admin():
    print("1 - set time/date exam")
    print("2 - add exam")
    print("3 - edit student's profile")
    print("4 - show all tickets")
    print("5 - ban/unban a student")
    selection = int(input("please enter your selection : "))
    return selection


def menu_student():
    print("1 - start exam")
    print("2 - show your grade")
    print("3 - show billboard")
    print("4 - submit a ticket ")
    print("5 - delete acc")
    selection = int(input("please enter your selection : "))
    return selection
