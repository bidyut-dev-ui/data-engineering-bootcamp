# Apache Airflow Interview Questions

## Overview
This document contains interview questions for Apache Airflow, focusing on workflow orchestration, DAG design, error handling, and optimization for data engineering pipelines. Questions are categorized by difficulty level and include practical scenarios relevant to the 8GB RAM constraint environment.

## Table of Contents
1. [Beginner Questions](#beginner-questions)
2. [Intermediate Questions](#intermediate-questions)
3. [Advanced Questions](#advanced-questions)
4. [Behavioral & Scenario Questions](#behavioral--scenario-questions)
5. [Practical Exercises](#practical-exercises)
6. [Evaluation Rubric](#evaluation-rubric)

---

## Beginner Questions

### 1. Core Concepts
**Q1.1:** What is Apache Airflow and what problem does it solve in data engineering?
**Q1.2:** Explain the key components of Airflow architecture (Webserver, Scheduler, Executor, Metadata Database).
**Q1.3:** What is a DAG (Directed Acyclic Graph) in Airflow? Why must it be acyclic?
**Q1.4:** Differentiate between Operators, Tasks, and DAGs in Airflow.
**Q1.5:** What are the different types of Operators available in Airflow? Give examples of when you'd use each.

### 2. Basic DAG Creation
**Q2.1:** Write a simple DAG that prints "Hello World" using PythonOperator.
**Q2.2:** How do you define task dependencies in Airflow? Show examples using `>>`, `<<`, and `set_upstream`/`set_downstream`.
**Q2.3:** What is `default_args` in a DAG and what common parameters does it include?
**Q2.4:** Explain the purpose of `start_date`, `schedule_interval`, and `catchup` parameters.
**Q2.5:** How do you prevent a DAG from running on a schedule? What's the difference between `schedule_interval=None` and `schedule_interval='@once'`?

### 3. Airflow UI & Monitoring
**Q3.1:** What information can you find in the Airflow UI's Tree View vs Graph View?
**Q3.2:** How do you manually trigger a DAG run from the UI? What happens when you do?
**Q3.3:** Where can you find task logs in the Airflow UI and what information do they contain?
**Q3.4:** What do the different task instance statuses mean (success, failed, running, queued, skipped)?
**Q3.5:** How do you clear a task instance and what are the implications?

---

## Intermediate Questions

### 4. Task Communication & Data Flow
**Q4.1:** What are XComs and when should you use them? What are their limitations?
**Q4.2:** Demonstrate how to push and pull data between tasks using XComs.
**Q4.3:** What are the alternatives to XComs for passing data between tasks in production?
**Q4.4:** How do you handle large data payloads that shouldn't be stored in the metadata database?
**Q4.5:** Explain the concept of TaskFlow API in Airflow 2.0+ and how it simplifies task dependencies.

### 5. Error Handling & Reliability
**Q5.1:** How do you configure retries for a task? What parameters control retry behavior?
**Q5.2:** What is the difference between `retries`, `retry_delay`, and `max_retry_delay`?
**Q5.3:** How do you implement task failure callbacks and success callbacks?
**Q5.4:** What are Sensors in Airflow and when would you use them? Give examples.
**Q5.5:** How do you handle external dependency failures (e.g., API downtime, database unavailability)?

### 6. Scheduling & Execution
**Q6.1:** Explain cron expressions in Airflow scheduling with examples.
**Q6.2:** What is the difference between `execution_date`, `start_date`, and `data_interval_start`?
**Q6.3:** How does Airflow handle DAG runs that are missed due to scheduler downtime?
**Q6.4:** What are the best practices for setting `start_date` to avoid unexpected DAG runs?
**Q6.5:** How do you implement backfilling in Airflow and when is it useful?

### 7. Resource Optimization (8GB RAM Focus)
**Q7.1:** What Airflow configuration parameters would you tune for a system with 8GB RAM?
**Q7.2:** How does the `parallelism`, `dag_concurrency`, and `max_active_runs` settings affect memory usage?
**Q7.3:** What strategies can you use to reduce memory footprint of Airflow components?
**Q7.4:** How do you monitor Airflow's memory usage and identify memory leaks?
**Q7.5:** What are lightweight alternatives to the standard Airflow operators for memory-constrained environments?

---

## Advanced Questions

### 8. DAG Design Patterns
**Q8.1:** Describe the "factory pattern" for DAG generation and when you'd use it.
**Q8.2:** How do you implement dynamic DAG generation based on external configuration?
**Q8.3:** What are subDAGs and why are they deprecated in Airflow 2.0? What are the alternatives?
**Q8.4:** How do you implement conditional task execution (if-else logic) in a DAG?
**Q8.5:** Explain how to implement task grouping and how it helps with DAG organization.

### 9. Production Deployment
**Q9.1:** What are the different Airflow executors (Local, Celery, Kubernetes) and when would you choose each?
**Q9.2:** How do you secure Airflow in production (authentication, authorization, network security)?
**Q9.3:** What database backends are supported for Airflow metadata and what are their trade-offs?
**Q9.4:** How do you implement high availability for Airflow components?
**Q9.5:** What are the best practices for deploying Airflow in a containerized environment?

### 10. Testing & CI/CD
**Q10.1:** How do you unit test Airflow DAGs and tasks?
**Q10.2:** What tools and frameworks are available for testing Airflow pipelines?
**Q10.3:** How do you implement CI/CD for Airflow DAG deployment?
**Q10.4:** What validation checks should be performed before deploying a DAG to production?
**Q10.5:** How do you version control DAGs and manage DAG lifecycle?

### 11. Performance & Scaling
**Q11.1:** How do you identify and resolve DAG performance bottlenecks?
**Q11.2:** What are common causes of scheduler latency and how do you mitigate them?
**Q11.3:** How do you scale Airflow horizontally for high-volume workflow execution?
**Q11.4:** What metrics should you monitor for Airflow performance and health?
**Q11.5:** How do you implement DAG prioritization and resource quotas?

### 12. Integration & Extensibility
**Q12.1:** How do you create custom operators in Airflow?
**Q12.2:** What are Airflow plugins and how do they extend Airflow functionality?
**Q12.3:** How do you integrate Airflow with external systems (databases, APIs, cloud services)?
**Q12.4:** Explain how to use Airflow with Docker and Kubernetes.
**Q12.5:** How do you implement custom authentication backends for Airflow?

---

## Behavioral & Scenario Questions

### 13. Problem-Solving Scenarios
**Q13.1:** You notice that a critical production DAG is failing due to memory issues on your 8GB RAM system. How would you diagnose and resolve this?
**Q13.2:** A DAG that usually takes 5 minutes suddenly starts taking 30 minutes. What steps would you take to investigate?
**Q13.3:** You need to backfill 6 months of data for a newly created DAG. How would you approach this without overwhelming the system?
**Q13.4:** Multiple teams are complaining about DAG execution delays. How would you prioritize and address their concerns?
**Q13.5:** You discover that a DAG has been incorrectly configured with `catchup=True` and has created thousands of unnecessary DAG runs. How do you clean this up?

### 14. Design Scenarios
**Q14.1:** Design an Airflow pipeline for a daily ETL job that:
   - Extracts data from an API with rate limits
   - Transforms the data (cleaning, aggregation)
   - Loads to a PostgreSQL database
   - Sends a Slack notification on success/failure
   - Includes data quality checks

**Q14.2:** How would you design a DAG that processes files from an S3 bucket, where the number of files varies daily?
**Q14.3:** Design a fault-tolerant pipeline that can handle intermittent API failures and resume from where it left off.
**Q14.4:** How would you implement a data pipeline that needs to process data in multiple stages with different teams owning different stages?
**Q14.5:** Design a monitoring and alerting system for Airflow that proactively identifies issues before they affect downstream systems.

### 15. Team & Collaboration
**Q15.1:** How would you onboard a new team member to your Airflow setup?
**Q15.2:** What documentation would you create for your Airflow DAGs and why?
**Q15.3:** How do you handle DAG ownership and permissions in a multi-team environment?
**Q15.4:** What processes would you establish for DAG code reviews and deployment?
**Q15.5:** How do you balance the need for standardized DAG patterns with allowing innovation and custom solutions?

---

## Practical Exercises

### Exercise 1: Basic DAG Creation
Create a DAG that:
1. Runs daily at 2 AM
2. Has three tasks: extract, transform, load
3. Uses appropriate operators for each task
4. Includes error handling with 3 retries and 5-minute delays
5. Sends an email notification on failure

### Exercise 2: Dynamic DAG Generation
Write a Python script that generates DAGs dynamically based on a configuration file. The configuration should specify:
- DAG names and schedules
- Task definitions and dependencies
- Resource requirements
- Alert configurations

### Exercise 3: Resource-Constrained Optimization
Given a system with 8GB RAM running 50+ DAGs:
1. Identify potential memory bottlenecks
2. Propose configuration changes to optimize memory usage
3. Design a monitoring dashboard to track resource utilization
4. Create a strategy for prioritizing critical DAGs during resource contention

### Exercise 4: Failure Recovery Design
Design a DAG that:
1. Processes financial transaction data
2. Includes checkpointing to handle mid-process failures
3. Can resume processing from the last successful checkpoint
4. Validates data integrity after recovery
5. Logs recovery actions for audit purposes

### Exercise 5: Integration Pattern
Create a custom operator that:
1. Connects to a REST API with pagination
2. Handles rate limiting and authentication token refresh
3. Implements exponential backoff for retries
4. Streams data to avoid memory overload
5. Includes comprehensive logging and metrics

---

## Evaluation Rubric

### Technical Knowledge (40%)
- **Excellent (35-40 pts)**: Demonstrates deep understanding of Airflow architecture, advanced features, and best practices. Can explain trade-offs between different approaches.
- **Good (25-34 pts)**: Solid understanding of core concepts, can design effective DAGs, understands error handling and scheduling.
- **Fair (15-24 pts)**: Basic understanding of Airflow components, can create simple DAGs but struggles with advanced topics.
- **Poor (0-14 pts)**: Limited knowledge, cannot explain basic Airflow concepts or create functional DAGs.

### Problem-Solving Ability (30%)
- **Excellent (25-30 pts)**: Approaches problems systematically, considers multiple solutions, evaluates trade-offs, proposes innovative solutions.
- **Good (18-24 pts)**: Identifies key issues, proposes reasonable solutions, considers practical constraints.
- **Fair (10-17 pts)**: Struggles to identify root causes, proposes simplistic or impractical solutions.
- **Poor (0-9 pts)**: Cannot articulate problem-solving approach or propose viable solutions.

### Practical Implementation (20%)
- **Excellent (17-20 pts)**: Code is clean, well-structured, follows best practices, includes proper error handling and documentation.
- **Good (12-16 pts)**: Functional implementation with minor issues, follows most best practices.
- **Fair (7-11 pts)**: Implementation works but has significant issues (poor error handling, inefficient code).
- **Poor (0-6 pts)**: Code does not work, major structural issues, ignores best practices.

### Communication & Collaboration (10%)
- **Excellent (9-10 pts)**: Clearly explains concepts, asks clarifying questions, considers team dynamics and collaboration needs.
- **Good (6-8 pts)**: Communicates effectively, can explain their approach, considers some collaboration aspects.
- **Fair (3-5 pts)**: Communication is unclear or incomplete, struggles to explain concepts.
- **Poor (0-2 pts)**: Poor communication skills, cannot articulate thoughts clearly.

### Total Score Interpretation
- **90-100 pts**: Exceptional candidate, ready for senior/lead roles
- **75-89 pts**: Strong candidate, ready for intermediate/senior roles
- **60-74 pts**: Competent candidate, suitable for junior/intermediate roles
- **40-59 pts**: Needs improvement, may require additional training
- **0-39 pts**: Not ready for Airflow-related roles

---

## Additional Resources

### Recommended Study Materials
1. **Official Documentation**: [Apache Airflow Documentation](https://airflow.apache.org/docs/)
2. **Books**: 
   - "Data Pipelines with Apache Airflow" by Bas P. Harenslak and Julian Rutger de Ruiter
   - "Mastering Apache Airflow" by Daniel Gaspar
3. **Courses**:
   - "The Complete Hands-On Introduction to Apache Airflow" (Udemy)
   - "Apache Airflow: The Hands-On Guide" (DataCamp)
4. **Community Resources**:
   - Airflow Slack community
   - Airflow GitHub repository and issues
   - Airflow Summit talks and recordings

### Practice Projects
1. **Weather Data Pipeline**: Build an ETL pipeline that fetches weather data, processes it, and loads to a database.
2. **Stock Market Analyzer**: Create a pipeline that processes stock data with technical indicators.
3. **Social Media Monitor**: Build a pipeline that aggregates social media posts and performs sentiment analysis.
4. **E-commerce Analytics**: Design a pipeline for processing e-commerce transactions and generating reports.

### Common Pitfalls to Avoid
1. **Memory Management**: Avoid storing large data in XComs; use external storage instead.
2. **Scheduling Issues**: Be careful with `start_date` and timezone configurations.
3. **Error Handling**: Always implement proper retry logic and failure notifications.
4. **Testing**: Test DAGs thoroughly before deploying to production.
5. **Monitoring**: Implement comprehensive monitoring for both Airflow itself and your DAGs.

---

## Version History
- **v1.0** (April 2026): Initial creation for Data Engineering Bootcamp
- **Focus Areas**: Airflow fundamentals, DAG design, error handling, 8GB RAM optimization
- **Target Audience**: Data engineers preparing for interviews involving workflow orchestration

## Notes for Interviewers
- Tailor questions based on the candidate's experience level
- Use practical exercises to assess hands-on skills
- Consider the 8GB RAM constraint as a realistic scenario for many organizations
- Focus on problem-solving approach rather than just memorized answers
- Evaluate both technical knowledge and communication skills