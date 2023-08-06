# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from typing import Tuple, Dict

from pdkmaster.technology import (
    property_ as _prp, primitive as _prm, technology_ as _tch
)
from pdkmaster.design import layout as lay, circuit as ckt
from pdkmaster.io import notebook as nb

__all__ = [
    "tech", "technology", "layoutfab", "layout_factory",
    "cktfab", "circuit_factory", "gds_layers", #"plotter",
]


class _IHPSG13G2(_tch.Technology):
    @property
    def name(self):
        return "IHPSG13G2"
    @property
    def grid(self):
        return 0.005

    def __init__(self):
        prims = _prm.Primitives(_prm.Base(type_=_prm.pBase))

        # TODO: angle design rules

        pin_prims = {
            name: _prm.Marker(name=f"{name}.pin")
            for name in (
                "Activ", "GatPoly",
                *(f"Metal{n}" for n in range(1, 5 + 1)),
                *(f"TopMetal{n}" for n in range(1, 2 + 1)),
                # "Passiv",
            )
        }
        prims += pin_prims.values()

        obs_prims: Dict[str, _prm.Marker] = {
            name: _prm.Marker(name=f"{name}.obs")
            for name in (
                "Activ", "GatPoly", "Cont",
                *(f"Metal{n}" for n in range(1, 5 + 1)),
                *(f"Via{n}" for n in range(1, 4 + 1)),
                *(f"TopMetal{n}" for n in range(1, 2 + 1)),
                *(f"TopVia{n}" for n in range(1, 2 + 1)),
            )
        }
        prims += obs_prims.values()

        # single mask based primitives
        NWell = _prm.Well(
            name="NWell", type_=_prm.nImpl,
            min_width=0.62, # NW.a
            min_space=0.62, # NW.b
        )
        # We need n implant layer as we currently don't support transistor
        # without an implant.
        # We take smame design rules as pSD
        virt_nSD = _prm.Implant(
            name="virt_nSD", type_=_prm.nImpl,
            min_width=0.31, # pSD.a
            min_space=0.31, # pSD.b
            min_area=0.25, # pSD.k
            # min_hole_area=0.25, # pSD.l
        )
        pSD = _prm.Implant(
            name="pSD", type_=_prm.pImpl,
            min_width=0.31, # pSD.a
            min_space=0.31, # pSD.b
            min_area=0.25, # pSD.k
            # min_hole_area=0.25, # pSD.l
        )
        ThickGateOx = _prm.Insulator(
            name="ThickGateOx",
            min_width=0.86, # TGO.f
            min_space=0.86, # TGO.e
        )
        # Recognition layers
        RES = _prm.Marker(name="RES")
        prims += (
            NWell, virt_nSD, pSD, ThickGateOx, #RES,
        )

        # layers diff and tap will be generated out of Activ
        Activ = _prm.WaferWire(
            name="Activ", pin=pin_prims["Activ"], blockage=obs_prims["Activ"],
            min_width=0.15, # Act.a
            min_space=0.21, # Act.b
            allow_in_substrate=True, well=NWell, implant=(virt_nSD, pSD),
            min_implant_enclosure=_prp.Enclosure(0.18), # pSD.c
            implant_abut="none",
            allow_contactless_implant=False,
            min_well_enclosure=_prp.Enclosure(0.31), # NW.c
            min_substrate_enclosure=_prp.Enclosure(0.31), # NW.d
            min_well_enclosure_same_type=_prp.Enclosure(0.03), # pSD.d1
            min_substrate_enclosure_same_type=_prp.Enclosure(0.03), # pSD.sc1
            allow_well_crossing=False,
            oxide=ThickGateOx,
            min_oxide_enclosure=_prp.Enclosure(0.27), # TGO.a
        )
        GatPoly = _prm.GateWire(
            name="GatPoly", pin=pin_prims["GatPoly"], blockage=obs_prims["GatPoly"],
            min_width=0.13, # Gat.a
            min_space=0.18, # Gat.b
            min_area=0.09, # Gat.e
            # IHP will do dummy insertion
            # min_density=0.15, # GFil.g
        )
        # wires
        metals: Dict[str, _prm.MetalWire] = {
            name: _prm.MetalWire(name=name, **wire_args) for name, wire_args in (
                ("Metal1", {
                    "pin": pin_prims["Metal1"],
                    "blockage": obs_prims["Metal1"],
                    "min_width": 0.16, # M1.a
                    "min_space": 0.18, # M1.b
                    # "space_table": (
                    #     ((0.3, 1.0), 0.22), # M1.e
                    #     ((10.0, 10.0), 0.60), # M1.f
                    # ),
                    "min_area": 0.144 # M1.d
                    # IHP will do dummy insertion
                    # "min_density": 0.35, # M1.j
                    # "max_density": 0.60, # M1.k
                    # TODO: M1.g/i 45deg line
                }),
                *(
                    (metal, {
                        "pin": pin_prims[metal],
                        "blockage": obs_prims[metal],
                        "min_width": 0.20, # Mn.a
                        "min_space": 0.21, # Mn.b
                        # "space_table": (
                        #     ((0.39, 1.0), 0.24), # Mn.e
                        #     ((10.0, 10.0), 0.60), # Mn.f
                        # ), # m1.3a+b, m2.3a+b
                        "min_area": 0.144 # Mn.d
                        # IHP will do dummy insertion
                        # "min_density": 0.35, # Mn.j
                        # "max_density": 0.60, # Mn.k
                        # TODO: Mn.g/i 45deg line
                    }) for metal in (f"Metal{n}" for n in range(2, 5 + 1))
                ),
                ("TopMetal1", {
                    "pin": pin_prims["TopMetal1"],
                    "blockage": obs_prims["TopMetal1"],
                    "min_width": 1.64, # TM1.a
                    "min_space": 1.64, # TM1.b
                    # IHP will do dummy insertion
                    # "min_density": 0.25, # TM1.c
                    # "max_density": 0.70, # TM1.d
                }),
                ("TopMetal2", {
                    "pin": pin_prims["TopMetal2"],
                    "blockage": obs_prims["TopMetal2"],
                    "min_width": 2.00, # TM2.a
                    "min_space": 2.00, # TM2.b
                    # "space_table": (
                    #     ((5.0, 50.0), 5.0), # TM2.b1R
                    # ),
                    # IHP will do dummy insertion
                    # "min_density": 0.25, # TM1.c
                    # "max_density": 0.70, # TM1.d
                }),
            )
        }
        # TODO: RDL option
        prims += (Activ, GatPoly, *metals.values())

        # vias
        vias: Dict[str, _prm.Via] = {
            via_args["name"]: _prm.Via(**via_args) for via_args in (
                {
                    "name": "Cont",
                    "blockage": obs_prims["Cont"],
                    "width": 0.16, # Cnt.a
                    "min_space": 0.18, # Cnt.b
                    "bottom": (Activ, GatPoly),
                    "top": metals["Metal1"],
                    "min_bottom_enclosure": (
                        _prp.Enclosure(0.07), # Cnt.c
                        _prp.Enclosure(0.07), # Cnt.d
                    ),
                    "min_top_enclosure": _prp.Enclosure((0.000, 0.080)), # li.5.-
                },
                {
                    "name": "Via1",
                    "blockage": obs_prims["Via1"],
                    "width": 0.19, # V1.a
                    "min_space": 0.22, # V1.b
                    "bottom": metals["Metal1"],
                    "top": metals["Metal2"],
                    # TODO: allow single side bigger enclosure
                    "min_bottom_enclosure": _prp.Enclosure((0.01, 0.05)), # V1.c/c1
                    "min_top_enclosure": _prp.Enclosure((0.005, 0.05)), # Mn.c/c1
                },
                *(
                    {
                        "name": f"Via{n}",
                        "blockage": obs_prims[f"Via{n}"],
                        "width": 0.170, # ct.1
                        "min_space": 0.190, # ct.2
                        "bottom": metals[f"Metal{n}"],
                        "top": metals[f"Metal{n + 1}"],
                        # TODO: allow single side bigger enclosure
                        "min_bottom_enclosure": _prp.Enclosure((0.005, 0.05)), # Mn.c/c1
                        "min_top_enclosure": _prp.Enclosure((0.005, 0.05)), # Vn.c/c1
                    } for n in range(2, 4 + 1)
                ),
                {
                    "name": "TopVia1",
                    "blockage": obs_prims["TopVia1"],
                    "width": 0.42, # TV1.a
                    "min_space": 0.42, # TV1.b
                    "bottom": metals["Metal5"],
                    "top": metals["TopMetal1"],
                    "min_bottom_enclosure": _prp.Enclosure(0.01), # TV1.c
                    "min_top_enclosure": _prp.Enclosure(0.42), # TV1.d
                },
                {
                    "name": "TopVia2",
                    "blockage": obs_prims["TopVia2"],
                    "width": 0.9, # TV2.a
                    "min_space": 1.06, # TV2.b
                    "bottom": metals["TopMetal1"],
                    "top": metals["TopMetal2"],
                    "min_bottom_enclosure": _prp.Enclosure(0.5), # TV1.c
                    "min_top_enclosure": _prp.Enclosure(0.42), # TV1.d
                },
            )
        }
        Passiv = _prm.PadOpening(
            name="Passiv", #pin=pin_prims["Passiv"],
            # TODO: Can min_width be reduced ?
            min_width=40.000, # Own rule
            # min_width=2.1, # Pas.a
            min_space=3.5, # Pas.b
            bottom=metals["TopMetal2"],
            min_bottom_enclosure=_prp.Enclosure(2.1), # Pas.c
        )
        prims += (*vias.values(), Passiv)

        # misc using wires
        prims += (
            # extra space rules
            _prm.Spacing( # NW.e
                primitives1=NWell, primitives2=Activ, min_space=0.24,
            ),
            _prm.Spacing( # TGO.b
                primitives1=Activ, primitives2=ThickGateOx, min_space=0.27,
            ),
            _prm.Spacing( # Gat.d
                primitives1=Activ, primitives2=GatPoly, min_space=0.07,
            ),
            _prm.Spacing( # Cnt.e
                primitives1=vias["Cont"], primitives2=Activ, min_space=0.14,
            ),
        )

        # transistors
        lvmosgate = _prm.MOSFETGate(name="lvmosgate",
            active=Activ, poly=GatPoly,
            # No need for overruling min_l or min_w
            min_sd_width=0.23, # Act.c
            min_polyactive_extension=0.18, # GatPoly.c
            contact=vias["Cont"], min_contactgate_space=0.11, # Cnt.f
        )
        hvmosgate = _prm.MOSFETGate(name="hvmosgate",
            active=Activ, poly=GatPoly, oxide=ThickGateOx,
            min_l=0.33, # Gat.a3/a4
            min_w=0.30, # from trnasistor model
            min_gate_space=0.25, # Gat.b1
            min_gateoxide_enclosure=_prp.Enclosure((0.34, 0.26)),
            min_sd_width=0.23, # Act.c
            min_polyactive_extension=0.18, # GatPoly.c
            contact=vias["Cont"],
            min_contactgate_space=0.11, # licon.11
        )
        trans = {
            name: _prm.MOSFET(name=name,
                gate=gate, implant=impl, well=well,
                min_gateimplant_enclosure=impl_enc, # Implant.1
            )
            for name, gate, well, impl, impl_enc in (
                ("sg13g2_lv_nmos", lvmosgate, None, virt_nSD, _prp.Enclosure(0.30)), # pSD.j
                ("sg13g2_lv_pmos", lvmosgate, NWell, pSD, _prp.Enclosure(0.30)), # pSD.i
                ("sg13g2_hv_nmos", hvmosgate, None, virt_nSD, _prp.Enclosure(0.40)), # pSD.j1
                ("sg13g2_hv_pmos", hvmosgate, NWell, pSD, _prp.Enclosure(0.40)), # pSD.i1
            )
        }
        # prims += (mosgate, mosgate_sc, hvmosgate, *trans.values())
        prims += (lvmosgate, hvmosgate, *trans.values())

        # bipolars =  tuple(
        #     _prm.Bipolar(name=name, type_=type_, indicator=ind)
        #     for name, type_, ind in (
        #         ("npn_05v5_w1u00l1u00", _prm.npnBipolarT, npn),
        #         ("npn_05v5_w1u00l2u00", _prm.npnBipolarT, npn),
        #         ("pnp_05v5_w0u68l0u68", _prm.pnpBipolarT, pnp),
        #         ("pnp_05v5_w3u40l3u40", _prm.pnpBipolarT, pnp),
        #     )
        # )
        # prims += bipolars

        # prims += _prm.Auxiliary(name="prBoundary")

        super().__init__(primitives=prims)

tech = technology = _IHPSG13G2()
cktfab = circuit_factory = ckt.CircuitFactory(tech=tech)
layoutfab = layout_factory = lay.LayoutFactory(tech=tech)

gds_layers: Dict[str, Tuple[int, int]] = {
    "virt_nSD": (7, 99), # (7, 0) is generated nSD layer
}
# Use datatype 100 for obstruction layer;
# datatype 23 'nofill' would cause no dummy generation if accidently not removed before tape-out
for name, layer, has_pin, has_obs in (
    ("Activ", 1, True, True),
    ("GatPoly", 5, True, True),
    ("Cont", 6, False, True),
    ("Metal1", 8, True, True),
    ("Passiv", 9, True, False),
    ("Metal2", 10, True, True),
    ("pSD", 14, False, False),
    ("Via1", 19, False, True),
    ("RES", 24, False, False),
    ("Via2", 29, False, True),
    ("Metal3", 30, True, True),
    ("NWell", 31, False, False),
    ("ThickGateOx", 44, False, False),
    ("Via3", 49, False, True),
    ("Metal4", 50, True, True),
    ("Via4", 66, False, True),
    ("Metal5", 67, True, True),
    ("TopVia1", 125, False, True),
    ("TopMetal1", 126, True, True),
    ("TopVia2", 133, False, True),
    ("TopMetal2", 134, True, True),
):
    gds_layers[name] = (layer, 0)
    if has_pin:
        gds_layers[f"{name}.pin"] = (layer, 2)
    if has_obs:
        gds_layers[f"{name}.obs"] = (layer, 100)

# plotter = nb.Plotter({
#     # "pwell": {"fc": (1.0, 1.0, 0.0, 0.2), "ec": "orange", "zorder": 10},
#     "nwm": {"fc": (0.0, 0.0, 0.0, 0.1), "ec": "grey", "zorder": 10},
#     "Activ": {"fc": "lawngreen", "ec": "lawngreen", "zorder": 11},
#     "poly": {"fc": "red", "ec": "red", "zorder": 12},
#     "nsdm": {"fc": "purple", "ec": "purple", "alpha": 0.3, "zorder": 13},
#     "psdm": {"fc": "blueviolet", "ec": "blueviolet", "alpha": 0.3, "zorder": 13},
#     "lvtn": {"fc": (0.0, 0.0, 0.0, 0.0), "ec": "grey", "zorder": 13},
#     "hvtp": {"fc": (1, 1, 1, 0.3), "ec": "whitesmoke", "zorder": 13},
#     "licon": {"fc": "black", "ec": "black", "zorder": 14},
#     "li": {"fc": (0.1, 0.1, 1, 0.4), "ec": "blue", "zorder": 15},
# })
