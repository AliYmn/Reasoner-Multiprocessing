from owlready2 import get_ontology


class Reasenor:
    def __init__(self, file_name: str, reasenor_type: str, rules: object, sleep_time: int) -> None:
        self.file_name = file_name
        self.reasenor_type = reasenor_type
        self.rules = rules
        self.sleep_time = sleep_time

    def onto(self) -> object:
        try:
            onto = get_ontology(self.file_name).load()
            return onto
        except FileNotFoundError:
            print("The specified file was not found in the location. '{file_name}'".format(file_name=self.file_name))


if __name__ == '__main__':
    reasenor = Reasenor(file_name="dsm.owl", reasenor_type=" ").loadRule()
    print('reasenor: ', reasenor)
