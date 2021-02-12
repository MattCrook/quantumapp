import React from "react";
import { BrowserRouter, useHistory } from "react-router-dom";
import Router from "./components/Router";
import CssBaseline from "@material-ui/core/CssBaseline";

const AdminApp = (props) => {
  const history = useHistory()
  return (
    <>
      <CssBaseline />
      <BrowserRouter history={history}>
        {/* <NavBar {...props} /> */}
        <Router {...props} />
      </BrowserRouter>
    </>
  );
};

export default AdminApp;
