import sys
from src.Asisstant import Asisstant
from src.Sorter import Sorter
from src.Interface import Terminal


def main():
    jarvis = Asisstant()
    commands_list = [
        "jarvis add contact\n",
        "jarvis show contacts\n",
        "jarvis find contact {name}\n",
        "jarvis change contact {name}\n",
        "jarvis delete contact {name}\n",
        "jarvis add phone {name}"
        "jarvis get birthdays {days_to}\n",
        "jarvis add note\n",
        "jarvis show notes\n",
        "jarvis find note {id/text/tag}\n",
        "jarvis change note {id}\n",
        "jarvis delete note {id}\n",
        "jarvis add tags {id}\n",
        "jarvis sort folder {path_to_folder}\n",
    ]
    user_commands = {
        "add contact": jarvis.add_contact,
        "show contacts": jarvis.address_book.show_all_records,
        "add note": jarvis.add_note,
        "show notes": jarvis.show_notes,
    }
    user_commands_with_arguments = {
        "find contact": jarvis.find_contact,
        "add phone": jarvis.add_phone,
        "change contact": jarvis.change_contact,
        "delete contact": jarvis.del_contact,
        "get birthdays": jarvis.get_birthdays,
        "sort folder": Sorter().sort,
        "find note": jarvis.find_note,
        "tag note": jarvis.note_book.find_by_tag,
        "change note": jarvis.change_note,
        "delete note": jarvis.delete_note,
        "add tags": jarvis.add_tags,
    }

    interface = Terminal()

    commands = interface.get_command()[1:]
    str_cmd = " ".join(commands)

    if len(interface.get_command()) == 1:
        print(
            f'Hello my name is "Jarvis" i am your virtual assistant.\nI support these commands:\n  {"  ".join(commands_list)}'
        )
    elif len(commands) == 2:
        if str_cmd in user_commands.keys():
            user_commands[str_cmd]()
        else:
            print(f"I do not support this command {str_cmd}")
    elif len(commands) == 3:

        str_cmd = " ".join(commands[0:2])
        user_argument = commands[-1]

        if str_cmd in user_commands_with_arguments.keys():
            user_commands_with_arguments[str_cmd](user_argument)
        else:
            print(f"I do not support this command {str_cmd}")
    else:
        print("Unknown command usage.")


if __name__ == "__main__":
    main()
