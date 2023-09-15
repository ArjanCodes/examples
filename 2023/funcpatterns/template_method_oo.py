from abc import ABC, abstractmethod


class Template(ABC):
    def template_method(self) -> None:
        self.base_operation1()
        self.required_operations1()
        self.base_operation2()
        if self.hook1():
            self.base_operation3()
        self.hook2()
        self.required_operations2()

    # These operations already have implementations.
    def base_operation1(self) -> None:
        print("Base operation1")

    def base_operation2(self) -> None:
        print("Base operation2")

    def base_operation3(self) -> None:
        print("Base operation3")

    # These operations have to be implemented in subclasses.
    @abstractmethod
    def required_operations1(self) -> None:
        pass

    @abstractmethod
    def required_operations2(self) -> None:
        pass

    # These are "hooks." Subclasses may override them, but it's not mandatory since the hooks already have default (but empty) implementation.
    def hook1(self) -> bool:
        return True

    def hook2(self) -> None:
        pass


class ConcreteClass1(Template):
    def required_operations1(self) -> None:
        print("ConcreteClass1 says: Required operation1")

    def required_operations2(self) -> None:
        print("ConcreteClass1 says: Required operation2")

    def hook2(self) -> None:
        print("ConcreteClass1 says: Hook2")


class ConcreteClass2(Template):
    def required_operations1(self) -> None:
        print("ConcreteClass2 says: Required operation1")

    def required_operations2(self) -> None:
        print("ConcreteClass2 says: Required operation2")

    def hook1(self) -> bool:
        print("ConcreteClass2 says: Hook1")
        return False


def main() -> None:
    concrete_class_1 = ConcreteClass1()
    concrete_class_1.template_method()

    concrete_class_2 = ConcreteClass2()
    concrete_class_2.template_method()


if __name__ == "__main__":
    main()
