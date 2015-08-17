from os.path import relpath
import javabridge


class Machine:
    def __init__(self, version='1.0.0'):
        """

        :param version : String

        :rtype : Machine
        """
        self.arguments = [
            '-Djava.awt.headless=true',
            '-Djava.util.prefs.PreferencesFactory=' + 'org.cellprofiler.headlesspreferences.HeadlessPreferencesFactory',
            '-Dloci.bioformats.loaded=true',
            '-Dlogback.configurationFile=logback.xml',
        ]

        self.classes = relpath('./prokaryote-{}.jar'.format(version))

        self.running = False

    def run(self):
        """

        :rtype : None
        """
        if not self.running:
            javabridge.start_vm(self.arguments)

            self.running = True

    def shutdown(self):
        """

        :rtype : None
        """
        if self.running:
            javabridge.kill_vm()

            self.running = False
