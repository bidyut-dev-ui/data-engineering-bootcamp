# GOTCHAS & BEST PRACTICES: OOP in Data Engineering

## 1. Don't use "Self" as a Garbage Bin
**Gotcha:** Storing massive datasets in `self.data` can lead to memory leaks if instances are not cleaned up.
**Best Practice:** Only store configuration and metadata in `self`. Pass large datasets as arguments to methods and let them go out of scope.

## 2. Favor Composition over Inheritance
**Gotcha:** Creating a deep inheritance tree (e.g., `Base -> Database -> Postgres -> ProdPostgres`) makes code rigid and impossible to test.
**Best Practice:** Build small, focused classes and "plug" them into each other. If you need a Postgres client in a pipeline, pass it as an argument (`__init__(self, db_client)`).

## 3. Be careful with Class Variables
**Gotcha:** Modifying a class variable (`cls.DEFAULT_TIMEOUT = 10`) changes it for ALL instances globally.
**Best Practice:** Use class variables for constants, but use instance variables (`self.timeout`) for anything that might vary between connections.

## 4. Use Abstract Base Classes (ABCs) for Data Contracts
**Gotcha:** Writing code that assumes a `loader` object has a `load()` method, only to have it crash at runtime with `AttributeError`.
**Best Practice:** Inherit from an ABC to catch these errors at **instantiation time**. If you forget to implement `load()`, Python won't even let the program start.

## 5. Avoid "God Objects"
**Gotcha:** Creating a single `PipelineManager` class that does extraction, transformation, loading, logging, AND alerting.
**Best Practice:** One class per responsibility. One for `Extractor`, one for `Transformer`, one for `Loader`. A `Manager` then coordinates them.
