import React, {useState} from "react";
import { useAuthUser } from "../../contexts/AuthUserContext";
import LockOpenIcon from "@material-ui/icons/LockOpen";
import LockIcon from '@material-ui/icons/Lock';
import HomeOutlinedIcon from '@material-ui/icons/HomeOutlined';
import AccountCircleIcon from '@material-ui/icons/AccountCircle';
import VerticalSplitOutlinedIcon from '@material-ui/icons/VerticalSplitOutlined';
import LanguageOutlinedIcon from '@material-ui/icons/LanguageOutlined';
import StorageIcon from '@material-ui/icons/Storage';
// import AccountCircleOutlinedIcon from '@material-ui/icons/AccountCircleOutlined';
import PermIdentityIcon from '@material-ui/icons/PermIdentity';
// import env from "../../../env-config.json";
import "./Nav.css";

const NavBar = (props) => {
  const defaultProfilePicture = "https://aesusdesign.com/wp-content/uploads/2019/06/mans-blank-profile-768x768.png";
  const { isLoading, userProfile, isAuthenticated, isLoggedIn, adminLogout } = useAuthUser();
  const [isOpen, setIsOpen] = useState(false);

  const handleProfileDropdown = () => {
    setIsOpen(!isOpen);
  };

  const redirectToDjangoAdmin = () => {
    const adminURI = window._env_.DJANGO_ADMIN_URI;
    window.location.href = adminURI
  };

  const redirectToRestFrameworkAdmin = () => {
    const drfURI = window._env_.REST_FRAMEWORK_ADMIN_URI;
    window.location.href = drfURI
  };

  const redirectToRestFrameworkUserDetails = () => {
    const drfURI = window._env_.REST_FRAMEWORK_ADMIN_URI_USER_DETAILS;
    window.location.href = drfURI
  };

const redirectToRestAPIRoot = () => {
  const apiRootURI = window._env_.REST_FRAMEWORK_API_ROOT;
  window.location.href = apiRootURI
};


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
            <div className="nav_action_button" onClick={() => props.history.push("/quantumadmin/")}>Home</div>
              <div className="nav_action_button">Monitoring </div>
              <div className="nav_action_button" onClick={() => props.history.push("/quantumadmin/logging/")}>Logging </div>
            <div className="nav_action_button" onClick={() => props.history.push("/quantumadmin/api-dashboard/")}>api dashboard</div>
          </div>
        </div>
              ) : null}

        <div className="nav_end">
          <div className="nav_profile_dropdown" onClick={() => handleProfileDropdown()}>
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
          {isOpen ? (
            <div className="dropdown_container">
              <div className="dropdown_row_wrapper">
                <div className="dropdown_item">Home</div>
                <HomeOutlinedIcon style={{ color: 'rgb(206, 206, 206)', fontSize: 17, marginRight: 6}} />
              </div>
              <div className="dropdown_row_wrapper">
                <div className="dropdown_item">Account</div>
                <AccountCircleIcon style={{ color: 'rgb(206, 206, 206)', fontSize: 17, marginRight: 6}} />
                </div>
                <div className="dropdown_row_wrapper">
                <div className="dropdown_item" onClick={() => redirectToDjangoAdmin()}>Django Admin</div>
                <VerticalSplitOutlinedIcon style={{ color: 'rgb(206, 206, 206)', fontSize: 17, marginRight: 6}} />
                </div>
                  <div className="dropdown_row_wrapper" style={{ marginBottom: 3 }}>
                <div className="dropdown_item" onClick={() => redirectToRestFrameworkAdmin()}>Rest Framework Admin</div>
                <StorageIcon style={{ color: 'rgb(206, 206, 206)', fontSize: 17, marginRight: 6}} />
              </div>
              <div className="dropdown_row_wrapper" style={{ marginBottom: 3 }}>
                <div className="dropdown_item" onClick={() => redirectToRestFrameworkUserDetails()}>Rest Framework Admin User Details</div>
                <PermIdentityIcon style={{ color: 'rgb(206, 206, 206)', fontSize: 17, marginRight: 6}} />
              </div>
              <div className="dropdown_row_wrapper" style={{ marginBottom: 3 }}>
                <div className="dropdown_item" onClick={() => redirectToRestAPIRoot()}>Rest Framework API Root</div>
                <LanguageOutlinedIcon style={{ color: 'rgb(206, 206, 206)', fontSize: 17, marginRight: 6}} />
                </div>
            </div>
          ) : null}
          <div className="login_logout_wrapper">
            {!isLoading && isAuthenticated && isLoggedIn ? (
              <>
              <div className="logout" onClick={() => adminLogout()}>Logout</div>
                <LockIcon style={{ color: 'white', fontSize: 18, marginBottom: 6, marginLeft: 8}} />
                </>
            ) : (
              <>
                <div className="login" onClick={() => props.history.push("/quantumadmin/login")}>Login</div>
                <LockOpenIcon style={{ color: 'white', fontSize: 18, marginBottom: 6, marginLeft: 8 }} />
              </>
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default NavBar;
