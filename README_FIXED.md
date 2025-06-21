# OpenHands Backend - Fixed Version

This is a fixed version of the OpenHands Backend that resolves the Playwright installation issues and provides a fallback API server when the main OpenHands app cannot be loaded.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/maroonrose17/OpenHands-Backend.git
   cd OpenHands-Backend
   ```

2. Run the startup script:
   ```bash
   ./start.sh
   ```

   This script will:
   - Install all required dependencies
   - Install Playwright browsers in a custom path
   - Start the application

## How It Works

The application has been modified to handle Playwright installation issues and provide a fallback API when the main OpenHands app cannot be loaded:

1. **Playwright Installation Fix**:
   - Uses a custom browser path in `/tmp/playwright_browsers`
   - Creates a temporary HOME directory to avoid permission issues
   - Tries multiple installation methods (with and without dependencies)
   - Falls back to direct download if needed

2. **Fallback API**:
   - When the main OpenHands app cannot be loaded, a fallback API is created
   - Provides basic endpoints for testing and simple conversations
   - Uses memory-based storage to avoid file permission issues

## Environment Variables

The application uses the following environment variables (set automatically by the startup script):

- `PORT` - The port to run the server on (default: 12000)
- `HOST` - The host to run the server on (default: 0.0.0.0)
- `PLAYWRIGHT_BROWSERS_PATH` - The path to store Playwright browsers (default: /tmp/playwright_browsers)
- `SETTINGS_STORE_TYPE`, `SECRETS_STORE_TYPE`, `CONVERSATION_STORE_TYPE`, `FILE_STORE`, `SESSION_STORE_TYPE` - All set to "memory" to avoid file permission issues
- `DISABLE_SECURITY`, `OPENHANDS_DISABLE_AUTH` - Set to "true" for public API access
- `DISABLE_FILE_LOGGING`, `DISABLE_PERSISTENT_SESSIONS` - Set to "true" to avoid file permission issues

## Troubleshooting

### Playwright Installation Issues

If you encounter issues with Playwright installation, the application will automatically:

1. Use a custom browser path in `/tmp/playwright_browsers`
2. Use a temporary HOME directory to avoid permission issues
3. Try multiple installation methods

### Permission Denied Errors

If you see "Permission denied: '/.cache'" errors, the application will use a temporary directory to avoid these issues.

### Module Import Errors

If you see "No module named 'openhands.app'" errors, the application will automatically create a fallback API with basic functionality.

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

### Health Check

```bash
curl -X GET http://localhost:12000/health
```