import streamlit as st
import logging
import time

from retrieval_response import (
    retrieve_relevant_chunks,
    generate_response,
    reformulate_query
)

from file_handler import extract_text_from_pdf
from processing import (
    chunk_documents,
    vectorize_chunks,
    store_vectors_in_faiss
)


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Load Gemini API key
api_key = st.secrets["gemini_api_key"]


# Logo URL
logo_url = (
    "https://i.pinimg.com/originals/"
    "5f/24/38/5f24384a518a90e30a2f1107141ab9d4.gif"
)


def main():

    # -----------------------------
    # Sidebar
    # -----------------------------

    st.sidebar.markdown(
        f"""
        <div style="text-align: center;">
            <img src="{logo_url}" width="100" height="100">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        """
        <h1 style="font-size: 24px; text-align: center;">
            DocuChat
        </h1>

        <h2 style="font-size: 18px; text-align: center;">
            RAG-based Chatbot
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.title("Upload File")

    uploaded_file = st.sidebar.file_uploader(
        "Upload a PDF file",
        type=["pdf"]
    )


    # -----------------------------
    # Initialize chat history
    # -----------------------------

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = [
            {
                "question": "",
                "answer": (
                    "Hi, I am your RAG-Based ChatBOT. "
                    "Please upload the PDF file if you didn't."
                )
            }
        ]


    # -----------------------------
    # Process uploaded PDF
    # -----------------------------

    if uploaded_file is not None:

        st.sidebar.write(
            f"File uploaded: {uploaded_file.name}"
        )

        # Extract text from PDF
        documents = extract_text_from_pdf(uploaded_file)

        # Split document into chunks
        chunks = chunk_documents(documents)

        # Convert chunks into vectors
        vectors, vectorizer = vectorize_chunks(chunks)

        # Store vectors in FAISS
        index = store_vectors_in_faiss(vectors)

        # Save processed data in session state
        st.session_state.index = index
        st.session_state.vectorizer = vectorizer
        st.session_state.chunks = chunks


    # -----------------------------
    # Chat input
    # -----------------------------

    user_query = st.chat_input("Ask a question:")


    if user_query:

        # Check whether PDF has been processed
        if (
            "index" in st.session_state
            and "vectorizer" in st.session_state
            and "chunks" in st.session_state
        ):

            try:

                # ---------------------------------
                # NEW FEATURE:
                # Reformulate follow-up question
                # using previous chat history
                # ---------------------------------

                search_query = reformulate_query(
                    st.session_state.chat_history,
                    user_query,
                    api_key
                )

                # Small delay between Gemini API calls
                time.sleep(1)


                # ---------------------------------
                # Retrieve relevant PDF chunks
                # using the reformulated query
                # ---------------------------------

                retrieved_chunks = retrieve_relevant_chunks(
                    st.session_state.index,
                    st.session_state.chunks,
                    search_query,
                    st.session_state.vectorizer
                )


                # ---------------------------------
                # Generate final answer
                # using the ORIGINAL user question
                # ---------------------------------

                response = generate_response(
                    "\n\n".join(retrieved_chunks),
                    user_query,
                    api_key
                )


                # Handle failed Gemini response
                if response is None:

                    response = (
                        "Sorry, Gemini didn't respond in time. "
                        "Please try asking again."
                    )


            except Exception as e:

                response = (
                    "An error occurred while generating "
                    f"the response: {str(e)}"
                )


        else:

            response = "Please upload a PDF file first."


        # -----------------------------
        # Save conversation
        # -----------------------------

        st.session_state.chat_history.append(
            {
                "question": user_query,
                "answer": response
            }
        )


    # -----------------------------
    # Display chat history
    # -----------------------------

    for chat in st.session_state.chat_history:

        if chat["question"]:

            with st.chat_message("user"):
                st.write(chat["question"])

        with st.chat_message("assistant"):
            st.write(chat["answer"])


    # -----------------------------
    # Watermark
    # -----------------------------

    st.markdown(
        """
        <div style="
            text-align: center;
            font-size: 12px;
            color: gray;
        ">
            Developed by Pranathi
        </div>
        """,
        unsafe_allow_html=True
    )


# -----------------------------
# Run application
# -----------------------------

if __name__ == "__main__":
    main()