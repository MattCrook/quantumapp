import React from "react";
import NavBar from "../nav/Nav";

const Home = (props) => {
  return (
    <>
      <NavBar {...props} />
      <div>Home</div>
    </>
  );
};

export default Home;
