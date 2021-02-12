import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router } from "react-router-dom";
import AdminApp from "./AdminApp";
// import "./index.css";

// The Context from React Router must be present in the component tree at a higher level
// for Auth0ProviderWithHistory to access the useHistory() hook from React Router.

ReactDOM.render(
  <Router>
    <AdminApp />
  </Router>,
  document.getElementById("app")
);
