import os


def create_toml_string(name: str, startpath: str, packages: list[str]) -> str:
    result = ""
    result += f'name = "{name}"'
    result += "\n\npackages = ["
    for idx, package in enumerate(packages):
        line = f'\n\t"{package}"' + ("," if idx < len(packages) - 1 else "")
        result += line
    result += "\n]"
    result += "\n\n[files]\n"
    for root, dirs, files in os.walk(startpath):
        if "__pycache__" in dirs:
            dirs.remove("__pycache__")
        for file in files:
            file_path = f"./{root.replace('\\', '/')}/{file}"
            result += f'"{file_path}" = "{file_path}"\n'
    return result


def save_toml_file(name: str, startpath: str, packages: list[str]) -> None:
    content = create_toml_string(name, startpath, packages)
    with open("pyscript.toml", "w") as f:
        f.write(content)


if __name__ == "__main__":
    save_toml_file(
        name="Datastream Defender",
        startpath="src",
        packages=["zengl", "pygame-ce", "numpy", "webwindow"],
    )
