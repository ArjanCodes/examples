import {
    Box,
    Button,
    FormControl,
    InputLabel,
    MenuItem,
    Select,
    TextField,
} from "@material-ui/core";
import SendIcon from "@material-ui/icons/Send";
import { useState } from "react";

export default function PolicySettings() {
    const [policy, setPolicy] = useState<string>("ict");
    const [emailAddress, setEmailAddress] = useState("");

    const handleChangePolicy = (
        event: React.ChangeEvent<{ value: unknown }>
    ) => {
        setPolicy(`${event.target.value}`);
    };

    const handleChangeEmailAddress = (
        event: React.ChangeEvent<{ value: unknown }>
    ) => {
        setEmailAddress(`${event.target.value}`);
    };

    const handleClickSendPolicy = () => {
        if (emailAddress === "") {
            alert("Error! Please provide an email address");
        }
    };

    return (
        <>
            <Box display="flex" flexDirection="row" alignItems="center">
                <FormControl
                    variant="outlined"
                    style={{ minWidth: 150, marginRight: 8 }}
                >
                    <InputLabel>Policy type</InputLabel>
                    <Select
                        value={policy}
                        onChange={handleChangePolicy}
                        label="Policy type"
                    >
                        <MenuItem value="holidays">Holidays</MenuItem>
                        <MenuItem value="ict">ICT services</MenuItem>
                        <MenuItem value="salary">Salary</MenuItem>
                        <MenuItem value="printing">Printing</MenuItem>
                        <MenuItem value="office">Office</MenuItem>
                        <MenuItem value="declarations">Declarations</MenuItem>
                    </Select>
                </FormControl>
                <TextField
                    variant="outlined"
                    label="User email address"
                    style={{ flexGrow: 1 }}
                    value={emailAddress}
                    onChange={handleChangeEmailAddress}
                />
            </Box>
            <Box>
                <Button
                    onClick={handleClickSendPolicy}
                    variant="contained"
                    color="secondary"
                    startIcon={<SendIcon />}
                    style={{ marginTop: 8 }}
                >
                    Send policy info
                </Button>
            </Box>
        </>
    );
}
