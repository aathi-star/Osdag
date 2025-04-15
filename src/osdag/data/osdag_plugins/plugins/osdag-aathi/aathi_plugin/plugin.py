class AathiPlugin:
    name = "Aathi Plugin"
    version = "1.0.0"
    description = "test plugin"
    author = "Aathithya Sharan"

    def register(self):
        # to resgister plugin with osdag
        print(f"{self.name} v{self.version} Registered")
        print(f"Created by: {self.author}")
        self.initialize_plugin()
        
    def initialize_plugin(self):
        print("Initializing Aathi Plugin...")
        print("Aathi Plugin initialized successfully!") 