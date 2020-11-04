from libs.constants import PERSONAL_INFO_HEADING, DUMMY_OUTPUT_PATH
from libs.utils import get_personal_elements_from_personal_info

class PdfParser:

    def __init__(self, input_path, output_path):
        self._input_path = input_path
        self._output_path = output_path
        self._parsed_text_list = None
        self._parsed_dict = None

    def open_pdf_file(self):
        """

        opens pdf file using the linux utility ps2ascii

        this module can be improved by removing the file write-read-delete paradigm used below and
        reading directly from ps2ascii's output

        """
        if self._input_path is None:
            raise Exception("Please provide a pdf file path. ")
        import os
        os.system("ps2ascii %s %s" % (self._input_path, DUMMY_OUTPUT_PATH))

        f = open(DUMMY_OUTPUT_PATH, "r")
        data = f.read()
        f.close()
        os.remove(DUMMY_OUTPUT_PATH)
        self._parsed_text_list = [" ".join(x.strip().split()) for x in data.split('\n')]

    def parse_and_populate(self):
        """
        this method parsed the text extracted from the pdf and processes it

        """
        current_heading = PERSONAL_INFO_HEADING
        self._parsed_dict = {current_heading: []}
        for i in range(len(self._parsed_text_list) - 1):
            if not self._parsed_text_list[i + 1]:
                if self._parsed_text_list[i]:
                    if current_heading == PERSONAL_INFO_HEADING:
                        self._parsed_dict[current_heading].append(self._parsed_text_list[i])
                    else:
                        self._parsed_dict[current_heading] = ' '.join([self._parsed_dict[current_heading], self._parsed_text_list[i]])
            elif not self._parsed_text_list[i + 1].strip("_"):
                current_heading = self._parsed_text_list[i]
                self._parsed_dict[current_heading] = ''
                self._parsed_text_list[i + 1] = self._parsed_text_list[i + 1].strip("_")
            else:
                if self._parsed_text_list[i]:
                    if current_heading == PERSONAL_INFO_HEADING:
                        self._parsed_dict[current_heading].append(self._parsed_text_list[i])
                    else:
                        self._parsed_dict[current_heading] = ' '.join([self._parsed_dict[current_heading], self._parsed_text_list[i]])

    def merge_parsed_info_with_derived_details(self):
        """
        derives required information and removes redundant data

        """
        personal_elements_dict = get_personal_elements_from_personal_info(self._parsed_dict[PERSONAL_INFO_HEADING])
        self._parsed_dict.pop(PERSONAL_INFO_HEADING)
        self._parsed_dict = {**personal_elements_dict, **self._parsed_dict}

    def get_parsed_dict_keys(self):
        """

        :return: a list of keys of the parsed data dict
        """
        return list(self._parsed_dict.keys())

    def write_parsed_data_to_json_file(self):
        """

        this method simply dumps the parsed data (dict) to a json file on disk

        """
        import json
        with open(self._output_path, 'w') as fp:
            json.dump(self._parsed_dict, fp, indent=4)
        fp.close()


    def process(self):
        """

        takes care of the flow of the steps necessary to do the processing the pdf file -> json file

        """
        self.open_pdf_file()
        self.parse_and_populate()
        self.merge_parsed_info_with_derived_details()
        self.write_parsed_data_to_json_file()
