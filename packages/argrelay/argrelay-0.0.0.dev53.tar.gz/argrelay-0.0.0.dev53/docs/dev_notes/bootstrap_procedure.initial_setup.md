
This procedure describes using [`FS_85_33_46_53.bootstrap_dev_env.md`][FS_85_33_46_53.bootstrap_dev_env.md] feature
to create new `argrelay`-based project from scratch.

If the project already exists, see [`bootstrap_procedure.subsequent_upgrade.md`][bootstrap_procedure.subsequent_upgrade.md] instead.

# Initial `argrelay` setup

Obtain (copy and paste or download) [`bootstrap_dev_env.bash`][bootstrap_dev_env.bash] into temporary path,<br/>
for example, `/tmp/bootstrap_dev_env.bash`.

Then, run it **from the project root directory**:
*   The project root dir is referred to as `@/` - see [`FS_29_54_67_86.dir_structure.md`][FS_29_54_67_86.dir_structure.md].
*   The project root dir is not necessarily Git repo root dir - it might be any sub-directory.

```sh
cd path/to/project/dir
bash /tmp/bootstrap_dev_env.bash
```

Keep re-running it addressing the issues until it succeeds (until it exits with code 0).

# What might bootstrap need?

If it is a new `argrelay`-based project created from scratch,<br/>
bootstrap will fail (exits with code other than 0) due to many missing files and dirs.

Normally, it is clear from the output what is the reason for the failure.

This is a non-exhaustive list of reasons and clues how to address them:

*   Missing `@/exe` dir.

    Bootstrap expects specific directory structure (see [`FS_29_54_67_86.dir_structure.md`][FS_29_54_67_86.dir_structure.md])
    and checks at least existence of `@/exe` dir.

    If it is correct directory (where new project is being created from scratch), simply create `@/exe` dir.

*   Missing `@/bin` dir.

    Create it - again, see also [`FS_29_54_67_86.dir_structure.md`][FS_29_54_67_86.dir_structure.md].

*   Missing `@/conf/python_conf.bash` file.

    This file provides config for Python interpreter and creation of Python virtual environment.

    If missing, bootstrap prints initial copy-and-paste-able content of this file.

*   Missing `@/exe/deploy_project.bash` file.

    This file is project-specific custom script to deploy project packages into Python venv.

    If missing, bootstrap prints initial copy-and-paste-able content of this file.

*   Missing `setup.py` file.

    This is expected by template version of `@/exe/deploy_project.bash` file.

    If missing, either create minimal `setup.py` or modify `@/exe/deploy_project.bash`.

*   Missing `argrelay` package.

    To generate client and server executables, bootstrap needs installed `argrelay` package
    in the venv (as configured in `@/conf/python_conf.bash`) used by the bootstrap process.

    In turn, `@/exe/deploy_project.bash` script should deploy `argrelay` (directly or indirectly via dependencies).

    *   Long-term fix is to ensure `@/exe/deploy_project.bash` installs `argrelay`.
    *   Short-term fix is to activate the same venv (as configured in `@/conf/python_conf.bash`) and install `argrelay` manually.

*   Other missing files.

    This could be:

    *   `@/exe/deploy_config_files_conf.bash`
    *   `@/exe/deploy_resource_files_conf.bash`
    *   `@/exe/build_project.bash`
    *   ...

    When missing, bootstrap prints initial copy-and-paste-able content for these files.

# When bootstrap succeeds

Eventually, it will also make a copy of itself into `@/exe/bootstrap_dev_env.bash` which should be version-controlled.

For any subsequent upgrade, see [`bootstrap_procedure.subsequent_upgrade.md`][bootstrap_procedure.subsequent_upgrade.md].

To see how it works, try [`FS_58_61_77_69.dev_shell.md`][FS_58_61_77_69.dev_shell.md].

[bootstrap_procedure.subsequent_upgrade.md]: bootstrap_procedure.subsequent_upgrade.md
[FS_85_33_46_53.bootstrap_dev_env.md]: ../feature_stories/FS_85_33_46_53.bootstrap_dev_env.md
[FS_29_54_67_86.dir_structure.md]: ../feature_stories/FS_29_54_67_86.dir_structure.md
[FS_58_61_77_69.dev_shell.md]: ../feature_stories/FS_58_61_77_69.dev_shell.md
[bootstrap_dev_env.bash]: ../../exe/bootstrap_dev_env.bash
[root_readme.md]: ../../readme.md
