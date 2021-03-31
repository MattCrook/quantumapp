import React, {useState} from "react";
import { useAuthUser } from "../../contexts/AuthUserContext";
import LockOpenIcon from "@material-ui/icons/LockOpen";
import LockIcon from '@material-ui/icons/Lock';

import "./Nav.css";

const NavBar = (props) => {
  const defaultProfilePicture = "https://aesusdesign.com/wp-content/uploads/2019/06/mans-blank-profile-768x768.png";
  const { isLoading, userProfile, isAuthenticated, isLoggedIn } = useAuthUser();
  const [isOpen, setIsOpen] = useState(false);

  const handleProfileDropdown = () => {
    
  }



  return (
    <>
      <div className="nav_main_container">
        <div className="nav_start">
          <div className="title_wrapper">
            <div className="title">Quantum Coasters Admin</div>
          </div>
              </div>
              {!isLoading && isAuthenticated && isLoggedIn ? (
        <div className="nav_middle">
          <div className="nav_buttons">
            <div className="nav_action_button">Home</div>
            <div className="nav_action_button">Monitoring </div>
            <div className="nav_action_button">api dashboard</div>
          </div>
        </div>
              ) : null}

        <div className="nav_end">
          <div className="nav_profile_dropdown">
            {!isLoading && userProfile.image ? (
              <img
                data-testid="home-profile-pic-testid"
                id="nav-profile-pic"
                src={userProfile.image.image}
                alt="My Avatar"
              />
            ) : (
              <img
                data-testid="home-profile-pic-testid"
                id="nav-profile-pic"
                src={defaultProfilePicture}
                alt="My Avatar"
              />
            )}
          </div>
          <div className="login_logout_wrapper">
            {!isLoading && isAuthenticated && isLoggedIn ? (
              <>
              <div className="logout">Logout</div>
                <LockIcon style={{ color: 'white', fontSize: 18, marginBottom: 14 }} />
                </>
            ) : (
              <>
                <div className="login" onClick={() => props.history.push("/quantumadmin/login")}>Login</div>
                <LockOpenIcon style={{ color: 'white', fontSize: 18, marginBottom: 14 }} />
              </>
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default NavBar;
