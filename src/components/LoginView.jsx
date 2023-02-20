// Import the material-ui components
import * as React from "react";
import { useState, useEffect } from "react";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import Paper from "@mui/material/Paper";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Alert from "@mui/material/Alert";
import Link from "@mui/material/Link";
import Collapse from "@mui/material/Collapse";
import Snackbar from "@mui/material/Snackbar";
import CustomLogoST from "./LogoST";
import LoginIcon from "@mui/icons-material/Login";

const LoginView = ({ handleViewChange }) => {
    const [openSnack, setOpenSnack] = React.useState(false);
    const [error, setError] = React.useState("")
    const handleClickSnack = (error) => {
        setOpenSnack(true);
        setError(error)
    };

    const handleClose = (event, reason) => {
        setOpenSnack(false);
    };

    // Custom styles to the logo
    const customStyles = {
        letterSpacing: "9px",
        fontSize: "4em",
        borderTop: "solid .2rem",
        borderBottom: "solid .2rem",
        userSelect: "none",
    };

    const [rememberUsername, setRememberUsername] = useState(true);
    const [username, setUsername] = useState("");
    const [date, setDate] = useState(new Date());
    const [open, setOpen] = useState(false);
    // State variables for keeping track of the checkbox state, username, date, and collapse state

    // Submit function that submits the form data to the server
    const handleSubmit = (event) => {
        // Prevent the default form submit behavior
        event.preventDefault();
        if (rememberUsername) {
            // If the remember username checkbox is checked, save the username to local storage
            localStorage.setItem("username", username);
        } else {
            // If the remember username checkbox is not checked, remove the username from local storage
            localStorage.removeItem("username");
        }

        // Send a POST request to the server
        const dataP = {
            request: "login",
            password: `${document.getElementById("clave").value}`,
            user: `${document.getElementById("usuario").value}`,
        };
        fetch("http://localhost:5000/App", {
            method: "POST",
            body: JSON.stringify(dataP),
        })
            .then((response) => {
                // Check if the response was successful
                if (!response.ok) {
                    handleClickSnack(response.statusText)
                    throw Error(response.statusText);
                }
                return response.json();
            })
            .then((data) => {
                console.log(
                    "conn:",
                    data.login,
                    "error",
                    data.error,
                );
                if (data.login === "success") {
                    handleViewChange("HomeView");
                } else {
                    handleClickSnack(data.error);
                }
            })
            .catch((error) => {
                handleClickSnack("Por favor envia este error a desarrollo: " + error.message);
                console.error("Error:", error.message);
            });
    };

    useEffect(() => {
        // Use effect hook to update the username from local storage if it exists
        setUsername(localStorage.getItem("username"));

        // Set the date on an interval to change each day the image show it in the loggin
        const intervalId = () => {
            setDate(new Date());
        };

        // Return a cleanup function to clear the interval to change each day the image show it in the loggin
        return () => clearInterval(intervalId);
    }, []);

    // Get the single digit of the current date
    let numDate = date.toISOString()[9];
    // images array to change the image show it each day in the loggin
    const images = [
        "https://github.com/S-e-b-a-s/images/blob/main/image1.jpg?raw=true",
        "https://github.com/S-e-b-a-s/images/blob/main/image2.jpg?raw=true",
        "https://github.com/S-e-b-a-s/images/blob/main/image3.jpg?raw=true",
        "https://github.com/S-e-b-a-s/images/blob/main/image4.jpg?raw=true",
        "https://github.com/S-e-b-a-s/images/blob/main/image5.jpg?raw=true",
        "https://github.com/S-e-b-a-s/images/blob/main/image6.jpg?raw=true",
        "https://github.com/S-e-b-a-s/images/blob/main/image7.jpg?raw=true",
        "https://github.com/S-e-b-a-s/images/blob/main/image8.jpg?raw=true",
        "https://github.com/S-e-b-a-s/images/blob/main/image9.jpg?raw=true",
        "https://github.com/S-e-b-a-s/images/blob/main/image0.jpg?raw=true",
    ];

    // Function to handle toggling the collapse state
    const handleClick = () => {
        setOpen(!open);
    };

    return (
        <Grid container component="main" sx={{ height: "100vh" }}>
            <CssBaseline />

            <Snackbar
                anchorOrigin={{ vertical: "top", horizontal: "center" }}
                open={openSnack}
                autoHideDuration={6000}
                onClose={handleClose}
                key={{ vertical: "top", horizontal: "center" }}
            >
                <Alert
                    onClose={handleClose}
                    severity="error"
                    sx={{ width: "100%" }}
                >
                    {error}
                </Alert>
            </Snackbar>
            <Grid
                item
                xs={false}
                sm={4}
                md={7}
                sx={{
                    backgroundImage: `url(${images[numDate]})`,
                    backgroundRepeat: "no-repeat",
                    backgroundColor: (t) =>
                        t.palette.mode === "light"
                            ? t.palette.grey[50]
                            : t.palette.grey[900],
                    backgroundSize: "cover",
                    backgroundPosition: "center",
                }}
            />
            <Grid
                item
                xs={12}
                sm={8}
                md={5}
                component={Paper}
                elevation={6}
                square
            >
                <Box
                    sx={{
                        my: 8,
                        mx: 4,
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                    }}
                >
                    <CustomLogoST styles={customStyles}></CustomLogoST>
                    <Box
                        component="form"
                        onSubmit={handleSubmit}
                        sx={{ mt: 1 }}
                    >
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="usuario"
                            label="Nombre de usuario"
                            name="usuario"
                            autoFocus
                            value={username}
                            onChange={(event) =>
                                setUsername(event.target.value)
                            }
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="clave"
                            label="Contraseña"
                            type="password"
                            id="clave"
                            autoComplete="off"
                        />

                        <FormControlLabel
                            control={
                                <Checkbox
                                    value="remember"
                                    color="primary"
                                    checked={rememberUsername}
                                    onChange={(event) =>
                                        setRememberUsername(
                                            event.target.checked
                                        )
                                    }
                                />
                            }
                            label="Recuérdame"
                        />
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            <Box sx={{ display: "flex", paddingRight: ".5em" }}>
                                <LoginIcon></LoginIcon>
                            </Box>
                            Iniciar Sesion
                        </Button>
                        <Button
                            onClick={() => handleViewChange("PermissionsView")}
                        >
                            SH
                        </Button>
                        <Button onClick={() => handleViewChange("SingUpView")}>
                            ALG
                        </Button>
                        <Link href="#" onClick={handleClick}>
                            ¿Has olvidado tu contraseña?
                        </Link>
                        <Collapse in={open}>
                            <Alert severity="info">
                                En caso de olvido o perdida de la contraseña
                                contacte con tecnologia para el restablecimiento
                                de la misma en:{" "}
                                <a
                                    href="https://helpdesk.cyc-bpo.com/"
                                    target="_blank"
                                    rel="noreferrer noopener"
                                >
                                    GLPI
                                </a>
                            </Alert>
                        </Collapse>
                        <Grid container>
                            <Grid item xs></Grid>
                        </Grid>
                    </Box>
                </Box>
            </Grid>
        </Grid>
    );
};
export default LoginView;