from imagej.machine import Machine


class TestMachine:
    def test_dependencies(self):
        machine = Machine(version='1.0.0')

        assert machine.classes == 'prokaryote-1.0.0.jar'

    def test_run(self):
        machine = Machine()

        machine.run()

        assert machine.running is True

        machine.shutdown()

    def test_shutdown(self):
        machine = Machine()

        machine.run()

        machine.shutdown()

        assert machine.running is False
