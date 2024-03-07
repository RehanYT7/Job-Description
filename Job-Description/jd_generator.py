import os
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
import pymysql
import json
import logging
import re
from db_connection import DatabaseConnection


class JobDescriptionGenerator:
    """Initialize with the path to the configuration file"""
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.load_config()   # Load configuration settings
        self.setup_logging()  # Setup logging
        # self.connect_to_database()  # This is commented out, for future use as the database connection is done inseparate file

    def load_config(self):
        """Load configuration from a JSON file"""
        with open(self.config_file_path, 'r') as config_file:
            self.config = json.load(config_file)
            self.openai_key = self.config['OpenAI']['api_key']

    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(filename="store.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filemode='a')
        self.logger_prompt = logging.getLogger("Prompt Generation:-")
        self.logger_prompt.setLevel(logging.INFO)
        self.logger_output = logging.getLogger("Generated Job Description:-")
        self.logger_output.setLevel(logging.INFO)

    def generated_job_description(self):
        try:
            db = DatabaseConnection()  # Create a database connection

            """SQL query to fetch data from the database"""
            query = "SELECT * FROM JD_details"
            output = db.execute_query(query)  # Execute the SQL query

            for columns in output:  # Iterate over each row
                columns

            os.environ['OPENAI_API_KEY'] = self.openai_key

            """Define a template for the job description"""
            prompt_parameters = PromptTemplate(
                input_variables=['job_role', 'skill_1', 'skill_2', 'skill_3', 'skill_4', 'skill_5', 'skill_6',
                                     'skill_7',
                                     'skill_8', 'skill_9', 'skill_10', 'year'],
                template="""Create a Detailed Job Description for a {job_role} with expertise in {skill_1},{skill_2},{skill_3},{skill_4},{skill_5},{skill_6},{skill_7},{skill_8},{skill_9},{skill_10}, having experience of {year} years.The generated Job Description should ONLY consist of sections "Job Brief", "Roles", "Responsibilities" and "Skills".""")

            """Initialize a ChatOpenAI object with the GPT-3.5 Turbo model and a temperature of 0.6"""
            llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.6)

            """Create an LLMChain using the ChatOpenAI object and the specified prompt template"""
            chain1 = LLMChain(llm=llm, prompt=prompt_parameters)

            # Format the prompt using data from the current row (columns) in the database
            prompt = prompt_parameters.format_prompt(job_role=columns[2], skill_1=columns[3],
                                                                       skill_2=columns[4], skill_3=columns[5],
                                                                       skill_4=columns[6],
                                                                       skill_5=columns[7], skill_6=columns[8],
                                                                       skill_7=columns[9],
                                                                       skill_8=columns[10],
                                                                       skill_9=columns[11], skill_10=columns[12],
                                                                       year=columns[13])

            # Convert the prompt to a string and replace "None," with an empty string
            prompt = str(prompt)
            p = prompt.replace("None,", "")

            # Log the modified prompt for debugging or tracking purposes
            self.logger_prompt.info(p)

            # Check if there are columns (data from the database)
            if columns:
                    # Generate a job description by running the LLMChain with the formatted prompt
                result = chain1.run(
                        {'job_role': columns[2], 'skill_1': columns[3], 'skill_2': columns[4], 'skill_3': columns[5],
                            'skill_4': columns[6],
                            'skill_5': columns[7], 'skill_6': columns[8], 'skill_7': columns[9], 'skill_8': columns[10],
                            'skill_9': columns[11],
                            'skill_10': columns[12], 'year': columns[13]})

                # This regex pattern is used to remove the last line from the result if it does not follow the specified pattern.
                # result_without_last_line = re.sub(r'\n(?!\w+:\n)([^\n]+\.\s+)$', '', result)
                result_without_last_line = re.sub(r'\n[^\n]*$', '', result)

                # pattern_for_correct_answer = r'(Note):(.+)'
                # # result_without_last_line = re.findall(pattern_for_correct_answer, result)
                # result_without_last_line = re.sub(pattern_for_correct_answer, '', result).strip()

                # SQL query to insert data into the database
                sql_insert = "INSERT INTO JD_information (email, generated_job_description) VALUES (%s, %s)"
                self.logger_output.info(result)

                if result_without_last_line:
                    #result_string = " ".join(result_without_last_line[0])  # Convert the list to a single string
                    values = (columns[1], result_without_last_line)  # Pass the string to the SQL query
                    db.execute_insert_query(sql_insert, values)
                    db.commit()
                else:
                    values = (columns[1], result)
                    db.execute_insert_query(sql_insert, values)


                # Execute the SQL insert query

                print("Data successfully inserted!")
                db.commit()  # Commit the transaction
                # continue

                # This will display at the server page when the data is inserted in the database table
            return columns[1]

        except Exception as e:
            print("An Exceptional error occurred: ", str(e))
        finally:
            db.close()  # Close the database connection

    def display_generated_jd(self, mail):
        generated_jd = None  # Initialize to None if no data is found
        try:
            db = DatabaseConnection()  # Create a database connection

            # Correct the SQL query syntax
            query = f"SELECT generated_job_description FROM JD_information WHERE email='{mail}' ORDER BY time_stamp DESC LIMIT 1"

            # Execute the SQL query and fetch only the third column (generated_job_description)
            result = db.execute_query(query)
            generated_jd = result[0][0] if result else None

            # Close the database connection
            db.close()

        except Exception as e:
            print(f"An Exceptional error occurred: {str(e)}")

        return generated_jd


if __name__ == "__main__":
    # Path to the configuration file
    config_file_path = 'config.json'

    # Create an instance of JobDescriptionGenerator using the config file path
    generator = JobDescriptionGenerator(config_file_path)

    # Call the generated_job_description method to start the job description generation
    mail = generator.generated_job_description()
    generator.display_generated_jd(mail)