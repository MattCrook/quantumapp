import React, { useState, useEffect } from "react";
import NavBar from "../nav/Nav";
import env from "../../../env-config.json";
import { api_endpoints_config } from "../../../api-endpoints";
import { healthCheck } from "../../modules/services";
import "./styles/ApiDashboard.css";

const ApiDashboard = (props) => {
  const [response, setResponse] = useState([]);
  const [health, setHealth] = useState([]);
  const defaultSchema = "None Selected";
  const [endpoint, setEndpoint] = useState(defaultSchema);
  const [schema, setSchema] = useState([]);

  const handleSelectSchema = (e) => {
    const index = e.target.id;
    const entries = Object.entries(api_endpoints_config);
    const selectedSchema = entries[index];
    const selectedSchemaName = selectedSchema[0];
    setEndpoint(selectedSchemaName);
  };

  const endpoints = () => {
    const entries = Object.entries(api_endpoints_config);
    const rows = entries.map((entry, i) => {
      return (
        <div key={i} id={i} className="api_endpoint_item" onClick={handleSelectSchema}>
          "{entry[0]}": "{entry[1]}"
        </div>
      );
    });
    return rows;
  };

  useEffect(() => {
    const getApiHealth = async () => {
      const healthResponse = await healthCheck();
      setResponse(healthResponse);
      const respJson = await healthResponse.json();
      setHealth(respJson);
    };
    getApiHealth();
  }, []);

  return (
    <>
      <NavBar {...props} />
      <div id="api_root_schema_master_container">
        <div id="quantumapi_root_container">
          <div className="title_wrapper">
            <div className="quantumapi_title">QuantumAPI</div>
          </div>
          <div className="endpoints">
            <div className="endpoint_info_container">
              <div className="endpoint_info">GET /api/</div>
              {/* Send a health check request and if comes back ok have like green check or the status below */}
              {response.status === 200 && response.ok === true ? (
                <>
                  <div className="status_container">
                    <div className="endpoint_info">HTTP 200 OK</div>
                    <i id="ok" className="far fa-check-circle"></i>
                  </div>
                </>
              ) : (
                <>
                  <div className="status_container">
                    <div className="endpoint_info">HTTP 500 FAILED</div>
                    <i id="fail" className="fas fa-exclamation-triangle"></i>
                  </div>
                </>
              )}
              <div className="endpoint_info">Allow: GET, HEAD, OPTIONS</div>
              <div className="endpoint_info">Content-Type: application/json</div>
              <div className="endpoint_info">Vary: Accept</div>
            </div>
            <div id="endpoints_list">{endpoints()}</div>
          </div>
        </div>
        <div className="schema_container">
        <div className="title_wrapper">
            <div className="quantumapi_title">API Endpoint Schema</div>
          </div>
          <div className="endpoint_info_container">
          <div className="endpoint_info">Endpoint: {endpoint}</div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ApiDashboard;
