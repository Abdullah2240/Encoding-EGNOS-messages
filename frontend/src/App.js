// App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import InputForm from "./components/InputForm"; // Option 1 (dynamic single component)
// OR import InputForm1, InputForm2, ... if using Option 2

function Home() {
  const buttonIds = [1, 2, 3, 4, 5, 6, 7, 9, 10, 12, 17, 18, 24, 25, 26, 27, 28];

  return (
    <div className="container d-flex justify-content-center align-items-center min-vh-100">
      <div className="card p-4 shadow-lg w-75">
        <h1 className="text-center mb-4">Message Type Selector</h1>
        <div className="d-grid gap-2">
          {buttonIds.map((id) => (
            <Link
              key={id}
              to={`/input/${id}`}
              className="btn btn-primary"
            >
              Message Type {id}
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        {/* If using Option 1 (dynamic InputForm) */}
        <Route path="/input/:id" element={<InputForm />} />

        {/* If using Option 2 (separate components), replace above with: */}
        {/* <Route path="/input/1" element={<InputForm1 />} /> */}
        {/* <Route path="/input/2" element={<InputForm2 />} /> */}
        {/* ... up to 28 */}
      </Routes>
    </Router>
  );
}
