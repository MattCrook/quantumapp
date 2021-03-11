import React from "react";
import { Route } from "react-router-dom";
import { useAuthUser } from "../contexts/AuthUserContext";
import LandingPage from "./home/LandingPage";
import Home from "./home/Home";
import Login from "./auth/Login";

const Views = (props) => {
  const { isAuthenticated, isLoading, isLoggedIn, authUser } = useAuthUser();
  // console.log(isLoggedIn)

  return (
    <React.Fragment>
      <Route
        exact
        path="/quantumadmin"
        render={(props) => {
          if (!isLoading && authUser && isAuthenticated && isLoggedIn) {
            return <Home {...props} />;
          } else {
            return <LandingPage {...props} />;
          }
        }}
      />
      <Route
        exact
        path="/quantumadmin/login"
        render={(props) => {
          if (!isLoading && !isAuthenticated && !isLoggedIn) {
            return <Login {...props} />;
          } else {
            return <Home {...props} />;
          }
        }}
      />
    </React.Fragment>
  );
};

export default Views;
