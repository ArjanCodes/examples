import pathlib
from os import chdir


def main() -> None:
    # current working directory and home directory
    cwd = pathlib.Path.cwd()
    home = pathlib.Path.home()
    print(f"Current working directory: {cwd}")
    print(f"Home directory: {home}")

    # creating paths
    path = pathlib.Path("/usr/bin/python3")

    # using backslashes on Windows
    path = pathlib.Path(r"C:\Windows\System32\cmd.exe")

    # using forward slash operator
    path = pathlib.Path("/usr") / "bin" / "python3"

    # using joinpath
    path = pathlib.Path("/usr").joinpath("bin", "python3")

    # reading a file from a path
    path = pathlib.Path().cwd() / "settings.yaml"
    with path.open() as file:
        print(file.read())

    # reading a file from a path using read_text
    print(path.read_text())

    # resolving a path
    path = pathlib.Path("settings.yaml")
    print(path)
    full_path = path.resolve()
    print(full_path)

    # path member variables
    print(f"Path: {full_path}")
    print(f"Parent: {full_path.parent}")
    print(f"Grandparent: {full_path.parent.parent}")
    print(f"Name: {full_path.name}")
    print(f"Stem: {full_path.stem}")
    print(f"Suffix: {full_path.suffix}")

    # testing whether a path is a directory or a file
    print(f"Is directory: {full_path.is_dir()}")
    print(f"Is file: {full_path.is_file()}")

    # testing whether a path exists
    print(f"Full path exists: {full_path.exists()}")
    wrong_path = pathlib.Path("/usr/does/not/exist")
    print(f"Wrong path exists: {wrong_path.exists()}")

    # creating a directory
    new_dir = pathlib.Path().cwd() / "new_dir"
    new_dir.mkdir()

    # changing to the new directory
    chdir(new_dir)
    print(f"Current working directory: {pathlib.Path.cwd()}")


if __name__ == "__main__":
    main()
