import { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
} from "recharts";

import {
  Activity,
  ShieldCheck,
  Clock3,
  GitBranch,
  RefreshCw,
  CheckCircle2,
  XCircle,
  FlaskConical,
} from "lucide-react";

import "./App.css";

const API = import.meta.env.VITE_API_BASE_URL;

function MetricCard({ title, value, subtitle, icon: Icon }) {
  return (
    <div className="metric-card">
      <div className="metric-top">
        <span>{title}</span>
        <Icon size={20} />
      </div>
      <h2>{value}</h2>
      <p>{subtitle}</p>
    </div>
  );
}

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [lastUpdated, setLastUpdated] = useState(null);

  async function fetchDashboard() {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API}/api/v1/dashboard/summary`);

      if (!response.ok) {
        throw new Error(`Backend returned HTTP ${response.status}`);
      }

      const result = await response.json();
      setData(result);
      setLastUpdated(new Date());
    } catch (err) {
      setError(err.message || "Unable to load dashboard");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchDashboard();
  }, []);

  const testChartData = data
    ? [
        { name: "Passed", value: data.passed_tests },
        { name: "Failed", value: data.failed_tests },
      ]
    : [];

  const recentChartData = data
    ? data.recent_runs.map((run, index) => ({
        name: `${run.module} ${index + 1}`,
        passed: run.passed,
        failed: run.failed,
      }))
    : [];

  const regressionChartData = data
    ? data.regression_history.map((run, index) => ({
        name: `${run.suite} ${index + 1}`,
        regressions: run.regression_count,
        passRate: run.pass_rate,
      }))
    : [];

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <FlaskConical size={24} />
          </div>
          <div>
            <h2>AI-TestLab</h2>
            <span>Quality Engineering</span>
          </div>
        </div>

        <nav>
          <div className="nav-item active">
            <Activity size={18} />
            Overview
          </div>
          <div className="nav-item">
            <CheckCircle2 size={18} />
            Test Analytics
          </div>
          <div className="nav-item">
            <ShieldCheck size={18} />
            Security
          </div>
          <div className="nav-item">
            <GitBranch size={18} />
            Regression
          </div>
        </nav>

        <div className="sidebar-footer">
          AI Quality Platform
          <br />
          <span>Version 1.0</span>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <span className="eyebrow">QUALITY ENGINEERING PLATFORM</span>
            <h1>Testing Overview</h1>
            <p>Monitor your AI application's quality and reliability.</p>
          </div>

          <button
            className="refresh-button"
            onClick={fetchDashboard}
            disabled={loading}
          >
            <RefreshCw size={16} className={loading ? "spin" : ""} />
            Refresh
          </button>
        </header>

        {loading && !data && (
          <div className="notice">Loading dashboard data...</div>
        )}

        {error && (
          <div className="error-box">
            <XCircle size={18} />
            {error}
            <button onClick={fetchDashboard}>Retry</button>
          </div>
        )}

        {data && (
          <>
            <div className="status-row">
              <span className="status-dot" />
              Backend connected
              <span className="updated">
                {lastUpdated
                  ? `Updated ${lastUpdated.toLocaleTimeString()}`
                  : ""}
              </span>
            </div>

            <section className="metrics-grid">
              <MetricCard
                title="Total Tests"
                value={data.total_tests}
                subtitle="Batch and reliability tests"
                icon={FlaskConical}
              />

              <MetricCard
                title="Passed Tests"
                value={data.passed_tests}
                subtitle="Successful executions"
                icon={CheckCircle2}
              />

              <MetricCard
                title="Failed Tests"
                value={data.failed_tests}
                subtitle="Unsuccessful executions"
                icon={XCircle}
              />

              <MetricCard
                title="Pass Rate"
                value={`${data.pass_rate}%`}
                subtitle="Across counted test runs"
                icon={Activity}
              />

              <MetricCard
                title="Security Scans"
                value={data.security_scans}
                subtitle={`${data.security_findings} failed cases`}
                icon={ShieldCheck}
              />

              <MetricCard
                title="Average Latency"
                value={`${data.average_latency_ms} ms`}
                subtitle={`${data.reliability_runs} reliability reports`}
                icon={Clock3}
              />

              <MetricCard
                title="Regression Runs"
                value={data.regression_runs}
                subtitle="Saved suite executions"
                icon={GitBranch}
              />

              <MetricCard
                title="Regressions"
                value={data.regression_count}
                subtitle="Newly failing test cases"
                icon={Activity}
              />
            </section>

            <section className="charts-grid">
              <div className="panel">
                <div className="panel-heading">
                  <div>
                    <h3>Test Results</h3>
                    <p>Passed versus failed tests</p>
                  </div>
                </div>

                {data.total_tests > 0 ? (
                  <ResponsiveContainer width="100%" height={250}>
                    <PieChart>
                      <Pie
                        data={testChartData}
                        dataKey="value"
                        nameKey="name"
                        cx="50%"
                        cy="50%"
                        outerRadius={85}
                        label
                      >
                        <Cell fill="#16a34a" />
                        <Cell fill="#ef4444" />
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="empty-chart">
                    No test results available yet.
                  </div>
                )}
              </div>

              <div className="panel">
                <div className="panel-heading">
                  <div>
                    <h3>Recent Test Runs</h3>
                    <p>Passed and failed by module</p>
                  </div>
                </div>

                {recentChartData.length > 0 ? (
                  <ResponsiveContainer width="100%" height={250}>
                    <BarChart data={recentChartData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" hide />
                      <YAxis allowDecimals={false} />
                      <Tooltip />
                      <Bar dataKey="passed" fill="#16a34a" />
                      <Bar dataKey="failed" fill="#ef4444" />
                    </BarChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="empty-chart">
                    No batch or reliability reports available.
                  </div>
                )}
              </div>
            </section>

            <section className="charts-grid">
              <div className="panel">
                <div className="panel-heading">
                  <div>
                    <h3>Regression History</h3>
                    <p>New failures across saved suite runs</p>
                  </div>
                </div>

                {regressionChartData.length > 0 ? (
                  <ResponsiveContainer width="100%" height={230}>
                    <LineChart data={regressionChartData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" hide />
                      <YAxis allowDecimals={false} />
                      <Tooltip />
                      <Line
                        type="monotone"
                        dataKey="regressions"
                        stroke="#f59e0b"
                        strokeWidth={3}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="empty-chart">
                    No regression history available.
                  </div>
                )}
              </div>

              <div className="panel">
                <div className="panel-heading">
                  <div>
                    <h3>Latest Regression Runs</h3>
                    <p>Recent saved regression results</p>
                  </div>
                </div>

                {data.regression_history.length > 0 ? (
                  <div className="run-list">
                    {data.regression_history.slice(0, 6).map((run, index) => (
                      <div className="run-row" key={`${run.suite}-${index}`}>
                        <div>
                          <strong>{run.suite}</strong>
                          <span>{run.pass_rate}% pass rate</span>
                        </div>
                        <span
                          className={
                            run.status === "PASS"
                              ? "pill success"
                              : "pill danger"
                          }
                        >
                          {run.status}
                        </span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="empty-chart">
                    No regression runs recorded.
                  </div>
                )}
              </div>
            </section>

            <section className="panel data-notes">
              <h3>Data availability</h3>
              {data.data_notes.map((note, index) => (
                <p key={index}>• {note}</p>
              ))}
              <p>
                AI quality evaluation scores are not displayed yet because
                Day 4 does not currently save evaluation history.
              </p>
            </section>

            <section className="panel">
              <h3>Recent executions</h3>

              {data.recent_runs.length > 0 ? (
                <div className="table-scroll">
                  <table>
                    <thead>
                      <tr>
                        <th>Module</th>
                        <th>Report</th>
                        <th>Total</th>
                        <th>Passed</th>
                        <th>Failed</th>
                        <th>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {data.recent_runs.map((run, index) => (
                        <tr key={`${run.file}-${index}`}>
                          <td>{run.module}</td>
                          <td>{run.file}</td>
                          <td>{run.total}</td>
                          <td>{run.passed}</td>
                          <td>{run.failed}</td>
                          <td>
                            <span
                              className={
                                run.status === "PASS"
                                  ? "pill success"
                                  : "pill danger"
                              }
                            >
                              {run.status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="empty-chart">
                  Run your batch and reliability tests to populate this table.
                </div>
              )}
            </section>
          </>
        )}
      </main>
    </div>
  );
}

export default App;