from openai import OpenAI

from functions.pdf_to_text import extract_text_from_pdf
from functions.response_format import response_format
from functions.get_yt_videos import replace_youtube_videos_with_links
from config import YTAPIKEY, AIMLAPIKEY


def generate_interview_cheatsheet(resume_path,job_description):
    try:
        resume_text = extract_text_from_pdf(resume_path)

        base_url = "https://api.aimlapi.com/v1"
        api_key = AIMLAPIKEY
        api = OpenAI(api_key=api_key, base_url=base_url)
        # Specify the desired response format in JSON schema

        # Send the prompt to the LLM
        response = api.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """You are a helpful assistant that helps candidates prepare for their interviews. 
                Create a cheatsheet that the candidate can use to revise the concepts that could be covered during the interview"""},
                {"role": "user",
                 "content": f"Here is the resume: {resume_text}\n\n Here is the job description {job_description}. Do not include any formatting. Do not use quotes"}
            ],
            temperature=0.7,
            max_tokens=8192,
            # temperature=0.5, (Uncomment if temperature needs to be adjusted)
            response_format={"type": "json_schema", "json_schema": response_format}
            # response_format =
        )

        # Parse the response
        message = response.choices[0].message
        # if hasattr(message, "refusal") and message.refusal:
        #     print(message.refusal)
        # else:
        #     print("hi")
        #     print(message.content)

        return replace_youtube_videos_with_links(message.content,api_key=YTAPIKEY)

    except Exception as e:
        print(f"Error during summarization: {e}")
        return ""
