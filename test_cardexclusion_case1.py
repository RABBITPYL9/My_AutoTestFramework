import requests
import unittest
import xml.etree.ElementTree as et

def fixed_xml_body_as_string():#тело запроса в виде xml
    return """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mux="http://www.psit.ru/3CardF/MUXAntiFraud">
   <soapenv:Header/>
   <soapenv:Body>
      <mux:CardExclusionRequest>
         <mux:Action>Add</mux:Action>
         <mux:Card>
            <!--You have a CHOICE of the next 2 items at this level-->
            
            
         <mux:Pan>4592261124724562</mux:Pan></mux:Card>
         <!--Optional:-->
         <mux:StartDateTime>2021-05-14T00:00:00.000+04:00</mux:StartDateTime>
         <!--Optional:-->
         <mux:EndDateTime>2021-05-14T00:00:00.000+04:00</mux:EndDateTime>
         <!--Optional:-->
         <mux:CountryList>
            <!--1 or more repetitions:-->
            <mux:Country>ABW</mux:Country>
         </mux:CountryList>
      </mux:CardExclusionRequest>
   </soapenv:Body>
</soapenv:Envelope>
"""

NSMAP = {
    'soapenv': "http://schemas.xmlsoap.org/soap/envelope/",
    'mux': "http://www.psit.ru/3CardF/MUXAntiFraud"
}

class CardExclusionAddTest(unittest.TestCase):#получение и проверка даты начала,конца отпуска(исключения), страны отпуска
    def test_send_xml_body_from_string_check_status_code_and_content_type(self):
        response = requests.post("http://192.168.131.158:8088",headers={"Content-Type": "text/xml"},data=fixed_xml_body_as_string())
        #response_body_as_xml = et.fromstring(response.content)
        #xml_tree = et.ElementTree(response_body_as_xml)
        answer = response.content
        response_body_as = et.fromstring(answer)
        xml_tr = et.ElementTree(response_body_as)
        status_code = response.status_code
        assert status_code == 200
        structure_startdate = xml_tr.find('*//mux:StartDateTime', namespaces=NSMAP)
        assert structure_startdate.text == '2021-05-12T00:00:00'
        structure_enddate = xml_tr.find('*//mux:EndDateTime', namespaces=NSMAP)
        assert structure_enddate.text == '2021-05-20T00:00:00'
        structure_country = xml_tr.find('*//mux:Country', namespaces=NSMAP)
        assert structure_country.text == 'ABW'
