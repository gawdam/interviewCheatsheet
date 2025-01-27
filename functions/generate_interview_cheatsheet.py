import os
import json
from openai import OpenAI
from functions.pdf_to_text import extract_text_from_pdf
from functions.response_format import response_format
from functions.get_yt_videos import replace_youtube_videos_with_links
from dotenv import load_dotenv

def generate_interview_cheatsheet(resume_path, job_description):
    load_dotenv()
    try:
        # Extract resume text
        resume_text = extract_text_from_pdf(resume_path)

        # Initialize OpenAI API
        base_url = "https://api.aimlapi.com/v1"
        api_key = os.getenv("AIMLAPIKEY")
        api = OpenAI(api_key=api_key, base_url=base_url)

        # Send the prompt to OpenAI
        response = api.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant..."},
                {"role": "user", "content": f"Here is the resume: {resume_text}\n\n Here is the job description {job_description}. Do not include any formatting. Do not use quotes"}
            ],
            temperature=0.7,
            max_tokens=8192,
            response_format={"type": "json_schema", "json_schema": response_format}
        )

        # Validate and parse response
        message = response.choices[0].message
        try:
            parsed_content = json.loads(message.content)  # Ensure JSON format
        except json.JSONDecodeError:
            raise ValueError("OpenAI response is not valid JSON")

        # Replace YouTube videos with links
        json_with_yt_link = replace_youtube_videos_with_links(parsed_content, api_key=os.getenv("YTAPIKEY"))

        return json_with_yt_link

    except Exception as e:
        print(f"Error during summarization: {e}")
        return ""
