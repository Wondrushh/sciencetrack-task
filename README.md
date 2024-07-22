# Library Management System

This Library Management System allows users to manage books and authors.


## Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Wondrushh/sciencetrack-task.git
   cd sciencetrack-task
   ```

2. **Set Up the Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the Server**:
   ```bash
   python manage.py runserver
   ```

### Using Docker

Alternatively, you can use Docker and Docker Compose to set up the project:

```bash
docker compose up --build
```

Your application will be available at http://localhost:8000.

## Testing

Run the following command to execute tests:

```bash
python manage.py test library
```