from typing import Dict, Tuple

from PIL import Image
import fitz

from newspaper_segmentation_client import run_newspaper_segmentation_on_image


def render_pdf_page(page: fitz.Page, dpi: int = 150) -> Image:
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat, annots=False, alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def bbox_to_textract_bounding_box(bbox: Tuple[float, float, float, float], image_box) -> Dict:
    left = min(max(0.0, (bbox[0] - image_box[0]) / (image_box[2] - image_box[0])), 1.0)
    top = min(max(0.0, (bbox[1] - image_box[1]) / (image_box[3] - image_box[1])), 1.0)
    right = min(max(0.0, (bbox[2] - image_box[0]) / (image_box[2] - image_box[0])), 1.0)
    bottom = min(max(0.0, (bbox[3] - image_box[1]) / (image_box[3] - image_box[1])), 1.0)
    return {'Width': right - left, 'Height': bottom - top, 'Left': left, 'Top': top}


def extract_pdf_text_to_textract_format(page: fitz.Page) -> Dict:
    pdf_text_textract_format = {
        'Rotation': 0.0,
        'Blocks': [{
            'BlockType': 'PAGE',
            'Text': '',
            'Id': '1',
            'Geometry': {
                'BoundingBox': {"Width": 1.0, "Height": 1.0, "Top": 0.0, "Left": 0.0},
                'Polygon': [{'X': 0.0, 'Y': 0.0}, {'X': 1.0, 'Y': 0.0}, {'X': 1.0, 'Y': 1.0}, {'X': 0.0, 'Y': 1.0}]
            }
        }]
    }
    page_text = page.get_text("dict")
    line_id = 2
    line_ids = []
    for block in page_text["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            line_text = "".join(span["text"] for span in line["spans"])
            if not line_text:
                continue
            image_box = page.bound()
            textract_bounding_box = bbox_to_textract_bounding_box(line["bbox"], image_box)
            x_min, y_min, x_max, y_max = textract_bounding_box["Left"], textract_bounding_box["Top"], \
                textract_bounding_box["Left"] + textract_bounding_box["Width"], \
                textract_bounding_box["Top"] + textract_bounding_box["Height"]

            polygon = [{'X': x_min, 'Y': y_min}, {'X': x_max, 'Y': y_min}, {'X': x_max, 'Y': y_max},
                       {'X': x_min, 'Y': y_max}]

            pdf_text_textract_format["Blocks"].append({
                'BlockType': 'LINE',
                'Text': line_text,
                'Id': str(line_id),
                'Geometry': {
                    'BoundingBox': textract_bounding_box,
                    'Polygon': polygon
                }
            })

            line_ids.append(str(line_id))
            line_id += 1

    pdf_text_textract_format["Blocks"][0]["Relationships"] = [
        {"Ids": line_ids, "Type": "CHILD"}
    ]

    return pdf_text_textract_format


def run_newspaper_segmentation_on_pdf_page(page: fitz.Page, api_key: str):
    image = render_pdf_page(page)
    pdf_text = extract_pdf_text_to_textract_format(page)
    return run_newspaper_segmentation_on_image(image, pdf_text, api_key)
