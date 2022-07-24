import time

from owlready2 import (
    Imp,
    destroy_entity,
    get_ontology,
    sync_reasoner,
    sync_reasoner_hermit,   
    sync_reasoner_pellet,
)


class Reasoner:
    """
    Semantic Reasenor Multiprocessing Java OutOfMemoryError Solution
    """

    def __init__(
        self,
        file_name: str,
        reasoner_type: str,
        sleep_time: int,
        infer_property_values: bool,
        infer_data_property_values: bool,
    ):
        """
        # Arguments Descriptions #
        file_name : owl file name. (ex : example.owl or /users/user/example.owl)
        reasoner_type : pellet, helmet or reasoner
        sleep_time : sleep second
        infer_property_values : True or False
        infer_data_property_values : True or False
        """
        self.file_name = file_name
        self.reasoner_type = reasoner_type
        self.sleep_time = sleep_time
        self.infer_property_values = infer_property_values
        self.infer_data_property_values = infer_data_property_values

    def ontoLoad(self) -> object:
        """owl file to the system."""
        try:
            print("This Owl file : {file_name} loaded.".format(file_name=self.file_name))
            return get_ontology(self.file_name).load()
        except FileNotFoundError:
            print("The specified file was not found in the location.'{file_name}'".format(file_name=self.file_name))

    def saveOnto(self) -> None:
        """saves the owl file."""
        print("This Owl file : {file_name} saved.".format(file_name=self.file_name))
        onto = get_ontology(self.file_name)
        onto.save(self.file_name)

    def reasonerType(self) -> object:
        """Determines the reasoner type."""
        print("It was started in Reasoner with this type : {reasoner_type}".format(reasoner_type=self.reasoner_type))
        if self.reasoner_type == "pellet":
            return sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
        elif self.reasoner_type == "hermit":
            return sync_reasoner_hermit(infer_property_values=self.infer_property_values)
        else:
            return sync_reasoner(
                infer_property_values=self.infer_property_values,
                infer_data_property_values=self.infer_data_property_values,
            )

    def deleteAllRules(self) -> None:
        """Deletes all rules."""
        count = len(list(self.ontoLoad().rules()))
        print("All rules have been deleted. (Count : {count})".format(count=count))
        for rule in self.ontoLoad().rules():
            destroy_entity(rule)
        self.saveOnto()

    def getRules(self) -> object:
        """All Rules return."""
        print("Getting All Rules...")
        rules = []
        for rule in self.ontoLoad().rules():
            rules.append(rule)

        return rules

    def insertRules(self, rules) -> None:
        """Insert All Rules"""
        print("All Rules have been added again.")
        with self.ontoLoad():
            reasonerImp = Imp()
            for rule in rules:
                reasonerImp.set_as_rule("""{rule}""".format(rule=rule))
                self.saveOnto()

    def sleepReasoner(self) -> None:
        """Sleep reasoner"""
        print("Sleeping a {time} sec".format(time=self.sleep_time))
        time.sleep(self.sleep_time)

    def run(self) -> None:
        """It runs the entire algorithm."""
        rules = self.getRules()
        print('rules: ', rules)
        self.deleteAllRules()
        with self.ontoLoad():
            reasonerImp = Imp()
            for rule in rules:
                reasonerImp.set_as_rule("""{rule}""".format(rule=rule))
                self.saveOnto()
                self.reasonerType()
                self.deleteAllRules()
                self.sleepReasoner()
                # You should check if reasoner found result...
                # for example ;
                """
                    for p in self.ontoPatients:
                        if p.hasDisease:
                            print("#### Disease found!...")
                """
        self.insertRules(rules)
        print("Successfully Completed.")
