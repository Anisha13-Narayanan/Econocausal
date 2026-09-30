import { useEffect, useState } from "react";
import Plot from "react-plotly.js";

const API_URL = "http://127.0.0.1:8000";

function Week2Dashboard() {
  const [summary, setSummary] = useState(null);
  const [curve, setCurve] = useState(null);
  const [iteData, setIteData] = useState([]);

  const [minIte, setMinIte] = useState("");
  const [maxIte, setMaxIte] = useState("");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadDashboard() {
    try {
      setLoading(true);
      setError("");

      const summaryResponse = await fetch(
        `${API_URL}/week2/ite-summary`
      );

      const curveResponse = await fetch(
        `${API_URL}/week2/uplift-curve`
      );

      if (!summaryResponse.ok || !curveResponse.ok) {
        throw new Error("Failed to load Week 2 data.");
      }

      const summaryData =
        await summaryResponse.json();

      const curveData =
        await curveResponse.json();

      setSummary(summaryData);
      setCurve(curveData);

      await loadIteData();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function loadIteData() {
    try {
      const params = new URLSearchParams();

      params.set("limit", "10000");

      if (minIte !== "") {
        params.set("min_ite", minIte);
      }

      if (maxIte !== "") {
        params.set("max_ite", maxIte);
      }

      const response = await fetch(
        `${API_URL}/week2/ite-data?${params.toString()}`
      );

      if (!response.ok) {
        throw new Error("Failed to load ITE data.");
      }

      const result = await response.json();

      setIteData(result.data);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  if (loading) {
    return (
      <div className="week2-dashboard">
        <h2>Week 2 — Causal Uplift Analysis</h2>
        <p>Loading Criteo ITE results...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="week2-dashboard">
        <h2>Week 2 — Causal Uplift Analysis</h2>
        <p className="error">{error}</p>
      </div>
    );
  }

  const points = curve?.points || [];

  const xValues = points.map(
    (point) => point.population_fraction * 100
  );

  const upliftValues = points.map(
    (point) => point.cumulative_uplift
  );

  const randomValues = points.map(
    (point) => point.random_baseline
  );

  return (
    <div className="week2-dashboard">

      <div className="week2-header">
        <h2>Week 2 — Causal Uplift Analysis</h2>

        <p>
          EconML CausalForestDML on the Criteo
          Uplift Modeling Dataset
        </p>
      </div>

      <div className="metric-grid">

        <div className="metric-card">
          <span>Customers</span>
          <strong>
            {summary.rows.toLocaleString()}
          </strong>
        </div>

        <div className="metric-card">
          <span>Mean ITE</span>
          <strong>
            {summary.mean_ite.toFixed(6)}
          </strong>
        </div>

        <div className="metric-card">
          <span>Positive Uplift</span>
          <strong>
            {summary.positive_uplift.toLocaleString()}
          </strong>
        </div>

        <div className="metric-card">
          <span>Negative Uplift</span>
          <strong>
            {summary.negative_uplift.toLocaleString()}
          </strong>
        </div>

      </div>

      <div className="chart-card">

        <h3>Uplift Curve</h3>

        <Plot
          data={[
            {
              x: xValues,
              y: upliftValues,
              type: "scatter",
              mode: "lines",
              name: "DML Uplift",
            },
            {
              x: xValues,
              y: randomValues,
              type: "scatter",
              mode: "lines",
              name: "Random Targeting",
              line: {
                dash: "dash",
              },
            },
          ]}
          layout={{
            title:
              "Cumulative Incremental Conversions",
            xaxis: {
              title:
                "Customers Targeted (%)",
            },
            yaxis: {
              title:
                "Cumulative Uplift",
            },
            hovermode: "x unified",
            autosize: true,
            margin: {
              l: 60,
              r: 30,
              t: 60,
              b: 60,
            },
          }}
          style={{
            width: "100%",
            height: "500px",
          }}
          useResizeHandler
          config={{
            responsive: true,
          }}
        />

      </div>

      <div className="chart-card">

        <h3>Qini Curve</h3>

        <Plot
          data={[
            {
              x: xValues,
              y: upliftValues,
              type: "scatter",
              mode: "lines",
              name: "DML Qini Curve",
            },
            {
              x: xValues,
              y: randomValues,
              type: "scatter",
              mode: "lines",
              name: "Random Baseline",
              line: {
                dash: "dash",
              },
            },
          ]}
          layout={{
            title: "Qini Analysis",
            xaxis: {
              title:
                "Customers Targeted (%)",
            },
            yaxis: {
              title:
                "Incremental Conversions",
            },
            hovermode: "x unified",
            autosize: true,
            margin: {
              l: 60,
              r: 30,
              t: 60,
              b: 60,
            },
          }}
          style={{
            width: "100%",
            height: "500px",
          }}
          useResizeHandler
          config={{
            responsive: true,
          }}
        />

      </div>

      <div className="filter-card">

        <h3>ITE Customer Filter</h3>

        <div className="filter-row">

          <div>
            <label>
              Minimum ITE
            </label>

            <input
              type="number"
              step="0.001"
              value={minIte}
              onChange={(e) =>
                setMinIte(e.target.value)
              }
            />
          </div>

          <div>
            <label>
              Maximum ITE
            </label>

            <input
              type="number"
              step="0.001"
              value={maxIte}
              onChange={(e) =>
                setMaxIte(e.target.value)
              }
            />
          </div>

          <button
            onClick={loadIteData}
          >
            Apply Filter
          </button>

        </div>

      </div>

      <div className="table-card">

        <h3>
          Customer ITE Results
        </h3>

        <p>
          Showing {iteData.length.toLocaleString()} customers
        </p>

        <div className="table-container">

          <table>

            <thead>
              <tr>
                <th>#</th>
                <th>Treatment</th>
                <th>Conversion</th>
                <th>ITE</th>
              </tr>
            </thead>

            <tbody>

              {iteData.map(
                (row, index) => (
                  <tr key={index}>

                    <td>
                      {index + 1}
                    </td>

                    <td>
                      {row.treatment}
                    </td>

                    <td>
                      {row.conversion}
                    </td>

                    <td>
                      {row.ite.toFixed(6)}
                    </td>

                  </tr>
                )
              )}

            </tbody>

          </table>

        </div>

      </div>

    </div>
  );
}

export default Week2Dashboard;