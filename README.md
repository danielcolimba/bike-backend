# Bike-BackEnd

This project is a backend API for managing bike sells and related operations in a cloud environment.

## Technologies Used

- Python
- Django
- Django REST Framework
- PostgreSQL 
- Docker 
- Git
- Cloud deployment tools: AWS

## Deployment Instructions (Without Docker)

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/bike-backend.git
    cd bike-backend
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables:**
    - Copy `.env.example` to `.env` and update the values as needed.

5. **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser (optional):**
    ```bash
    python manage.py createsuperuser
    ```

7. **Start the development server:**
    ```bash
    python manage.py runserver
    ```

8. **Access the API:**
    - Open your browser and go to `http://localhost:8000/`