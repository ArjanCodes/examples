import {
    Box,
    Button,
    FormControlLabel,
    makeStyles,
    Switch,
} from "@material-ui/core";
import { DataGrid, GridRowId } from "@material-ui/data-grid";
import AddIcon from "@material-ui/icons/Add";
import SendIcon from "@material-ui/icons/Send";
import * as React from "react";

const columns = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "firstName", headerName: "First name", width: 130 },
    { field: "lastName", headerName: "Last name", width: 130 },
    {
        field: "age",
        headerName: "Age",
        type: "number",
        width: 90,
    },
    {
        field: "fullName",
        headerName: "Full name",
        description: "This column has a value getter and is not sortable.",
        sortable: false,
        width: 160,
        valueGetter: (params: any) =>
            `${params.getValue("firstName") || ""} ${
                params.getValue("lastName") || ""
            }`,
    },
];

const rows = [
    { id: 1, lastName: "Snow", firstName: "Jon", age: 35 },
    { id: 2, lastName: "Lannister", firstName: "Cersei", age: 42 },
    { id: 3, lastName: "Lannister", firstName: "Jaime", age: 45 },
    { id: 4, lastName: "Stark", firstName: "Arya", age: 16 },
    { id: 5, lastName: "Targaryen", firstName: "Daenerys", age: null },
    { id: 6, lastName: "Melisandre", firstName: null, age: 150 },
    { id: 7, lastName: "Clifford", firstName: "Ferrara", age: 44 },
    { id: 8, lastName: "Frances", firstName: "Rossini", age: 36 },
    { id: 9, lastName: "Roxie", firstName: "Harvey", age: 65 },
];

const useStyles = makeStyles((theme) => ({
    emailButton: {
        marginLeft: theme.spacing(1),
    },
}));

export default function UserTable() {
    const [selectionModel, setSelectionModel] = React.useState<GridRowId[]>([]);
    const classes = useStyles();
    return (
        <>
            <Box>
                <FormControlLabel
                    control={<Switch color="primary" />}
                    label="Show only system administrators"
                />
            </Box>
            <div style={{ height: 370, width: "100%" }}>
                <DataGrid
                    rows={rows}
                    columns={columns}
                    pageSize={5}
                    checkboxSelection
                    onSelectionModelChange={(newSelection) => {
                        console.log(newSelection.selectionModel);
                        setSelectionModel(newSelection.selectionModel);
                    }}
                    selectionModel={selectionModel}
                />
            </div>

            <Box textAlign="right" mt={1}>
                <Button
                    variant="contained"
                    color="primary"
                    startIcon={<AddIcon />}
                >
                    Add users
                </Button>
                {selectionModel.length > 0 && (
                    <Button
                        variant="contained"
                        color="primary"
                        className={classes.emailButton}
                        startIcon={<SendIcon />}
                    >
                        Send email to users
                    </Button>
                )}
            </Box>
        </>
    );
}
