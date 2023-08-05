from argparse import ArgumentParser
from pathlib import Path


BASE_FILES = Path(__file__).resolve().parents[0] / Path("../base_files")


def build_dir(d: Path):
    print(f"Creating {d}")
    d.mkdir(parents=True, exist_ok=True)


def write_base_file(in_file: Path, out_file: Path, **kwargs):
    """

    :param in_file: Input txt file
    :param out_file: Output file
    :param kwargs: params to fill
    :return: Nada
    """
    print(f"Writing {in_file} to {out_file}")
    with open(in_file, 'r') as i:
        s = i.read()
    for key, value in kwargs.items():
        s = s.replace(f"<{key}>", value)
    with open(out_file, 'w') as o:
        o.write(s)


def write_file(out_file: Path, contents: str):
    print(f"Writing {out_file}")
    with open(out_file, "w") as o:
        o.write(contents)


def main(project_directory: Path, python_pkg_name: str):
    """
    Build an app at the given location.

    :param project_directory:
    :param python_pkg_name: valid Python package name
    :return:
    """
    # Create the project_directory if DNE
    build_dir(project_directory)

    # Create tests directory
    build_dir(project_directory / "tests")

    # Create FastAPI app directory and contents
    app_dir = project_directory / "app"
    build_dir(app_dir)
    write_base_file(in_file=BASE_FILES / "app.main.txt",
                    out_file=app_dir / "main.py")
    write_base_file(in_file=BASE_FILES / "app.run.txt",
                    out_file=app_dir / "run.py",
                    PKG_NAME=python_pkg_name)
    write_file(out_file=app_dir / "__init__.py", contents="")

    # Create src directory and contents
    src_dir = project_directory / "src"
    pkg_dir = src_dir / python_pkg_name
    build_dir(pkg_dir)
    write_base_file(in_file=BASE_FILES / "pkg.__init__.txt",
                    out_file=pkg_dir / "__init__.py")
    write_base_file(in_file=BASE_FILES / "pkg.config.txt",
                    out_file=pkg_dir / "config.py")
    postgres_dir = pkg_dir / "postgres"
    build_dir(postgres_dir)
    write_file(out_file=postgres_dir / "__init__.py", contents="")
    write_base_file(in_file=BASE_FILES / "pkg.postgres.orm.txt",
                    out_file=postgres_dir / "orm.py")
    write_base_file(in_file=BASE_FILES / "pkg.postgres.postgres_client.txt",
                    out_file=postgres_dir / "postgres_client.py",
                    PKG_NAME=python_pkg_name)

    # Write .env
    write_base_file(in_file=BASE_FILES / "env.txt",
                    out_file=project_directory / ".env")

    # Write Docker stuff
    write_base_file(in_file=BASE_FILES / "build-docker.txt",
                    out_file=project_directory / "build-docker.sh",
                    PKG_NAME=python_pkg_name)
    write_base_file(in_file=BASE_FILES / "Dockerfile.txt",
                    out_file=project_directory / "Dockerfile",
                    PKG_NAME=python_pkg_name)

    # Write requirements
    write_base_file(in_file=BASE_FILES / "requirements.txt",
                    out_file=project_directory / "requirements.txt")


if __name__ == "__main__":
    arg_parser = ArgumentParser(description="Postgres with FastAPI boilerplate")
    arg_parser.add_argument("project_directory", type=Path)
    arg_parser.add_argument("python_pkg_name", type=str)
    args = arg_parser.parse_args()

    main(project_directory=args.project_directory,
         python_pkg_name=args.python_pkg_name)
