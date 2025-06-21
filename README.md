# Video Feature Extraction and Retrieval API

This is a FastAPI application that allows you to upload a video, extract frames, compute feature vectors for each frame, store them in a Qdrant vector database, and then query for similar frames.

## Project Structure

- `main.py`: The main FastAPI application file containing the API endpoints.
- `utils/`: A directory containing helper modules for video processing, feature extraction, and Qdrant client.
- `frames/`: The default directory where extracted frames are saved.
- `config.py`: The configuration file for the application.
- `requirements.txt`: A file containing all the project dependencies.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\\Scripts\\activate`
    pip install -r requirements.txt
    ```

3.  **Run the FastAPI application:**
    ```bash
    uvicorn main:app --reload
    ```

The application will be running at `http://127.0.0.1:8000`.

## API Endpoints

You can access the API documentation at `http://127.0.0.1:8000/docs`.

- **`POST /upload-video/`**: Upload a video file.
- **`POST /index-frames/`**: Index the extracted frames.
- **`POST /query-similar/`**: Query for similar frames.

## Usage

1.  **Upload a video:**
    Send a POST request to `/upload-video/` with a video file.

2.  **Index the frames:**
    Send a POST request to `/index-frames/`.

3.  **Query for similar frames:**
    Send a POST request to `/query-similar/` with a JSON payload containing the path to an image. 