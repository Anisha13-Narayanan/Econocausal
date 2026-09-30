import Week2Dashboard from "./Week2Dashboard";
import causalAudit from "./CausalAudit";


import { useState } from "react";
import axios from "axios";
import "./styles.css";

function App() {
  const [file, setFile] = useState(null);
  const [budget, setBudget] = useState(5000);
  const [message, setMessage] = useState("");
  const [uploading, setUploading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a CSV file first.");
      return;
    }

    setUploading(true);
    setMessage("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData
      );

      setMessage(response.data.message);
    } catch (error) {
      console.error(error);
      setMessage(
        "Upload failed. Make sure the FastAPI backend is running."
      );
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="app">

      {/* HEADER */}
      <header className="header">
        <h1>EconoCausal</h1>

        <p>
          Dynamic Pricing via Double Machine Learning
        </p>
      </header>


      {/* MAIN DASHBOARD */}
      <main className="dashboard">

        {/* HISTORICAL DATA */}
        <section className="card">

          <h2>Historical Campaign Data</h2>

          <p>
            Upload historical campaign data for causal analysis.
          </p>

          <div className="upload-area">

            <input
              type="file"
              accept=".csv"
              onChange={(event) => {
                setFile(event.target.files[0]);
                setMessage("");
              }}
            />

            {file && (
              <p className="selected-file">
                Selected file: <strong>{file.name}</strong>
              </p>
            )}

            <button
              className="primary-button"
              onClick={handleUpload}
              disabled={uploading}
            >
              {uploading
                ? "Uploading..."
                : "Upload Dataset"}
            </button>

            {message && (
              <p className="upload-message">
                {message}
              </p>
            )}

          </div>

        </section>


        {/* BUDGET */}
        <section className="card">

          <h2>Budget Constraints</h2>

          <p>
            Set the maximum campaign budget available
            for personalized discounts.
          </p>

          <label>
            Maximum Budget ($)
          </label>

          <input
            className="budget-input"
            type="number"
            min="0"
            value={budget}
            onChange={(event) =>
              setBudget(event.target.value)
            }
          />

          <div className="budget-display">

            Selected Budget:

            <strong>
              ${Number(budget).toLocaleString()}
            </strong>

          </div>

        </section>


        {/* CAUSAL MODEL */}
        <section className="card full-width">

          <h2>Week 1 Causal Model</h2>

          <p>
            Variables identified from the Criteo
            uplift dataset.
          </p>

          <div className="model-grid">

            <div className="model-item">
              <span>Treatment</span>
              <strong>treatment</strong>
            </div>

            <div className="model-item">
              <span>Outcome</span>
              <strong>conversion</strong>
            </div>

            <div className="model-item">
              <span>Covariates</span>
              <strong>f0 – f11</strong>
            </div>

            <div className="model-item">
              <span>Causal Framework</span>
              <strong>DoWhy</strong>
            </div>

          </div>

        </section>


        {/* DATASET INFORMATION */}
        <section className="card full-width">

          <h2>Criteo Dataset</h2>

          <div className="dataset-info">

            <div>
              <span>Dataset</span>
              <strong>Criteo Uplift</strong>
            </div>

            <div>
              <span>Rows</span>
              <strong>13,979,592</strong>
            </div>

            <div>
              <span>Treatment</span>
              <strong>treatment</strong>
            </div>

            <div>
              <span>Outcome</span>
              <strong>conversion</strong>
            </div>

          </div>

        </section>


        {/* DAG */}
        <section className="card full-width">

          <h2>Causal DAG</h2>

          <p>
            Week 1 causal graph generated using
            DoWhy.
          </p>

          <div className="dag-container">

            <img
              src="http://127.0.0.1:8000/dag"
              alt="Causal DAG"
              onError={(event) => {
                event.currentTarget.style.display =
                  "none";
              }}
            />

            <p>
              The generated DAG is available in:
            </p>

            <code>
              backend/data/week1_causal_dag.png
            </code>

          </div>

        </section>

      </main>


      {/* WEEK 2 DASHBOARD */}
      <section className="card full-width">

        <Week2Dashboard />

      </section>

       {/* MID-PROJECT CAUSAL AUDIT */}
      <section className="card full-width">

        <CausalAudit />

      </section>

    </div>
  );
}

export default App;