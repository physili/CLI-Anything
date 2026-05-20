from cli_anything.joplin.utils.joplin_backend import BackendConfig, run_joplin_command, run_joplin_json


def list_notebooks(
    config: BackendConfig,
    limit: int | None = None,
    sort: str | None = None,
    reverse: bool = False,
    long: bool = False,
) -> dict:
    args = ["ls", "/", "--format", "json"]
    if limit:
        args += ["--limit", str(limit)]
    if sort:
        args += ["--sort", sort]
    if reverse:
        args.append("--reverse")
    if long:
        args.append("--long")
    return run_joplin_json(args, config)


def create_notebook(config: BackendConfig, title: str, parent: str | None = None) -> dict:
    args = ["mkbook", title]
    if parent:
        args += ["-p", parent]
    return run_joplin_command(args, config)


def use_notebook(config: BackendConfig, notebook: str) -> dict:
    return run_joplin_command(["use", notebook], config)


def remove_notebook(config: BackendConfig, notebook: str, force: bool = True, permanent: bool = False) -> dict:
    args = ["rmbook", notebook]
    if force:
        args.append("-f")
    if permanent:
        args.append("-p")
    return run_joplin_command(args, config)
