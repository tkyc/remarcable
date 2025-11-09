## Assumptions

- **A product can belong to many categories**
- **A category can have many products** 
- **A product can have many tags**
- **A tag can have many products**
- Frontend is built in React with no styling, focusing on functionality
- Only GET endpoints implemented for product filtering (no POST endpoints for creation)
- Filtered results follow this logic: `(search text match) AND (category1 OR category2 OR...) AND (tag1 OR tag2 OR...)`

## Environment Requirements

- **Docker** must be installed on your system
- **Ports 3000 and 8000 must be free** (frontend and backend ports)

## Getting Started

1. **Navigate to the root of the project where the docker compose YAML file is located**

2. **Run the application:**
   ```bash
   docker compose up
   ```

   This will:
   - Build the Docker images for frontend and backend
   - Launch all services

3. **Wait for all services to be fully started**

## Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000

## API Endpoints

### Products Filtering
```
GET /api/products/?search=text&categories=1,2,3&tags=4,5,6
```

**Parameters:**
- `search` (optional): Text to search in product descriptions
- `category` (optional): Comma delimited category IDs
- `tag` (optional): Comma delimited tag IDs

## Stopping the Application

Press `Ctrl+C` in the terminal or run:
```bash
docker compose down
```

## Development Notes
- LLM was used for framework documentation parsing and test case idea generation
- The application containers are built from the Dockerfiles in the `frontend/` and `backend/` directories
