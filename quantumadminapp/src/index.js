import React from "react";
import ReactDOM from "react-dom";
import {AuthUserProvider} from "./contexts/AuthUserContext";
import AdminApp from "./AdminApp";
import '@babel/polyfill'
// import '@babel/core'
// import '@babel/preset-env'
// import '@babel/preset-react'



ReactDOM.render(
  <AuthUserProvider>
    <AdminApp />
  </AuthUserProvider>,
  document.getElementById("app")
);
