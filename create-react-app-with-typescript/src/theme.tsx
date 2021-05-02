import red from "@material-ui/core/colors/red";
import { createMuiTheme } from "@material-ui/core/styles";

// A custom theme for this app
const theme = createMuiTheme({
    palette: {
        primary: {
            main: "#F77F00",
        },
        secondary: {
            main: "#FCBF49",
        },
        error: {
            main: red.A400,
        },
        background: {
            default: "#fff",
        },
    },
});

export default theme;
