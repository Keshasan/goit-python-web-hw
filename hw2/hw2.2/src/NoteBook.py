import os
import pickle
from collections import UserList
from sys import platform



class Tag:
    def __init__(self, value: str) -> None:
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        self.__value = value


class Note:
    def __init__(self, text: str, tags, id: int) -> None:
        self.text = text
        self.id = id
        if len(tags) != 0:
            self.tags = [Tag(tag) for tag in tags]
        else:
            self.tags = []

    def __str__(self) -> str:
        tags = []

        for tag in self.tags:

            tags.append(tag.value)

        note_tags = ", ".join(tags)
        text = f"ID:{self.id}\nNote: \n{self.text}"

        if len(tags) != 0:
            text += f"Tags: {note_tags}\n"
        return text


class NoteBook(UserList):
    """
    Desrcibes object fo personal book with notes
    """

    def set_ID(self):
        if len(self.data) == 0:
            return 1
        else:
            return self.data[-1].id + 1

    def add_note(self, text: str, tags: list) -> None:
        """Method for adding note to list"""
        id = self.set_ID()
        new_note = Note(text, tags, id)
        self.data.append(new_note)
        print("[+] New note was added")

    def find_note(self, subtext: str) -> list:
        """Method to find notes by text or ID"""
        subtext = subtext.lower()
        notes_list = []
        for note in self.data:

            if subtext in note.text.lower() or subtext == str(note.id):
                notes_list.append(note)
        notes_list += self.find_by_tag(subtext)
        return list(set(notes_list))

    def del_note(self, id: int) -> None:
        """Method to delete note by ID"""
        try:
            id = int(id)
        except ValueError:
            raise ValueError("Input a number")
        del_note = None
        for note in self.data:
            if id == note.id:
                del_note = self.data.pop(id - 1)
                print(f"[-] Note ID={id} was deleted")
        if not del_note:
            print(f"ID={id} is not valide")

    def change_note(self, id: str, new_text: str) -> None:
        """Method searches for a note by ID and changes its text"""
        try:
            id = int(id)
        except ValueError:
            raise ValueError("Input a number")
        for note in self.data:
            if id == note.id:
                note.text = new_text

    def add_note_tags(self, id: str, tags) -> None:
        """Method add tags to tags-list in note by ID"""
        try:
            id = int(id)
        except ValueError:
            raise ValueError("Input a number")
        for note in self.data:
            if id == note.id:
                if len(note.tags) != 0:
                    note.tags.extend([Tag(tag) for tag in tags])
                    print("[+] Tags was added")
                else:
                    note.tags = [Tag(tag) for tag in tags]

    def find_by_tag(self, subtext: str) -> None:
        """Method to find notes by tag"""

        notes_list = []
        for note in self.data:
            note_tags = [tag.value.lower() for tag in note.tags]

            if subtext in note_tags:
                notes_list.append(note)
        return notes_list

    def save_data(self) -> None:
        folder_sep = "//" if platform == "win32" else "/"
        jarvis_folder = os.environ["HOME"] + folder_sep + "jarvis"

        if os.path.exists(jarvis_folder):
            with open(jarvis_folder + folder_sep + "notes.bin", "wb") as file:
                pickle.dump(self.data, file)
        else:
            os.mkdir(jarvis_folder)
            with open(jarvis_folder + folder_sep + "notes.bin", "wb") as file:
                pickle.dump(self.data, file)

    def load_data(self) -> None:

        folder_sep = "//" if platform == "win32" else "/"

        jarvis_notes = (
            os.environ["HOME"] + folder_sep + "jarvis" + folder_sep + "notes.bin"
        )

        if os.path.exists(jarvis_notes):
            with open(jarvis_notes, "rb") as file:
                self.data = pickle.load(file)
