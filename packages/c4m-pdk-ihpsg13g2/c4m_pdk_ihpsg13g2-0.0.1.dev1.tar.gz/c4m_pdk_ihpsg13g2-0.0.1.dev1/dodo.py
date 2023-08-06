# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
import os, sys, site, re, yaml
from os.path import basename, relpath
from pathlib import Path
from textwrap import dedent
from typing import List, Tuple, Dict, Generator

from doit import get_var
from doit.action import BaseAction, CmdAction
from doit.tools import check_timestamp_unchanged, create_folder

import pdkmaster, c4m, c4m.flexcell

### Config

DOIT_CONFIG = {
    "default_tasks": [
        "install", "open_pdk", "gds", "klayout", "coriolis",
    ],
}


### support functions

def get_var_env(name, default=None):
    """Uses get_var to get a command line variable, also checks
    environment variables for default value

    If os.environ[name.upper()] exists that value will override the
    default value given.
    """
    try:
        default = os.environ[name.upper()]
    except:
        # Keep the specified default
        pass
    return get_var(name, default=default)


### globals

top_dir = Path(__file__).parent

dist_dir = top_dir.joinpath("dist")

open_pdk_dir = top_dir.joinpath("open_pdk")
open_pdk_ihpsg13g2_dir = open_pdk_dir.joinpath("C4M.ihpsg13g2")
open_pdk_tech_dir = open_pdk_ihpsg13g2_dir.joinpath("libs.tech")
open_pdk_ref_dir = open_pdk_ihpsg13g2_dir.joinpath("libs.ref")

override_dir = top_dir.joinpath("override")

pdkmaster_inst_dir = Path(pdkmaster.__file__).parent
c4m_local_dir = top_dir.joinpath("c4m")
ihpsg13g2_local_dir = c4m_local_dir.joinpath("pdk", "ihpsg13g2")
c4m_inst_dir = Path(site.getsitepackages()[0]).joinpath("c4m")
ihpsg13g2_inst_dir = c4m_inst_dir.joinpath("pdk", "ihpsg13g2")
flexcell_inst_dir = Path(c4m.flexcell.__file__).parent

c4m_py_files = tuple(c4m_local_dir.rglob("*.py"))

# variables
python = get_var_env("python", default="python3")
pip = get_var_env("pip", default="pip3")

### cell list

cell_list_file = top_dir.joinpath("cell_list.yml")

def task_cell_list():
    """Regenerate cell list.

    This task is not run by default. It needs to be run manually when the cell list
    has been changed and then the updated file has to be commit to git.
    """
    def write_list():
        import yaml

        from c4m.pdk import ihpsg13g2
        # from doitlib import libs

        cell_list = {
            lib.name: list(cell.name for cell in lib.cells)
            for lib in ihpsg13g2.__libs__
        }
        with cell_list_file.open("w") as f:
            yaml.dump(cell_list, f)

    return {
        "title": lambda _: "Creating cell list file",
        "targets": (
            cell_list_file,
        ),
        "actions": (
            write_list,
        ),
    }

# We assume that the cell list is stored in git and is available in the top directory.
assert cell_list_file.exists()
with cell_list_file.open("r") as f:
    cell_list: Dict[str, List[str]]
    cell_list = yaml.safe_load(f)

lib_module_paths = {
    "StdCell1V2Lib": (pdkmaster_inst_dir, flexcell_inst_dir),
    "StdCell3V3Lib": (pdkmaster_inst_dir, flexcell_inst_dir),
}


### main tasks

#
# install
def task_install():
    """Install the python module

    It will not install dependencies to avoid overwriting locally installed versions
    with release versions.
    """

    return {
        "title": lambda _: "Installing python module",
        "file_dep": (
            *c4m_py_files,
        ),
        "targets": (ihpsg13g2_inst_dir,),
        "actions": (
            f"{pip} install --no-deps {top_dir}",
            f"{pip} check",
        ),
    }


#
# dist
def task_dist():
    """Create distributable python module"""

    return {
        "title": lambda _: "Creating wheel",
        "file_dep": (top_dir.joinpath("setup.py"), *c4m_py_files),
        "targets": (dist_dir,),
        "actions": (f"{python} -m build",)
    }


#
# open_pdk
def task_open_pdk():
    """Create open_pdk dir"""
    # This is separate task so we can clean up full open_pdk directory

    return {
        "title": lambda _: "Creating open_pdk directory",
        "targets": (open_pdk_dir,),
        "actions": (
            (create_folder, (open_pdk_dir,)),
        ),
        "clean": (f"rm -fr {str(open_pdk_dir)}",),
    }


#
# gds
def task_gds():
    """Generate GDSII files"""

    gds_dirs = tuple(
        open_pdk_ref_dir.joinpath(lib, "gds") for lib in cell_list.keys()
    )
    gds_files: Dict[str, Tuple[Path, ...]] = {}
    for lib, cells in cell_list.items():
        gds_files[lib] = tuple(
            open_pdk_ref_dir.joinpath(lib, "gds", f"{cell}.gds")
            for cell in cells
        )

    def gen_gds(libname):
        from pdkmaster.io.klayout import export2db
        from c4m.pdk import ihpsg13g2
        # from doitlib import libs

        lib = None
        for lib2 in ihpsg13g2.__libs__:
            if lib2.name == libname:
                lib = lib2
                break
        assert lib is not None

        out_dir = open_pdk_ref_dir.joinpath(libname, "gds")
        layout = export2db(
            lib, gds_layers=ihpsg13g2.gds_layers, cell_name=None, merge=False,
            add_pin_label=True,
        )
        layout.write(str(out_dir.joinpath(f"{libname}.gds")))
        for cell in layout.each_cell():
            assert cell.name != libname
            cell.write(str(out_dir.joinpath(f"{cell.name}.gds")))

    for libname in cell_list.keys():
        yield {
            "name": libname,
            "doc": f"Creating gds files for {libname}",
            "file_dep": c4m_py_files,
            "uptodate": tuple(
                check_timestamp_unchanged(str(dir)) for dir in lib_module_paths[libname]
            ),
            "targets": gds_files[libname],
            "actions": (
                *(
                    (create_folder, (dir_,)) for dir_ in gds_dirs
                ),
                (gen_gds, (libname,)),
            ),
        }


#
# klayout
klayout_dir = open_pdk_tech_dir.joinpath("klayout")
klayout_tech_dir = klayout_dir.joinpath("tech", "C4M.ihpsg13g2")
klayout_bin_dir = klayout_dir.joinpath("bin")
klayout_lvs_script = klayout_bin_dir.joinpath("lvs_ihpsg13g2")
klayout_drc_script = klayout_bin_dir.joinpath("drc_ihpsg13g2")
def task_klayout():
    """Generate klayout files"""

    klayout_drc_dir = klayout_tech_dir.joinpath("drc")
    klayout_lvs_dir = klayout_tech_dir.joinpath("lvs")
    klayout_share_dir = klayout_dir.joinpath("share")

    klayout_lyt_file = klayout_tech_dir.joinpath("C4M.ihpsg13g2.lyt")
    klayout_drc_lydrc_file = klayout_drc_dir.joinpath("DRC.lydrc")
    klayout_extract_lylvs_file = klayout_lvs_dir.joinpath("Extract.lylvs")
    klayout_drc_file = klayout_share_dir.joinpath("ihpsg13g2.drc")
    klayout_extract_file = klayout_share_dir.joinpath("ihpsg13g2_extract.lvs")
    klayout_extract_script = klayout_bin_dir.joinpath("extract_ihpsg13g2")
    klayout_lvs_file = klayout_share_dir.joinpath("ihpsg13g2.lvs")

    def gen_klayout():
        from pdkmaster.io.klayout import FileExporter
        from c4m.pdk import ihpsg13g2
        from xml.etree.ElementTree import ElementTree

        expo = FileExporter(
            tech=ihpsg13g2.tech, gds_layers=ihpsg13g2.gds_layers,
            export_name=f"C4M.{ihpsg13g2.tech.name}",
            prims_spiceparams=ihpsg13g2.prims_spiceparams,
        )()

        # DRC
        with klayout_drc_file.open("w") as f:
            f.write(expo["drc"])
        with klayout_drc_script.open("w") as f:
            relfile = relpath(klayout_drc_file, klayout_bin_dir)
            f.write(dedent(f"""
                #!/bin/sh
                d=`dirname $0`
                deck=`realpath $d/{relfile}`

                if [ $# -ne 2 ]
                then
                    echo "Usage `basename $0` input report"
                    exit 20
                fi

                export SOURCE_FILE=$1 REPORT_FILE=$2
                klayout -b -r ${{deck}}
            """[1:]))
        klayout_drc_script.chmod(0o755)

        # Extract
        with klayout_extract_file.open("w") as f:
            f.write(expo["extract"])
        with klayout_extract_script.open("w") as f:
            relfile = relpath(klayout_extract_file, klayout_bin_dir)
            f.write(dedent(f"""
                #!/bin/sh
                d=`dirname $0`
                deck=`realpath $d/{relfile}`

                if [ $# -ne 2 ]
                then
                    echo "Usage `basename $0` input spice_out"
                    exit 20
                fi

                export SOURCE_FILE=$1 SPICE_FILE=$2
                klayout -b -r ${{deck}}
            """[1:]))
        klayout_extract_script.chmod(0o755)

        # LVS
        with klayout_lvs_file.open("w") as f:
            f.write(expo["lvs"])
        with klayout_lvs_script.open("w") as f:
            relfile = relpath(klayout_lvs_file, klayout_bin_dir)
            f.write(dedent(f"""
                #!/bin/sh
                d=`dirname $0`
                deck=`realpath $d/{relfile}`

                if [ $# -ne 3 ]
                then
                    echo "Usage `basename $0` gds spice report"
                    exit 20
                fi

                export SOURCE_FILE=`realpath $1` SPICE_FILE=`realpath $2` REPORT_FILE=$3
                klayout -b -r ${{deck}}
            """[1:]))
        klayout_lvs_script.chmod(0o755)

        # klayout technology
        et = ElementTree(expo["ly_drc"])
        et.write(klayout_drc_lydrc_file, encoding="utf-8", xml_declaration=True)
        et = ElementTree(expo["ly_extract"])
        et.write(klayout_extract_lylvs_file, encoding="utf-8", xml_declaration=True)
        et = ElementTree(expo["ly_tech"])
        et.write(klayout_lyt_file, encoding="utf-8", xml_declaration=True)

    return {
        "title": lambda _: "Creating klayout files",
        "file_dep": c4m_py_files,
        "uptodate": (
            check_timestamp_unchanged(str(pdkmaster_inst_dir)),
        ),
        "targets": (
            klayout_lyt_file, klayout_drc_lydrc_file, klayout_extract_lylvs_file,
            klayout_drc_file, klayout_drc_script, klayout_extract_file,
            klayout_extract_script, klayout_lvs_file, klayout_lvs_script,
        ),
        "actions": (
            (create_folder, (klayout_share_dir,)),
            (create_folder, (klayout_bin_dir,)),
            (create_folder, (klayout_drc_dir,)),
            (create_folder, (klayout_lvs_dir,)),
            gen_klayout,
        ),
    }


#
# coriolis
def task_coriolis():
    """Generate coriolis support files"""

    coriolis_dir = open_pdk_tech_dir.joinpath("coriolis")
    corio_dir = coriolis_dir.joinpath("techno", "etc", "coriolis2")
    corio_node180_dir = corio_dir.joinpath("node180")
    corio_ihpsg13g2_dir = corio_node180_dir.joinpath("ihpsg13g2")

    corio_nda_init_file = corio_dir.joinpath("__init__.py")
    corio_node130_init_file = corio_node180_dir.joinpath("__init__.py")
    corio_ihpsg13g2_init_file = corio_ihpsg13g2_dir.joinpath("__init__.py")
    corio_ihpsg13g2_techno_file = corio_ihpsg13g2_dir.joinpath("techno.py")
    corio_ihpsg13g2_lib_files = tuple(
        corio_ihpsg13g2_dir.joinpath(f"{lib}.py") for lib in cell_list.keys()
    )

    def gen_init():
        from c4m.pdk import ihpsg13g2
        # from doitlib import libs

        with corio_ihpsg13g2_init_file.open("w") as f:
            print("from .techno import *", file=f)
            # for lib in libs.__libs__:
            for lib in ihpsg13g2.__libs__:
                print(f"from .{lib.name} import setup as {lib.name}_setup", file=f)

            print(
                "\n__lib_setups__ = [{}]".format(
                    # ",".join(f"{lib.name}.setup" for lib in libs.__libs__)
                    ",".join(f"{lib.name}.setup" for lib in ihpsg13g2.__libs__)
                ),
                file=f,
            )

    def gen_coriolis():
        from pdkmaster.io import coriolis as _iocorio
        from c4m.flexcell import coriolis_export_spec
        from c4m.pdk import ihpsg13g2
        # from doitlib import libs

        expo = _iocorio.FileExporter(
            tech=ihpsg13g2.tech, gds_layers=ihpsg13g2.gds_layers, spec=coriolis_export_spec,
        )

        with corio_ihpsg13g2_techno_file.open("w") as f:
            f.write(dedent("""
                # Autogenerated file
                # SPDX-License-Identifier: GPL-2.0-or-later OR AGPL-3.0-or-later OR CERN-OHL-S-2.0+
            """))
            f.write(expo())

        # for lib in libs.__libs__:
        for lib in ihpsg13g2.__libs__:
            with corio_ihpsg13g2_dir.joinpath(f"{lib.name}.py").open("w") as f:
                f.write(expo(lib))

    return {
        "title": lambda _: "Creating coriolis files",
        "file_dep": c4m_py_files,
        "uptodate": (
            check_timestamp_unchanged(str(pdkmaster_inst_dir)),
            check_timestamp_unchanged(str(flexcell_inst_dir)),
            # check_timestamp_unchanged(str(flexio_inst_dir)),
            # check_timestamp_unchanged(str(flexmem_inst_dir)),
        ),
        "targets": (
            corio_nda_init_file, corio_node130_init_file, corio_ihpsg13g2_init_file,
            corio_ihpsg13g2_techno_file, *corio_ihpsg13g2_lib_files,
        ),
        "actions": (
            (create_folder, (corio_ihpsg13g2_dir,)),
            corio_nda_init_file.touch, corio_node130_init_file.touch,
            gen_init, gen_coriolis,
        ),
    }


#
# release
def task_tarball():
    """Create a tarball"""
    from datetime import datetime

    tarballs_dir = top_dir.joinpath("tarballs")
    t = datetime.now()
    tarball = tarballs_dir.joinpath(f'{t.strftime("%Y%m%d_%H%M")}_c4m_pdk_ihpsg13g2.tgz')

    return {
        "title": lambda _: "Create release tarball",
        "task_dep": (
            "coriolis", "klayout", "gds",
        ),
        "targets": (tarball,),
        "actions": (
            (create_folder, (tarballs_dir,)),
            f"cd {str(top_dir)}; tar czf {str(tarball)} open_pdk",
        )
    }


#
# drc
def task_drc():
    "Run drc checks"
    drc_dir = top_dir.joinpath("drc")

    def run_drc(lib, cell):
        gds_dir = open_pdk_ref_dir.joinpath(lib, "gds")

        drcrep = drc_dir.joinpath(lib, f"{cell}.rep")
        gdsfile = gds_dir.joinpath(f"{cell}.gds")

        try:
            CmdAction(
                f"{str(klayout_drc_script)} {str(gdsfile)} {str(drcrep)}",
            ).execute()
            with drcrep.open("r") as f:
                # Each DRC error has an <item> section in the output XML
                ok = not any(("<item>" in line for line in f))
        except:
            ok = False
        if not ok:
            print(f"DRC of {lib}/{cell} failed!", file=sys.stderr)

    def lib_rep(lib, cells):
        with drc_dir.joinpath(f"{lib}.rep").open("w") as librep:
            for cell in cells:
                drcrep = drc_dir.joinpath(lib, f"{cell}.rep")
                with drcrep.open("r") as f:
                    # Each DRC error has an <item> section in the output XML
                    ok = not any(("<item>" in line for line in f))

                print(f"{cell}: {'OK' if ok else 'NOK'}", file=librep)

    for lib, cells in cell_list.items():
        drc_lib_dir = drc_dir.joinpath(lib)
        for cell in cells:
            yield {
                "name": f"{lib}:{cell}",
                "doc": f"Running DRC check for lib {lib} cell {cell}",
                "file_dep": c4m_py_files,
                "task_dep": (f"gds:{lib}", "klayout"),
                "uptodate": tuple(
                    check_timestamp_unchanged(str(dir)) for dir in lib_module_paths[lib]
                ),
                "targets": (drc_dir.joinpath(lib, f"{cell}.rep"),),
                "actions": (
                    (create_folder, (drc_lib_dir,)),
                    (run_drc, (lib, cell)),
                ),
            }

        # If there exist a Gallery cell then do only DRC on that cell by default
        if "Gallery" in cells:
            cells = ("Gallery",)

        yield {
            "name": f"{lib}",
            "doc": f"Assembling DRC results for lib",
            "file_dep": c4m_py_files,
            "task_dep": (
                *(f"drc:{lib}:{cell}" for cell in cells),
                "klayout",
            ),
            "uptodate": tuple(
                check_timestamp_unchanged(str(dir)) for dir in lib_module_paths[lib]
            ),
            "targets": (drc_dir.joinpath(f"{lib}.rep"),),
            "actions": (
                (lib_rep, (lib, cells)),
            ),
            "clean": (f"rm -fr {str(drc_lib_dir)}",),
        }
