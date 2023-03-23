"""Code explainer app using OpenAI API"""

import time

import streamlit as st
from explainer import retrieve_code_explanation, retrieve_code_language
from streamlit.runtime.uploaded_file_manager import UploadedFile


def display_header() -> None:
    """Shows the app's header."""
    st.image("img/logo.jpg")
    st.title("Welcome to AI-rjan Code Explainer")
    st.text("Just upload your code or copy and paste in the field below")
    st.warning("Warning: uploaded files have precendence on copied and pasted code.")


def display_widgets() -> tuple[UploadedFile, str]:
    """Brings the code input widgets to the app."""

    file = st.file_uploader("Upload your script here.")
    text = st.text_area("or copy and paste your code here (press Ctrl + Enter to send)")

    if not (text or file):
        st.error("Bring your code with one of the options from above.")

    return file, text


def retrieve_content_from_file(file: UploadedFile) -> str:
    """Reads the code from a file."""
    return file.getvalue().decode("utf8")


def extract_code() -> str:
    """Extract from widgets the code to be explained."""
    uploaded_script, pasted_code = display_widgets()

    if uploaded_script:
        return retrieve_content_from_file(uploaded_script)
    return pasted_code or ""


def main() -> None:
    """Runs the app."""
    display_header()

    if code_to_explain := extract_code():
        with st.spinner(text="In progress"):
            time.sleep(5)
            st.success("Done")

            language = retrieve_code_language(code=code_to_explain)
            explanation = retrieve_code_explanation(code=code_to_explain)
            st.markdown(f"**Language:** {language}")
            st.markdown(f"**Explanation:** {explanation}")


if __name__ == "__main__":
    main()
