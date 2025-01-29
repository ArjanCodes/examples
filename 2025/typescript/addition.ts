function add(a: number, b: number): number {
	return a + b;
}

console.log(add(5, 10)); // Compiles fine
console.log(add("5", "10")); // Compilation error
console.log(add("5", 10)); // Compilation error