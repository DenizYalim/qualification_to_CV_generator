import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
(os.getenv("OPENAI_API_KEY"))
client = openai.OpenAI()


def getResponse(prompt, context=None):
    if context is None:
        context = "There is a job position that I want to send my CV to, I want you to choose which qualities I should choose to include in my CV. I will give you both qualification of mine and the job position details."
    response = client.chat.completions.create(
        model="gpt-4", # Maybe experiment with other models too
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content

def askForMatchingQualifications(qualificationsList, jobDetails):
    context = "There is a job position that I want to send my CV to, I want you to choose which qualities I should choose to include in my CV. I will give you both qualification of mine and the job position details."
    prompt = f"I want to apply to this job: {jobDetails}, here is a list with my qualities/past projects etc.: {qualificationsList}, which qualities I shoulda include in my CV for this job application?"

    response = getResponse(prompt, context=context)

    print(prompt +"\n")
    print(response)

    return response

if __name__ != "__main__":
    pass
