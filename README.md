## Setup

1. Clone the repository.
2. Set up the virtual environment:
   ```sh
   python -m venv chatbot-env
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   source chatbot-env/bin/activate  # On Windows, use `chatbot-env\Scripts\activate`
   

3. Install required libraries
   ```
   pip install -r requirements.txt
   python -m nltk.downloader all
   python -m spacy download en_core_web_sm
   Set-ExecutionPolicy Restricted -Scope CurrentUser
   ```

4. Run the project:
   ```
   python .\backend\run.py
   ```

5. App is running on
   ```
   http://127.0.0.1:5000/api/hello
   ```
