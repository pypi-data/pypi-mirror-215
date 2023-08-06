<!-- SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in> -->
<!-- SPDX-License-Identifier: CC0-1.0 -->

gentle
======

[![Build Status](https://drone.tildegit.org/api/badges/CyberTaIlor/gentle/status.svg)](https://drone.tildegit.org/CyberTaIlor/gentle)

**Gent**oo **L**azy **E**ntry — a `metadata.xml` generator.


Supported generators
--------------------

* [Bower](https://github.com/bower/spec/blob/master/json.md)
* Crystal ([Shards](https://github.com/crystal-lang/shards/blob/master/docs/shard.yml.adoc))
* Node.js ([npm](https://docs.npmjs.com/files/package.json/))
* Python ([PEP 621](https://peps.python.org/pep-0621/))
* Rust ([Cargo](https://doc.rust-lang.org/cargo/reference/manifest.html))


Dependencies
------------

* [Portage](https://pypi.org/project/portage/)
* [PyYAML](https://pyyaml.org/) *(optional)*
* [Tomli](https://pypi.org/project/tomli/) *(optional)*


Installing
----------

### Gentoo

```sh
eselect repository enable guru
emerge app-portage/gentle
```

### Other systems

`pip install gentle-mxml --user`


Packaging
---------

You can track new releases using an [atom feed][atom] provided by GitHub.

[atom]: https://github.com/cybertailor/gentle/releases.atom


Contributing
------------

Patches and pull requests are welcome. Please use either [git-send-email(1)][1]
or [git-request-pull(1)][2], addressed to <cyber@sysrq.in>.

Your commit message should conform to the following standard:

```
file/changed: Concice and complete statement of the purpose

This is the body of the commit message.  The line above is the
summary.  The summary should be no more than 72 chars long.  The
body can be more freely formatted, but make it look nice.  Make
sure to reference any bug reports and other contributors.  Make
sure the correct authorship appears.
```

[1]: https://git-send-email.io/
[2]: https://git-scm.com/docs/git-request-pull


License
-------

WTFPL
