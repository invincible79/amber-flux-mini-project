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

- **`POST /upload-video/`**: Uploads a video file and extracts its frames.
- **`POST /index-frames/`**: Computes feature vectors for all extracted frames and stores them in the vector database.
- **`POST /get-vector/`**: Computes and returns the feature vector for a single image. This is useful for getting a vector to use in the query endpoint.
- **`POST /query-similar/`**: Queries the database using a provided feature vector to find similar frames.

## Usage

The intended workflow is a 4-step process:

1.  **Upload a video:**
    Send a `POST` request to `/upload-video/` with a video file (e.g., `.mp4`).

2.  **Index the frames:**
    Send a `POST` request to `/index-frames/`. This processes all the frames in the `frames/` directory and populates the vector database.

3.  **Get a query vector:**
    To perform a similarity search, you first need a vector to search with.
    - Send a `POST` request to `/get-vector/`.
    - In the request body, provide the path to one of the extracted frames (e.g., `{"image_path": "frames/frame_00000.jpg"}`).
    - Copy the `vector` array from the response.

4.  **Query for similar frames:**
    - Send a `POST` request to `/query-similar/`.
    - In the request body, paste the vector you copied in the previous step (e.g., `{"vector": [0.1, 0.2, ...]}`).
    - The API will return a list of the most similar frames from the database. 
