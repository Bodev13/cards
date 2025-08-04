# Flask Web App "Cards"

This is a `Flask` web application that lets you record interpretations after selecting one or more (tarot) cards, add notes or update them later, and manage readings (create, edit, delete). Each reading has a date of creation. All data is stored in `MongoDB`.
You can containerize and run this Flas application using Docker.

---

### Prerequisites

---
- MongoDB
- Flask

## Quickstart

### 1. Clone the repository

```bash
git clone git@github.com:Bodev13/cards.git
cd cards
```

### Usage


### 2. Create and activate a virtual environment (optional but recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate    # On Mac/Linux
# or
.venv\Scripts\activate       # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your `.env` file

```bash
cp example.env .env
```

### 5 Run the application
Note: If running inside Docker, make sure your app.run() uses host="0.0.0.0" so the app is accessible from outside the container.

```bash
python app.py
```


### 6. Update your app.py (if using Docker)
Make sure your Flask app runs on all interfaces

### 7. Build and run the container with docker-compose

```bash
docker-compose up --build
```

### 8. Open your browser and go to
```bash
http://localhost:5001
```

### 8. CI/CD with GitHub Actions

The workflow file is located at [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml)


## What the CI/CD pipeline does:

- Checks out the repository code
- Sets up Python (version 3.11)
- Installs dependencies from requirements.txt
- Runs automated tests using pytest
- Builds a Docker image for the application

## Triggering:

The workflow is triggered automatically

- On every push to the main branch
- On every pull request targeting the main branch








