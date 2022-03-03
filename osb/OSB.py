class OSB():
    def __init__(self, filename=None, framerate=60, overwrite=False):
        self.framerate = framerate
        self.overwrite = overwrite
        if type(filename) == str:
            self.load_osb(filename)

    def load_osb(file):
        with open(file) as f:
            data = f.read()
