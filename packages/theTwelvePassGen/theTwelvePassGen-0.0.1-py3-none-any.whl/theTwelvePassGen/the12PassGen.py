import random

def randomGen(name: str, age: int, randomWord: str, randomNumber: int) -> str:
    counter = random.randint(0, 1)
    password: str
    if counter == 0:
        password = name[random.randint(0, len(name) - 1)] + str(age)[random.randint(0, len(str(age)) - 1)] + randomWord[random.randint(0, len(randomWord) - 1)] + str(randomNumber)[random.randint(0, len(str(randomNumber)) - 1)]
    elif counter == 1:
        password = name[random.randint(0, len(name) - 1)].upper() + str(age)[random.randint(0, len(str(age)) - 1)] + randomWord[random.randint(0, len(randomWord) - 1)] + str(randomNumber)[random.randint(0, len(str(randomNumber)) - 1)]
    
    counter2 = random.randint(0, len(password) - 1)
    counter3 = random.randint(0, 2)
    if counter3 == 0:
        password = password.replace(password[counter2], "&")
    elif counter3 == 1:
        password = password.replace(password[counter2], "@")
    elif counter3 == 2:
        password = password.replace(password[counter2], "#")
    return password


def generatePass() -> str:
    print("Based on your information we'll make you password.")

    name = input("Enter your name: ")
    try:
        age = int(input("Enter your age: "))
    except ValueError:
        print("Please enter the correct value.")

    randomWord = input("A random word: ").split(" ")[0]
    try:
        randomNumber = str(input("A random 10 digits number: ")).split(" ")[0]
        if len(randomNumber) == 10:
            password = randomGen(name, age, randomWord, randomNumber) + randomGen(name, age, randomWord, randomNumber) + randomGen(name, age, randomWord, randomNumber)
            print(password)
        else:
            print("Enter a 10 digit number")
            exit()
    except ValueError:
        print("Please enter the correct value.")

generatePass()