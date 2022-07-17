import xml.etree.ElementTree as ET
import os
from Core.utilities import QList

if __name__ == "__main__":

    junit_xml = os.environ['junitxml.path']
    test_suite_name = os.environ['testsuite.name']

    print("Processing: " + junit_xml)
    print("Changing to test suite name: " + test_suite_name)

    path = os.path.join(os.getcwd(), junit_xml)
    with open(path, 'r') as f:
        tree = ET.parse(path)

    root = tree.getroot()

    test_suite = QList(root).first()

    test_suite_attributes = test_suite.attrib

    print("Changing test suite from " + test_suite_attributes['name'] + " to " + test_suite_name)
    test_suite_attributes['name'] = test_suite_name

    with open(junit_xml, 'wb') as f:
        tree.write(f)