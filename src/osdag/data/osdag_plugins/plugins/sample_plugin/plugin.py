class SamplePlugin:
    name = "Sample Plugin"
    version = "1.0.0"
    description = "A sample plugin demonstrating the plugin system"
    author = "Aathithya Sharan"

    def register(self):
        #register  plugin
        print(f"{self.name} v{self.version} Registered")
        print(f"Created by: {self.author}")
        print(f"Description: {self.description}")
        
    def get_info(self):
        #return plugin info
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author
        } 