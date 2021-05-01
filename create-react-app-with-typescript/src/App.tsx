import { Box, Button } from "@material-ui/core";
import AppBar from "@material-ui/core/AppBar";
import CssBaseline from "@material-ui/core/CssBaseline";
import { makeStyles } from "@material-ui/core/styles";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import ChevronLeftIcon from "@material-ui/icons/ChevronLeft";
import React from "react";
import BasicMenu from "./BasicMenu";
import LeftDrawer from "./LeftDrawer";
import UserTable from "./UserTable";

const drawerWidth = 260;

const useStyles = makeStyles((theme) => ({
    root: {
        display: "flex",
    },
    appBar: {
        width: `calc(100% - ${drawerWidth}px)`,
        marginLeft: drawerWidth,
    },
    drawer: {
        width: drawerWidth,
        flexShrink: 0,
    },
    drawerPaper: {
        width: drawerWidth,
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
        <div className={classes.root}>
            <CssBaseline />
            <AppBar position="fixed" className={classes.appBar}>
                <Toolbar>
                    <Typography variant="h6" noWrap>
                        Company User Administration
                    </Typography>
                </Toolbar>
            </AppBar>

            <LeftDrawer />
            <main className={classes.content}>
                <div className={classes.toolbar} />
                <Box textAlign="right">
                    <Button
                        startIcon={<ChevronLeftIcon />}
                        color="secondary"
                        variant="contained"
                    >
                        Back to home
                    </Button>
                    <BasicMenu />
                </Box>
                <Typography paragraph>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
                    do eiusmod tempor incididunt ut labore et dolore magna
                    aliqua. Rhoncus dolor purus non enim praesent elementum
                    facilisis leo vel. Risus at ultrices mi tempus imperdiet.
                    Semper risus in hendrerit gravida rutrum quisque non tellus.
                    Convallis convallis tellus id interdum velit laoreet id
                    donec ultrices. Odio morbi quis commodo odio aenean sed
                    adipiscing. Amet nisl suscipit adipiscing bibendum est
                    ultricies integer quis. Cursus euismod quis viverra nibh
                    cras. Metus vulputate eu scelerisque felis imperdiet proin
                    fermentum leo. Mauris commodo quis imperdiet massa
                    tincidunt. Cras tincidunt lobortis feugiat vivamus at augue.
                    At augue eget arcu dictum varius duis at consectetur lorem.
                    Velit sed ullamcorper morbi tincidunt. Lorem donec massa
                    sapien faucibus et molestie ac.
                </Typography>
                <UserTable />
            </main>
        </div>
    );
}
