
# FamPay Assignment

## Description
This project implements a service that continuously fetches the latest videos from YouTube for a predefined search query and stores relevant video data in a database. The server runs asynchronously, making periodic API calls to ensure the database is always up-to-date with the most recent videos. The stored data includes essential fields such as video title, description, publishing date-time, and thumbnail URLs, optimized for fast retrieval with proper indexing.

Additionally, a GET API provides a paginated response, allowing users to fetch the stored videos in descending order of their publishing date-time. The solution is designed to handle potential API rate limits by switching between API keys as needed.

## Features
### **Core Features:**

1.  **Continuous YouTube API Calls (Async)**:
    -   The server will call the YouTube API at regular intervals to fetch the latest videos for a predefined search query for always providing up-to-date information. 
   
2.  **Data Storage with Indexing**:
    
    -   The system allows for saving and lookup of predefined queries as well as user input queries allowing for a more flexible approach.
    
4.  **GET API for Paginated Responses**:
    
    -   Provides paginated responses in sorted order to save bandwidth as well as maximizing the overall inference for the user
    

### **Bonus Features:**

1.  **Multiple API Key Support**:
    
    -   The system is designed to be able to handle multiple API keys to work around the API quota limitations.
    -   This is achieved by automatically switching to the next available key when one is exhausted.

2.  **Dashboard**:
    -   Interface for viewing stored video data.
    -   Include filtering and sorting options to enhance data browsing experience.

## Technology

1. Python (Programming Language)  
2. Django (Web Framework)  
3. SQLite (Database)
4. API YouTube Data API

### Design Considerations
1. **Asynchronous Task Management**
-- Focus should also be on making it efficient from resource consumption standpoint and something that can be hosted as containers.  
2. **Efficient storage and retrieval**
-- Ordering data to ensure efficient querying for both paginated GET requests and background inserts.


### API Endpoints


#### Fetch Videos

-  **Endpoint**: `GET api/videos`
-  **Parameters**:
--  `query` (optional): Looks up a specific query for searching videos
--  `page_number` (optional): Returns the given page number, empty list is page does not exist
-  **Purpose**: This endpoint retrieves a paginated list of videos sorted by their publish date in descending order. It allows clients to fetch videos with optional pagination parameters.


#### Add Keys
- **Endpoint**: `GET POST api/api_key `
- GET request is used to list out all keys along with their status
- POST request is used  to add new keys to the database


#### Interface
- `GET /` The interface is provided at the root level for easy interaction with the system

## Getting Started

To run the project locally, follow these steps:

1. Clone the repository:

```bash
git  clone  https://github.com/omkargwagholikar/FamPay_Backend_Assignment.git
```

2. Create a `.env` file

* Rename `.example.env` to `.env`.
* The default query can then be manipulated from the `.env` file.

## Running the application

This application can be run either locally or using Docker. Choose the method that best suits your environment.

**Setup**
```bash
git clone https://github.com/omkargwagholikar/FamPay_Backend_Assignment.git
```
1.  **Prerequisites:**
* Python 3.10+
* pip (package installer)

2. **Running the web app**

****
```bash
# Clone the repository:
git  clone  https://github.com/omkargwagholikar/FamPay_Backend_Assignment.git
# Create a virtual environment:
python3  -m  venv  venv
cd  FamPay_Task/
#Activate the virtual environment:
#Windows
.\env\Scripts\activate
#Linux
source  env/bin/activate
#Install dependencies within the virtual environment:
pip  install  -r  requirements.txt
# Run the application within the virtual environment:
cd  FamPay
python  manage.py  runserver
```

The API's will be accessible at `http://localhost:8000`.

With these instructions, users will be guided on how to set up and run the application within a virtual environment.
 
4.  **Alternatively: Run with Docker:**

  
```bash
docker  build  -t  drf-app  .
docker  run  -d  -p  8000:8000  --name  drf-app  drf-app
```

This will build a Docker image and run the application on port 8000.


The API will be accessible at `http://localhost:8000`.

## Learnings
- Task Scheduling and Intervals
- Handling Failures and Retries
-- Understood the considerations that go into making  the system more  resilient and handling edge cases