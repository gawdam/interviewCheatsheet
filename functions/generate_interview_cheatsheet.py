import os
import json
from functions.pdf_to_text import extract_text_from_pdf
from functions.response_format import  schema
from functions.get_yt_videos import replace_youtube_videos_with_links
from dotenv import load_dotenv
from google import genai

import sys


def generate_interview_cheatsheet(resume, job_description):
    load_dotenv()

    try:
        # Extract resume text
        resume_text = extract_text_from_pdf(resume)



        # Initialize OpenAI API
        api_key = os.getenv("GEMINIAPIKEY")
        client = genai.Client(api_key=api_key)


        # Send the prompt to OpenAI
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=f"Create a cheatsheet for my interview. Here is the resume: {resume_text}\n\n Here is the job description {job_description}. Do not include any formatting. Do not use quotes",
            config={
                'max_output_tokens': 5000,
                'temperature' : 0.1,
                'response_mime_type': 'application/json',
                'response_schema': schema,

            },
        )

        # Validate and parse response
        message = response.text
        print(message)

        try:
            parsed_content = json.loads(message)  # Ensure JSON format
        except json.JSONDecodeError:
            raise ValueError("OpenAI response is not valid JSON")
        # Replace YouTube videos with links
        json_with_yt_link = replace_youtube_videos_with_links(parsed_content, api_key=os.getenv("YTAPIKEY"))
        print(json_with_yt_link)
        return json_with_yt_link

    except Exception as e:
        print(f"Error during summarization: {e}")
        return ""
