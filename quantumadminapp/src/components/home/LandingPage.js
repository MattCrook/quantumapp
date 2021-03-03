import React from "react";
import NavBar from "../nav/Nav";

const LandingPage = (props) => {
  return (
    <>
      <NavBar {...props} />
      <div>Landing Page</div>
    </>
  );
};

export default LandingPage;
