function printInput(input: string | number): void {
    if (typeof input === "string") {
        console.log("String:", input);
    } else {
        console.log("Number:", input);
    }
}