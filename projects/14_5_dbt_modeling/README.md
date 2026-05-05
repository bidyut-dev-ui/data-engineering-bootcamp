# Project 14.5: dbt (data build tool) Fundamentals

## Overview
**dbt** is the most popular tool for managing SQL transformations in a modern data stack. It follows the **ELT** (Extract, Load, Transform) pattern, where data is loaded raw into the warehouse and then transformed using modular SQL.

A Team Lead needs to know how to structure dbt projects, write tests, and manage macros.

## Learning Objectives
- Master the **dbt project structure** (models, tests, snapshots).
- Understand **Staging vs. Marts**: How to layer your SQL transformations.
- Use **Jinja templating** to make your SQL dynamic.
- Write **Schema Tests** to ensure data quality.
- Generate **dbt Documentation** for stakeholders.

## Core Concepts
- **Models:** SQL files that define your tables/views.
- **Sources:** Raw data tables coming from external sources.
- **Seeds:** Static CSV files loaded into the warehouse (e.g., country codes).
- **Macros:** Reusable SQL snippets (like Python functions).

## Structure
- `dbt_project.yml`: Configuration for the whole project.
- `models/staging/`: Initial cleaning of raw data.
- `models/marts/`: Business-ready datasets (e.g., `dim_users`, `fct_orders`).
- `tests/`: Custom SQL tests for data quality.

## Exercise
1. Create a staging model for raw sales data.
2. Create a mart model that calculates daily revenue.
3. Add a `not_null` and `unique` test to the `order_id` column.
