from common_functions import *
from shutil import copyfile
import xml.etree.ElementTree as ET


# Start of parsing process
ET.register_namespace("con", "http://eviware.com/soapui/config")
project_file_path = input_file_path()
project_data = ET.parse(project_file_path).getroot()


# Select target suite
project_suites = project_data.findall('.//{http://eviware.com/soapui/config}testSuite')
i_suite = get_element_index("suite", project_suites)


# Select target test case
project_test_cases = project_suites[i_suite].findall('.//{http://eviware.com/soapui/config}testCase')
i_case = get_element_index("case", project_test_cases)
target_case = project_test_cases[i_case]


# Select the templates you wish to insert
new_data = choose_template()
new_data = check_for_duplicates(target_case, new_data)


# Create backup and update the project file
target_case.extend(new_data)
backup_file_path = project_file_path + "_backup"
copyfile(project_file_path, backup_file_path)
with open(project_file_path, "w+") as file:
    file.write(ET.tostring(project_data))

# Closing the script
print("\nProject file updated. Remember to reload your project in the SoapUI to review changes.")