type HasName = {
    name: string;
};

type HasAge = {
    age: number;
};

type Person = HasName & HasAge; // Intersection type

const person: Person = {
    name: "Arjan",
    age: 35,
};

console.log(`${person.name} is ${person.age} years old.`);