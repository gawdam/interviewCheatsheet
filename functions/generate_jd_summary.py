import os
import json
from functions.response_format import jd_summary_schema
from dotenv import load_dotenv
from google import genai


def generate_jd_summary(job_description):
    load_dotenv()

    try:
        # Initialize OpenAI API
        api_key = os.getenv("GEMINIAPIKEY")
        client = genai.Client(api_key=api_key)

        # Send the prompt to OpenAI
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=f"Summarize this job requirement for me. \n\n Here is the job description {job_description}. Do not include any formatting. Do not use quotes",
            config={
                'max_output_tokens': 5000,
                'temperature' : 0.1,
                'response_mime_type': 'application/json',
                'response_schema': jd_summary_schema,

            },
        )

        # Validate and parse response
        message = response.text

        try:
            parsed_content = json.loads(message)  # Ensure JSON format
        except json.JSONDecodeError:
            raise ValueError("OpenAI response is not valid JSON")

        return parsed_content

    except Exception as e:
        print(f"Error during summarization: {e}")
        return ""
