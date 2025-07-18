from collections import UserDict
import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, number):
        self.checking(number)
        super().__init__(number)

    def checking(self, number):
        if type(number) != str or len(number) != 10:
            raise ValueError("Phone number must be a string of 10 digits.")

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, number):
        self.phones.append(Phone(number))

    def remove_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                self.phones.remove(phone)
                break

    def edit_phone(self, old_number, new_number):
        for idx, phone in enumerate(self.phones):
            if phone.value == old_number:
                self.phones[idx] = Phone(new_number)
                break

    def find_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    
    def add_birthday(self, value):
        self.birthday = Birthday(value)

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
     
    def get_upcoming_birthdays(self):
        congratulation_date = []
        today = datetime.date.today()
        
        for record in self.data.values():
            if record.birthday:
                bday_this_year = record.birthday.value.replace(year=today.year)

                if bday_this_year < today:
                    bday_this_year = bday_this_year.replace(year=today.year + 1)

                days_left = bday_this_year - today
                weekday = bday_this_year.weekday()

                if days_left < datetime.timedelta(days=7):
                    if weekday == 5:  # Якщо субота
                        bday_this_year += datetime.timedelta(days=2)
                    elif weekday == 6:  # Якщо неділя
                        bday_this_year += datetime.timedelta(days=1)

                    congratulation_date.append({"name": record.name.value, "congratulation_date": bday_this_year.strftime("%d.%m.%Y")})

        return congratulation_date
