function processData(data: string): string {
	return data.toLowerCase();
}

console.log(processData("Hello")); // Works
console.log(processData(123)); // Compilation error