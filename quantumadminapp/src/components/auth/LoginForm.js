import React from "react";
import { makeStyles, withTheme } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";

const useStyles = makeStyles((theme) => ({
  root: {
    "& > *": {
      margin: theme.spacing(1),
      width: "35ch",
      display: "flex",
      flexDirection: "column",
      color: "white",
    },
  },
}));

export default function AuthForm() {
  const classes = useStyles();

  return (
    <>
      <div className="form_container">
        <form id="auth_form" className={classes.root} noValidate autoComplete="off">
          <TextField id="standard-secondary" label="Email" color="secondary" />
          <TextField
            id="standard-secondary"
            label="Password"
            color="secondary"
          />

          {/* 
      <TextField
      id="outlined-secondary"
      label="Outlined secondary"
      variant="outlined"
      color="secondary"
    /> */}
        </form>
      </div>
    </>
  );
}
