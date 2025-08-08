# Backend README

# Fullstack Website Backend

This is the backend component of the Fullstack Website project. It is built using Python and Flask, and it handles incoming requests from the frontend, processes user input, and returns responses.

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd fullstack-website/backend
   ```

2. **Create a virtual environment (optional but recommended):**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   python app.py
   ```

The server will start on `http://127.0.0.1:5000`.

## API Endpoint

### POST /numbers

This endpoint accepts a comma-separated list of numbers ranging from 1 to 210, with a maximum of 51 numbers.

#### Request Body

- Content-Type: application/json
- Example:
  ```json
  {
    "numbers": "1,2,3,4,5"
  }
  ```

#### Response

- Returns a JSON object with the processed data or an error message if the input is invalid.

## Usage Example

To test the API, you can use tools like Postman or curl. Here’s an example using curl:

```bash
curl -X POST http://127.0.0.1:5000/numbers -H "Content-Type: application/json" -d '{"numbers": "1,2,3,4,5"}'
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.