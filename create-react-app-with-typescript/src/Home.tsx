import { Grid, makeStyles } from "@material-ui/core";
import { useHistory } from "react-router";
import DeptCard from "./DeptCard";

const useStyles = makeStyles((theme) => ({
    content: {
        flexGrow: 1,
        backgroundColor: theme.palette.background.default,
        padding: theme.spacing(3),
        marginTop: 64,
    },
}));

export default function Home() {
    const classes = useStyles();
    const history = useHistory();

    const handleClickAdmin = () => history.push("/admin");
    return (
        <>
            <main className={classes.content}>
                <Grid container spacing={2}>
                    <Grid item sm={12} md={6} lg={4}>
                        <DeptCard
                            name="Sales"
                            image="sales.jpg"
                            description="Internal tools for the sales department such as lead
                        management, sales target setting and analysis, and more."
                        />
                    </Grid>

                    <Grid item sm={12} md={6} lg={4}>
                        <DeptCard
                            name="Marketing"
                            image="marketing.jpg"
                            description="Manage advertisement budget, branding and logos, track app usage analytics for lead generation."
                        />
                    </Grid>
                    <Grid item sm={12} md={6} lg={4}>
                        <DeptCard
                            name="Finance"
                            image="finance.jpg"
                            description="Track company spending, assign individual staff allowances, and generate quarterly finance reports."
                        />
                    </Grid>
                    <Grid item sm={12} md={6} lg={4}>
                        <DeptCard
                            name="Admin"
                            image="admin.jpg"
                            description="Manage company users and roles, check overall system integrity and view system analytics, and send out company policies."
                            onClick={handleClickAdmin}
                        />
                    </Grid>
                </Grid>
            </main>
        </>
    );
}
