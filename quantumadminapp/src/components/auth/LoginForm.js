import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import "./styles/Login.css"

const useStyles = makeStyles((theme) => ({
  root: {
    "& > *": {
      margin: theme.spacing(1),
      width: "35ch",
      display: "flex",
      flexDirection: "column",
      color: "white",
    },
    text: {
      color: "white",
    }
  },
}));

export default function AuthForm(props) {
  const classes = useStyles();
  const onSubmit = (e) => {
    e.preventDefault();
  }

  return (
    <>
      <div className="form_container" onSubmit={props.handleLogin}>
        <form id="auth_form" className={classes.root} noValidate autoComplete="off">
          <TextField id="email" label="Email" color="secondary" ref={props.email}/>
          <TextField
            id="password"
            label="Password"
            color="secondary"
            ref={props.password}
            type="password"
          />
          <div className="login_btn_wrapper">
          <button className="admin_login_submit_button" type="submit" onClick={(e) => onSubmit(e)}>Login</button>
          </div>
        </form>
      </div>
    </>
  );
}
