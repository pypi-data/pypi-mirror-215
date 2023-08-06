# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2022-2023 Anna <cyber@sysrq.in>
# No warranty

import argparse
import logging
import os
import re
from pathlib import Path
from tempfile import TemporaryDirectory

import gentle
from gentle.generators import AbstractGenerator, GeneratorClass
from gentle.metadata import MetadataXML

import gentle.generators.bower
import gentle.generators.cargo
import gentle.generators.composer
import gentle.generators.doap
import gentle.generators.hpack
import gentle.generators.npm
import gentle.generators.pkg_info
import gentle.generators.pyproject
import gentle.generators.shards

try:
    import portage
    from portage.package.ebuild.doebuild import doebuild
except ModuleNotFoundError:
    _HAS_PORTAGE = False
else:
    _HAS_PORTAGE = True

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")


def portage_src_unpack(ebuild: Path, tmpdir: str) -> Path:
    """
    Unpack the sources using Portage.

    :param ebuild: path to the ebuild file
    :param tmpdir: temporary directory
    :return: the value of ``${S}``
    """
    ebuild = ebuild.resolve()
    portdir = str(ebuild.parents[2])

    # pylint: disable=protected-access
    if portdir not in portage.portdb.porttrees:
        portdir_overlay = portage.settings.get("PORTDIR_OVERLAY", "")
        os.environ["PORTDIR_OVERLAY"] = (portdir_overlay
                                         + " "
                                         + portage._shell_quote(portdir))

        print(f"Appending {portdir} to PORTDIR_OVERLAY...")
        portage._reset_legacy_globals()

    tmpsettings: portage.config = portage.portdb.doebuild_settings
    tmpsettings["PORTAGE_USERNAME"] = os.getlogin()
    tmpsettings["PORTAGE_TMPDIR"] = tmpdir
    tmpsettings["DISTDIR"] = tmpdir
    tmpsettings.features._features.clear()  # pylint: disable=protected-access
    tmpsettings.features.add("unprivileged")
    settings = portage.config(clone=tmpsettings)

    status = doebuild(str(ebuild), "unpack",
                      tree="porttree",
                      settings=settings,
                      vartree=portage.db[portage.root]["vartree"])
    if status != 0:
        raise RuntimeError("Unpack failed")

    env = Path(settings.get("T")) / "environment"
    srcdir_re = re.compile(r'^declare -x S="(?P<val>.+)"$')
    with open(env) as file:
        for line in file:
            if (match := srcdir_re.match(line)) is not None:
                return Path(match.group("val"))
    raise RuntimeError("No ${S} value found")


def main() -> None:
    """
    Parse command-line arguments and run the program.
    """

    pm = []
    if _HAS_PORTAGE:
        pm.append("portage")

    if len(pm) == 0:
        raise RuntimeError("No package manager installed. Aborting")

    parser = argparse.ArgumentParser("gentle", description=gentle.__doc__)
    parser.add_argument("ebuild", type=Path, help="path to the ebuild file")
    parser.add_argument("--api", "-a", choices=pm, default=pm[0],
                        help="package manager API to use")
    parser.add_argument("-v", action="version", version=gentle.__version__)
    args = parser.parse_args()

    mxml_file = args.ebuild.parent / "metadata.xml"
    mxml = MetadataXML(mxml_file)

    with TemporaryDirectory(prefix="gentle-") as tmpdir:
        srcdir = portage_src_unpack(args.ebuild, tmpdir)
        cls: GeneratorClass
        for cls in AbstractGenerator.get_generator_subclasses():
            generator = cls(srcdir)
            if generator.active:
                logger.info("Starting %s", cls.__name__)
                generator.update_metadata_xml(mxml)
    mxml.dump()


if __name__ == "__main__":
    main()
