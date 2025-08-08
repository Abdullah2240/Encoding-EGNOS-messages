# Full Stack Website Project

This project is a full-stack web application that consists of a backend built with Python and Flask, and a frontend built with React. The application accepts a comma-separated list of numbers from the user, validates the input, and returns a response.

## Project Structure

```
fullstack-website
├── backend
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
├── frontend
│   ├── public
│   │   └── index.html
│   ├── src
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── README.md
└── README.md
```

## Backend Setup

1. Navigate to the `backend` directory:
   ```
   cd backend
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```
   python app.py
   ```

## Frontend Setup

1. Navigate to the `frontend` directory:
   ```
   cd frontend
   ```

2. Install the required dependencies:
   ```
   npm install
   ```

3. Start the React application:
   ```
   npm start
   ```

## Usage

- Open your browser and go to `http://localhost:3000`.
- Enter a comma-separated list of numbers (1-210) with a maximum of 51 numbers in the input field.
- Submit the form to see the response from the backend.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.