import Week2Dashboard from "./Week2Dashboard";
import CausalAudit from "./CausalAudit";

import { useState } from "react";
import axios from "axios";
import "./styles.css";

function App() {
  const [file, setFile] = useState(null);
  const [budget, setBudget] = useState(5000);
  const [message, setMessage] = useState("");
  const [uploading, setUploading] = useState(false);
  const [activeSection, setActiveSection] = useState("overview");
  const [discountOptions, setDiscountOptions] = useState([0, 10, 20]);
  const [optimization, setOptimization] = useState(null);
  const [optimizing, setOptimizing] = useState(false);
  const [optimizationError, setOptimizationError] = useState("");

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
      setMessage("Upload failed. Make sure the FastAPI backend is running.");
    } finally {
      setUploading(false);
    }
  };

  const handleOptimize = async () => {
  const budgetValue = Number(budget);

  if (!Number.isFinite(budgetValue) || budgetValue < 0) {
    setOptimizationError("Enter a valid non-negative budget.");
    return;
  }

  setOptimizing(true);
  setOptimizationError("");
  setOptimization(null);

  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/optimize",
      {
        budget: budgetValue,
        max_discount: 20,
        discount_options: discountOptions,
      }
    );

    setOptimization(response.data);
  } catch (error) {
    console.error(error);
    setOptimizationError(
      error.response?.data?.detail ||
      "Optimization failed. Check that the FastAPI backend is running."
    );
  } finally {
    setOptimizing(false);
  }
};

  const scrollTo = (id) => {
    setActiveSection(id);
    document.getElementById(id)?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  };

  return (
    <div className="platform-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">EC</div>
          <div>
            <div className="brand-name">EconoCausal</div>
            <div className="brand-subtitle">Causal Pricing Intelligence</div>
          </div>
        </div>

        <div className="sidebar-label">PLATFORM</div>

        <nav className="side-nav">
          <button
            className={activeSection === "overview" ? "nav-item active" : "nav-item"}
            onClick={() => scrollTo("overview")}
          >
            <span className="nav-icon">⌂</span>
            Overview
          </button>

          <button
            className={activeSection === "data" ? "nav-item active" : "nav-item"}
            onClick={() => scrollTo("data")}
          >
            <span className="nav-icon">▦</span>
            Data
          </button>

          <button
            className={activeSection === "causal" ? "nav-item active" : "nav-item"}
            onClick={() => scrollTo("causal")}
          >
            <span className="nav-icon">◎</span>
            Causal Model
          </button>

          <button
            className={activeSection === "ite" ? "nav-item active" : "nav-item"}
            onClick={() => scrollTo("ite")}
          >
            <span className="nav-icon">↗</span>
            ITE Analysis
          </button>

          <button
            className={activeSection === "audit" ? "nav-item active" : "nav-item"}
            onClick={() => scrollTo("audit")}
          >
            <span className="nav-icon">✓</span>
            Causal Audit
          </button>

          <button
            className={
              activeSection === "optimization" ? "nav-item active" : "nav-item"
            }
            onClick={() => scrollTo("optimization")}
          >
            <span className="nav-icon">$</span>
            Budget Optimization
          </button>
        </nav>

        <div className="sidebar-footer">
          <div className="system-status">
            <span className="status-dot"></span>
            <div>
              <strong>API Online</strong>
              <span>FastAPI connected</span>
            </div>
          </div>
          <div className="version-tag">MID-PROJECT REVIEW · v1.0</div>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div>
            <div className="breadcrumb">EconoCausal / Analytics</div>
            <h1>Decision Intelligence</h1>
          </div>

          <div className="topbar-actions">
            <div className="review-badge">
              <span className="review-dot"></span>
              Mid-Project Review
            </div>
            <div className="avatar">EC</div>
          </div>
        </header>

        <div className="content">
          <section id="overview" className="hero-section">
            <div className="hero-copy">
              <div className="eyebrow">CAUSAL AI PLATFORM</div>
              <h2>Understand the impact.<br />Optimize the decision.</h2>
              <p>
                EconoCausal uses Double Machine Learning and causal inference
                to estimate how an intervention changes customer conversion.
              </p>
              <div className="hero-tags">
                <span>EconML</span>
                <span>DoWhy</span>
                <span>Double ML</span>
                <span>Plotly</span>
              </div>
            </div>

            <div className="hero-visual">
              <div className="orb orb-one"></div>
              <div className="orb orb-two"></div>
              <div className="hero-chart">
                <div className="mini-chart-title">CAUSAL EFFECT SIGNAL</div>
                <div className="signal-bars">
                  <span style={{ height: "28%" }}></span>
                  <span style={{ height: "42%" }}></span>
                  <span style={{ height: "36%" }}></span>
                  <span style={{ height: "62%" }}></span>
                  <span style={{ height: "51%" }}></span>
                  <span style={{ height: "76%" }}></span>
                  <span style={{ height: "68%" }}></span>
                  <span style={{ height: "88%" }}></span>
                  <span style={{ height: "72%" }}></span>
                  <span style={{ height: "96%" }}></span>
                </div>
                <div className="mini-chart-footer">
                  <span>ITE distribution</span>
                  <strong>+0.0957%</strong>
                </div>
              </div>
            </div>
          </section>

          <section className="stat-grid">
            <div className="stat-card">
              <div className="stat-label">DATASET SIZE</div>
              <div className="stat-value">13.98M</div>
              <div className="stat-meta">Criteo uplift records</div>
            </div>

            <div className="stat-card">
              <div className="stat-label">MEAN ITE</div>
              <div className="stat-value">0.0957%</div>
              <div className="stat-meta positive">Average estimated uplift</div>
            </div>

            <div className="stat-card">
              <div className="stat-label">POSITIVE ITE</div>
              <div className="stat-value">237.7K</div>
              <div className="stat-meta">Potential responders</div>
            </div>

            <div className="stat-card accent-card">
              <div className="stat-label">QINI COEFFICIENT</div>
              <div className="stat-value">926.15</div>
              <div className="stat-meta">Model uplift metric</div>
            </div>
          </section>

          <section id="data" className="platform-section">
            <div className="section-heading">
              <div>
                <div className="section-kicker">01 · DATA FOUNDATION</div>
                <h3>Dataset & campaign configuration</h3>
                <p>Historical campaign data used by the causal analysis pipeline.</p>
              </div>
            </div>

            <div className="data-grid">
              <div className="panel">
                <div className="panel-header">
                  <div>
                    <h4>Historical Campaign Data</h4>
                    <span>Upload a compatible CSV dataset</span>
                  </div>
                  <span className="panel-icon">↑</span>
                </div>

                <div className="upload-box">
                  <div className="upload-symbol">⇧</div>
                  <strong>{file ? file.name : "Choose historical campaign data"}</strong>
                  <span>CSV files only</span>
                  <input
                    type="file"
                    accept=".csv"
                    onChange={(event) => {
                      setFile(event.target.files[0]);
                      setMessage("");
                    }}
                  />
                  <button className="primary-button" onClick={handleUpload} disabled={uploading}>
                    {uploading ? "Uploading..." : "Upload Dataset"}
                  </button>
                  {message && <div className="upload-message">{message}</div>}
                </div>
              </div>

              <div className="panel">
                <div className="panel-header">
                  <div>
                    <h4>Budget Constraints</h4>
                    <span>Reserved for prescriptive optimization</span>
                  </div>
                  <span className="panel-icon">$</span>
                </div>

                <div className="budget-panel">
                  <div className="budget-label">MAXIMUM CAMPAIGN BUDGET</div>
                  <div className="budget-value">
                    <span>$</span>
                    <input
                      type="number"
                      min="0"
                      value={budget}
                      onChange={(event) => setBudget(event.target.value)}
                    />
                  </div>
                  <div className="budget-line">
                    <span>Configured budget</span>
                    <strong>${Number(budget || 0).toLocaleString()}</strong>
                  </div>
                  <div className="budget-note">
                    Set your campaign budget here, then run Week 3 optimization below.
                  </div>
                </div>
              </div>
            </div>

            <div className="dataset-strip">
              <div><span>DATASET</span><strong>Criteo Uplift Modeling</strong></div>
              <div><span>ROWS</span><strong>13,979,592</strong></div>
              <div><span>TREATMENT</span><strong>treatment</strong></div>
              <div><span>OUTCOME</span><strong>conversion</strong></div>
              <div><span>COVARIATES</span><strong>f0 – f11</strong></div>
            </div>
          </section>

          <section id="causal" className="platform-section">
            <div className="section-heading">
              <div>
                <div className="section-kicker">02 · CAUSAL ENGINE</div>
                <h3>Causal model foundation</h3>
                <p>Week 1 causal structure carried forward into the Week 2 DML pipeline.</p>
              </div>
              <span className="section-status">MODEL DEFINED</span>
            </div>

            <div className="causal-overview">
              <div className="causal-card">
                <span>TREATMENT</span>
                <strong>treatment</strong>
                <small>Campaign intervention</small>
              </div>
              <div className="causal-arrow">→</div>
              <div className="causal-card highlighted">
                <span>CAUSAL EFFECT</span>
                <strong>ITE</strong>
                <small>Individual Treatment Effect</small>
              </div>
              <div className="causal-arrow">→</div>
              <div className="causal-card">
                <span>OUTCOME</span>
                <strong>conversion</strong>
                <small>Observed response</small>
              </div>
            </div>

            <div className="dag-panel">
              <div className="panel-header">
                <div>
                  <h4>Week 1 Causal DAG</h4>
                  <span>DoWhy graph used to define the causal structure</span>
                </div>
                <span className="method-pill">DoWhy</span>
              </div>
              <div className="dag-container">
                <img
                  src="http://127.0.0.1:8000/dag"
                  alt="Causal DAG"
                  onError={(event) => {
                    event.currentTarget.style.display = "none";
                  }}
                />
                <div className="dag-caption">
                  <span>Confounders</span>
                  <strong>f0 – f11</strong>
                  <span>→ treatment → conversion</span>
                </div>
              </div>
            </div>
          </section>

          <section id="ite" className="platform-section">
            <div className="section-heading">
              <div>
                <div className="section-kicker">03 · ITE & UPLIFT ANALYTICS</div>
                <h3>Customer-level causal intelligence</h3>
                <p>Interactive treatment-effect analysis generated by EconML CausalForestDML.</p>
              </div>
              <span className="section-status">WEEK 2 COMPLETE</span>
            </div>

            <div className="embedded-module">
              <Week2Dashboard />
            </div>
          </section>

          <section id="audit" className="platform-section">
            <div className="section-heading">
              <div>
                <div className="section-kicker">04 · CAUSAL AUDIT</div>
                <h3>Mid-project validation</h3>
                <p>DoWhy refutation tests used to evaluate robustness of the estimated causal effect.</p>
              </div>
              <span className="section-status">AUDIT READY</span>
            </div>

            <div className="embedded-module audit-module">
              <CausalAudit />
            </div>
          </section>
          
<section id="optimization" className="platform-section">
  <div className="section-heading">
    <div>
      <div className="section-kicker">05 · WEEK 3 OPTIMIZATION</div>
      <h3>Budget Optimization & Allocation Matrix</h3>
      <p>
        Allocate customer discounts using estimated treatment effects
        while respecting the campaign budget.
      </p>
    </div>
    <span className="section-status">SCI-PY MILP</span>
  </div>

  <div className="panel">
    <div className="panel-header">
      <div>
        <h4>Campaign optimization</h4>
        <span>Configure the budget and available discount options</span>
      </div>
    </div>

    <div className="budget-panel">
      <label htmlFor="optimization-budget">Campaign budget ($)</label>
      <input
        id="optimization-budget"
        type="number"
        min="0"
        value={budget}
        onChange={(event) => setBudget(event.target.value)}
      />

      <div className="budget-note">
        Choose the available discount amounts.
      </div>

      <div className="allocation-options">
        {[0, 10, 20].map((discount) => (
          <label key={discount}>
            <input
              type="checkbox"
              checked={discountOptions.includes(discount)}
              onChange={(event) => {
                setDiscountOptions((current) =>
                  event.target.checked
                    ? [...current, discount].sort((a, b) => a - b)
                    : current.filter((value) => value !== discount)
                );
              }}
            />
            ${discount}
          </label>
        ))}
      </div>

      <button
        className="primary-button"
        onClick={handleOptimize}
        disabled={optimizing || discountOptions.length === 0}
      >
        {optimizing ? "Optimizing..." : "Run Budget Optimization"}
      </button>

      {optimizationError && (
        <div className="upload-message">{optimizationError}</div>
      )}
    </div>
  </div>

  {optimization && (
    <>
      <div className="stat-grid">
        <div className="stat-card">
          <div className="stat-label">BUDGET</div>
          <div className="stat-value">
            ${Number(optimization.summary.budget).toLocaleString()}
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">SPENT</div>
          <div className="stat-value">
            ${Number(optimization.summary.spent).toFixed(2)}
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">EXPECTED INCREMENTAL REVENUE</div>
          <div className="stat-value">
            ${Number(
              optimization.summary.expected_incremental_revenue
            ).toFixed(2)}
          </div>
        </div>

        <div className="stat-card accent-card">
          <div className="stat-label">EXPECTED NET GAIN</div>
          <div className="stat-value">
            ${Number(optimization.summary.expected_net_gain).toFixed(2)}
          </div>
        </div>
      </div>

      <div className="panel allocation-panel">
        <div className="panel-header">
          <div>
            <h4>Customer Allocation Matrix</h4>
            <span>
              {optimization.summary.customers_targeted} customers selected
              · Remaining budget: $
              {(
                Number(optimization.summary.budget) -
                Number(optimization.summary.spent)
              ).toFixed(2)}
            </span>
          </div>
        </div>

        <div className="allocation-table-wrap">
          <table className="allocation-table">
            <thead>
              <tr>
                <th>Customer ID</th>
                <th>ITE (20)</th>
                <th>Discount</th>
                <th>Expected Incremental Revenue</th>
                <th>Expected Net Gain</th>
              </tr>
            </thead>
            <tbody>
              {optimization.allocation.map((item) => (
                <tr key={item.customer_id}>
                  <td>{item.customer_id}</td>
                  <td>{Number(item.ite_20).toFixed(6)}</td>
                  <td>${Number(item.discount).toFixed(2)}</td>
                  <td>
                    ${Number(item.expected_incremental_revenue).toFixed(2)}
                  </td>
                  <td>
                    ${Number(item.expected_net_gain).toFixed(2)}
                  </td>
                </tr>
              ))}

              {optimization.allocation.length === 0 && (
                <tr>
                  <td colSpan="5">No profitable allocations found for this budget.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        <p className="budget-note">
          These values are model-based estimates. The $10 discount effect
          is approximated as half of the estimated $20 treatment effect;
          it is not independently estimated.
        </p>
      </div>
    </>
  )}
</section>


          <footer className="platform-footer">
            <div>
              <strong>EconoCausal</strong>
              <span>Dynamic Pricing via Double Machine Learning</span>
            </div>
            <span>Infotact Solutions · Mid-Project Review</span>
          </footer>
        </div>
      </main>
    </div>
  );
}

export default App;
