# Traditional Chinese Medicine (TCM) Backend API

This is a Flask backend for a Traditional Chinese Medicine (TCM) website, providing search result APIs in JSON format.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tcm_flask_backend.git
   cd tcm_flask_backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. Run the application:
   ```bash
   python run.py
   ```

## API Endpoints

### Search

- **URL**: `/api/search`
- **Method**: GET
- **Query Parameters**:
  - `query`: The search term to look for in herbs and treatments.
- **Response**: JSON object with arrays of matching herbs and treatments.

#### Example Request
```bash
curl -X GET "http://127.0.0.1:5111/api/search?query=ginseng"
```

#### Example Response
```json
{
  "herbs": [
    {
      "id": 1,
      "name": "Ginseng",
      "description": "Ginseng is a herb used in traditional medicine..."
    }
  ],
  "treatments": []
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.