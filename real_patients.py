import sqlite3

import streamlit as st

DB_PATH = "counsellor_training.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_real_patient_database():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS real_patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                patient_code TEXT NOT NULL,
                gender TEXT NOT NULL,
                age_group TEXT NOT NULL,
                concern TEXT NOT NULL,
                notes TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            """
        )


def create_real_patient(
    user_id,
    patient_code,
    gender,
    age_group,
    concern,
    notes
):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO real_patients (
                user_id,
                patient_code,
                gender,
                age_group,
                concern,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                patient_code,
                gender,
                age_group,
                concern,
                notes
            )
        )


def get_real_patients(user_id):
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT *
            FROM real_patients
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,)
        ).fetchall()


def update_real_patient_notes(patient_id, user_id, notes):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE real_patients
            SET notes = ?
            WHERE id = ? AND user_id = ?
            """,
            (notes, patient_id, user_id)
        )


def delete_real_patient(patient_id, user_id):
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM real_patients WHERE id = ? AND user_id = ?",
            (patient_id, user_id)
        )


def render_real_patients_page(user_id):
    st.title("Real Patients")

    st.warning(
        "For privacy, use an anonymous patient code or initials. "
        "Do not enter names, contact details, or other identifying "
        "information. This application is for training purposes only."
    )

    existing_tab, create_tab = st.tabs(
        ["Existing Patients", "Add Real Patient"]
    )

    with existing_tab:
        patients = get_real_patients(user_id)

        if not patients:
            st.info("No real-patient records have been added.")

        for patient in patients:
            with st.container(border=True):
                st.subheader(patient["patient_code"])

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
                        f'**Main concern:** {patient["concern"]}'
                    )

                notes = st.text_area(
                    "Session notes",
                    value=patient["notes"],
                    key=f'real_notes_{patient["id"]}',
                    height=150
                )

                if st.button(
                    "Save Notes",
                    key=f'save_real_{patient["id"]}'
                ):
                    update_real_patient_notes(
                        patient["id"],
                        user_id,
                        notes.strip()
                    )
                    st.success("Session notes saved.")

                
                confirm_delete = st.checkbox(
                    "Confirm deletion of this record",
                    key=f'confirm_delete_real_{patient["id"]}'
                )

                if st.button(
                    "Delete Patient",
                    key=f'delete_real_{patient["id"]}',
                    disabled=not confirm_delete
                ):
                    delete_real_patient(patient["id"], user_id)
                    st.rerun()


    with create_tab:
        with st.form("real_patient_form"):
            patient_code = st.text_input(
                "Anonymous patient code or initials",
                placeholder="For example: Patient A or J.D."
            )

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

            concern = st.text_area(
                "Main concern",
                placeholder=(
                    "Use a general description without "
                    "identifying information."
                )
            )

            notes = st.text_area(
                "Initial session notes",
                placeholder=(
                    "Enter anonymous training notes here."
                )
            )

            add_button = st.form_submit_button(
                "Add Real Patient"
            )

        if add_button:
            if (
                not patient_code.strip()
                or not concern.strip()
            ):
                st.error(
                    "Patient code and main concern are required."
                )
            else:
                create_real_patient(
                    user_id,
                    patient_code.strip(),
                    gender,
                    age_group,
                    concern.strip(),
                    notes.strip()
                )

                st.success("Real-patient record added.")
                st.rerun()

