import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import axios from "axios";
import Plot from "react-plotly.js";
import "./styles.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [training, setTraining] = useState(null);
  const [optimization, setOptimization] = useState(null);
  const [audit, setAudit] = useState(null);
  const [budget, setBudget] = useState(5000);
  const [loading, setLoading] = useState(false);

  async function trainModel() {
    setLoading(true);
    try {
      const r = await axios.post(`${API}/train`, { n_estimators: 200 });
      setTraining(r.data);
    } finally {
      setLoading(false);
    }
  }

  async function optimizeBudget() {
    setLoading(true);
    try {
      const r = await axios.post(`${API}/optimize`, {
        budget: Number(budget),
        discount_options: [0, 10, 20]
      });
      setOptimization(r.data);
    } finally {
      setLoading(false);
    }
  }

  async function runAudit() {
    const r = await axios.post(`${API}/causal-audit`, { n_samples: 1000 });
    setAudit(r.data);
  }

  const customers = training?.customers || [];
  const segments = customers.reduce((a, x) => {
    a[x.segment] = (a[x.segment] || 0) + 1;
    return a;
  }, {});

  return (
    <div className="app">
      <header>
        <h1>EconoCausal</h1>
        <p>Dynamic Pricing via Double Machine Learning</p>
      </header>

      <section className="controls">
        <button onClick={trainModel}>Train Causal Model</button>
        <label>
          Budget ($)
          <input value={budget} onChange={e => setBudget(e.target.value)} />
        </label>
        <button onClick={optimizeBudget}>Optimize Allocation</button>
        <button onClick={runAudit}>Run Causal Audit</button>
      </section>

      {loading && <div className="card">Running model...</div>}

      {training && (
        <>
          <section className="cards">
            <div className="card"><b>Method</b><span>{training.method}</span></div>
            <div className="card"><b>Mean ITE</b><span>{training.mean_ite.toFixed(4)}</span></div>
            <div className="card"><b>Customers</b><span>{training.rows}</span></div>
            <div className="card"><b>Top 10% uplift proxy</b><span>{training.qini_proxy.toFixed(2)}</span></div>
          </section>

          <section className="panel">
            <h2>Individual Treatment Effect</h2>
            <Plot
              data={[{
                x: customers.map(x => x.customer_id),
                y: customers.map(x => x.ite),
                type: "scatter",
                mode: "markers",
                text: customers.map(x => x.segment),
                hovertemplate: "Customer %{x}<br>ITE %{y:.4f}<br>%{text}<extra></extra>"
              }]}
              layout={{
                autosize: true,
                height: 430,
                xaxis: { title: "Customer ID" },
                yaxis: { title: "Estimated Treatment Effect" },
                margin: { l: 60, r: 20, t: 30, b: 50 }
              }}
              useResizeHandler
              style={{ width: "100%" }}
            />
          </section>

          <section className="panel">
            <h2>Customer Segments</h2>
            <pre>{JSON.stringify(segments, null, 2)}</pre>
          </section>
        </>
      )}

      {optimization && (
        <section className="panel">
          <h2>Budget Prescription</h2>
          <div className="cards">
            <div className="card"><b>Budget</b><span>${optimization.summary.budget.toFixed(2)}</span></div>
            <div className="card"><b>Spent</b><span>${optimization.summary.spent.toFixed(2)}</span></div>
            <div className="card"><b>Expected Revenue</b><span>${optimization.summary.expected_incremental_revenue.toFixed(2)}</span></div>
            <div className="card"><b>Targeted Users</b><span>{optimization.summary.customers_targeted}</span></div>
          </div>
          <table>
            <thead><tr><th>Customer</th><th>Discount</th><th>ITE</th><th>Expected Net Gain</th></tr></thead>
            <tbody>
              {optimization.allocation.slice(0, 20).map(x => (
                <tr key={x.customer_id}>
                  <td>{x.customer_id}</td>
                  <td>${x.discount.toFixed(2)}</td>
                  <td>{x.ite_20.toFixed(4)}</td>
                  <td>${x.expected_net_gain.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}

      {audit && (
        <section className="panel">
          <h2>Causal Audit</h2>
          <pre>{JSON.stringify(audit, null, 2)}</pre>
        </section>
      )}
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
