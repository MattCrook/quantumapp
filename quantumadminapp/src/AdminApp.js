import React from "react";
import { BrowserRouter, useHistory } from "react-router-dom";
import Views from "./components/Views";
import CssBaseline from "@material-ui/core/CssBaseline";

const AdminApp = (props) => {
  const history = useHistory()
  return (
    <>
      <CssBaseline />
      <BrowserRouter history={history}>
        {/* <NavBar {...props} /> */}
        <Views {...props} />
      </BrowserRouter>
    </>
  );
};

export default AdminApp;
