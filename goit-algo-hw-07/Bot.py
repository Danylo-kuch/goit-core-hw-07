from collections import UserDict
from datetime import datetime, timedelta


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return (self.value)

class Name(Field):
		pass

class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Номер телефону повинен містити рівно 10 цифр")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
            self.value = value 
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        

def input_error(func):
    def inner(args, book):
        try:
            if not args and func.__name__ not in ("show_all_contacts", "birthdays"):
                return "Missing arguments"

            
            elif func.__name__ == "add_contact" and len(args) != 2:
                return "Usage: add <name> <phone>"
            
            elif func.__name__ == "change_contacts_phone" and len(args) != 3:
                return "Usage: change <name> <old_phone> <new_phone>"
            
            elif func.__name__ == "show_contacts_phones" and len(args) != 1:
                return "Usage: phone <name>"
            
            elif func.__name__ == "show_all_contacts" and len(args) > 0:
                return "Usage: all"
            
            elif func.__name__ == "add_birthday" and len(args) != 2:
                return "Usage: add-birthday <name> <birthday (DD.MM.YYYY)>"
            
            elif func.__name__ == "show_birthday" and len(args) != 1:
                return "Usage: show-birthday <name>"
            
            elif func.__name__ == "birthdays" and len(args) > 0:
                return "Usage: birthdays"
            
            return func(args, book)
        except KeyError:
            return f"The name {args[0]} wasn't found in your contacts"
        except (ValueError, IndexError) as e: 
            return str(e)
    return inner

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        phones_str = ";".join(str(phones) for phones in self.phones)
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "---"
        return f"Ім'я контакту: {self.name}, номери телефону: {phones_str}, День народження: {birthday_str}"
    
    
    
    def add_phone(self, phone: str):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone: str):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)
        else:
            raise ValueError (f"Номер {phone} не було знайдено")
    
    def edit_phone(self, old:str, new:str):
        phone_obj = self.find_phone(old)
        if phone_obj:
            self.add_phone(new)
            self.remove_phone(old)
        else:
            raise ValueError("Старий номер не було знайдено")
    
    def find_phone(self, phone:str):
        for phones in self.phones:
            if phones.value == phone:
                return phones
        return None
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)



class AddressBook(UserDict):
    
    def add_record(self, record: Record):
        if record.name.value in self.data:
            raise ValueError(f"Контакт {record.name.value} вже існує!")
        else:
            self.data[record.name.value] = record


    def find(self, name: str):
        record = self.data.get(name)
        if not record:
            return None
        return record

    
    def delete(self, name: str):
        if self.data.get(name):
            del self.data[name]
        else:
            raise ValueError(f"Ім'я {name} не було знайдено")

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        contacts_with_upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year = today.year)
                days_for_birthday_this_year = (birthday_this_year - today).days
                if 0 <= days_for_birthday_this_year <= 7:
                    if birthday_this_year.weekday() == 5:
                        birthday_this_year += timedelta(days = 2)
                    elif birthday_this_year.weekday() == 6:
                        birthday_this_year += timedelta(days = 1)
                    contacts_with_upcoming_birthdays.append({
                    "name": record.name.value,
                    "birthday": birthday_this_year
                    })

        return contacts_with_upcoming_birthdays
    
    def __str__(self):
        result = []
        for record in self.data.values():
            result.append(str(record))
        return "\n".join(result)

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    try:
        record = book.find(name)
        message = "Contact updated."
    except ValueError:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    if not record.find_phone(phone):
        record.add_phone(phone)
    else:
        message = "This phone number already exists for this contact."

    return message


@input_error
def change_contacts_phone(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return "Contact updated"

@input_error
def show_contacts_phones(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    phones_str = ";".join(phone.value for phone in record.phones)
    return f"Contacts phones ({name}): {phones_str}"

@input_error
def show_all_contacts(args, book: AddressBook):
    if not book.data:
        return "No contacts found."
    return str(book)

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    try:
        record = book.find(name)
    except ValueError:
        record = Record(name)
        book.add_record(record)
    if record.birthday:
        return "The birthday is already given!"
    record.add_birthday(birthday)
    return "The birthday added."
    
@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    try:
        record = book.find(name)
        if record.birthday:
            return record.birthday.value.strftime("%d.%m.%Y")
        else:
            return "Birthday is not set"
    except ValueError:
        return f"Contact {name} not found"
    
@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    result = ["Upcoming birthdays:"]
    for item in upcoming:
        result.append(f"{item['name']}: {item['birthday'].strftime('%d.%m.%Y')}")
    return "\n".join(result)



def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contacts_phone(args, book))

        elif command == "phone":
            print(show_contacts_phones(args, book))

        elif command == "all":
            print(show_all_contacts(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))


        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()