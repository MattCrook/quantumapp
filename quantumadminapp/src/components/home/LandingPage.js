import React from "react";
import NavBar from "../nav/Nav";

const LandingPage = (props) => {
    // const backgroundImage = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.corporatecomplianceinsights.com%2Fprotiviti-study-data-and-analytics-are-top-priorities-for-finance-executives%2F&psig=AOvVaw2Gv_KBsdHV7JOy-x8KZTMu&ust=1614962331732000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCJCVvd2Jl-8CFQAAAAAdAAAAABAR"
  return (
    <>
      <NavBar {...props} />
          <div id="landing_page_background_picture" className="bg-img">
              {/* <img className="bg_image" src={backgroundImage}/> */}
      </div>
      <div className="signature">
        <p id="signature_font">
          Made by <a href="https://matt-crook-io.now.sh/">Quantum Coasters</a> <i className="fas fa-trademark"></i>
        </p>
      </div>
    </>
  );
};

export default LandingPage;
