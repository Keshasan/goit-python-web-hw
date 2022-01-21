from os import terminal_size

from AdressBook import *
from NoteBook import *


class Asisstant:
    def __init__(self) -> None:
        self.address_book = AddressBook()
        self.address_book.load_data()
        self.note_book = NoteBook()
        self.note_book.load_data()

    def add_contact(self) -> str:
        name = input("Name is key value, please write name: ").capitalize()
        phone = input('Write phone: ')
        email = input("OPTIONAL, write email: ")
        adress = input("OPTIONAL, write adress: ")
        birthday = input("OPTIONAL, write birthday date: ")
        phones = phone.replace(' ', '').split(',')

        new_contact = Record(name=name, phones=phones,
                             email=email, address=adress, birthday=birthday)
        self.address_book.add_record(new_contact)
        self.address_book.save_data()

        print(f"[+] Successfully added contact {name} to contact book")

    def __change_name(self, name: str) -> str:
        new_name = input("Write new name: ").capitalize()
        while len(new_name) < 4:
            new_name = input(
                '"Error" name length must be at least 4, please write name: '
            ).capitalize()
        old_record = self.address_book.data[name]
        new_record = Record(
            name=new_name,
            phones=old_record.get_phones(),
            birthday=str(old_record.birthday.value),
            email=old_record.email.value,
            address=old_record.address.value,
        )
        self.address_book.add_record(new_record)
        self.address_book.delete_record(name)
        self.address_book.save_data()
        return f"Successfully changed name for contact {name}"

    def __change_phone(self, name: str) -> str:
        old_phone = input("Write old phone: ")
        while old_phone not in self.address_book[name].get_phones():
            old_phone = input(
                f'I do not have such phone: "{old_phone}", write old phone: '
            )
        self.address_book[name].delete_phone(old_phone)
        new_phone = input("Write new phone: ")
        self.address_book[name].add_phone(new_phone)
        while new_phone not in self.address_book[name].get_phones():
            new_phone = input("Write new phone: ")
            self.address_book[name].add_phone(new_phone)
            self.address_book[name].delete_phone([])
        self.address_book.save_data()
        return f"Successfully changed phone for contact {name}"

    def __change_birthday(self, name: str) -> str:
        new_birthday = input("Write new birthday: ")
        while str(self.address_book[name].birthday.value) != new_birthday:
            self.address_book[name].add_birthday(new_birthday)
            if str(self.address_book[name].birthday.value) != new_birthday:
                new_birthday = input("Write new birthday: ")
        self.address_book.save_data()
        return f"Successfully changed birthday for contact {name}"

    def __change_email(self, name: str) -> str:
        new_email = input("Write new email: ")
        while str(self.address_book[name].email.value) != new_email:
            self.address_book[name].add_email(new_email)
            if str(self.address_book[name].email.value) != new_email:
                new_email = input("Write new email: ")
        self.address_book.save_data()
        return f"Successfully changed email for contact {name}"

    def __change_address(self, name: str) -> str:
        new_address = input("Write new address: ").capitalize()
        while str(self.address_book[name].address.value) != new_address:
            self.address_book[name].add_address(new_address)
            if str(self.address_book[name].address.value) != new_address:
                new_address = input("Write new address: ").capitalize()
        self.address_book.save_data()
        return f"Successfully changed address for contact {name}"

    def change_contact(self, name: str) -> None:

        if name not in self.address_book.keys():
            print(f"I do not have {name} contact in my book")
            name = input("Write contact name: ").capitalize()
        user_commands = {
            "phone": Asisstant().__change_phone,
            "name": Asisstant().__change_name,
            "birthday": Asisstant().__change_birthday,
            "email": Asisstant().__change_email,
            "address": Asisstant().__change_address,
        }
        what_change = input("What you want to change?\n")
        while what_change not in user_commands.keys():
            print("I can change only phone, name, birthday, email, address")
            what_change = input("What you want to change?\n")
        print(user_commands[what_change](name))
        print("Successfully saved new value in data")

    def del_contact(self, name: str) -> None:

        if name not in self.address_book.keys():
            print(f"I do not have {name} contact in my book")
            name = input("Write contact name: ").capitalize()
        approve = input("Are you sure? [y/n]").lower()
        if approve in ("y", "yes", "ok"):
            self.address_book.delete_record(name)

            print(f"[-] Successfully deleted contact {name} from contact book")

    def find_contact(self, name: str) -> None:

        result = self.address_book.find_record(name)
        print(result)

    def get_birthdays(self, days: int) -> None:
        while days.isdigit() is False:
            days = input(
                '"Error please enter digits"\nFor how many days do you want to know the birthdays?\n'
            )
        days = int(days)
        birthday_list = self.address_book.birthday_in_days(days)
        for info in birthday_list:
            print(info)

    def __get_text_note(self) -> Optional[str]:
        text = ''
        while True:
            row = input()
            if row:
                text += row + "\n"
            else:
                break
        return text

    def add_note(self) -> None:
        print("Write down your note:")
        text = self.__get_text_note()

        if text == "":
            return
        text_tags = input("OPTIONAL, write tags to this note: ")
        if text_tags != "":
            tags = text_tags.split(",")
            tags = [tag.strip() for tag in tags]
            self.note_book.add_note(text, tags)
            self.note_book.save_data()
        else:
            self.note_book.add_note(text, [])
            self.note_book.save_data()

    def find_note(self, value: str) -> None:
        notes = self.note_book.find_note(value)
        for note in notes:
            print(note)

    def show_notes(
        self,
    ) -> None:
        if len(self.note_book.data) == 0:
            print("You don't have notes yet.")
            return
        for note in self.note_book.data:
            print(note)

    def change_note(self, id: str) -> None:
        print("Write down your new note: ")
        text = self.__get_text_note()
        self.note_book.change_note(id, text)
        self.note_book.save_data()

    def delete_note(self, id: str) -> None:
        self.note_book.del_note(id)
        self.note_book.save_data()

    def add_tags(self, id: str) -> str:
        text_tags = input("Write tags to this note: ")
        tags = text_tags.split(",")
        tags = [tag.strip() for tag in tags]
        self.note_book.add_note_tags(id, tags)
        self.note_book.save_data()

    def add_phone(self, name: str) -> None:
        name = name.capitalize()
        if name not in self.address_book.keys():
            print(f"I do not have {name} contact in my book")
            name = input("Write contact name: ").capitalize()
        phone = input('Phone: ')
        self.address_book[name].add_phone(phone)
        self.address_book.save_data()
