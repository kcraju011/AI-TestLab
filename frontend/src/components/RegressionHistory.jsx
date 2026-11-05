import { useEffect, useState } from "react";

const API =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000";

export default function RegressionHistory() {
  const [runs, setRuns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadHistory() {
      try {
        const response = await fetch(
          `${API}/api/v1/regression/history`
        );

        if (!response.ok) {
          throw new Error("Unable to load regression history");
        }

        const data = await response.json();
        setRuns(data.items || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadHistory();
  }, []);

  if (loading) return <p>Loading regression history...</p>;
  if (error) return <p>{error}</p>;

  return (
    <section>
      <h2>Regression History</h2>

      {runs.length === 0 ? (
        <p>No regression runs found.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Run ID</th>
              <th>Tests</th>
              <th>Passed</th>
              <th>Regressions</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            {runs.map((run) => (
              <tr key={run.id}>
                <td>{run.source_run_id}</td>
                <td>{run.total_tests}</td>
                <td>{run.passed}</td>
                <td>{run.failed}</td>
                <td>{run.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
