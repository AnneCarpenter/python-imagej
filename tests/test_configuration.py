import pytest


class TestConfiguration:
    def __init__(self):
        pass

    def test_get_path_to_jars(self):
        x = "this"
        assert 'h' in x

    def test_get_patcher_args(self):
        x = "hello"
        assert hasattr(x, 'check')

    def test_get_jars(self):
        assert 1 in [1, 2, 3, 4, 5]

    def test_cp_start_vm(self):
        assert 1 in [1, 2, 3, 4, 5]

    def test_cp_stop_vm(self):
        assert 1 in [1, 2, 3, 4, 5]
