from owlready2 import (
    Imp,
    destroy_entity,
    get_ontology,
    sync_reasoner,
    sync_reasoner_hermit,
    sync_reasoner_pellet,
)


class Reasoner:
    def __init__(
        self,
        file_name: str,
        reasoner_type: str,
        sleep_time: int,
        infer_property_values: bool,
        infer_data_property_values: bool,
    ):
        self.file_name = file_name
        self.reasoner_type = reasoner_type
        self.sleep_time = sleep_time
        self.infer_property_values = infer_property_values
        self.infer_data_property_values = infer_data_property_values

    def ontoLoad(self) -> object:
        try:
            return get_ontology(self.file_name).load()
        except FileNotFoundError:
            print("The specified file was not found in the location.'{file_name}'".format(file_name=self.file_name))

    def saveOnto(self) -> None:
        onto = get_ontology(self.file_name)
        onto.save(self.file_name)

    def reasonerType(self) -> object:
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
        for rule in self.ontoLoad().rules():
            destroy_entity(rule)
        self.saveOnto()

    def getRules(self) -> object:
        rules = []
        for rule in self.ontoLoad().rules():
            rules.append(rule)

        return rules

    def insertRules(self, rules) -> None:
        with self.ontoLoad():
            reasonerImp = Imp()
            for rule in rules:
                reasonerImp.set_as_rule("""{rule}""".format(rule=rule))
                self.saveOnto()

    def run(self) -> None:
        rules = self.getRules()
        self.deleteAllRules()
        with self.ontoLoad():
            reasonerImp = Imp()
            for rule in rules:
                reasonerImp.set_as_rule("""{rule}""".format(rule=rule))
                self.saveOnto()
                self.reasonerType()
                self.deleteAllRules()

        self.insertRules(rules)
