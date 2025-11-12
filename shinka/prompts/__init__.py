# __init__.py (in your current package)
import os
import sys
import types
import importlib
import importlib.util
import pkgutil
from pathlib import Path

# Name of the env var pointing to the directory that contains the external package
ENV_VAR = "SHINKA_PROMPT_ROOT"   # set this to an absolute path to the package folder
# Optional: a stable name under which we'll register the external package in sys.modules
ENV_PKG_ALIAS = "_env_prompts"

def _load_external_package(pkg_dir: str, alias: str) -> types.ModuleType:
    """
    Load a package from a filesystem path that has an __init__.py, register it
    under `alias` in sys.modules, and return the loaded package module.
    """
    pkg_dir = str(Path(pkg_dir).resolve())
    init_file = str(Path(pkg_dir) / "__init__.py")

    spec = importlib.util.spec_from_file_location(
        alias,
        init_file,
        submodule_search_locations=[pkg_dir],  # <-- crucial so Python treats it as a package
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create import spec for package at {pkg_dir}")

    mod = importlib.util.module_from_spec(spec)
    sys.modules[alias] = mod
    spec.loader.exec_module(mod)  # executes the package's __init__.py
    return mod

def _import_submodules_into_current_ns(pkg_alias: str, pkg_dir: str):
    """
    Import every top-level submodule/package under pkg_dir and expose them
    in *this* package's namespace (so `from mypkg import prompts_full` works).
    """
    for finder, name, ispkg in pkgutil.iter_modules([pkg_dir]):
        fqname = f"{pkg_alias}.{name}"
        submod = importlib.import_module(fqname)
        globals()[name] = submod  # expose as sibling here
        __all__.append(name)      # re-export

def _export_public_symbols(src_mod: types.ModuleType):
    """
    Copy public objects from the external package into *this* package's namespace,
    respecting __all__ if present, otherwise non-underscore names.
    """
    public_names = getattr(src_mod, "__all__", None)
    if public_names is None:
        public_names = [k for k in vars(src_mod).keys() if not k.startswith("_")]

    for name in public_names:
        globals()[name] = getattr(src_mod, name)
    __all__.extend(public_names)

# Start with a default __all__ so we can append safely
__all__ = []

# Try to load from env path; fallback to local modules if not set/available
_env_path = os.getenv(ENV_VAR)
if _env_path:
    try:
        pkg = _load_external_package(_env_path, ENV_PKG_ALIAS)
        _export_public_symbols(pkg)
        _import_submodules_into_current_ns(ENV_PKG_ALIAS, _env_path)
        print("Loaded external package", ENV_PKG_ALIAS)
    except Exception as e:
        # Fallback to built-in/local prompts if external load fails
        # (You may want to log/raise depending on your tolerance.)
        # print(f"[prompts] External load failed: {e}")
        _env_path = None
        raise e

if not _env_path:
    # --- Local fallback: import your existing modules and re-export exactly as before ---
    from .prompts_base import (
        construct_eval_history_msg,
        construct_individual_program_msg,
        perf_str,
        format_text_feedback_section,
        BASE_SYSTEM_MSG,
    )
    from .prompts_diff import DIFF_SYS_FORMAT, DIFF_ITER_MSG
    from .prompts_full import (
        FULL_SYS_FORMAT_DEFAULT,
        FULL_ITER_MSG,
        FULL_SYS_FORMATS,
    )
    from .prompts_cross import (
        CROSS_SYS_FORMAT,
        CROSS_ITER_MSG,
        get_cross_component,
    )
    from .prompts_init import INIT_SYSTEM_MSG, INIT_USER_MSG
    from .prompts_meta import (
        META_STEP1_SYSTEM_MSG,
        META_STEP1_USER_MSG,
        META_STEP2_SYSTEM_MSG,
        META_STEP2_USER_MSG,
        META_STEP3_SYSTEM_MSG,
        META_STEP3_USER_MSG,
    )
    from .prompts_novelty import NOVELTY_SYSTEM_MSG, NOVELTY_USER_MSG

    __all__ = [
        "construct_eval_history_msg",
        "construct_individual_program_msg",
        "perf_str",
        "format_text_feedback_section",
        "BASE_SYSTEM_MSG",
        "DIFF_SYS_FORMAT",
        "DIFF_ITER_MSG",
        "FULL_SYS_FORMAT_DEFAULT",
        "FULL_SYS_FORMATS",
        "FULL_ITER_MSG",
        "CROSS_SYS_FORMAT",
        "CROSS_ITER_MSG",
        "get_cross_component",
        "INIT_SYSTEM_MSG",
        "INIT_USER_MSG",
        "META_STEP1_SYSTEM_MSG",
        "META_STEP1_USER_MSG",
        "META_STEP2_SYSTEM_MSG",
        "META_STEP2_USER_MSG",
        "META_STEP3_SYSTEM_MSG",
        "META_STEP3_USER_MSG",
        "NOVELTY_SYSTEM_MSG",
        "NOVELTY_USER_MSG",
    ]
