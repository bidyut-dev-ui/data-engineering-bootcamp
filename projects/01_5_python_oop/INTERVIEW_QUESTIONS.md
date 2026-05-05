# Senior/Lead Interview Questions: OOP & Python Architecture

### Q1: What is the difference between a @classmethod and a @staticmethod? When would you use each in a data pipeline?
**Answer:** 
- `@classmethod` takes `cls` as the first argument. Use it for "Factory" methods (e.g., creating a `DatabaseClient` from an environment variable string).
- `@staticmethod` takes no implicit first argument. Use it for utility functions that belong logically to the class but don't need any state (e.g., validating a string format).

### Q2: Why is "Composition over Inheritance" often preferred in Data Engineering?
**Answer:** Inheritance creates a tight coupling ("is-a" relationship). If you change the base class, everything breaks. Composition ("has-a" relationship) allows you to swap components easily. For example, a `Pipeline` class that takes any `Loader` object is much more flexible than a `Pipeline` that *is* a `Loader`.

### Q3: How do Abstract Base Classes (ABCs) help in a team of Data Engineers?
**Answer:** ABCs act as "Data Contracts". They ensure that any new component (like a new `FileExchanger`) implements the required methods (like `send()` and `receive()`). This prevents runtime errors and allows the Lead to define the architecture while others implement the details.

### Q4: What is the `super()` function used for?
**Answer:** `super()` allows you to call methods from a parent class. It is commonly used in `__init__` to ensure the parent class is initialized properly before adding child-specific logic.

### Q5: Scenario: You need to implement a library that supports multiple database types (Redshift, BigQuery, Snowflake). How would you use OOP to design this?
**Answer:**
1. Create an ABC `BaseDataClient` with abstract methods `query()` and `upload()`.
2. Implement concrete classes `RedshiftClient`, `BigQueryClient`, etc., that inherit from `BaseDataClient`.
3. Create a `ClientFactory` class with a static method that returns the correct client based on a configuration string.
4. The rest of the application code only interacts with the `BaseDataClient` interface, making it agnostic to the underlying database.
