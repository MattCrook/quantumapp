import React, { useState } from "react";
import NavBar from "../nav/Nav";
import env from "../../../env-config.json";
import { api_endpoints_config } from "../../../api-endpoints";
import "./styles/ApiDashboard.css";

const ApiDashboard = (props) => {
  const endpoints = () => {
    const entries = Object.entries(api_endpoints_config);
    const rows = entries.map((entry, i) => {
      return (
        <div key={i} className="api_endpoint_item">
          "{entry[0]}": "{entry[1]}"
        </div>
      );
    });
    return rows;
  };

  return (
    <>
      <NavBar {...props} />
      <div id="quantumapi_root_container">
        <div className="title_wrapper">
          <div className="quantumapi_title">QuantumAPI</div>
        </div>
        <div className="endpoints">
          <div className="endpoint_info_container">
            <div className="endpoint_info">GET /api/</div>
            {/* Send a health check request and if comes back ok have like green check or the status below */}
            <div className="endpoint_info">HTTP 200 OK</div>
            <div className="endpoint_info">Allow: GET, HEAD, OPTIONS</div>
            <div className="endpoint_info">Content-Type: application/json</div>
            <div className="endpoint_info">Vary: Accept</div>
          </div>
          <div>{endpoints()}</div>
        </div>
      </div>
    </>
  );
};

export default ApiDashboard;
