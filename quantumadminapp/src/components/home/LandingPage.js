import React from "react";
import NavBar from "../nav/Nav";
// import backgroundImage from "../../../../media/2657aeea59db557.jpg"
import backgroundImage from "../../../images/data-analytics.jpg";
const LandingPage = (props) => {
  return (
    <>
      <NavBar {...props} />
      <div id="landing_page_container">
        <img className="bg_image" src={backgroundImage} />
        {/* <div className="home_page_container">
          <div className="logo_banner">
            <h1 className="add-shadow">Quantum Coasters Admin</h1>
            <div className="logo_container">
              <p className="add-shadow">
                A Quantum LLC systems management application
              </p>
            </div>
          </div>
        </div> */}

        <div className="signature">
          <p id="signature_font">
            Made by <a href="https://matt-crook-io.now.sh/">Quantum Coasters</a>{" "}
            <i className="fas fa-trademark"></i>
          </p>
        </div>
      </div>
    </>
  );
};

export default LandingPage;
