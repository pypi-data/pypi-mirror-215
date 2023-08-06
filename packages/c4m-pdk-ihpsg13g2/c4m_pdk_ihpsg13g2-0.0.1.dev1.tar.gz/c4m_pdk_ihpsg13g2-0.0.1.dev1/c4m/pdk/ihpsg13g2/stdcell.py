# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from typing import cast

from pdkmaster.technology import property_ as _prp, primitive as _prm
from pdkmaster.design import circuit as _ckt, layout as _lay, library as _lbry
from pdkmaster.io.klayout import merge

from c4m.flexcell import factory as _fab

from .pdkmaster import tech, cktfab, layoutfab

__all__ = [
    "stdcell1v2canvas", "StdCell1V2Factory", "stdcell1v2lib",
    "stdcell3v3canvas", "StdCell3V3Factory", "stdcell3v3lib",
]

prims = tech.primitives


class StdCell1V2Factory(_fab.StdCellFactory):
    def __init__(self, *,
        lib: _lbry.RoutingGaugeLibrary, name_prefix: str = "", name_suffix: str = "",
    ):
        super().__init__(
            lib=lib, cktfab=cktfab, layoutfab=layoutfab,
            name_prefix=name_prefix, name_suffix=name_suffix,
            canvas=stdcell1v2canvas,
        )


stdcell1v2canvas = _fab.StdCellCanvas(
    tech=tech, lambda_=0.05,
    nmos=cast(_prm.MOSFET, prims.sg13g2_lv_nmos), pmos=cast(_prm.MOSFET, prims.sg13g2_lv_pmos),
)
stdcell1v2lib = _lbry.RoutingGaugeLibrary(
    name="StdCell1V2Lib", tech=tech, routinggauge=stdcell1v2canvas.routinggauge,
)
StdCell1V2Factory(lib=stdcell1v2lib).add_default()
merge(stdcell1v2lib)


class StdCell3V3Factory(_fab.StdCellFactory):
    def __init__(self, *,
        lib: _lbry.RoutingGaugeLibrary, name_prefix: str = "", name_suffix: str = "",
    ):
        super().__init__(
            lib=lib, cktfab=cktfab, layoutfab=layoutfab,
            name_prefix=name_prefix, name_suffix=name_suffix,
            canvas=stdcell3v3canvas,
        )


stdcell3v3canvas = _fab.StdCellCanvas(
    tech=tech, lambda_=0.06,
    nmos=cast(_prm.MOSFET, prims.sg13g2_hv_nmos), pmos=cast(_prm.MOSFET, prims.sg13g2_hv_pmos),
    inside=prims.ThickGateOx, inside_enclosure=prims.Activ.min_oxide_enclosure[0],
)
stdcell3v3lib = _lbry.RoutingGaugeLibrary(
    name="StdCell3V3Lib", tech=tech, routinggauge=stdcell3v3canvas.routinggauge,
)
StdCell3V3Factory(lib=stdcell3v3lib).add_default()
merge(stdcell3v3lib)
