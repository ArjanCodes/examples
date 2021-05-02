import {
    IconButton,
    ListItemIcon,
    ListItemText,
    Menu,
    MenuItem,
} from "@material-ui/core";
import FileCopyIcon from "@material-ui/icons/FileCopy";
import FileDownloadIcon from "@material-ui/icons/GetApp";
import MoreVertIcon from "@material-ui/icons/MoreVert";
import FileUploadIcon from "@material-ui/icons/Publish";
import SettingsIcon from "@material-ui/icons/Settings";
import { useState } from "react";

export default function BasicMenu() {
    const [anchorEl, setAnchorEl] = useState(null);
    const open = Boolean(anchorEl);

    const handleClick = (event: any) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };
    return (
        <>
            <IconButton onClick={handleClick}>
                <MoreVertIcon />
            </IconButton>
            <Menu
                id="long-menu"
                anchorEl={anchorEl}
                keepMounted
                open={open}
                onClose={handleClose}
            >
                <MenuItem onClick={handleClose}>
                    <ListItemIcon>
                        <FileCopyIcon />
                    </ListItemIcon>
                    <ListItemText primary="Share invite code" />
                </MenuItem>
                <MenuItem onClick={handleClose}>
                    <ListItemIcon>
                        <FileUploadIcon />
                    </ListItemIcon>
                    <ListItemText primary="Import user data" />
                </MenuItem>
                <MenuItem onClick={handleClose}>
                    <ListItemIcon>
                        <FileDownloadIcon />
                    </ListItemIcon>
                    <ListItemText primary="Export user data" />
                </MenuItem>
                <MenuItem onClick={handleClose}>
                    <ListItemIcon>
                        <SettingsIcon />
                    </ListItemIcon>
                    <ListItemText primary="Settings" />
                </MenuItem>
            </Menu>
        </>
    );
}
