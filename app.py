import streamlit as st

from chat_page import render_chat_page
from real_patients import init_real_patient_database, render_real_patients_page

from database import authenticate_user, init_database, register_user
from patients import (
    create_patient,
    get_patient,
    get_patients,
    init_patient_database,
)

st.set_page_config(
    page_title="Counsellor Training App",
    page_icon="🧠"
)

init_database()
init_patient_database()
init_real_patient_database()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_patient_id" not in st.session_state:
    st.session_state.selected_patient_id = None


# Login and registration page
if not st.session_state.logged_in:
    st.title("Counsellor Training App")
    st.write(
        "Practice counselling conversations with simulated patients."
    )

    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        with st.form("login_form"):
            login_username = st.text_input("Username")
            login_password = st.text_input(
                "Password",
                type="password"
            )
            login_button = st.form_submit_button("Login")

        if login_button:
            user_id = authenticate_user(
                login_username.strip(),
                login_password
            )

            if user_id is not None:
                st.session_state.logged_in = True
                st.session_state.username = login_username.strip()
                st.session_state.user_id = user_id
                st.session_state.page = "home"
                st.rerun()
            else:
                st.error("Incorrect username or password.")

    with register_tab:
        with st.form("register_form"):
            new_username = st.text_input("Choose a username")
            new_password = st.text_input(
                "Choose a password",
                type="password"
            )
            confirm_password = st.text_input(
                "Confirm password",
                type="password"
            )
            register_button = st.form_submit_button("Register")

        if register_button:
            username = new_username.strip()

            if not username or not new_password:
                st.error("Username and password cannot be empty.")
            elif len(new_password) < 6:
                st.error(
                    "Password must contain at least 6 characters."
                )
            elif new_password != confirm_password:
                st.error("The two passwords do not match.")
            elif register_user(username, new_password):
                st.success(
                    "Registration successful. You can now log in."
                )
            else:
                st.error("That username already exists.")

    st.stop()


# Logout button
if st.sidebar.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_id = None
    st.session_state.page = "home"
    st.rerun()


# Home page
if st.session_state.page == "home":
    st.title("Counsellor Training App")
    st.success(f"Welcome, {st.session_state.username}!")

    st.subheader("Choose a training mode")

    left_column, right_column = st.columns(2)

    with left_column:
        if st.button(
            "Real Patients",
            use_container_width=True
        ):
            st.session_state.page = "real_patients"
            st.rerun()

    with right_column:
        if st.button(
            "Simulated Patients",
            use_container_width=True
        ):
            st.session_state.page = "patients"
            st.rerun()


# Real patients page
elif st.session_state.page == "real_patients":
    if st.button("← Back to home"):
        st.session_state.page = "home"
        st.rerun()

    render_real_patients_page(st.session_state.user_id)


# Simulated patient list and creation page
elif st.session_state.page == "patients":
    if st.button("← Back to home"):
        st.session_state.page = "home"
        st.rerun()

    st.title("Simulated Patients")

    existing_tab, create_tab = st.tabs(
        ["Existing Patients", "Create New Patient"]
    )

    with existing_tab:
        patients = get_patients(st.session_state.user_id)

        if not patients:
            st.info(
                "You have not created any simulated patients yet."
            )

        for patient in patients:
            with st.container(border=True):
                st.subheader(patient["name"])

                st.write(
                    f'{patient["gender"]}, '
                    f'{patient["age_group"]}, '
                    f'{patient["ethnicity"]}'
                )

                st.write(
                    f'**Main concern:** {patient["concern"]}'
                )

                if patient["summary"]:
                    st.write(
                        f'**Previous session:** '
                        f'{patient["summary"]}'
                    )

                if st.button(
                    f'Start session with {patient["name"]}',
                    key=f'patient_{patient["id"]}'
                ):
                    st.session_state.selected_patient_id = (
                        patient["id"]
                    )
                    st.session_state.page = "patient"
                    st.rerun()

    with create_tab:
        with st.form("patient_form"):
            patient_name = st.text_input("Patient name")

            gender = st.selectbox(
                "Gender",
                [
                    "Female",
                    "Male",
                    "Non-binary",
                    "Prefer not to say"
                ]
            )

            age_group = st.selectbox(
                "Age group",
                [
                    "Child",
                    "Teenager",
                    "Young adult",
                    "Adult",
                    "Older adult"
                ]
            )

            ethnicity = st.text_input(
                "Ethnicity or cultural background"
            )

            concern = st.text_area(
                "Main concern",
                placeholder=(
                    "For example: anxiety, grief, "
                    "or family conflict..."
                )
            )

            create_button = st.form_submit_button(
                "Create patient"
            )

        if create_button:
            if (
                not patient_name.strip()
                or not concern.strip()
            ):
                st.error(
                    "Patient name and main concern are required."
                )
            else:
                patient_id = create_patient(
                    st.session_state.user_id,
                    patient_name.strip(),
                    gender,
                    age_group,
                    ethnicity.strip() or "Not specified",
                    concern.strip()
                )

                st.session_state.selected_patient_id = patient_id
                st.session_state.page = "patient"
                st.rerun()


# Patient profile page
elif st.session_state.page == "patient":
    patient = get_patient(
        st.session_state.selected_patient_id,
        st.session_state.user_id
    )

    if patient is None:
        st.error("Patient not found.")

        if st.button("Return to patient list"):
            st.session_state.page = "patients"
            st.rerun()

    else:
        if st.button("← Back to patients"):
            st.session_state.page = "patients"
            st.rerun()

        st.title(patient["name"])
        st.subheader("Patient Profile")

        first_column, second_column = st.columns(2)

        with first_column:
            st.write(
                f'**Gender:** {patient["gender"]}'
            )
            st.write(
                f'**Age group:** {patient["age_group"]}'
            )

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

        render_chat_page(patient)

