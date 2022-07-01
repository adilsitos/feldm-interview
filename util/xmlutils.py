import xml.etree.ElementTree as ET

class XMLUtils:
    def __init__(self, xmlfile: str = "./eurofxref-hist-90d.xml"):
        self.filename = xmlfile
        self.xmlRoot = self.parseXML()
        
    def parseXML(self):
        tree = ET.parse(self.filename)
        root = tree.getroot()
        return root

    def getConversionRates(self, currency: str = "USD"):
        conversion_rates = {}

        namespace = {"url": "http://www.ecb.int/vocabulary/2002-08-01/eurofxref"}
        
        for cube in self.xmlRoot.findall(".//url:Cube[@time]", namespaces=namespace):
            for child in cube.iter():
               if child.get('currency') == currency:
                conversion_rates[cube.get('time') + " 00:00:00"] = float(child.get('rate'))
        return conversion_rates