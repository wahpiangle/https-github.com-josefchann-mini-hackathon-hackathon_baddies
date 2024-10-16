# Project Setup

To install the required packages for this project, run the following command:

```bash
pip install -r requirements.txt
```

To create the Virtual Environment for Python 3.9.12 (The one we are using)

```bash
py -3.9 -m venv venv
```

### To activate the virtual environment

```bash
.\venv\Scripts\Activate
```

### To deactivate the virtual environment

```bash
deactivate
```

Here’s a more polished and structured version for your `README.md` that provides clear instructions on running the FastAPI server and testing the API:

---

## How to Run the FastAPI Server and Test the API

### Step 1: Run the FastAPI Server

To start the FastAPI server, run the following command in your terminal:

```bash
uvicorn pipeline:app --reload
```

This command will:

- Launch the server at `http://127.0.0.1:8000`.
- Enable **hot reloading**, so the server will restart automatically when you make changes to your code.

### Step 2: Download Postman to Test the API

You can use [Postman](https://www.postman.com/downloads/) to easily test the API endpoints.

1. Download and install Postman.
2. Create a new request in Postman, choose the appropriate HTTP method (e.g., `POST`), and enter your API endpoint URL.
3. Provide the necessary input data (e.g., JSON payload that you can find in spellingCheckerSample.txt) and hit **Send**.
4. Review the API response directly within Postman.

Alternatively, you can use FastAPI's built-in interactive docs at `http://127.0.0.1:8000/docs` to explore and test the API.

---

### Download Ollama

Download and install Ollama from [Ollama Download Page](https://ollama.com/download) based on your operating system.

After installation, verify the Ollama installation by running:

```bash
ollama --version
```

Ensure that you have the correct version installed. You should be using Ollama version 0.3.12.

Pull the ollama2 model from the registry (this will download the required model to your local machine):

```bash
ollama pull llama3.1
```
