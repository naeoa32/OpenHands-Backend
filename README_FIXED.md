# OpenHands Backend - Fixed Version

This is a fixed version of the OpenHands Backend that resolves the Playwright installation issues and provides a simplified API server.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/maroonrose17/OpenHands-Backend.git
   cd OpenHands-Backend
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Playwright:
   ```bash
   pip install playwright
   ```

## Running the Application

There are two ways to run the application:

### 1. Simple API Server

The simple API server provides basic endpoints without requiring the full OpenHands functionality:

```bash
python simple_app.py
```

This will start a server on http://0.0.0.0:12000 with the following endpoints:
- `/` - Root endpoint with API information
- `/health` - Health check endpoint
- `/api/simple/conversation` - Simple conversation endpoint
- `/api/test-chat` - Test chat endpoint
- `/api/options/models` - Available models
- `/api/options/agents` - Available agents

### 2. Full OpenHands Backend

If you want to run the full OpenHands backend:

```bash
python app.py
```

## Environment Variables

The application uses the following environment variables:

- `PORT` - The port to run the server on (default: 12000)
- `HOST` - The host to run the server on (default: 0.0.0.0)
- `PLAYWRIGHT_BROWSERS_PATH` - The path to store Playwright browsers (default: /tmp/playwright_browsers)

## Troubleshooting

### Playwright Installation Issues

If you encounter issues with Playwright installation, the application will automatically:

1. Use a custom browser path in `/tmp/playwright_browsers`
2. Use a temporary HOME directory to avoid permission issues
3. Try multiple installation methods

### Permission Denied Errors

If you see "Permission denied: '/.cache'" errors, the application will use a temporary directory to avoid these issues.

## API Usage Examples

### Simple Conversation

```bash
curl -X POST -H "Content-Type: application/json" -d '{"message": "Hello, world!"}' http://localhost:12000/api/simple/conversation
```

### Test Chat

```bash
curl -X POST -H "Content-Type: application/json" -d '{"message": "Hello, world!"}' http://localhost:12000/api/test-chat
```

### Get Available Models

```bash
curl -X GET http://localhost:12000/api/options/models
```

### Get Available Agents

```bash
curl -X GET http://localhost:12000/api/options/agents
```