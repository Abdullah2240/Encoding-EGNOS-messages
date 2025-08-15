// App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

// Import your forms
import InputForm1 from "./components/InputForm1.js";
import InputForm2 from "./components/InputForm2.js";
import InputForm3 from "./components/InputForm3.js";
import InputForm4 from "./components/InputForm4.js";
import InputForm5 from "./components/InputForm5.js";
import InputForm6 from "./components/InputForm6.js";
import InputForm7 from "./components/InputForm7.js";
import InputForm9 from "./components/InputForm9.js";
import InputForm10 from "./components/InputForm10.js";
import InputForm12 from "./components/InputForm12.js";
import InputForm17 from "./components/InputForm17.js";
import InputForm18 from "./components/InputForm18.js";
import InputForm24 from "./components/InputForm24.js";
import InputForm25 from "./components/InputForm25.js";
import InputForm26 from "./components/InputForm26.js";
import InputForm27 from "./components/InputForm27.js";
import InputForm28 from "./components/InputForm28.js";

function Home() {
  const buttonIds = [1, 2, 3, 4, 5, 6, 7, 9, 10, 12, 17, 18, 24, 25, 26, 27, 28];

  return (
    <div className="container d-flex justify-content-center align-items-center min-vh-100">
      <div className="card p-4 shadow-lg w-75">
        <h1 className="text-center mb-4">Message Type Selector</h1>
        <div className="d-grid gap-2">
          {buttonIds.map((id) => (
            <Link key={id} to={`/input/${id}`} className="btn btn-primary">
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

        <Route path="/input/1" element={<InputForm1 />} />
        <Route path="/input/2" element={<InputForm2 />} />
        <Route path="/input/3" element={<InputForm3 />} />
        <Route path="/input/4" element={<InputForm4 />} />
        <Route path="/input/5" element={<InputForm5 />} />
        <Route path="/input/6" element={<InputForm6 />} />
        <Route path="/input/7" element={<InputForm7 />} />
        <Route path="/input/9" element={<InputForm9 />} />
        <Route path="/input/10" element={<InputForm10 />} />
        <Route path="/input/12" element={<InputForm12 />} />
        <Route path="/input/17" element={<InputForm17 />} />
        <Route path="/input/18" element={<InputForm18 />} />
        <Route path="/input/24" element={<InputForm24 />} />
        <Route path="/input/25" element={<InputForm25 />} />
        <Route path="/input/26" element={<InputForm26 />} />
        <Route path="/input/27" element={<InputForm27 />} />
        <Route path="/input/28" element={<InputForm28 />} />
      </Routes>
    </Router>
  );
}
