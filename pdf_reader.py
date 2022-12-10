import os

import PyPDF2


class PdfReader:

    @staticmethod
    def convert_to_string(path: str) -> str:
        path = os.path.abspath(path)
        ret_string = ''
        with open(path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                ret_string += text
        return ret_string
