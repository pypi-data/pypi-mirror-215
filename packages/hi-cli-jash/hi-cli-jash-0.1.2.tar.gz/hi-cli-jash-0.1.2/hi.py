def hi(name):
    print(f"Hi, {name}!")

def install():
    name = input("Enter your name: ")
    number = input("Enter your number: ")
    with open('.hi_module_data', 'w') as f:
        f.write(f"{name}\n{number}")

try:
    with open('.hi_module_data', 'r') as f:
        name, number = f.readlines()
        name = name.strip()
        number = number.strip()
except FileNotFoundError:
    name = ""
    number = ""

if __name__ == "__main__":
    hi(name)
