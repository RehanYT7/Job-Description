# Job Description Generator

## Overview

This repository contains scripts that leverage OpenAI's GPT-3.5 model and a MySQL database connection to generate job descriptions. These scripts automate the process of generating job descriptions and store the results in a MySQL database. They offer various functionalities, including job description generation, database connectivity, and a Flask-based web service for easy access.

## Files

### 1. main.py

#### Description:
This file contains the core functionality for generating job descriptions using OpenAI's GPT-3.5 model.

#### Dependencies:
- `langchain`: Library for natural language processing tasks.
- `pymysql`: Library for interacting with MySQL databases.
- `json`: Library for handling JSON data.
- `logging`: Library for logging messages.
- `re`: Library for regular expressions.
- `db_connection`: Module for managing database connections.

#### Usage:
1. **Importing JobDescriptionGenerator**: Import the `JobDescriptionGenerator` class from `main.py`.
   
2. **Initialization**: Initialize the `JobDescriptionGenerator` class with the path to the `config.json` file.

3. **Generating Job Descriptions**: Call the `generated_job_description()` method to generate job descriptions.

#### Functions within `JobDescriptionGenerator` Class:

1. `__init__(self, config_file_path)`
   - **Use**: Initializes the class, loads settings from a configuration file, and sets up logging.
   - **Purpose**: Ensures proper setup by loading necessary configurations and preparing the logging mechanism.

2. `load_config(self)`
   - **Use**: Loads configuration settings from a JSON file.
   - **Purpose**: Retrieves crucial settings such as the OpenAI API key required for the job description generation process.

3. `setup_logging(self)`
   - **Use**: Sets up the logging configuration.
   - **Purpose**: Establishes a logging mechanism to record actions and outcomes during the job description generation process.

4. `generated_job_description(self)`
   - **Use**: Fetches data from a database, constructs job description templates, utilizes AI models to generate descriptions, refines and logs the generated descriptions, and stores them back in the database.
   - **Purpose**: Executes the entire job description generation workflow, from data retrieval to generating, refining, and storing job descriptions based on fetched information.

### 2. db_connection.py

#### Description:
This module manages the database connection and execution of SQL queries.

#### Dependencies:
- `pymysql`: Library for interacting with MySQL databases.
- `json`: Library for handling JSON data.

#### Functions within `DatabaseConnection` Class:

1. `__init__(self)`
   - **Use**: Establishes a connection to a MySQL database using the configuration from `config.json`.
   - **Purpose**: Ensures a database connection is established upon initialization of the class.

2. `connect(self)`
   - **Use**: Establishes a database connection and returns a session.
   - **Purpose**: Provides a method to connect to the database when needed.

3. `close(self)`
   - **Use**: Closes the database connection.
   - **Purpose**: Properly closes the database connection to release resources.

4. `execute_query(self, query)`
   - **Use**: Executes a SQL query and returns the result.
   - **Purpose**: Enables execution of SQL queries and retrieval of data from the database.

5. `execute_insert_query(self, query, values)`
   - **Use**: Executes an INSERT SQL query with provided values.
   - **Purpose**: Facilitates insertion of data into the database.

6. `commit(self)`
   - **Use**: Commits the current transaction.
   - **Purpose**: Commits changes made to the database to make them permanent.

### 3. config.json

#### Description:
Configuration file containing database server details and OpenAI API key.
#### Purpose:
Stores sensitive information such as database credentials and API keys in a structured format for easy access by the scripts.

### 4. app.py
#### Description:
Implements a Flask-based web service for generating job descriptions via HTTP requests.

#### Dependencies:
- Flask: Web framework for building APIs.
- langchain: Library for natural language processing tasks.
- pymysql: Library for interacting with MySQL databases.
- json: Library for handling JSON data.
- logging: Library for logging messages.
- re: Library for regular expressions.
- db_connection: Module for managing database connections.
#### Usage:
- Run the Flask application app.py to create an endpoint (/test) for generating job descriptions via HTTP GET requests.

#### Setup Instructions:
#### Environment Setup:
- Ensure Python is installed (preferably Python 3.x).
- Install necessary dependencies using the command: pip install -r requirements.txt.
#### Database Configuration:
- Update the config.json file with your specific database server details, including server address, database name, username, password, and API key.
#### Running the Application:
- Execute the Python file app.py to start the Flask-based web service for job description generation.

#### Notes:
- Ensure proper setup of dependencies and correct configurations in config.json before executing the scripts.
- Protect sensitive information such as API keys and database credentials.


This documentation provides detailed information about each code file, its purpose, dependencies, usage instructions, and setup requirements. It aims to facilitate understanding and usage of the Job Description Generator scripts.
