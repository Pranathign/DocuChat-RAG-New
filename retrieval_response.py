import streamlit as st
import requests
import time
import random


api_key = st.secrets["gemini_api_key"]


def reformulate_query(chat_history, user_query, api_key):
    """
    Rewrites a follow-up question into a standalone question using
    recent chat history.

    Falls back to the original query if anything goes wrong.
    """

    recent_turns = [
        c for c in chat_history
        if c["question"]
    ][-3:]

    if not recent_turns:
        return user_query

    history_text = "\n".join(
        f"User: {c['question']}\nAssistant: {c['answer'][:300]}"
        for c in recent_turns
    )

    prompt = f"""
Rewrite the follow-up question into a standalone question using
the conversation history.

Replace vague words like "that", "it", and "this" with the actual
topic being discussed.

Example:

History:
User: What is 2NF?
Assistant: 2NF means a relation is in 1NF and every non-key attribute
is fully dependent on the key.

Follow-up: "give example for that"

Rewritten: "give an example of 2NF"

Now do the same for this conversation:

History:
{history_text}

Follow-up: "{user_query}"

Output ONLY the rewritten question, nothing else.

Rewritten:
"""

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/gemini-3.5-flash-lite:generateContent"
    )

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            params={"key": api_key},
            json=data,
            timeout=30
        )

        response.raise_for_status()

        rewritten = (
            response.json()["candidates"][0]["content"]["parts"][0]["text"]
            .strip()
            .strip('"')
        )

        st.caption(
            f"Searched for: {rewritten if rewritten else user_query}"
        )

        return rewritten if rewritten else user_query

    except requests.exceptions.RequestException as e:
        st.caption(
            f"Reformulation failed, using original query. ({repr(e)})"
        )
        return user_query


def retrieve_relevant_chunks(
    index,
    chunks,
    query,
    vectorizer,
    top_n=3
):
    """
    Retrieves the most relevant document chunks using FAISS.
    """

    query_vec = vectorizer.transform([query]).toarray()

    distances, indices = index.search(
        query_vec,
        top_n
    )

    return [
        chunks[i]
        for i in indices[0]
    ]


def generate_response(
    retrieved_chunks,
    user_query,
    api_key
):
    """
    Generates an answer using the retrieved document chunks
    and Gemini AI.
    """

    prompt = f"""
You are a chatbot that answers questions based only on the following
document content:

{retrieved_chunks}

User Question: "{user_query}"

Provide a clear and accurate answer based on the provided document content.
"""

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/gemini-3.5-flash-lite:generateContent"
    )

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    max_retries = 3

    for attempt in range(max_retries):

        try:
            response = requests.post(
                url,
                headers=headers,
                params={"key": api_key},
                json=data,
                timeout=60
            )

            # Handle temporary server overload or rate limiting
            if response.status_code in (503, 429):

                if attempt < max_retries - 1:

                    wait_time = (
                        (2 ** attempt)
                        + random.uniform(0, 1)
                    )

                    time.sleep(wait_time)
                    continue

                if response.status_code == 429:
                    st.error(
                        "You're sending requests too quickly. "
                        "Please wait a little before asking again."
                    )
                else:
                    st.error(
                        "Gemini is temporarily unavailable. "
                        "Please try your question again in a few seconds."
                    )

                return None

            response.raise_for_status()

            generated_content = (
                response.json()["candidates"][0]["content"]["parts"][0]["text"]
            )

            return generated_content.strip()

        except requests.exceptions.RequestException as e:

            if attempt < max_retries - 1:

                wait_time = (
                    (2 ** attempt)
                    + random.uniform(0, 1)
                )

                time.sleep(wait_time)

            else:

                st.error(
                    f"Gemini request failed: {repr(e)}"
                )

                return None