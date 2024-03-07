from flask import Flask, jsonify
from jd_generator import JobDescriptionGenerator

app = Flask(__name__)

# Path to the configuration file
config_file_path = 'config.json'

# Create an instance of JobDescriptionGenerator using the config file path
generator = JobDescriptionGenerator(config_file_path)

@app.route('/generate_job_description', methods=['GET'])
def generate_job_description():
    """Endpoint to generate a job description"""
    try:
        # Call the generated_job_description method to generate a job description
        mail = generator.generated_job_description()
        questions_data = [
            {"generated_jd": generator.display_generated_jd(mail)}
        ]
        return jsonify(questions_data)
    except FileNotFoundError as e:
        error_message = f"Configuration file '{config_file_path}' not found."
        return jsonify({"error": error_message}), 500
    except ValueError as e:
        error_message = f"Invalid configuration file: {str(e)}"
        return jsonify({"error": error_message}), 500
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return jsonify({"error": error_message}), 500

if __name__ == "__main__":
    # Run the Flask application on host 0.0.0.0 (all available network interfaces) and port 5000
    app.run(debug = True, host='0.0.0.0', port=5000)