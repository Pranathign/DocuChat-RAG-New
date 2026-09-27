# DocuChat - RAG based Chatbot using Google Gemini API

This Streamlit application allows users to upload PDF files, extract text from these files, and interact with a Retrieval Augmented Generation (RAG)-based chatbot. The chatbot provides responses based on the content of the uploaded documents. The app uses a vector database (FAISS) for efficient retrieval and the Gemini API for generating responses.

## Architecture Diagram

![image](https://assets-global.website-files.com/6473d8d02a3cf26273f2787d/651bace425f4ab9a433ebb58_lza0eo3oqTb6m0PqYyqi2kvaE5FqV5DCjTilL54lzbaMyycn8OgUA9aVadwWKtFwSjcJnAzj7bFxTWuywBKKYzRle5yw7V51CrnUlmmulJyCnnIdKzi9CB4YgAiTo-XEzg7RQpKkfKLohOvcVFaj61E.png)

## Features

- **PDF Upload**: Users can upload PDF files via the Streamlit file uploader.
- **Text Extraction**: Extracts text from the uploaded PDF file.
- **Document Processing**: Converts documents into chunks, vectors, and stores them in FAISS.
- **Chatbot Interaction**: Users can ask questions and get responses based on the content of the uploaded PDF.
- **Session Management**: Maintains chat history during the user's session.

## Requirements

- Python 3.7 or higher
- Streamlit
- PyPDF2
- scikit-learn
- faiss-cpu
- requests

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/RAHULMYDUR/RAG-Based-ChatBOT.git
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **API Key**:
   - Obtain an API key from the Gemini API service.
   - Replace `YOUR_API_KEY_HERE` in `app.py` with your actual API key.

## Code Overview

- **`app.py`**: Main application script that manages file uploads, processes the PDF, and handles chatbot interactions.
- **`file_handler.py`**: Contains functions to extract text from the PDF file.
- **`processing.py`**: Handles document chunking, vectorization, and storage in FAISS.
- **`retrieval_response.py`**: Manages retrieval of relevant chunks and generates responses using the Gemini API.

## Usage

1. **Run the Application Locally**:
   ```bash
   streamlit run app.py
   ```

2. **Upload a PDF**:
   - Use the file uploader in the sidebar to upload a PDF file.
   - The file will be processed, and the text will be extracted.

3. **Ask Questions**:
   - Enter your question in the text input field and click "Get Answer".
   - The chatbot will provide a response based on the content of the uploaded PDF.

4. **View Chat History**:
   - The chat history will be displayed below the input field, showing your questions and the chatbot’s responses.

## Live Application

You can access the live version of the chatbot application [here](https://rag-based-chatbot-for-pdf.streamlit.app/). Test the app to see how it works with your PDF files and interact with the chatbot.
![image](https://github.com/user-attachments/assets/9a6ca425-a54a-49de-a626-dccbadd6d7f3)


## Deployment

### On Streamlit Sharing

1. **Create a GitHub Repository**:
   - Create a new repository on GitHub.
   - Add your code files (`app.py`, `file_handler.py`, `processing.py`, `retrieval_response.py`) to the repository.
   - Include a `.gitignore` file to exclude unnecessary files.

2. **Push Code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

3. **Deploy on Streamlit**:
   - Go to [Streamlit Sharing](https://streamlit.io/sharing).
   - Click on "New App".
   - Connect your GitHub account and select the repository.
   - Configure the settings, such as branch (`main`) and main file (`app.py`).
   - Click "Deploy".

## File Handling

- **Temporary Storage**: Uploaded files are temporarily stored in memory. They are not saved to the server's filesystem and are available only during the session.

## Troubleshooting

- **Large Files**: If processing large files, ensure the application has sufficient memory.
- **Dependencies**: Ensure all required packages are listed in `requirements.txt`.

## Contributing

Feel free to fork the repository and submit pull requests. Contributions and improvements are welcome!

## Contact

For any questions or issues, please open an issue on the GitHub repository or contact the maintainer at rahulmydur@gmail.com.
