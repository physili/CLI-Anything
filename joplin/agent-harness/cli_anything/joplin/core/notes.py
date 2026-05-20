from cli_anything.joplin.utils.joplin_backend import BackendConfig, run_joplin_command, run_joplin_json


def list_notes(
    config: BackendConfig,
    pattern: str | None = None,
    limit: int | None = None,
    sort: str | None = None,
    reverse: bool = False,
    item_type: str | None = None,
    long: bool = False,
) -> dict:
    args = ["ls"]
    if pattern:
        args.append(pattern)
    if limit:
        args += ["-n", str(limit)]
    if sort:
        args += ["--sort", sort]
    if reverse:
        args.append("--reverse")
    if item_type:
        args += ["--type", item_type]
    if long:
        args.append("--long")
    args += ["--format", "json"]
    return run_joplin_json(args, config)


def create_note(config: BackendConfig, title: str) -> dict:
    return run_joplin_command(["mknote", title], config)


def set_note_field(config: BackendConfig, note_ref: str, field: str, value: str) -> dict:
    return run_joplin_command(["set", note_ref, field, value], config)


def get_note(config: BackendConfig, note_ref: str, verbose: bool = False) -> dict:
    args = ["cat", note_ref]
    if verbose:
        args.append("-v")
    return run_joplin_command(args, config)


def remove_note(config: BackendConfig, note_ref: str, force: bool = True, permanent: bool = False) -> dict:
    args = ["rmnote", note_ref]
    if force:
        args.append("-f")
    if permanent:
        args.append("-p")
    return run_joplin_command(args, config)


def copy_note(config: BackendConfig, note_ref: str, notebook: str | None = None) -> dict:
    args = ["cp", note_ref]
    if notebook:
        args.append(notebook)
    return run_joplin_command(args, config)


def move_note(config: BackendConfig, item: str, notebook: str) -> dict:
    return run_joplin_command(["mv", item, notebook], config)


def rename_note(config: BackendConfig, item: str, new_name: str) -> dict:
    return run_joplin_command(["ren", item, new_name], config)


def duplicate_note(config: BackendConfig, note_ref: str, notebook: str | None = None) -> dict:
    return copy_note(config, note_ref, notebook=notebook)
