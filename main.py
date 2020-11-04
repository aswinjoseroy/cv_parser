import sys

from libs.pdf_parser import PdfParser

# Driver Code
if __name__ == "__main__":
    """
    example usage:

    python main.py --input tests/resources/Interview_sample_data.pdf --output output.json

    """
    arguments_list = sys.argv
    input_file = arguments_list[2]
    output_file = arguments_list[4]
    cv_parser = PdfParser(input_file, output_file)
    cv_parser.process()
