import { Box, makeStyles, Typography } from "@material-ui/core";
import InfoIcon from "@material-ui/icons/Info";
import Color from "color";
import BasicMenu from "./BasicMenu";
import LeftDrawer from "./LeftDrawer";
import PolicySettings from "./PolicySettings";
import UserTable from "./UserTable";

const useStyles = makeStyles((theme) => ({
    content: {
        flexGrow: 1,
        backgroundColor: theme.palette.background.default,
        padding: theme.spacing(3),
        marginTop: 64,
    },
    info: {
        padding: theme.spacing(1),
        backgroundColor: Color(theme.palette.secondary.main)
            .alpha(0.2)
            .toString(),
        marginBottom: theme.spacing(5),
        display: "flex",
        flexDirection: "row",
    },
}));

export default function Admin() {
    const classes = useStyles();

    return (
        <>
            <LeftDrawer />
            <main className={classes.content}>
                <Box display="flex" flexDirection="row" alignItems="center">
                    <Typography
                        variant="h4"
                        style={{ flexGrow: 1 }}
                        gutterBottom
                    >
                        User administration
                    </Typography>
                    <BasicMenu />
                </Box>
                <Box className={classes.info}>
                    <InfoIcon style={{ marginRight: 16 }} />
                    <Typography>
                        Manage your users on this page, send them company policy
                        updates, or contact them by email.
                    </Typography>
                </Box>
                <PolicySettings />
                <UserTable />
            </main>
        </>
    );
}
