import CssBaseline from "@material-ui/core/CssBaseline";
import { makeStyles } from "@material-ui/core/styles";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Admin from "./admin_v2/Admin";
import Header from "./Header";
import Home from "./Home";

const useStyles = makeStyles((theme) => ({
    root: {
        display: "flex",
    },
    brand: {
        height: 30,
        marginRight: theme.spacing(2),
    },
    // necessary for content to be below app bar
    toolbar: theme.mixins.toolbar,
    content: {
        flexGrow: 1,
        backgroundColor: theme.palette.background.default,
        padding: theme.spacing(3),
    },
}));

export default function App() {
    const classes = useStyles();

    return (
        <Router>
            <div className={classes.root}>
                <CssBaseline />
                <Header />

                <Switch>
                    <Route path="/admin">
                        <Admin />
                    </Route>
                    <Route path="/">
                        <Home />
                    </Route>
                </Switch>
            </div>
        </Router>
    );
}
