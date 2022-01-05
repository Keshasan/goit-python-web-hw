from abc import ABC, abstractmethod
import json
import pickle


class SerializationInterface(ABC):
    @abstractmethod
    def save_data(self):
        """Save data"""

    @abstractmethod
    def get_data(self):
        """Get data"""


class SerializationJson(SerializationInterface):
    def save_data(self, data, filename):
        with open(filename, "w") as file:
            json.dump(data, file)

    def get_data(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)
            return data


class SerializationBin(SerializationInterface):
    def save_data(self, data, filename):
        with open(filename, "wb") as file:
            pickle.dump(data, file)

    def get_data(self, filename):
        with open(filename, "rb") as file:
            data = pickle.load(file)
            return data


# TEST

test_data = {"president": {"name": "Zelenskiy", "country": "Ukraine"}}

js = SerializationJson()
bn = SerializationBin()
js.save_data(test_data, "test.json")
bn.save_data(test_data, "test.bin")

data1 = js.get_data("test.json")
data2 = bn.get_data("test.bin")
print(data1)
print("#" * 10)
print(data2)
