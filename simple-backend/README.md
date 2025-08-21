# DictyExpress Simple Backend (Django REST Framework)

A Django REST Framework backend that provides mock gene expression data for the DictyExpress application.

## Features

- **Gene Search API**: Search genes by name, feature ID, or full name
- **Time Series Data**: Manage time series experiments and partitions
- **Expression Data**: Store and retrieve gene expression values
- **Basket Management**: Create and manage sample baskets
- **User Authentication**: Basic user management endpoints
- **Debug Tools**: State inspection for development

## Quick Start

### Prerequisites

- Python 3.8+
- pip or pipenv

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run database migrations:**
```bash
python manage.py migrate
```

3. **Start the development server:**
```bash
python manage.py runserver 0.0.0.0:3001
```

The server will be available at `http://localhost:3001`

### Health Check

Visit `http://localhost:3001/health/` to verify the server is running.

## API Endpoints

### Time Series

- `GET /api/relation/` - Get time series data with filtering
- `POST /api/relation/` - Add new time series data

### Gene Search

- `GET /api/kb/feature/` - Search genes (supports query, source, species, limit parameters)
- `GET /api/genelist/` - Get genes by feature IDs
- `POST /api/genes/` - Add new genes

### Expression Data

- `GET /api/data/` - Get sample data by IDs
- `POST /api/data/` - Add new sample data
- `GET /api/storage/<id>/` - Get expression storage by ID
- `POST /api/storage/` - Add new expression storage

### Baskets

- `POST /api/basket/_/add_samples/` - Create basket with samples
- `GET /api/_modules/visualizations/basket_expressions/` - Get basket expressions

### User Management

- `GET /api/user/` - Get user information

### Debug

- `GET /api/debug/state/` - Get complete backend state (for development)

## Example Usage

### Search for genes containing "actin":
```bash
curl "http://localhost:3001/api/kb/feature/?query=actin&limit=10"
```

### Get time series data:
```bash
curl "http://localhost:3001/api/relation/?category=Time%20series"
```

### Add a new gene:
```bash
curl -X POST http://localhost:3001/api/genes/ \
  -H "Content-Type: application/json" \
  -d '{
    "feature_id": "DDB_G0999999",
    "name": "testGene",
    "full_name": "Test Gene",
    "description": "A test gene",
    "source": "dictybase",
    "species": "dictyostelium"
  }'
```

### Create a basket:
```bash
curl -X POST http://localhost:3001/api/basket/_/add_samples/ \
  -H "Content-Type: application/json" \
  -d '{
    "samples": ["101", "102", "103"]
  }'
```

## Configuration

### Environment Variables

- `DEBUG`: Set to `False` for production
- `SECRET_KEY`: Django secret key (change in production)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### CORS Settings

The backend is configured to allow all origins for development. For production, update the CORS settings in `settings.py`.

## Migration from Node.js Backend

This Django backend provides the same API endpoints as the original Node.js Express backend:

1. **Endpoint Compatibility**: All endpoints maintain the same URL patterns and response formats
2. **Data Structure**: Mock data structure preserved from the original implementation
3. **Response Format**: Maintains the `{"data": [...]}` wrapper for list endpoints
4. **Error Handling**: Similar error responses and status codes

### Differences from Node.js Version

- Built on Django REST Framework instead of Express.js
- Uses Python instead of JavaScript
- SQLite database ready (currently using in-memory storage for baskets)
- Built-in Django admin interface available
- Better request validation and serialization

## Development

### Adding New Endpoints

1. Add view function in `api/views.py`
2. Add URL pattern in `api/urls.py`
3. Update this README with endpoint documentation

### Mock Data

Mock data is stored in `api/mock_data.py`. Modify this file to add or update sample data.

### Database Models

Currently using in-memory storage for simplicity. To add persistent models:

1. Create models in `api/models.py`
2. Create and run migrations
3. Update views to use database models instead of mock data

## Deployment

For production deployment:

1. Set `DEBUG = False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up proper CORS and security settings
4. Use a WSGI server like Gunicorn
5. Configure static file serving

## Troubleshooting

### Common Issues

1. **Port already in use**: The default port is 3001. Change it with: `python manage.py runserver 0.0.0.0:8000`
2. **CORS errors**: Ensure CORS settings allow your frontend domain
3. **Missing dependencies**: Run `pip install -r requirements.txt`

### Debug Mode

Use the debug endpoint to inspect backend state:
```bash
curl http://localhost:3001/api/debug/state/
```