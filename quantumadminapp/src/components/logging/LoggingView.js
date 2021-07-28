import React, { useState, useEffect } from "react";
import NavBar from "../nav/Nav";
import env from "../../../env-config.json";
import { api_endpoints_config } from "../../../api-endpoints";
import { healthCheck } from "../../modules/services";
import "./styles/Logging.css";

const LoggingView = (props) => {
  return (
    <>
      <NavBar {...props} />
      <div id="logging_navigation_container">
        <div className="logging_buttons_wrapper">
          <div className="logging_navigation_btn">Error Logs</div>
          <div className="logging_navigation_btn">Bug Reports</div>
          <div className="logging_navigation_btn">App Login Data Logs</div>
          <div className="logging_navigation_btn">Activity Logs</div>
          <div className="logging_navigation_btn">Login History</div>
          <div className="logging_navigation_btn">Login User Credentials</div>
        </div>
      </div>
      <div>Straight Read on Error Log Table</div>
    </>
  );
};

export default LoggingView;
