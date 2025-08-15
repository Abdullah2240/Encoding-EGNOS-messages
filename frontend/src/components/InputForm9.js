import { useState } from "react";

function MessageType9() {
  const [formData, setFormData] = useState({
    preamble: "53",
    t0: "",
    ura: "",
    xg: "",
    yg: "",
    zg: "",
    xg_rate: "",
    yg_rate: "",
    zg_rate: "",
    xg_acc: "",
    yg_acc: "",
    zg_acc: "",
    agf0: "",
    agf1: ""
  });
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handlePreambleChange = (preambleValue) => {
    setFormData({ ...formData, preamble: preambleValue });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://127.0.0.1:5000/api/numbers/9", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      setResult(data.hex_string || data.error);
    } catch (err) {
      setResult("Network error. Check backend.");
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center min-vh-100">
      <div className="card m-20 p-4 shadow-lg w-100">
        <h1 className="text-center mb-4">Message Type 9 (GEO Navigation)</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-2">
            <label className="form-label">Select Preamble:</label>
            <div className="d-flex gap-2">
              <button type="button" className={`btn ${formData.preamble === "53" ? "btn-primary" : "btn-outline-primary"}`} onClick={() => handlePreambleChange("53")}>53</button>
              <button type="button" className={`btn ${formData.preamble === "9A" ? "btn-primary" : "btn-outline-primary"}`} onClick={() => handlePreambleChange("9A")}>9A</button>
              <button type="button" className={`btn ${formData.preamble === "C6" ? "btn-primary" : "btn-outline-primary"}`} onClick={() => handlePreambleChange("C6")}>C6</button>
            </div>
          </div>

          <small className="text-muted">Provide values within the indicated ranges. Encoding uses the LSB scale per spec.</small>

          <div className="row g-2 mt-2 mb-3">
            <div className="col-6">
              <input className="form-control" name="t0" type="number" min="0" max="86384" step="1" placeholder="t0 [0…86384] s (LSB=16 s; encoded in 16s steps)" title="0 to 86384 seconds; encoded in 16 s steps" value={formData.t0} onChange={handleChange} required />
            </div>
            <div className="col-6">
              <input className="form-control" name="ura" type="number" min="0" max="15" step="1" placeholder="URA [0…15] " title="User Range Accuracy exponent 0…15; 15 means Do Not Use" value={formData.ura} onChange={handleChange} required />
            </div>
          </div>

          <h6>ECEF Position (meters)</h6>
          <div className="row g-2 mb-3">
            <div className="col">
              <input className="form-control" name="xg" type="number" step="0.01" placeholder="XG [-42,949,673 … +42,949,673] m (LSB=0.08 m)" title="Range ±42,949,673 m; LSB 0.08 m" value={formData.xg} onChange={handleChange} required />
            </div>
            <div className="col">
              <input className="form-control" name="yg" type="number" step="0.01" placeholder="YG [-42,949,673 … +42,949,673] m (LSB=0.08 m)" title="Range ±42,949,673 m; LSB 0.08 m" value={formData.yg} onChange={handleChange} required />
            </div>
            <div className="col">
              <input className="form-control" name="zg" type="number" step="0.1" placeholder="ZG [-6,710,886.4 … +6,710,886.4] m (LSB=0.4 m)" title="Range ±6,710,886.4 m; LSB 0.4 m" value={formData.zg} onChange={handleChange} required />
            </div>
          </div>

          <h6>Velocity (meters/second)</h6>
          <div className="row g-2 mb-3">
            <div className="col">
              <input className="form-control" name="xg_rate" type="number" step="0.000625" placeholder="ẊG [-40.96 … +40.96] m/s (LSB=0.000625)" title="Range ±40.96 m/s; LSB 0.000625" value={formData.xg_rate} onChange={handleChange} required />
            </div>
            <div className="col">
              <input className="form-control" name="yg_rate" type="number" step="0.000625" placeholder="ẎG [-40.96 … +40.96] m/s (LSB=0.000625)" title="Range ±40.96 m/s; LSB 0.000625" value={formData.yg_rate} onChange={handleChange} required />
            </div>
            <div className="col">
              <input className="form-control" name="zg_rate" type="number" step="0.004" placeholder="ŻG [-524.288 … +524.288] m/s (LSB=0.004)" title="Range ±524.288 m/s; LSB 0.004" value={formData.zg_rate} onChange={handleChange} required />
            </div>
          </div>

          <h6>Acceleration (meters/second²)</h6>
          <div className="row g-2 mb-3">
            <div className="col">
              <input className="form-control" name="xg_acc" type="number" step="0.0000125" placeholder="ẌG [-0.0064 … +0.0064] m/s² (LSB=0.0000125)" title="Range ±0.0064 m/s²; LSB 0.0000125" value={formData.xg_acc} onChange={handleChange} required />
            </div>
            <div className="col">
              <input className="form-control" name="yg_acc" type="number" step="0.0000125" placeholder="ẎG [-0.0064 … +0.0064] m/s² (LSB=0.0000125)" title="Range ±0.0064 m/s²; LSB 0.0000125" value={formData.yg_acc} onChange={handleChange} required />
            </div>
            <div className="col">
              <input className="form-control" name="zg_acc" type="number" step="0.0000625" placeholder="ŻG [-0.032 … +0.032] m/s² (LSB=0.0000625)" title="Range ±0.032 m/s²; LSB 0.0000625" value={formData.zg_acc} onChange={handleChange} required />
            </div>
          </div>

          <h6>Clock Terms</h6>
          <div className="row g-2 mb-3">
            <div className="col">
              <input className="form-control" name="agf0" type="number" step="any" placeholder="aGf0 [±9.537e-7] s (LSB=2^-31 s)" title="Range approx ±0.9537 microseconds; LSB 2^-31 s" value={formData.agf0} onChange={handleChange} required />
            </div>
            <div className="col">
              <input className="form-control" name="agf1" type="number" step="any" placeholder="aGf1 [±1.1642e-10] s/s (LSB=2^-40 s/s)" title="Range approx ±1.1642e-10 s/s; LSB 2^-40 s/s" value={formData.agf1} onChange={handleChange} required />
            </div>
          </div>

          <button type="submit" className="btn btn-primary w-100">Submit</button>
        </form>

        {result && (
          <div className="mt-4 p-3 bg-light border rounded">
            <p className="mb-0">{result}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default MessageType9;
