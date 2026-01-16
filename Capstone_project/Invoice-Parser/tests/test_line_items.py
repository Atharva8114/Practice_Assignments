from services.line_item_extractor import extract_line_items

def test_extract_line_items():
    words = ["Paper", "10", "25.00", "Pens", "5", "2.00"]
    boxes = [[0,0,10,10]] * len(words)

    items = extract_line_items(words, boxes)

    assert isinstance(items, list)
    assert len(items) > 0
