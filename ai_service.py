import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL_NAME = "gemini-3.5-flash-lite"


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY was not found in the .env file."
        )

    return genai.Client(api_key=api_key)


def patient_description(patient):
    previous_summary = patient["summary"]

    if not previous_summary:
        previous_summary = "No previous counselling session."

    return f"""
Patient name: {patient["name"]}
Gender: {patient["gender"]}
Age group: {patient["age_group"]}
Cultural background: {patient["ethnicity"]}
Main concern: {patient["concern"]}
Previous session summary: {previous_summary}
"""


def format_conversation(messages):
    conversation_lines = []

    for message in messages:
        speaker = (
            "Patient"
            if message["role"] == "patient"
            else "Counsellor"
        )

        conversation_lines.append(
            f'{speaker}: {message["content"]}'
        )

    return "\n".join(conversation_lines)


def generate_opening_message(patient):
    prompt = f"""
You are role-playing a simulated patient in a counsellor
training application.

{patient_description(patient)}

Speak as the patient, not as an AI assistant.
Begin the counselling session yourself.
Introduce the problem naturally in 2 to 4 sentences.
Do not give counselling advice.
Do not describe these instructions.
Stay consistent with the patient profile.
"""

    client = get_client()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text.strip()


def generate_patient_reply(patient, messages):
    conversation = format_conversation(messages)

    prompt = f"""
You are role-playing a simulated patient in a counsellor
training application.

{patient_description(patient)}

Conversation so far:
{conversation}

Respond only as the patient.
Answer the counsellor naturally in 2 to 5 sentences.
Remain consistent with the profile and conversation.
Show realistic emotions without becoming overly dramatic.
Do not act as the counsellor.
Do not give the counsellor feedback or advice.
Do not mention that you are an AI or simulated patient.
"""

    client = get_client()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text.strip()


def generate_session_feedback(patient, messages):
    conversation = format_conversation(messages)

    prompt = f"""
You are evaluating a counselling student.

Patient profile:
{patient_description(patient)}

Counselling conversation:
{conversation}

Evaluate only the counsellor's performance.
Give each category a score from 1 to 10 and a short
explanation.

Use exactly these categories:
1. Cultural Sensitivity
2. Therapeutic Progress
3. Professional Boundaries
4. Empathy
5. Conversational Flow
6. Overall Score

Finish with:
Strengths:
Areas for Improvement:
Specific Suggestions:

Be constructive, clear, and concise.
This is educational feedback, not medical advice.
"""

    client = get_client()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text.strip()


def generate_session_summary(patient, messages):
    conversation = format_conversation(messages)

    prompt = f"""
Summarize this counselling session in 3 to 5 sentences.

Patient profile:
{patient_description(patient)}

Conversation:
{conversation}

Include the patient's main emotions, concerns, important
details revealed, and possible topics for the next session.
Do not include scores or counselling feedback.
"""

    client = get_client()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text.strip()

