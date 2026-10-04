# Counsellor Training App

A Python application for practising counselling conversations with AI simulated patients. The interface uses Streamlit, Gemini generates conversations and feedback, and SQLite stores accounts and patient records.

## Features

- Register, log in, and log out.
- Create simulated patients with a gender, age group, cultural background, and main concern.
- Let the simulated patient begin the conversation.
- Practise a multi-turn counselling conversation.
- Receive scores, strengths, and suggestions after ending a session.
- Save a session summary for the patient's next conversation.
- Add anonymous real-patient training records, update notes, and delete records.
- Keep patient records separate for each user account.

## Setup

The application was tested with Python 3.10.

1. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

2. Copy the configuration example:

   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and replace the placeholder with your own Gemini API key:

   ```text
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. Start the application:

   ```bash
   streamlit run app.py
   ```

The SQLite database is created automatically when the application starts.

## How to Use

Register an account and log in. Choose Simulated Patients and create a patient. The AI patient starts the conversation, and you respond as the counsellor. Select End Session and Get Feedback to receive an evaluation and save a summary.

Choose Real Patients to add anonymous training records, edit session notes, or delete a record.

## Main Files

- `app.py`: Login, registration, and page navigation.
- `database.py`: User account storage and authentication.
- `patients.py`: Simulated patient storage and session summaries.
- `ai_service.py`: Gemini prompts and API calls.
- `chat_page.py`: Conversation interface and session feedback.
- `real_patients.py`: Anonymous records and notes.
- `requirements.txt`: Required Python packages.
- `.env.example`: API key configuration example.

## Limitations

This is a coursework training prototype, not a clinical application. AI feedback may be inaccurate and is not a substitute for supervision. Use fictional or anonymous test data.

Conversation messages and feedback are kept in the current Streamlit session. The patient summary is saved in SQLite, but full transcripts and feedback history are not stored permanently.

Gemini features require internet access and a valid API key with access to the model configured in `ai_service.py`. API limits or model availability may affect operation.

Do not upload your `.env` file or local database to GitHub.
