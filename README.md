# AZ-104 Exam Reviewer

A containerized application for reviewing Azure AZ-104 exam questions. Built with Python and Docker.

## Features

- Complete set of 572 AZ-104 practice exam questions
- Interactive quiz interface with progress tracking
- Detailed statistics including correct/incorrect answer counts and time spent
- Progress bar to visualize your completion status
- Responsive design for desktop and mobile devices

## Docker Image

The application is available as a Docker image on DockerHub:

```
docker pull lloydismael12/az104-reviewer:latest
```

## Running the Application

You can run the application using Docker:

```
docker run -p 5000:5000 lloydismael12/az104-reviewer:latest
```

Then open your browser and navigate to http://localhost:5000

## Development

### Prerequisites

- Python 3.11+
- Docker (optional for containerization)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/lloydismael/AZ-104-Reviewer.git
   cd AZ-104-Reviewer
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python run.py
   ```

The application will be available at http://localhost:5000

### Building the Docker Image

```
docker build -t az104-reviewer .
```

## License

MIT
