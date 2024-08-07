from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

if __name__ == '__main__':
    images = convert_from_path('data/Sample.pdf')
    print(images)
