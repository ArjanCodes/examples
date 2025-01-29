interface Vehicle {
    speed: number;
    drive(): void;
}

class Car implements Vehicle {
    constructor(public speed: number) {}

    drive(): void {
        console.log(`Driving at ${this.speed} km/h`);
    }
}

const myCar: Vehicle = new Car(120);
myCar.drive(); // ✅ Works fine

const randomObject = { speed: 100, drive: () => console.log("Zoom!") };
const anotherCar: Vehicle = randomObject; // ✅ Also works because it matches the interface