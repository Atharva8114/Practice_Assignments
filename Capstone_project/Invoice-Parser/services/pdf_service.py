from pdf2image import convert_from_bytes


def pdf_to_images(pdf_bytes):
    """
    Converts PDF bytes into a list of PIL Images
    """
    images = convert_from_bytes(pdf_bytes)
    return images
