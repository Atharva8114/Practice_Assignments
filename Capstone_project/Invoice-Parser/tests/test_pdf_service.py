def test_pdf_to_images_empty():
    from services.pdf_service import pdf_to_images
    images = pdf_to_images(b"")
    assert images == []
