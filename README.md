# FastAPI RAG Project

## Overview

The FastAPI RAG (Retrieval-Augmented Generation) Project is a full-stack application for managing documents with integrated Natural Language Processing (NLP) capabilities. It allows users to upload documents, which are processed and stored in a database, and enables querying of document content using a simple interface with ChatGPT for contextual responses.

## Features

- **Authentication**: JWT-based authentication for secure access.
- **Document Upload**: Users can upload documents which are processed and stored in the database.
- **Document Querying**: Users can query documents based on content, and responses are generated using ChatGPT.
- **RAG Capabilities**: Utilizes unstructured.io for document processing and ChatGPT for querying and generating responses.

## Project Structure

- **FastAPI**: The backend API framework.
- **Database**: Stores document metadata and processed content.
- **Unstructured.io**: Used for processing document content.
- **ChatGPT**: Provides context-based responses to queries.

## API Endpoints

### Authentication Endpoints

#### `POST /auth/register`

- **Summary**: Register a new user.
- **Request Body**: JSON with `username`, `email`, and `password`.
- **Response**: JWT token for authentication.

#### `POST /auth/login`

- **Summary**: Login a user and get a JWT token.
- **Request Body**: JSON with `username` and `password`.
- **Response**: JWT token for authentication.

### Document Management Endpoints

#### `POST /documents/upload`

- **Summary**: Upload a document.
- **Request Body**: Multipart form data with the document file.
- **Response**: Confirmation of document upload.

#### `GET /documents/`

- **Summary**: List all uploaded documents.
- **Parameters**: JWT token in query parameter.
- **Response**: List of documents with metadata.

### Query Endpoints

#### `POST /query/`

- **Summary**: Query a document's content using NLP.
- **Request Body**: JSON with `document_id`, `query`, and JWT token.
- **Response**: Generated response based on the query.

## Database Schema

- **Document Table**: Stores metadata of uploaded documents.
- **Document_Content Table**: Stores processed content of documents for querying.

## How to Run the Project

### 1. Clone the repository:

```bash
git clone <repository-url>
```

### 2. Install Docker and Docker Compose

Ensure Docker and Docker Compose are installed on your machine. If not, follow the instructions from Docker's official website to install Docker.

### 3. Create a .env File

In the root of your project, create a .env file with the following contents:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres <your db url> # Change it
SECRET_KEY=<your secret>
UNSTRUCTURED_API_KEY=<your secret>
UNSTRUCTURED_API_URL=<your url>
ELASTICSEARCH_URL=http://localhost:9200
OPEN_AI_SECRET_KEY=<your secret>
```

### 4. Build and Start the Docker Containers

Use Docker Compose to build and run the project with the following commands:

```bash
docker-compose build
docker-compose up
```

### 5. Access the Application

Once the Docker containers are running, the FastAPI application will be available at:

    API Docs: http://localhost:8000/docs
    OpenAPI Schema: http://localhost:8000/openapi.json

### 6. Example Requests

#### 1. Register User

```bash
curl -X POST "http://localhost:8000/auth/register" -H "Content-Type: application/json" -d '{
  "username": "john_doe",
  "email": "john.doe@example.com",
  "password": "password123"
}'
```

#### 2. Login User

```bash
curl -X POST "http://localhost:8000/auth/login" -H "Content-Type: application/json" -d '{
  "username": "john_doe",
  "password": "password123"
}'
```

#### 3. Upload Document

```bash
curl -X POST "http://localhost:8000/documents/upload?token=your_jwt_token" -H "Content-Type: multipart/form-data" -F "file=@path/to/document.pdf"
```

#### 4. Query Document

```bash
curl -X POST "http://localhost:8000/query/?document_id=1&query=objective&token=your_jwt_token"
```

## Technologies Used

- FastAPI: Web framework for building APIs.
- Pydantic: Data validation and settings management.
- Elasticsearch: Used for storing and searching document content.
- Unstructured.io: Document processing API.
- JWT: Authentication mechanism.
- OpenAI (ChatGPT): For NLP-based responses.

### Key Points in This Setup:

- **.env File**: Contains environment variables required for the project to run, including database URLs, API keys, and JWT secrets.
- **Docker Setup**: You can easily build and start the entire project using `docker-compose` with a single command. The setup assumes you have Docker and Docker Compose installed.
- **API Endpoints**: The `README.md` includes example requests for registering, logging in, uploading documents, and querying document content.

This setup will allow you to deploy and test the project quickly, leveraging Docker to manage services like the database and Elasticsearch.
