class Config:
    _instance = None

    def __init__(self):
        self.db_url = "sqlite:///:memory:"
        self.debug = True

    def __new__(cls):
        if cls._instance is None:
            print("Creating new instance")
            cls._instance = super().__new__(cls)
        return cls._instance
    
def main():
    s1 = Config()
    s2 = Config()

    print(s1 is s2)
    print(id(s1))
    print(id(s2))

if __name__ == "__main__":
    main()