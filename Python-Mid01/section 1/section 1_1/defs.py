import pyfiglet

def check_correct_password(password):
    if password == "admin":
        return pyfiglet.figlet_format("hello admin")
    else:
        return "not correct"