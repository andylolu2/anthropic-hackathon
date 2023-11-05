import "./index.css";

import React from "react";
import ReactDOM from "react-dom/client";

import { createTheme, ThemeProvider } from "@mui/material/styles";

import App from "./App";
import reportWebVitals from "./reportWebVitals";

const theme = createTheme({
    palette: {
        mode: "light",
        primary: {
            light: "rgb(255, 255, 255)",
            main: "rgb(223, 214, 200)",
        },
        secondary: {
            main: "rgb(204, 120, 92)",
        },
    },
});

const root = ReactDOM.createRoot(document.getElementById("root") as HTMLElement);
root.render(
    <React.StrictMode>
        <ThemeProvider theme={theme}>
            <App />
        </ThemeProvider>
    </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
