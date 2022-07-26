from reasoner import Reasoner

file_name = "example.owl"
reasoner_type = "pellet"
sleep_time = 10
infer_property_values = True
infer_data_property_values = True

Reasoner(
        file_name = file_name,
        reasoner_type = reasoner_type,
        sleep_time = sleep_time,
        infer_property_values = infer_property_values,
        infer_data_property_values = infer_data_property_values,
).run()