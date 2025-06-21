# Video Feature Extraction and Retrieval API

This is a FastAPI application that allows you to upload a video, extracts frames, computes feature vectors for each frame, stores them in a Qdrant vector database, and then query for similar frames.

## Try the Live API

You are welcome to test the live, deployed application using the interactive Swagger UI.

**Live API Docs Link:** `https://amber-flux-mini-project-pushkarmahajan.onrender.com/docs`


**Note:** This is a free-tier deployment. The application will "go to sleep" after a period of inactivity and may take up to a minute to wake up on the first request.

## How It Works

This application is built with a modern, stateless architecture suitable for cloud deployment:

-   **Backend**: FastAPI handles the web server and API endpoints.
-   **Video & Image Processing**: OpenCV (`cv2`) is used to extract frames from videos and compute color histograms as feature vectors.
-   **Vector Database**: Feature vectors are stored and queried in a managed [Qdrant Cloud](https://cloud.qdrant.io/) instance.
-   **Deployment**: The application is hosted on [Render](https://render.com), which automatically deploys from the `main` branch of this repository.

## Project Structure

This repository contains the source code for the application:

-   `main.py`: The main FastAPI application file containing the API endpoints.
-   `utils/`: A directory containing helper modules for video processing, feature extraction, and the Qdrant client.
-   `config.py`: The configuration file. On the deployed version, secrets are managed via environment variables.
-   `requirements.txt`: A file containing all the project dependencies.

## API Endpoints

- **`POST /upload-video/`**: The primary endpoint. Uploads a video, extracts frames, computes feature vectors, and indexes them in the Qdrant database all in one step.
- **`POST /get-vector/`**: A helper endpoint that accepts an image file upload and returns its computed feature vector.
- **`POST /query-similar/`**: Queries the database using a provided feature vector to find similar frames.

## How to Test the Live Application

Here is a simple, 2-step process to test the core functionality directly from the live API documentation:

1.  **Upload a Video & Get a Sample Vector:**
    - Navigate to the `POST /upload-video/` endpoint.
    - Click "Try it out", upload a video file (e.g., `.mp4`), and click "Execute".
    - The response will contain a `sample_query` object. **Copy the `vector` array** from this object. It looks like `[0.1, 0.2, ...]`.

2.  **Query for Similar Frames:**
    - Navigate to the `POST /query-similar/` endpoint.
    - Click "Try it out". In the request body, **paste the vector you copied** from the previous step.
    - Click "Execute". The API will return a list of the most similar frames from the video you just uploaded.

The `/get-vector` endpoint is also available as a helper if you wish to provide your own image file instead of using the sample from the video upload. 
