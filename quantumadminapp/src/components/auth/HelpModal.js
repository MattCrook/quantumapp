import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Modal from "@material-ui/core/Modal";
import Backdrop from "@material-ui/core/Backdrop";
import Fade from "@material-ui/core/Fade";

const useStyles = makeStyles((theme) => ({
  modal: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 100,
  },
  paper: {
    // backgroundColor: theme.palette.background.paper,
    backgroundColor: "rgb(44, 44, 44)",
    border: "2px solid #000",
    boxShadow: theme.shadows[5],
    width: 560,
    padding: theme.spacing(2, 4, 3),
  },
}));

const LoginHelpModal = (props) => {
  const classes = useStyles();

  return (
    <div>
      <Modal
        aria-labelledby="transition-modal-title"
        aria-describedby="transition-modal-description"
        className={classes.modal}
        open={props.open}
        onClose={props.handleClose}
        closeAfterTransition
        BackdropComponent={Backdrop}
        BackdropProps={{
          timeout: 500,
        }}
      >
        <Fade in={props.open}>
          <div className={classes.paper}>
            <div className="help_modal_title" id="transition-modal-title">
              Help
              <i className="far fa-question-circle"></i>
            </div>
            <p id="transition-modal-description">
              If you are logging in for the first time, click "Register Your Admin Account" and login with your email
              and password given to you by your system administrators.{" "}
            </p>
            <p id="transition-modal-description">
              You will log in with your admin email, choose a username of your liking, confirm the password given to you
              by your system administrator - which will be valid only for one first time log in, and change that
              password to something of your choice.
            </p>
            <p id="transition-modal-description">
              Once you are logged in for the first time and your password has been changed, you may use that password
              for every login in the future.
            </p>
            <p id="transition-modal-description">
              Returning admin users, please log in with your email and password you have set for your account on first
              log in.
            </p>
            <div className="help_modal_exit_btn">
              <div className="help_modal_exit_btn_text" onClick={() => props.handleClose()}>
                Exit
              </div>
            </div>
            <div className="signature">
              <p id="signature_font_help_modal">
                Made by <a href="https://matt-crook-io.now.sh/">Quantum Coasters</a>
                <i id="i" className="fas fa-trademark"></i>
              </p>
            </div>
          </div>
        </Fade>
      </Modal>
    </div>
  );
};

export default LoginHelpModal;
