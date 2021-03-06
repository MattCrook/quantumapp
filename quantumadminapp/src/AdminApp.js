import React from "react";
import { BrowserRouter, useHistory } from "react-router-dom";
import { useAuthUser } from "./contexts/AuthUserContext";
import Views from "./components/Views";
import CssBaseline from "@material-ui/core/CssBaseline";
import "./AdminApp.css";

const AdminApp = (props) => {
  const history = useHistory()
  const { isLoading } = useAuthUser();
  if (isLoading) {
    return (
      <div className="loading fade_in">
        <div className="loading-text">
          <span className="loading-text-words">L</span>
          <span className="loading-text-words">O</span>
          <span className="loading-text-words">A</span>
          <span className="loading-text-words">D</span>
          <span className="loading-text-words">I</span>
          <span className="loading-text-words">N</span>
          <span className="loading-text-words">G</span>
        </div>
      </div>
    )
  }
  return (
    <>
      <CssBaseline />
      <BrowserRouter history={history}>
        <Views {...props} />
      </BrowserRouter>
    </>
  );
};

export default AdminApp;
