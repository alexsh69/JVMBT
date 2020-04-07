from lxml.html import Element
from lxml import etree

from service.exceptions import LoadMavenPOMFileException, ProcessXPathException

class XmlFactory(object):

    @staticmethod
    def load_xml_file(xml_file):
        try:
            tree = etree.parse(xml_file)
            return tree.getroot()
        except Exception as e:
            LoadMavenPOMFileException(f"Can't load {xml_file} for XML processing. Exception: {e.with_traceback()}")

    @staticmethod
    def process_xpath(xml_file, xpath_str) -> str:
        pom_xml = XmlFactory.load_xml_file(xml_file)
        try:
            xpath = etree.XPath(xpath_str)
            result = xpath(pom_xml)
            return result[0] if len(result) == 1 else None
        except Exception as e:
            ProcessXPathException(f"Can't process XPATH {xpath_str}. Exception: {e.with_traceback()}")


