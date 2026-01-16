def test_extract_entities_import():
    import services.layoutlm_service as svc
    assert hasattr(svc, "extract_entities")
