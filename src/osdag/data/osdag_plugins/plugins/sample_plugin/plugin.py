class SamplePlugin:
    name = "Sample Plugin"
    version = "1.0.0"
    description = "A sample plugin"
    author = "Aathithya Sharan"

    def register(self):
        print(f"{self.name} v{self.version} Registered")
        print(f"Created by: {self.author}")
        print(f"Description: {self.description}")
        
    def get_info(self):
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author
        } 