import streamlit as st

from ai_service import (
    generate_opening_message,
    generate_patient_reply,
    generate_session_feedback,
    generate_session_summary,
)
from patients import update_patient_summary


def start_new_session(patient):
    st.session_state.chat_patient_id = patient["id"]
    st.session_state.chat_messages = []
    st.session_state.session_ended = False
    st.session_state.session_feedback = ""

    try:
        with st.spinner(
            f"{patient['name']} is preparing to speak..."
        ):
            opening_message = generate_opening_message(patient)

        st.session_state.chat_messages.append(
            {
                "role": "patient",
                "content": opening_message
            }
        )

    except Exception as error:
        st.error(f"Could not start the conversation: {error}")


def render_chat_page(patient):
    if (
        "chat_patient_id" not in st.session_state
        or st.session_state.chat_patient_id != patient["id"]
    ):
        start_new_session(patient)

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    if "session_ended" not in st.session_state:
        st.session_state.session_ended = False

    if "session_feedback" not in st.session_state:
        st.session_state.session_feedback = ""

    with st.expander("View Patient Profile"):
        first_column, second_column = st.columns(2)

        with first_column:
            st.write(f'**Gender:** {patient["gender"]}')
            st.write(f'**Age group:** {patient["age_group"]}')

        with second_column:
            st.write(
                f'**Background:** {patient["ethnicity"]}'
            )
            st.write(
                f'**Main concern:** {patient["concern"]}'
            )

        if patient["summary"]:
            st.write(
                f'**Previous session summary:** '
                f'{patient["summary"]}'
            )

    st.subheader("Counselling Session")
    st.caption(
        "You are the counsellor. The AI is playing the patient."
    )

    for message in st.session_state.chat_messages:
        if message["role"] == "patient":
            with st.chat_message(
                "assistant",
                avatar="🧑"
            ):
                st.write(message["content"])
        else:
            with st.chat_message(
                "user",
                avatar="🧠"
            ):
                st.write(message["content"])

    if st.session_state.session_ended:
        st.success("The counselling session has ended.")
        st.subheader("Training Feedback")
        st.markdown(st.session_state.session_feedback)

        if st.button("Start a New Session"):
            st.session_state.chat_patient_id = None
            st.rerun()

        return

    counsellor_message = st.chat_input(
        "Type your response as the counsellor..."
    )

    if counsellor_message:
        st.session_state.chat_messages.append(
            {
                "role": "counsellor",
                "content": counsellor_message
            }
        )

        try:
            with st.spinner(
                f"{patient['name']} is responding..."
            ):
                patient_reply = generate_patient_reply(
                    patient,
                    st.session_state.chat_messages
                )

            st.session_state.chat_messages.append(
                {
                    "role": "patient",
                    "content": patient_reply
                }
            )

            st.rerun()

        except Exception as error:
            st.error(
                f"Could not generate a patient response: {error}"
            )

    has_counsellor_message = any(
        message["role"] == "counsellor"
        for message in st.session_state.chat_messages
    )

    if st.button(
        "End Session and Get Feedback",
        disabled=not has_counsellor_message
    ):
        try:
            with st.spinner(
                "Generating your training feedback..."
            ):
                feedback = generate_session_feedback(
                    patient,
                    st.session_state.chat_messages
                )

                summary = generate_session_summary(
                    patient,
                    st.session_state.chat_messages
                )

            update_patient_summary(
                patient["id"],
                summary
            )

            st.session_state.session_feedback = feedback
            st.session_state.session_ended = True
            st.rerun()

        except Exception as error:
            st.error(
                f"Could not finish the session: {error}"
            )

