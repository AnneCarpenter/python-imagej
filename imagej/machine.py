from os.path import relpath
import javabridge


class Machine:
    def __init__(self, version='1.0.0'):
        self.dependencies = relpath('./prokaryote-{}.jar'.format(version))

        self.running = False

    def run(self):
        if not self.running:
            javabridge.start_vm()

            self.running = True

    def shutdown(self):
        if self.running:
            javabridge.kill_vm()

            self.running = False
