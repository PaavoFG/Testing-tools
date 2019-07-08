from os import path
import random as rand
import xml.etree.ElementTree as ET


templates = {
            "Update customer information [DH-111-1]":"./xml_editors/step_data/DH-111-1.xml",
            "Create ACP [MIN] [DH-121]":"./xml_editors/step_data/DH-121.xml",
            "Requesting ACP information":"./xml_editors/step_data/DH-131-1.xml",
            "Current supplier requests customer information":"./xml_editors/step_data/DH-132-1.xml",
            "DSO requests customer information":"./xml_editors/step_data/DH-134-1.xml",
            "Third party requests customer information [MIN]":"./xml_editors/step_data/DH-135 [MIN].xml",
            "Third party requests customer information [MAX]":"./xml_editors/step_data/DH-135 [MAX].xml",
            "Create sales agreement":"./xml_editors/step_data/DH-311-1.xml",
            "Confirm grid agreement":"./xml_editors/step_data/DH-312-1.xml",
            "Give authorisation to a third party":"./xml_editors/step_data/DH-812.xml",
            "New supplier requests customer and ACP information [MIN]":"./xml_editors/step_data/DH-133-1 [MIN].xml",
            "New supplier requests customer and ACP information [MAX]":"./xml_editors/step_data/DH-133-1 [MAX].xml"
            }


def input_file_path():
    while True:
        print("Please give path to the project you wish to modify:")
        file_path = str(raw_input("Give the path of the project: ")).strip()
        print("Given file name is " + file_path)
        if path.isfile(file_path):
            return file_path
        else:
            print("\nCouldn't find the given file. Please give a new file path.")


def get_option_index(element_type, list_of_elements):
    last_index = get_options(element_type, list_of_elements)
    while True:

        # Validate that input is in integer format
        try:
            user_input = int(raw_input("Give the index of the " + element_type + ": "))
        except ValueError:
            print("\nGiven index is not a number. Please give a valid index number.")
            continue

        # Validate that the input is within allowable bounds
        if user_input < 0 or user_input >= last_index:
            print("\nInvalid index given. Please give a valid index number.")

        # If all criteria are met
        else:
            break
    return user_input
    

def get_options(element_type, list_of_elements):
    index = 0
    print("Available " + element_type + "s:\n")
    for element in list_of_elements:
        try:
            print(str(index) + " - " + element.attrib["name"])
        except AttributeError:
            print(str(index) + " - " + element)
        index += 1
    return index


def choose_template():
    template_keys = list(templates.keys())
    template_indices = validate_template_indices(template_keys)
    template_data = None
    previous_template_data = None
    for index in template_indices[::-1]:
        if template_data != None:
            previous_template_data = template_data
        template_file = templates[template_keys[int(index)]]
        template_data = ET.parse(template_file).getroot()
        template_data = finalize_new_steps(template_data)
        if previous_template_data != None:
            template_data = check_for_duplicates(previous_template_data, template_data)
            template_data.extend(previous_template_data)
    return template_data


def validate_template_indices(template_keys):
    last_index = get_options("template", template_keys)
    print("\nSelect the templates you wish to inject into the test case.")
    while True:
        invalid_input = False
        user_input = raw_input("Give index or indices of the templates you wish to insert: ")
        indices = str(user_input).split()
        for part in indices:
            try:

                # Validate that the inputted part is within allowed bounds
                if int(part) >= last_index or int(part) < 0:
                    print("One of the given indices is out of bounds. Please give a new index or sequence.")
                    invalid_input = True
                    break

            # Demand a new input if any of the parts are non-integers
            except ValueError:
                print("One of the given indices is not an integer. Please only input valid indices.")
                invalid_input = True
                break

        # If validation of all parts are successful, loop is broken and input is returned
        if not invalid_input:
            break
    return indices


def finalize_new_steps(template_data):
    template_steps = template_data.findall('.//{http://eviware.com/soapui/config}testStep')
    for step in template_steps:
        step.attrib["id"] = generate_id()
    return template_data


def generate_id():
    symbols = "abcdefghijklmnopqrstuvwxyz1234567890"
    id = ""
    for i in range (0, len(symbols)):
        if i == 8 or i == 13 or i == 18:
            id += "-"
        else:
            id += rand.choice(symbols)
    return id


def check_for_duplicates(old_data, new_data):
    new_steps = new_data.findall('.//{http://eviware.com/soapui/config}testStep')
    existing_steps = old_data.findall('.//{http://eviware.com/soapui/config}testStep')
    existing_step_names = []
    for existing_step in existing_steps[::-1]:
        existing_step_names.append(existing_step.attrib["name"])
    for step in new_steps[::-1]:
        postfix = "*"
        while True:
            if step.attrib["name"] in existing_step_names:
                step.attrib["name"] += "*"
            else:
                existing_step_names.append(step.attrib["name"])
                break
    return new_data