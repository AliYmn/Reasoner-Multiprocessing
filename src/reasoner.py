from http.client import IM_USED
from owlready2 import get_ontology,Imp, sync_reasoner,sync_reasoner_hermit,sync_reasoner_pellet,destroy_entity


class Reasoner:
    def __init__(self, file_name: str, reasoner_type: str, sleep_time: int, 
                infer_property_values : bool, infer_data_property_values : bool) -> None:
        self.file_name = file_name
        self.reasoner_type = reasoner_type
        self.sleep_time = sleep_time
        self.infer_property_values = infer_property_values
        self.infer_data_property_values = infer_data_property_values

    def ontoLoad(self) -> object:
        try:
            onto = get_ontology(self.file_name).load()
            return onto
        except FileNotFoundError:
            print("The specified file was not found in the location. '{file_name}'".format(file_name=self.file_name))

    def deleteAllRules(self) -> None:
        for rule in self.ontoLoad.rules():
            destroy_entity(rule)
        self.ontoLoad.save()

    def getRules(self) -> object:
        rules = []
        rule = self.ontoLoad().rules()
        if len(list(rule)) == 0:
            raise Exception("There not found any rule.")
        else:
            for r in rule:
                rules.append(r)
            self.deleteAllRules()
            return rule 

    def reasonerType(self) -> object:
        if self.reasoner_type == "pellet":
            return sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)
        elif self.reasoner_type == "hermit":
            return sync_reasoner_hermit(infer_property_values=self.infer_property_values)
        else:
            return sync_reasoner(infer_property_values = self.infer_property_values, infer_data_property_values = self.infer_data_property_values)
        
    def run(self):
        with self.ontoLoad():
            reasonerImp = Imp()
            for rule in self.getRules():
                reasonerImp.set_as_rule("""{rule_syntax}""".format(rule_syntax=rule))
                self.ontoLoad().save()
                self.reasonerType()
            self.deleteAllRules()
            
# if __name__ == '__main__':
#     reasoner = Reasoner(file_name="dsm.owl", reasoner_type=" ")
#     print('reasoner: ', reasoner)
