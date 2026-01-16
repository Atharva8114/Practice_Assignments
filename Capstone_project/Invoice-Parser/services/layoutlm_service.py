import torch
from transformers import LayoutLMv3Processor, LayoutLMv3Model

MODEL = "microsoft/layoutlmv3-base"

# IMPORTANT: apply_ocr=False because we use Tesseract
processor = LayoutLMv3Processor.from_pretrained(
    MODEL,
    apply_ocr=False
)

model = LayoutLMv3Model.from_pretrained(MODEL)
model.eval()


def extract_entities(image, words, boxes):
    """
    Runs LayoutLMv3 embeddings using external OCR (Tesseract)
    """
    encoding = processor(
        image,
        words,
        boxes=boxes,
        return_tensors="pt",
        truncation=True
    )

    with torch.no_grad():
        outputs = model(
            input_ids=encoding["input_ids"],
            bbox=encoding["bbox"],
            attention_mask=encoding["attention_mask"],
            pixel_values=encoding["pixel_values"],
        )

    # Return OCR tokens (layout-aware)
    return encoding.tokens()
