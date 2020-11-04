from unittest import TestCase

from libs.constants import TEST_INPUT_PATH
from libs.pdf_parser import PdfParser
from libs.utils import get_personal_elements_from_personal_info


class TestPdfParser(TestCase):

    def test_pdf_reader(self):
        pdf_parser = PdfParser(TEST_INPUT_PATH, None)
        pdf_parser.open_pdf_file()
        pdf_parser.parse_and_populate()
        pdf_parser.merge_parsed_info_with_derived_details()

        self.assertEqual(['name', 'email', 'address', 'Education', 'Leadership Experience',
                          'Professional Experience', 'Additional Projects', 'Skills & Interests'],
                         pdf_parser.get_parsed_dict_keys())


    def test_deriving_personal_elements(self):
        test_personal_info = ['Aswin Jose Roy', '(XXX) XXX-XXX | zerokool@gmail.com |', 'City, State Zip Code']
        personal_elements_dict = get_personal_elements_from_personal_info(test_personal_info)
        self.assertEqual({'name': 'Aswin Jose Roy', 'email': 'zerokool@gmail.com',
                          'address': '(XXX) XXX-XXX City, State Zip Code'},
                         personal_elements_dict)
