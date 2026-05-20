import json
from pathlib import Path

from cli_anything.joplin.utils.joplin_backend import BackendConfig, find_joplin, run_joplin_command, run_joplin_json


def version_info(config: BackendConfig) -> dict:
    try:
        return run_joplin_command(["version"], config)
    except RuntimeError as exc:
        # Joplin 3.6.2's installed `command-version.js` may require
        # `../package.json`, which is missing in npm -g layouts. Fall back to
        # the package metadata next to the installed CLI.
        if "package.json" not in str(exc):
            raise

        binary = Path(find_joplin(config.binary))
        package_json = binary.parent / "node_modules" / "joplin" / "package.json"
        if not package_json.exists():
            raise
        metadata = json.loads(package_json.read_text(encoding="utf-8"))
        return {
            "command": [str(binary), "version"],
            "returncode": 0,
            "stdout": metadata.get("version", ""),
            "stderr": f"Fallback after broken Joplin version command: {exc}",
            "metadata": {
                "name": metadata.get("name"),
                "version": metadata.get("version"),
                "description": metadata.get("description"),
            },
        }


def dump_database(config: BackendConfig) -> dict:
    return run_joplin_json(["dump"], config, timeout=600)


def keymap(config: BackendConfig) -> dict:
    return run_joplin_command(["keymap"], config)


def geoloc(config: BackendConfig, note_ref: str) -> dict:
    return run_joplin_command(["geoloc", note_ref], config)


def export_sync_status(config: BackendConfig) -> dict:
    return run_joplin_command(["export-sync-status"], config, timeout=300)


def server_status(config: BackendConfig) -> dict:
    return run_joplin_command(["server", "status"], config)


def server_start(config: BackendConfig, exit_early: bool = True, quiet: bool = False) -> dict:
    args = ["server", "start"]
    if exit_early:
        args.append("--exit-early")
    if quiet:
        args.append("--quiet")
    return run_joplin_command(args, config, timeout=300)


def server_stop(config: BackendConfig) -> dict:
    return run_joplin_command(["server", "stop"], config)


def e2ee_status(config: BackendConfig) -> dict:
    return run_joplin_command(["e2ee", "status"], config)


def e2ee_target_status(config: BackendConfig, target_path: str, verbose: bool = False) -> dict:
    args = ["e2ee", "target-status", target_path]
    if verbose:
        args.append("--verbose")
    return run_joplin_command(args, config, timeout=300)


def e2ee_decrypt(
    config: BackendConfig,
    encrypted_text: str | None = None,
    retry_failed_items: bool = False,
    force: bool = False,
) -> dict:
    args = ["e2ee", "decrypt"]
    if encrypted_text:
        args.append(encrypted_text)
    if retry_failed_items:
        args.append("--retry-failed-items")
    if force:
        args.append("--force")
    return run_joplin_command(args, config, timeout=600)


def e2ee_decrypt_file(config: BackendConfig, file_path: str, output_dir: str | None = None) -> dict:
    args = ["e2ee", "decrypt-file", file_path]
    if output_dir:
        args += ["--output", output_dir]
    return run_joplin_command(args, config, timeout=600)
