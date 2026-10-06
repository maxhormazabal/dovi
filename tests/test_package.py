import dovi


def test_public_api():
    assert isinstance(dovi.__version__, str)
    for name in ("DocumentGenerator", "DocumentReplicator", "DoviDocument"):
        assert hasattr(dovi, name)
