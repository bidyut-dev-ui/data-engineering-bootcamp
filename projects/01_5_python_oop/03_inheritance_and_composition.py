"""
03_inheritance_and_composition.py
Focus: "Is-A" vs "Has-A" relationships in pipeline architecture.
"""

# --- Inheritance ("Is-A") ---
# Used for sharing behavior and specialization.

class BaseScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def fetch(self):
        print(f"Fetching raw data from {self.base_url}")
        return "raw_data_string"

class JsonScraper(BaseScraper):
    """JsonScraper IS-A BaseScraper with specific parsing logic."""
    def parse(self, raw_data):
        print("Parsing raw data as JSON...")
        return {"data": raw_data}

# --- Composition ("Has-A") ---
# Used for building flexible systems by plugging components together.
# This is usually PREFERRED over deep inheritance in Data Engineering.

class DataPipeline:
    """A Pipeline HAS-A Scraper and HAS-A Storage."""
    def __init__(self, scraper_tool):
        # We don't inherit from Scraper, we USE it (dependency injection)
        self.scraper = scraper_tool
        self.storage = []

    def run(self):
        raw = self.scraper.fetch()
        # Check if scraper has a parse method (Polymorphism)
        if hasattr(self.scraper, 'parse'):
            processed = self.scraper.parse(raw)
        else:
            processed = raw
            
        self.storage.append(processed)
        print(f"Pipeline completed. Storage: {self.storage}")

# --- Execution ---
if __name__ == "__main__":
    print("--- Using Inheritance ---")
    js = JsonScraper("https://api.example.com")
    data = js.fetch()
    parsed = js.parse(data)

    print("\n--- Using Composition ---")
    # We plug the JsonScraper into the Pipeline
    my_pipeline = DataPipeline(scraper_tool=js)
    my_pipeline.run()

    # Key Takeaway for DE:
    # Inheritance is great for "Types of X" (e.g., PostgresLoader, S3Loader).
    # Composition is better for "The Process of X" (e.g., A Pipeline that uses a Loader).
    # "Favor composition over inheritance" to keep your code flexible.
