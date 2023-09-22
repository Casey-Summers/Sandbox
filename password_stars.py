"""Password to star converter"""

password = str(input("Password: "))
for character in range(len(password)):
    print("*", end="")
