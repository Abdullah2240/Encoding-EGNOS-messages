import React, { useState } from 'react';

function App() {
    const [input, setInput] = useState('');
    const [iodp, setIodp] = useState('');
    const [bitString, setBitString] = useState('');
    const [hexString, setHexString] = useState('');
    const [receivedPRNs, setReceivedPRNs] = useState([]);
    const [error, setError] = useState('');

    const handleInputChange = (event) => {
        setInput(event.target.value);
    };

    const handleIodpChange = (event) => {
        setIodp(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const res = await fetch('/api/numbers', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ numbers: input }),
            });

            if (!res.ok) {
                // Extract the error response from the body and throw it
                const errorData = await res.json();
                throw new Error(errorData.message || 'Something went wrong');
            }

            const data = await res.json();

            // Log the full response data to the console
            console.log(data);

            // Set the individual pieces of the response to display them
            setBitString(data.bit_string);
            setHexString(data.hex_string);
            setReceivedPRNs(data.received_PRNs);

            // Clear any existing error
            setError('');
        } 
        catch (error) {
            console.error('Error:', error);
            setError('Error: ' + error.message);
        }
    };


    return (
        <div className="container d-flex justify-content-center align-items-center min-vh-100">
            <div className="card p-4 shadow-lg w-50">
                <h1 className="text-center mb-4">Number Input</h1>
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <input
                            type="text"
                            value={input}
                            onChange={handleInputChange}
                            className="form-control"
                            placeholder="Enter numbers (1-210) separated by commas"
                        />
                        <input
                            type="text"
                            value={iodp}
                            onChange={handleIodpChange}
                            className="form-control"
                            placeholder="Enter numbers (1-210) separated by commas"
                        />
                    </div>
                    <button type="submit" className="btn btn-primary w-100">Submit</button>
                </form>

                {/* Display Error */}
                {error && <p className="mt-4 text-danger">{error}</p>}

                {/* Display the response data */}
                {bitString && (
                    <div className="mt-6">
                        <h4 className="text-center">Bit String</h4>
                        <div className="alert alert-secondary">
                            <p className="text-break">{bitString}</p>
                        </div>
                    </div>
                )}
                {hexString && (
                    <div className="mt-6">
                        <h4 className="text-center">Hex String</h4>
                        <div className="alert alert-secondary">
                            <p className="text-break">{hexString}</p>
                        </div>
                    </div>
                )}
                {receivedPRNs.length > 0 && (
                    <div className="mt-6">
                        <h4 className="text-center">Received PRNs</h4>
                        <ul className="list-group">
                            {receivedPRNs.map((prn, index) => (
                                <li key={index} className="list-group-item">
                                    {prn}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
        </div>
    );
}

export default App;
