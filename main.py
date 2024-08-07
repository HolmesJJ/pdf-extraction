import os
import shutil
import layoutparser as lp

import matplotlib.pyplot as plt
from pdf2image import convert_from_path
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.styles import Alignment
from openpyxl.drawing.image import Image as OpenpyxlImage

DATA_DIR = 'data'
OUTPUT_DIR = 'output'
TEMP_DIR = 'temp'
FILE_NAME = 'TEST User Guide-F40'
INPUT_FILE = os.path.join(DATA_DIR, f'{FILE_NAME}.pdf')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f'{FILE_NAME}.xlsx')


DPI = 300
FONT_SIZE = 14


def display_image(image, title):
    plt.figure(figsize=(6, 10))
    plt.imshow(image)
    plt.title(title)
    plt.axis('off')
    plt.show()


def load_pdf(pdf_path):
    images = convert_from_path(pdf_path, dpi=DPI)
    return images


def clean_text(text):
    lines = text.split('\n')
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    return '\n'.join(cleaned_lines)


def calculate_cell_width(text):
    lines = text.split('\n')
    max_length = max(len(line) for line in lines)
    return max_length


def pixels_to_points(pixels):
    return (pixels / 96) * 72


def pixels_to_width_units(pixels):
    return pixels / 8


def run(debug=False):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_images = load_pdf(INPUT_FILE)
    model = lp.AutoLayoutModel('lp://efficientdet/PubLayNet/tf_efficientdet_d0')
    wb = Workbook()
    ws = wb.active
    row = 1
    max_cell_width = 0
    for page_number, page_image in enumerate(pdf_images, 1):
        layout = model.detect(page_image)
        if debug:
            display_image(page_image, 'Page ' + str(page_number))
        for element in layout:
            if element.type == 'Figure':
                os.makedirs(TEMP_DIR, exist_ok=True)
                img_path = os.path.join(TEMP_DIR, f'image_p{page_number}_{element.id}.png')
                segment_image = page_image.crop(element.coordinates)
                segment_image.save(img_path)
                if debug:
                    display_image(segment_image, f'Page {str(page_number)} Figure')
                img = OpenpyxlImage(img_path)
                img.width, img.height = segment_image.width, segment_image.height
                ws.add_image(img, f'A{row}')
                ws.row_dimensions[row].height = pixels_to_points(img.height)
                max_cell_width = max(max_cell_width, pixels_to_width_units(img.width))
            else:
                segment_image = page_image.crop(element.coordinates)
                text = lp.TesseractAgent().detect(segment_image)
                cleaned_text = clean_text(text)
                if debug:
                    print('=' * 10)
                    print(cleaned_text)
                    print('=' * 10)
                    display_image(segment_image, f'Page {str(page_number)} Title / Text / List')
                cell = ws[f'A{row}']
                cell.value = cleaned_text
                cell.alignment = Alignment(wrapText=True, vertical='center')
                if element.type == 'Title':
                    cell.font = Font(size=FONT_SIZE + 2, bold=True)
                else:
                    cell.font = Font(size=FONT_SIZE)
                num_lines = cleaned_text.count('\n') + 1
                ws.row_dimensions[row].height = 20 * num_lines
                cell_width = calculate_cell_width(cleaned_text)
                max_cell_width = max(max_cell_width, cell_width)
            row += 1
    ws.column_dimensions['A'].width = max_cell_width
    wb.save(OUTPUT_FILE)
    wb.close()
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)


if __name__ == '__main__':
    print(list(lp.models.auto_layoutmodel.ALL_AVAILABLE_BACKENDS))
    print(len(convert_from_path(INPUT_FILE)))
    run(debug=False)
