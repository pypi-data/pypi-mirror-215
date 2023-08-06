
TODO: Content of this file is obsolete due to FS_85_33_46_53 `bootstrap_dev_env.bash`. To be updated.

# Subsequent `argrelay` upgrade

Run `@/exe/dev_shell.bash` to activate `venv`:

```sh
./exe/dev_shell.bash
```

Upgrade `argrelay` package to newer version:

```sh
pip install --upgrade --force-reinstall argrelay
```

Re-run `@/exe/bootstrap_dev_env.bash`:

``sh
./exe/bootstrap_dev_env.bash
``

Most of the details specific to custom project come with customization (using custom plugins)<br/>
which may require setting up additional dependencies - see `plugin_development.md`.

To run real Mongo DB (instead of `mongomock`), see also `mongo_notes.md`.

[root_readme.md]: ../../readme.md
