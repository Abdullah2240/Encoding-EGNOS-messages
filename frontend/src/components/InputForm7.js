import { useState } from "react";

function MessageType7() {
  const [formData, setFormData] = useState({
    preamble: "53",
    tlat: "",
    iodp: "",
    aii: ""
  });
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handlePreambleChange = (preambleValue) => {
    setFormData({
      ...formData,
      preamble: preambleValue
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://127.0.0.1:5000/api/numbers/7", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      setResult(data.hex_string || data.error);
    } catch (err) {
      console.error("Error:", err);
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center min-vh-100">
      <div className="card p-4 shadow-lg w-75">
        <h1 className="text-center mb-4">Message Type 7 (Fast Corr. Degradation)</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Select Preamble:</label>
            <div className="d-flex gap-2">
              <button
                type="button"
                className={`btn ${formData.preamble === "53" ? "btn-primary" : "btn-outline-primary"}`}
                onClick={() => handlePreambleChange("53")}
              >
                53
              </button>
              <button
                type="button"
                className={`btn ${formData.preamble === "9A" ? "btn-primary" : "btn-outline-primary"}`}
                onClick={() => handlePreambleChange("9A")}
              >
                9A
              </button>
              <button
                type="button"
                className={`btn ${formData.preamble === "C6" ? "btn-primary" : "btn-outline-primary"}`}
                onClick={() => handlePreambleChange("C6")}
              >
                C6
              </button>
            </div>
          </div>

          <div className="row g-2 mb-3">
            <div className="col">
              <input type="number" min="0" max="15" name="tlat" value={formData.tlat} onChange={handleChange} className="form-control" placeholder="System latency tlat (0-15 s)" required />
            </div>
            <div className="col">
              <input type="number" min="0" max="3" name="iodp" value={formData.iodp} onChange={handleChange} className="form-control" placeholder="IODP (0-3)" required />
            </div>
          </div>

          <div className="mb-3">
            <textarea
              name="aii"
              className="form-control"
              rows={4}
              placeholder="Enter up to 51 degradation factor indicators aii (comma separated, each 0-15). Missing entries default to 0."
              value={formData.aii}
              onChange={handleChange}
            />
          </div>

          <button type="submit" className="btn btn-primary w-100">Submit</button>
        </form>

        {result && (
          <div className="mt-4 p-3 bg-light border rounded">
            <p className="mb-0">Result: {result}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default MessageType7;
