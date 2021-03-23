import React from "react";
import NavBar from "../nav/Nav";

const Home = (props) => {
  return (
    <>
      <NavBar {...props} />
      <div style={{color: "white"}}>Home</div>
    </>
  );
};

export default Home;
