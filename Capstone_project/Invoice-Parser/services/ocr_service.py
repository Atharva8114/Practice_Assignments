import pytesseract
from PIL import Image

# If needed for Windows local testing (Docker already has it)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def run_ocr(image: Image.Image):
    """
    Runs Tesseract OCR and returns:
    - words: list[str]
    - boxes: list[list[int]] normalized to LayoutLM format (0–1000)
    """

    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    words = []
    boxes = []

    width, height = image.size

    for i in range(len(data["text"])):
        text = data["text"][i].strip()
        if not text:
            continue

        x, y, w, h = (
            data["left"][i],
            data["top"][i],
            data["width"][i],
            data["height"][i],
        )

        # Normalize bounding box to 0–1000
        box = [
            int(1000 * x / width),
            int(1000 * y / height),
            int(1000 * (x + w) / width),
            int(1000 * (y + h) / height),
        ]

        words.append(text)
        boxes.append(box)

    return words, boxes
