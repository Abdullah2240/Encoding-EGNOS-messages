import { useState } from "react";

function MessageType12() {
  const [formData, setFormData] = useState({
    preamble: "53",
    iodp: "",
    iodf: "",
    pseudoRangeCorrections: "",
    udreis: ""
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
      const res = await fetch("http://127.0.0.1:5000/api/numbers/12", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      setResult(data.hex_string);
    } catch (err) {
      console.error("Error:", err);
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center min-vh-100">
      <div className="card p-4 shadow-lg w-75">
        <h1 className="text-center mb-4">Message Type 12</h1>
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
          <div className="mb-3">
            <input
              type="number"
              name="iodp"
              placeholder="Enter IODP (0-3)"
              className="form-control"
              value={formData.iodp}
              onChange={handleChange}
              required
            />
          </div>
          <div className="mb-3">
            <input
              type="number"
              name="iodf"
              placeholder="Enter IODF (0-3)"
              className="form-control"
              value={formData.iodf}
              onChange={handleChange}
              required
            />
          </div>
          <div className="mb-3">
            <input
              type="text"
              name="pseudoRangeCorrections"
              placeholder="Enter up to 13 Pseudo Range Corrections (comma separated, in meters)"
              className="form-control"
              value={formData.pseudoRangeCorrections}
              onChange={handleChange}
              required
            />
          </div>
          <div className="mb-3">
            <input
              type="text"
              name="udreis"
              placeholder="Enter up to 13 UDREIs (comma separated)"
              className="form-control"
              value={formData.udreis}
              onChange={handleChange}
              required
            />
          </div>
          <button type="submit" className="btn btn-primary w-100">Submit</button>
        </form>

        {result && (
          <div className="mt-4 p-3 bg-light border rounded">
            <p className="mb-0">Hex String: {result}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default MessageType12;
