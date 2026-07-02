def login(username, password):
    if username == "admin" and password == "123":
        return True
    return False

def logout():
    return "Logged out"