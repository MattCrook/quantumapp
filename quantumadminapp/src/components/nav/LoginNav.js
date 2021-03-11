import React from "react";
import ExitToAppRoundedIcon from "@material-ui/icons/ExitToAppRounded";
import "./Nav.css";

const LoginNav = (props) => {
  return (
    <>
      <div className="nav_main_container">
        <div className="nav_start">
          <div className="title_wrapper">
            <div className="title">Quantum Coasters Admin</div>
          </div>
        </div>

        <div className="nav_end">
          <div className="login_logout_wrapper">
            <div
              className="back_to_landing_page"
              onClick={() => props.history.push("/quantumadmin")}
            >
              Back
            </div>
            <ExitToAppRoundedIcon style={{ color: 'white', fontSize: 18, marginBottom: 4 }} />
          </div>
        </div>
      </div>
    </>
  );
};

export default LoginNav;
