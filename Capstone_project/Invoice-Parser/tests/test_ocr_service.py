from services.ocr_service import run_ocr
from PIL import Image
import pytesseract

def test_run_ocr_mock(monkeypatch):
    def fake_ocr(image, output_type=None):
        return {
            "text": ["Invoice"],
            "left": [0],
            "top": [0],
            "width": [50],
            "height": [10]
        }

    monkeypatch.setattr(pytesseract, "image_to_data", fake_ocr)

    img = Image.new("RGB", (100, 100))
    words, boxes = run_ocr(img)

    assert words == ["Invoice"]
    assert len(boxes) == 1
