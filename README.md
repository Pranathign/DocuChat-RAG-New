# DocuChat - RAG-Based Document Assistant

DocuChat is a Streamlit-based Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and interact with them through a conversational AI interface.

The application extracts content from uploaded PDFs, processes the document into searchable chunks, retrieves relevant information using FAISS, and uses Google's Gemini API to generate responses based on the retrieved document content.

## Features

- **PDF Upload**
  Upload PDF documents directly through the Streamlit interface.

- **PDF Text Extraction**
  Extract text content from uploaded PDF files.

- **Document Chunking**
  Split extracted document content into smaller chunks for efficient retrieval.

- **Vector Search with FAISS**
  Convert document chunks into vectors and retrieve the most relevant content using FAISS similarity search.

- **History-Aware Query Reformulation**
  Use recent conversation history to rewrite contextual follow-up questions into standalone queries before performing FAISS retrieval. This allows questions containing references such as "that", "this", or "it" to be understood based on the previous conversation.

- **Gemini AI Responses**
  Use Google's Gemini API to generate responses based on the retrieved document content.

- **Conversational Interface**
  Ask multiple questions about the uploaded document through a ChatGPT-style interface.

- **Session Chat History**
  Maintain the conversation history during the current application session.

## RAG Architecture

The application follows the RAG pipeline with history-aware query reformulation:

```text
PDF Document
     ↓
Text Extraction
     ↓
Document Chunking
     ↓
Vectorization
     ↓
User Question
     ↓
Conversation History
     ↓
History-Aware Query Reformulation
     ↓
FAISS Vector Search
     ↓
Relevant Document Chunks
     ↓
Gemini AI
     ↓
Generated Response
