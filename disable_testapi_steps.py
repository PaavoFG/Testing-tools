import common_functions as cf
import shutil
import xml.etree.ElementTree as ET


# Start of parsing process
ET.register_namespace("con", "http://eviware.com/soapui/config")
project_file_path = cf.input_file_path()
project_data = ET.parse(project_file_path).getroot()


# Give options to user
options = ["disable", "enable"]
option = cf.get_element_index("option", options)


# Run the selected option for all test steps in the project
project_suites = project_data.findall('.//{http://eviware.com/soapui/config}testSuite')
for suite in project_suites:
    project_test_cases = suite.findall('.//{http://eviware.com/soapui/config}testCase')
    for case in project_test_cases:
        for step in case.findall('.//{http://eviware.com/soapui/config}testStep'):
            if "testapi" in step.attrib["name"].lower():
                if option == 0:
                    step.set("disabled", "true")
                else:
                    step.attrib.pop("disabled", None)


# Create backup and update the project file
backup_file_path = project_file_path + "_backup"
shutil.copyfile(project_file_path, backup_file_path)
with open(project_file_path, "w+") as file:
    file.write(ET.tostring(project_data))

# Closing the script
print("All Test API steps have been " + options[option] + "d. Remember to reload your project to make the changes effective.")
    