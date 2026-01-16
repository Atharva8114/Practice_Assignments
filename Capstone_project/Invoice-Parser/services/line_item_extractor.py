from collections import defaultdict
import re


def extract_line_items(words, boxes):
    """
    words: OCR words list
    boxes: bounding boxes (normalized 0–1000)
    """

    rows = defaultdict(list)

    for word, box in zip(words, boxes):
        y_center = (box[1] + box[3]) // 2
        rows[y_center // 20].append((word, box))

    line_items = []

    for _, row in rows.items():
        row_text = " ".join(w for w, _ in row)

        # Quantity
        qty_match = re.search(r"\b\d+\b", row_text)
        price_match = re.findall(r"\d+\.\d{2}", row_text)

        if qty_match and len(price_match) >= 1:
            item = {
                "description": re.sub(r"\d+|\d+\.\d{2}", "", row_text).strip(),
                "quantity": int(qty_match.group()),
                "unit_price": float(price_match[0]),
                "amount": float(price_match[-1]) if len(price_match) > 1 else None
            }
            line_items.append(item)

    return line_items
