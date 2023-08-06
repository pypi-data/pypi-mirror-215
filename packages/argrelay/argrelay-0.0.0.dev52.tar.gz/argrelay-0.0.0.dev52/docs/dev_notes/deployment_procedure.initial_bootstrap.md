
TODO: Content of this file is obsolete due to FS_85_33_46_53 `bootstrap_dev_env.bash`. To be updated.

# Initial `argrelay` boostrap

It is assumed the project integrating with `argrelay` has Python already configured (e.g. via `venv`).

To upgrade package:

```sh
pip install argrelay
```

Find `bootstrap_dev_env.bash` script, for example:

```sh
find . -name 'bootstrap_dev_env.bash'
```

```
./venv/lib/python3.10/site-packages/argrelay/custom_integ_res/bootstrap_dev_env.bash
```

Run it to deploy necessary artifacts from `@/` integration project root dir<br/>
(it creates necessary artifacts relative to the dir where it is called from, not where it resides):

```sh
./venv/lib/python3.10/site-packages/argrelay/custom_integ_res/bootstrap_dev_env.bash
```

Depending on current state of config files, it may prompt for more info - follow the instructions.

Eventually, it will deploy:

*   Helper scripts relative to the **current directory**.

*   Copy of itself into `@/exe/bootstrap_dev_env.bash` to be version controlled together with the integration project.

One of the deployed script is `@/exe/dev_shell.bash` -
it should work the same way as the demo in the main [readme.md][root_readme.md].

See [deployment_procedure.subsequent_upgrade.md][deployment_procedure.subsequent_upgrade.md]
for subsequent `argrelay` version upgrades via re-run of `@/exe/bootstrap_dev_env.bash` script.

[root_readme.md]: ../../readme.md
[deployment_procedure.subsequent_upgrade.md]: deployment_procedure.subsequent_upgrade.md
