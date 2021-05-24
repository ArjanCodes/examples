import {
    Card,
    CardActionArea,
    CardContent,
    CardMedia,
    makeStyles,
    Typography,
} from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
    media: {
        height: 100,
    },
}));

export interface DeptCardProps {
    name: string;
    image: string;
    description: string;
    onClick?: () => void;
}

export default function DeptCard(props: DeptCardProps) {
    const { name, image, description, onClick } = props;
    const classes = useStyles();
    return (
        <Card>
            <CardActionArea onClick={onClick}>
                <CardMedia className={classes.media} image={image} />
                <CardContent>
                    <Typography gutterBottom variant="h5" component="h2">
                        {name}
                    </Typography>
                    <Typography
                        variant="body2"
                        color="textSecondary"
                        component="p"
                    >
                        {description}
                    </Typography>
                </CardContent>
            </CardActionArea>
        </Card>
    );
}
