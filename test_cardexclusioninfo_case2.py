import requests
import unittest
import xml.etree.ElementTree as et

def fixed_xml_body_as_string():
    return """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mux="http://www.psit.ru/3CardF/MUXAntiFraud">
   <soapenv:Header/>
   <soapenv:Body>
      <mux:CardExclusionInfoRequest>
         <mux:Card>
            <!--You have a CHOICE of the next 2 items at this level-->
            
            
         <mux:Pan>6479020100075230</mux:Pan></mux:Card>
      </mux:CardExclusionInfoRequest>
   </soapenv:Body>
</soapenv:Envelope>
"""

NSMAP = {
    'soapenv': "http://schemas.xmlsoap.org/soap/envelope/",
    'mux': "http://www.psit.ru/3CardF/MUXAntiFraud"
}

class CardExclusionInfoTest(unittest.TestCase):
    def test_send_xml_body_from_string_check_status_code_and_content_type(self):
        response = requests.post("http://192.168.131.158:8088",headers={"Content-Type": "text/xml"},data=fixed_xml_body_as_string())
        response_body_as_xml = et.fromstring(response.content)
        xml_tree = et.ElementTree(response_body_as_xml)
        answer = response.content
        response_body_as = et.fromstring(answer)
        xml_tr = et.ElementTree(response_body_as)
        savings_accounts = xml_tr.find('*//mux:Country', namespaces=NSMAP)
        assert savings_accounts.text == 'ABW'
