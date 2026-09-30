import { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:8000";

function CausalAudit() {
  const [audit, setAudit] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadAudit() {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(
        `${API_URL}/mid-review/causal-audit`
      );

      if (!response.ok) {
        throw new Error(
          "Failed to load causal audit results."
        );
      }

      const data = await response.json();

      setAudit(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadAudit();
  }, []);

  if (loading) {
    return (
      <div className="causal-audit">
        <h2>Mid-Project Causal Audit</h2>
        <p>Loading DoWhy refutation results...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="causal-audit">
        <h2>Mid-Project Causal Audit</h2>
        <p className="error">{error}</p>
      </div>
    );
  }

  if (!audit) {
    return null;
  }

  const tests = [
    {
      key: "random_common_cause",
      name: "Random Common Cause",
      description:
        "Adds a randomly generated common cause and checks the stability of the estimated effect.",
    },
    {
      key: "placebo_treatment",
      name: "Placebo Treatment",
      description:
        "Replaces the treatment with a placebo treatment to test whether the estimated effect persists.",
    },
    {
      key: "data_subset",
      name: "Data Subset",
      description:
        "Re-estimates the effect using a subset of the audit data.",
    },
  ];

  return (
    <div className="causal-audit">

      {/* HEADER */}
      <div className="audit-header">

        <h2>Mid-Project Causal Audit</h2>

        <p>
          DoWhy refutation tests applied to the
          Criteo Uplift Modeling Dataset.
        </p>

      </div>


      {/* AUDIT INFORMATION */}
      <div className="metric-grid">

        <div className="metric-card">
          <span>Audit Sample</span>
          <strong>
            {audit.sample_size.toLocaleString()}
          </strong>
        </div>

        <div className="metric-card">
          <span>Estimated ATE</span>
          <strong>
            {audit.estimated_ate.toFixed(6)}
          </strong>
        </div>

        <div className="metric-card">
          <span>Treatment</span>
          <strong>
            {audit.treatment}
          </strong>
        </div>

        <div className="metric-card">
          <span>Outcome</span>
          <strong>
            {audit.outcome}
          </strong>
        </div>

      </div>


      {/* REFUTATION RESULTS */}
      <div className="audit-results">

        <h3>DoWhy Refutation Tests</h3>

        <div className="audit-table-container">

          <table>

            <thead>
              <tr>
                <th>Refutation Test</th>
                <th>Original Effect</th>
                <th>New Effect</th>
                <th>p-value</th>
                <th>Runtime</th>
              </tr>
            </thead>

            <tbody>

              {tests.map((test) => {

                const result =
                  audit.refutation_tests[test.key];

                return (
                  <tr key={test.key}>

                    <td>
                      <strong>
                        {test.name}
                      </strong>
                    </td>

                    <td>
                      {result.estimated_effect !== null
                        ? result.estimated_effect.toFixed(6)
                        : "N/A"}
                    </td>

                    <td>
                      {result.new_effect !== null
                        ? result.new_effect.toFixed(6)
                        : "N/A"}
                    </td>

                    <td>
                      {result.p_value !== null
                        ? result.p_value.toFixed(2)
                        : "N/A"}
                    </td>

                    <td>
                      {result.runtime_seconds.toFixed(2)} s
                    </td>

                  </tr>
                );

              })}

            </tbody>

          </table>

        </div>

      </div>


      {/* TEST DETAILS */}
      <div className="audit-details">

        <h3>Refutation Test Details</h3>

        {tests.map((test) => {

          const result =
            audit.refutation_tests[test.key];

          return (
            <div
              className="audit-detail-card"
              key={test.key}
            >

              <h4>
                {test.name}
              </h4>

              <p>
                {test.description}
              </p>

              <div className="audit-detail-values">

                <div>
                  <span>Original Effect</span>
                  <strong>
                    {result.estimated_effect.toFixed(6)}
                  </strong>
                </div>

                <div>
                  <span>Refuted Effect</span>
                  <strong>
                    {result.new_effect.toFixed(6)}
                  </strong>
                </div>

                <div>
                  <span>p-value</span>
                  <strong>
                    {result.p_value.toFixed(2)}
                  </strong>
                </div>

              </div>

            </div>
          );

        })}

      </div>


      {/* AUDIT INTERPRETATION */}
      <div className="audit-note">

        <h3>Audit Interpretation</h3>

        <p>
          These DoWhy refutation tests provide
          robustness checks for the estimated causal
          effect under the specified perturbations.
          They should not be interpreted as proof that
          all possible hidden confounding has been
          eliminated.
        </p>

      </div>


      {/* DATASET INFORMATION */}
      <div className="audit-source">

        <p>
          <strong>Dataset:</strong>{" "}
          {audit.dataset}
        </p>

        <p>
          <strong>Covariates:</strong>{" "}
          {audit.covariates.join(", ")}
        </p>

      </div>

    </div>
  );
}

export default CausalAudit;