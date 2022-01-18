from abc import ABC, abstractmethod
import sys


class Interface(ABC):
    @abstractmethod
    def get_command():
        """Get command from user"""


class Terminal(Interface):
    @staticmethod
    def get_command():
        """Get command from user in terminal"""
        return sys.argv
