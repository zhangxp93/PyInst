def _get_version() -> str:

    from importlib.resources import files
    from pathlib import Path

    import versioningit

    module_path = files("pyinst")
    if isinstance(module_path, Path):
        return versioningit.get_version(project_dir=Path(module_path).parent.parent)
    else:
        return "0.0"


__version__ = "0.0.3"
