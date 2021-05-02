import AppBar from "@material-ui/core/AppBar";
import { makeStyles } from "@material-ui/core/styles";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";

const useStyles = makeStyles((theme) => ({
    toolbar: {
        backgroundColor: "#003049",
        color: "white",
    },
    brand: {
        height: 40,
        marginRight: theme.spacing(2),
    },
}));

export default function Header() {
    const classes = useStyles();

    return (
        <AppBar position="fixed">
            <Toolbar className={classes.toolbar}>
                <img src="logo.png" className={classes.brand} />
                <Typography variant="h4" noWrap>
                    Insiders
                </Typography>
            </Toolbar>
        </AppBar>
    );
}
