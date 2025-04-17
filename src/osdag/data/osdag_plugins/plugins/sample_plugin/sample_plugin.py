class SamplePlugin:
    def __init__(self):
        self.name = "Sample Plugin"
        self.version = "1.0.0"
        self.description = "A sample plugin"
        self.author = "Aathithya Sharan"

    def register(self):
        print("Sample plugin registered")
        return True 