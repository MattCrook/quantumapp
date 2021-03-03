import React from "react";
import { Route } from "react-router-dom";
import { useAuthUser } from "../contexts/AuthUserContext";
import LandingPage from "./home/LandingPage";
import Home from "./home/Home";



const Views = (props) => {
  const { isAuthenticated, isLoading, isLoggedIn, authUser } = useAuthUser();


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
    </React.Fragment>
  );
};

export default Views;
