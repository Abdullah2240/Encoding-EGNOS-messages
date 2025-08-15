import { useState } from "react";

function MessageType1() {
  const [numbers, setNumbers] = useState("");
  const [iodp, setIodp] = useState("");
  const [preamble, setPreamble] = useState("53");
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://127.0.0.1:5000/api/numbers/1", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          iodp: iodp,
          numbers: numbers,
          preamble: preamble,
        }),
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
        <h1 className="text-center mb-4">Message Type 1</h1>

        <form onSubmit={handleSubmit} className="mt-4">
          <div className="mb-3">
            <label className="form-label">Select Preamble:</label>
            <div className="d-flex gap-2">
              <button
                type="button"
                className={`btn ${preamble === "53" ? "btn-primary" : "btn-outline-primary"}`}
                onClick={() => setPreamble("53")}
              >
                53
              </button>
              <button
                type="button"
                className={`btn ${preamble === "9A" ? "btn-primary" : "btn-outline-primary"}`}
                onClick={() => setPreamble("9A")}
              >
                9A
              </button>
              <button
                type="button"
                className={`btn ${preamble === "C6" ? "btn-primary" : "btn-outline-primary"}`}
                onClick={() => setPreamble("C6")}
              >
                C6
              </button>
            </div>
          </div>
          <div className="mb-3">
            <input
              type="text"
              placeholder="Enter PRN mask for satellites (comma separated)"
              value={numbers}
              onChange={(e) => setNumbers(e.target.value)}
              className="form-control"
              required
            />
          </div>
          <div className="mb-3">
            <input
              type="text"
              placeholder="Enter IODP (0-3)"
              value={iodp}
              onChange={(e) => setIodp(e.target.value)}
              className="form-control"
              required
            />
          </div>
          <button
            type="submit"
            className="btn btn-primary w-100"
          >
            Submit
          </button>
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

export default MessageType1;
