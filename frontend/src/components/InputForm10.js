import { useState } from "react";

function MessageType10() {
  const [formData, setFormData] = useState({
    preamble: "53",
    Brrc: "",
    Cltc_lsb: "",
    Cltc_v1: "",
    Iltc_v1: "",
    Cltc_v0: "",
    Iltc_v0: "",
    Cgeo_lsb: "",
    Cgeo_v: "",
    Igeo: "",
    Cer: "",
    Ciono_step: "",
    Iiono: "",
    Ciono_ramp: "",
    RSSUDRE: "",
    RSSiono: "",
    Ccovariance: "",
  });

  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handlePreambleChange = (val) => {
    setFormData({ ...formData, preamble: val });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://127.0.0.1:5000/api/numbers/10", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      setResult(data.hex_string);
    } catch (err) {
      console.error("Error:", err);
      setError(err.message || "An error occurred while submitting the form.");
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center min-vh-100">
      <div className="card m-20 p-4 shadow-lg w-100">
        <h1 className="text-center mb-4">Message Type 10 (Correction Parameters)</h1>
        <form onSubmit={handleSubmit}>
          {/* Preamble */}
          <div className="mb-2">
            <label className="form-label">Select Preamble:</label>
            <div className="d-flex gap-2">
              {["53", "9A", "C6"].map((p) => (
                <button
                  key={p}
                  type="button"
                  className={`btn ${
                    formData.preamble === p ? "btn-primary" : "btn-outline-primary"
                  }`}
                  onClick={() => handlePreambleChange(p)}
                >
                  {p}
                </button>
              ))}
            </div>
          </div>

          <small className="text-muted">
            Enter values within the indicated ranges. Encodings use the given scale factors.
          </small>

          {/* Group 1: LT Corrections */}
          <h6 className="mt-3">Long-Term Corrections</h6>
          <div className="row g-2 mb-3">
            <div className="col">
              <input
                className="form-control"
                name="Brrc"
                type="number"
                step="0.002"
                min="0"
                max="2.046"
                placeholder="Brrc (0 - 2.046 m)"
                value={formData.B_rrc}
                onChange={handleChange}
                required
              />
            </div>
            <div className="col">
              <input
                className="form-control"
                name="Cltc_lsb"
                type="number"
                step="0.002"
                min="0"
                max="2.046"
                placeholder="Cltc_lsb (0 - 2.046 m)"
                value={formData.C_ltc_lsb}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="row g-2 mb-3">
            <div className="col">
              <input
                className="form-control"
                name="Cltc_v1"
                type="number"
                step="0.00005"
                min="0"
                max="0.05115"
                placeholder="Cltc_v1 (0 - 0.05115 m/s)"
                value={formData.C_ltc_v1}
                onChange={handleChange}
                required
              />
            </div>
            <div className="col">
              <input
                className="form-control"
                name="Iltc_v1"
                type="number"
                step="1"
                min="0"
                max="511"
                placeholder="Iltc_v1 (0 - 511 s)"
                value={formData.I_ltc_v1}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="row g-2 mb-3">
            <div className="col">
              <input
                className="form-control"
                name="Cltc_v0"
                type="number"
                step="0.002"
                min="0"
                max="2.046"
                placeholder="Cltc_v0 (0 - 2.046 m)"
                value={formData.C_ltc_v0}
                onChange={handleChange}
                required
              />
            </div>
            <div className="col">
              <input
                className="form-control"
                name="Iltc_v0"
                type="number"
                step="1"
                min="0"
                max="511"
                placeholder="Iltc_v0 (0 - 511 s)"
                value={formData.I_ltc_v0}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          {/* Group 2: GEO Corrections */}
          <h6>GEO Corrections</h6>
          <div className="row g-2 mb-3">
            <div className="col">
              <input
                className="form-control"
                name="Cgeo_lsb"
                type="number"
                step="0.0005"
                min="0"
                max="0.5115"
                placeholder="Cgeo_lsb (0 - 0.5115 m)"
                value={formData.C_geo_lsb}
                onChange={handleChange}
                required
              />
            </div>
            <div className="col">
              <input
                className="form-control"
                name="Cgeo_v"
                type="number"
                step="0.00005"
                min="0"
                max="0.05115"
                placeholder="Cgeo_v (0 - 0.05115 m/s)"
                value={formData.C_geo_v}
                onChange={handleChange}
                required
              />
            </div>
            <div className="col">
              <input
                className="form-control"
                name="Igeo"
                type="number"
                step="1"
                min="0"
                max="511"
                placeholder="Igeo (0 - 511 s)"
                value={formData.I_geo}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          {/* Group 3: Ionospheric Corrections */}
          <h6>Ionospheric Corrections</h6>
          <div className="row g-2 mb-3">
            <div className="col">
              <input
                className="form-control"
                name="Ciono_step"
                type="number"
                step="0.001"
                min="0"
                max="1.023"
                placeholder="Ciono_step (0 - 1.023 m)"
                value={formData.C_iono_step}
                onChange={handleChange}
                required
              />
            </div>
            <div className="col">
              <input
                className="form-control"
                name="Iiono"
                type="number"
                step="1"
                min="0"
                max="511"
                placeholder="Iiono (0 - 511 s)"
                value={formData.I_iono}
                onChange={handleChange}
                required
              />
            </div>
            <div className="col">
              <input
                className="form-control"
                name="Ciono_ramp"
                type="number"
                step="0.000005"
                min="0"
                max="0.005115"
                placeholder="Ciono_ramp (0 - 0.005115 m/s)"
                value={formData.C_iono_ramp}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          {/* Group 4: Other Parameters */}
          <h6>Other Parameters</h6>
          <div className="row g-2 mb-3">
            <div className="col">
              <input
                className="form-control"
                name="Cer"
                type="number"
                step="0.5"
                min="0"
                max="31.5"
                placeholder="Cer (0 - 31.5 m)"
                value={formData.C_er}
                onChange={handleChange}
                required
              />
            </div>
            <div className="col">
              <input
                className="form-control"
                name="Ccovariance"
                type="number"
                step="0.1"
                min="0"
                max="12.7"
                placeholder="Ccovariance (0 - 12.7)"
                value={formData.C_covariance}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="row g-2 mb-3">
            <div className="col">
              <input
                className="form-control"
                name="RSSUDRE"
                type="number"
                min="0"
                max="1"
                placeholder="RSS UDRE (0 or 1)"
                value={formData.RSS_udre}
                onChange={handleChange}
                required
              />
            </div>
            <div className="col">
              <input
                className="form-control"
                name="RSSiono"
                type="number"
                min="0"
                max="1"
                placeholder="RSS Iono (0 or 1)"
                value={formData.RSS_iono}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          {/* Submit */}
          <button type="submit" className="btn btn-primary w-100">
            Submit
          </button>
        </form>

        {error && (
          <div className="mt-3 alert alert-danger"> 
            <strong>Error:</strong> {error}
          </div>
        )}
        {result && (
          <div className="mt-4 p-3 bg-light border rounded">
            <p className="mb-0">Hex String: {result}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default MessageType10;
