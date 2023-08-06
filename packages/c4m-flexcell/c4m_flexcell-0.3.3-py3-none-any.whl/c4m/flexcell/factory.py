# SPDX-License-Identifier: GPL-2.0-or-later OR AGPL-3.0-or-later OR CERN-OHL-S-2.0+
from typing import Tuple, Optional, Union, cast
import os
import abc

from pdkmaster.technology import geometry as _geo
from pdkmaster.design import (
    circuit as _ckt, layout as _lay, library as _lbry, factory as _fab,
)
from pdkmaster.io.coriolis import CoriolisExportSpec

from ._cells import _cells, _oldcells
from .canvas import StdCellCanvas
from .cell import _Cell
from .stdcell import _StdCellConverter


__all__ = ["coriolis_export_spec", "StdCellFactory"]


def _direction_cb(net_name: str) -> str:
    if net_name == "vdd":
        return "supply"
    elif net_name == "vss":
        return "ground"
    elif net_name == "ck":
        return "clock"
    elif net_name in ("nq", "q", "one", "zero"):
        return "out"
    else:
        return "in"
coriolis_export_spec = CoriolisExportSpec(
    globalnets=("vdd", "vss"), net_direction_cb=_direction_cb,
)


class _Fill(_Cell):
    def __init__(self, *, fab: "StdCellFactory", name: str, width: int=1):
        super().__init__(fab=fab, name=name)

        canvas = fab.canvas

        self.set_width(width=width*canvas._cell_horplacement_grid)


class _Tie(_Cell):
    def __init__(self, *,
        fab: "StdCellFactory", name: str, max_diff: bool=False, max_poly: bool=False, width: int=1,
    ):
        if max_diff and max_poly:
            raise ValueError("only one of max_diff and max_poly can be 'True'")

        canvas = fab.canvas
        tech = fab.tech

        super().__init__(fab=fab, name=name)

        cell_width = width*canvas._cell_horplacement_grid
        self.set_width(width=cell_width)

        active = canvas._active
        nimplant = canvas._nimplant
        pimplant = canvas._pimplant
        nwell = canvas._nwell
        poly = canvas._poly
        contact = canvas._contact
        metal1 = canvas._metal1

        ckt = self.circuit
        layouter = self._layouter

        vdd = ckt.nets.vdd
        vss = ckt.nets.vss

        min_actwell_space = tech.computed.min_space(primitive1=active, primitive2=nwell)
        min_actpoly_space = tech.computed.min_space(primitive1=active, primitive2=poly)

        if not max_diff:
            # vss min tap
            l_ch = layouter.wire_layout(
                net=vss, wire=contact, rows=canvas._min_tap_chs,
                bottom=active, bottom_implant=pimplant, bottom_enclosure="wide",
            )
            impl_bb = l_ch.bounds(mask=pimplant.mask)
            x = 0.5*cell_width
            y = 0.5*pimplant.min_space - impl_bb.bottom
            vss_tap_lay = layouter.place(object_=l_ch, x=x, y=y)

            # vdd min tap
            l_ch = layouter.wire_layout(
                net=vdd, well_net=vdd, wire=contact, rows=canvas._min_tap_chs,
                bottom=active, bottom_implant=nimplant, bottom_well=nwell,
                bottom_enclosure="wide",
            )
            impl_bb = l_ch.bounds(mask=nimplant.mask)
            x = 0.5*cell_width
            y = canvas._cell_height - 0.5*pimplant.min_space - impl_bb.top
            vdd_tap_lay = layouter.place(object_=l_ch, x=x, y=y)

            if max_poly:
                # Add big poly
                vss_dio_tap_bb = vss_tap_lay.bounds(mask=active.mask)
                vdd_dio_tap_bb = vdd_tap_lay.bounds(mask=active.mask)
                left = 0.5*poly.min_space
                right = cell_width - 0.5*poly.min_space
                bottom = vss_dio_tap_bb.top + min_actpoly_space
                top = vdd_dio_tap_bb.bottom - min_actpoly_space
                layouter.add_wire(net=vss, wire=poly, shape=_geo.Rect(
                    left=left, bottom=bottom, right=right, top=top,
                ))

                l_ch = layouter.wire_layout(net=vss, wire=contact, bottom=poly)
                poly_bb = l_ch.bounds(mask=poly.mask)
                ch_bb = l_ch.bounds(mask=contact.mask)
                x = 0.5*cell_width
                y = bottom - poly_bb.bottom
                if canvas._min_contact_active_space is not None:
                    y = max(
                        y,
                        vss_dio_tap_bb.top + canvas._min_contact_active_space - ch_bb.bottom
                    )
                vss_polych_lay = layouter.place(object_=l_ch, x=x, y=y)
                vss_polych_m1_bb = vss_polych_lay.bounds(mask=metal1.mask)
                if vss_polych_m1_bb.bottom > canvas._m1_vssrail_width:
                    layouter.add_wire(net=vss, wire=metal1, shape=_geo.Rect.from_rect(
                        rect=vss_polych_m1_bb, bottom=0.0,
                    ))
        else: # max_diff == True
            # vss tap
            # First create ch to compute dimension of big diode
            l_ch = layouter.wire_layout(
                net=vss, wire=contact, bottom=active, bottom_implant=pimplant,
            )
            impl_bb = l_ch.bounds(mask=pimplant.mask)
            impl_w = impl_bb.width
            # Compute the possible hor. expansion
            d = cell_width - impl_w - pimplant.min_space
            assert tech.on_grid(d) >= 0.0
            act_bb = l_ch.bounds(mask=active.mask)
            # Maximize width
            act_w = act_bb.width + d
            # Maximize height
            enc = act_bb.bottom - impl_bb.bottom
            bottom = 0.5*pimplant.min_space + enc
            top = canvas._well_edge_height - min_actwell_space
            act_h = tech.on_grid(
                top - bottom, mult=2, rounding="floor",
            )

            # diode with right dimensions
            l_ch = layouter.wire_layout(
                net=vss, wire=contact, bottom=active, bottom_implant=pimplant,
                bottom_width=act_w, bottom_height=act_h,
            )
            impl_bb = l_ch.bounds(mask=pimplant.mask)
            x = 0.5*cell_width
            y = 0.5*pimplant.min_space - impl_bb.bottom
            layouter.place(object_=l_ch, x=x, y=y)

            # vdd tap
            # First create ch to compute dimension of big diode
            l_ch = layouter.wire_layout(
                net=vdd, well_net=vdd, wire=contact,
                bottom=active, bottom_implant=nimplant, bottom_well=nwell,
            )
            impl_bb = l_ch.bounds(mask=nimplant.mask)
            impl_w = impl_bb.width
            # Compute the possible hor. expansion
            d = cell_width - impl_w - nimplant.min_space
            assert tech.on_grid(d) >= 0.0
            act_bb = l_ch.bounds(mask=active.mask)
            # Maximize width
            act_w = act_bb.width + d
            # Maximize height
            enc = act_bb.bottom - impl_bb.bottom
            bottom = canvas._well_edge_height + canvas._min_active_well_enclosure
            top = canvas._cell_height - 0.5*nimplant.min_space - enc
            act_h = tech.on_grid(
                top - bottom, mult=2, rounding="floor",
            )

            # diode with right dimensions
            l_ch = layouter.wire_layout(
                net=vdd, well_net=vdd, wire=contact,
                bottom=active, bottom_implant=nimplant, bottom_well=nwell,
                bottom_width=act_w, bottom_height=act_h,
            )
            impl_bb = l_ch.bounds(mask=nimplant.mask)
            x = 0.5*cell_width
            y = canvas._cell_height - 0.5*nimplant.min_space - impl_bb.top
            layouter.place(object_=l_ch, x=x, y=y)


class _Diode(_Cell):
    def __init__(self, *,
        fab: "StdCellFactory", name: str,
    ):
        canvas = fab.canvas
        tech = fab.tech

        super().__init__(fab=fab, name=name)

        cell_width = canvas._cell_horplacement_grid
        self.set_width(width=cell_width)

        active = canvas._active
        nimplant = canvas._nimplant
        pimplant = canvas._pimplant
        nwell = canvas._nwell
        contact = canvas._contact
        metal1 = canvas._metal1
        metal1pin = canvas._metal1pin

        ckt = self.circuit
        layouter = self._layouter

        vdd = ckt.nets.vdd
        vss = ckt.nets.vss

        i_ = ckt.new_net(name="i", external=True)

        min_actwell_space = tech.computed.min_space(primitive1=active, primitive2=nwell)
        try:
            s = tech.computed.min_space(primitive1=active.in_(nimplant), primitive2=nwell)
        except:
            pass
        else:
            min_actwell_space = max(min_actwell_space, s)
        enc = active.min_substrate_enclosure
        if enc is not None:
            min_actwell_space = max(min_actwell_space, enc.max())

        nimpl_idx = active.implant.index(nimplant)
        pimpl_idx = active.implant.index(pimplant)
        min_actnimpl_enc = active.min_implant_enclosure[nimpl_idx].max()
        min_actpimpl_enc = active.min_implant_enclosure[pimpl_idx].max()

        # Min active space without implants overlapping
        min_act_space = max(
            active.min_space,
            min_actnimpl_enc + min_actpimpl_enc,
        )

        # vss min tap
        l_ch = layouter.wire_layout(
            net=vss, wire=contact, rows=canvas._min_tap_chs,
            bottom=active, bottom_implant=pimplant,
        )
        impl_bb = l_ch.bounds(mask=pimplant.mask)
        x = 0.5*cell_width
        y = 0.5*pimplant.min_space - impl_bb.bottom
        vss_tap_lay = layouter.place(object_=l_ch, x=x, y=y)
        vss_tap_act_bb = vss_tap_lay.bounds(mask=active.mask)

        # vdd min tap
        l_ch = layouter.wire_layout(
            net=vdd, well_net=vdd, wire=contact, rows=canvas._min_tap_chs,
            bottom=active, bottom_implant=nimplant, bottom_well=nwell
        )
        impl_bb = l_ch.bounds(mask=nimplant.mask)
        x = 0.5*cell_width
        y = canvas._cell_height - 0.5*pimplant.min_space - impl_bb.top
        vdd_tap_lay = layouter.place(object_=l_ch, x=x, y=y)
        vdd_tap_act_bb = vdd_tap_lay.bounds(mask=active.mask)

        # vss diode
        bottom = max(
            vss_tap_act_bb.top + min_act_space,
            canvas._m1_vssrail_width + metal1.min_space,
        )
        top = canvas._well_edge_height - min_actwell_space
        h = tech.on_grid(top - bottom, mult=2, rounding="floor")
        vss_dio_x = 0.5*cell_width
        vss_dio_y = bottom + 0.5*h
        vss_dio_lay = layouter.add_wire(
            net=vss, wire=contact, bottom=active, bottom_implant=nimplant,
            x=vss_dio_x, y=vss_dio_y, bottom_height=h, top_height=h,
        )
        vss_dio_m1_bb = vss_dio_lay.bounds(mask=metal1.mask)

        # vdd diode
        bottom = canvas._well_edge_height + canvas._min_active_well_enclosure
        top = min(
            vdd_tap_act_bb.bottom - min_act_space,
            canvas._cell_height - canvas._m1_vddrail_width - metal1.min_space,
        )
        h = tech.on_grid(top - bottom, mult=2, rounding="floor")
        vdd_dio_x = 0.5*cell_width
        vdd_dio_y = top - 0.5*h
        vdd_dio_lay = layouter.add_wire(
            net=vdd, well_net=vdd, wire=contact,
            bottom=active, bottom_implant=pimplant, bottom_well=nwell,
            x=vdd_dio_x, y=vdd_dio_y, bottom_height=h, top_height=h,
        )
        vdd_dio_m1_bb = vdd_dio_lay.bounds(mask=metal1.mask)

        # input pin
        left = 0.5*cell_width - 0.5*canvas._pin_width
        right = left + canvas._pin_width
        bottom = vss_dio_m1_bb.bottom
        top = vdd_dio_m1_bb.top
        layouter.add_wire(
            net=i_, wire=metal1, pin=metal1pin, shape=_geo.Rect(
                left=left, bottom=bottom, right=right, top=top,
            )
        )


class _ZeroOneDecap(_Cell):
    def __init__(self, *,
        fab: "StdCellFactory", name: str, zero_pin: bool, one_pin: bool,
    ):
        """A cell that can represent a logic zero and/or one; it can be used as decap
        cell with optional extra mos capacitance.
        """
        # TODO: optional extra moscap
        super().__init__(fab=fab, name=name)

        canvas = fab.canvas
        tech = fab.tech
        ckt = self.circuit
        layouter = self._layouter

        vdd = ckt.nets.vdd
        vss = ckt.nets.vss
        zero = ckt.new_net(name="zero", external=zero_pin)
        one = ckt.new_net(name="one", external=one_pin)

        nmos = canvas._nmos
        pmos = canvas._pmos
        l = canvas.l

        active = canvas._active
        nimplant = canvas._nimplant
        pimplant = canvas._pimplant
        nwell = canvas._nwell
        poly = canvas._poly
        contact = canvas._contact
        metal1 = canvas._metal1
        metal1pin = canvas._metal1pin

        # We intermix circuit and layout generation as w of transistors
        # is computed on other element's layou
        min_actwell_space = tech.computed.min_space(primitive1=active, primitive2=nwell)
        min_actpoly_space = tech.computed.min_space(primitive1=active, primitive2=poly)

        # first create most of the wires/device layout unplaced

        # taps
        _n_tap_lay = layouter.wire_layout(
            net=vss, wire=contact, bottom=active, bottom_implant=pimplant,
            columns=canvas._min_tap_chs, bottom_enclosure="wide",
            bottom_implant_enclosure="wide",
        )
        _n_tap_impl_bb = _n_tap_lay.bounds(mask=pimplant.mask)
        _n_tap_act_bb = _n_tap_lay.bounds(mask=active.mask)
        n_tap_y = 0.5*pimplant.min_space - _n_tap_impl_bb.bottom

        _p_tap_lay = layouter.wire_layout(
            net=vdd, well_net=vdd, wire=contact,
            bottom=active, bottom_implant=nimplant, bottom_well=nwell,
            columns=canvas._min_tap_chs, bottom_enclosure="wide",
            bottom_implant_enclosure="wide",
        )
        _p_tap_impl_bb = _p_tap_lay.bounds(mask=nimplant.mask)
        _p_tap_act_bb = _p_tap_lay.bounds(mask=active.mask)
        p_tap_y = canvas._cell_height - 0.5*nimplant.min_space - _p_tap_impl_bb.top

        # poly pads
        _one_polypad_lay = layouter.wire_layout(
            net=one, wire=contact, bottom=poly, bottom_enclosure="wide",
        )
        _one_polypad_poly_bb = _one_polypad_lay.bounds(mask=poly.mask)
        _one_polypad_ch_bb = _one_polypad_lay.bounds(mask=contact.mask)
        _one_polypad_m1_bb = _one_polypad_lay.bounds(mask=metal1.mask)
        one_polypad_y = (
            canvas._well_edge_height
            - 0.5*poly.min_space - _one_polypad_poly_bb.top
        )

        _zero_polypad_lay = layouter.wire_layout(
            net=zero, wire=contact, bottom=poly, bottom_enclosure="wide",
        )
        _zero_polypad_poly_bb = _zero_polypad_lay.bounds(mask=poly.mask)
        _zero_polypad_ch_bb = _zero_polypad_lay.bounds(mask=contact.mask)
        _zero_polypad_m1_bb = _zero_polypad_lay.bounds(mask=metal1.mask)
        zero_polypad_y = (
            canvas._well_edge_height
            + 0.5*poly.min_space - _zero_polypad_poly_bb.bottom
        )

        # nmos transistor
        act_bottom = n_tap_y + _n_tap_act_bb.top + max(
            active.min_space,
            min_actpoly_space + nmos.computed.min_polyactive_extension,
        )
        act_top = min(
            canvas._well_edge_height - min_actwell_space,
            one_polypad_y + _one_polypad_poly_bb.bottom - min_actpoly_space,
        )
        if canvas._min_contact_active_space is not None:
            act_top = min(
                act_top,
                one_polypad_y + _one_polypad_ch_bb.bottom - canvas._min_contact_active_space,
            )
        n_w = tech.on_grid(act_top - act_bottom, mult=2, rounding="floor")
        n_y = act_bottom + 0.5*n_w
        n_inst = ckt.instantiate(nmos, name="n", l=l, w=n_w)
        vss.childports += (n_inst.ports.bulk, n_inst.ports.sourcedrain1)
        one.childports += n_inst.ports.gate
        zero.childports += n_inst.ports.sourcedrain2
        _n_lay = layouter.inst_layout(inst=n_inst)
        _n_poly_bb = _n_lay.bounds(mask=poly.mask)

        # pmos transistor
        act_bottom = max(
            canvas._well_edge_height + canvas._min_active_well_enclosure,
            zero_polypad_y + _zero_polypad_poly_bb.top + min_actpoly_space,
        )
        if canvas._min_contact_active_space is not None:
            act_bottom = max(
                act_bottom,
                zero_polypad_y + _zero_polypad_ch_bb.top + canvas._min_contact_active_space,
            )
        act_top = p_tap_y + _p_tap_act_bb.bottom - max(
            active.min_space,
            min_actpoly_space + pmos.computed.min_polyactive_extension,
        )
        p_w = tech.on_grid(act_top - act_bottom, mult=2, rounding="floor")
        p_y = act_bottom + 0.5*p_w
        p_inst = ckt.instantiate(pmos, name="p", l=l, w=p_w)
        vdd.childports += (p_inst.ports.bulk, p_inst.ports.sourcedrain2)
        zero.childports += p_inst.ports.gate
        one.childports += p_inst.ports.sourcedrain1
        _p_lay = layouter.inst_layout(inst=p_inst)
        _p_poly_bb = _p_lay.bounds(mask=poly.mask)

        # active contacts
        _n_vssch_lay = layouter.wire_layout(
            net=vss, wire=contact, bottom=active, bottom_implant=nimplant,
            bottom_height=n_w,
        )
        _n_vssch_impl_bb = _n_vssch_lay.bounds(mask=nimplant.mask)
        _n_vssch_cont_bb = _n_vssch_lay.bounds(mask=contact.mask)
        _n_vssch_m1_bb = _n_vssch_lay.bounds(mask=metal1.mask)
        n_vssch_y = n_y
        _n_zeroch_lay = layouter.wire_layout(
            net=zero, wire=contact, bottom=active, bottom_implant=nimplant,
            bottom_height=n_w,
        )
        _n_zeroch_m1_bb = _n_zeroch_lay.bounds(mask=metal1.mask)
        # zeroch m1 needs to keep distance from vssrail
        d = n_y + _n_zeroch_m1_bb.bottom - canvas._m1_vssrail_width - metal1.min_space
        if d > -0.5*tech.grid:
            n_zeroch_y = n_y
        else:
            h = tech.on_grid(_n_zeroch_m1_bb.height + d, mult=2, rounding="floor")
            _n_zeroch_lay = layouter.wire_layout(
                net=zero, wire=contact, bottom=active, bottom_implant=nimplant,
                bottom_height=h, top_height=h,
            )
            _n_zeroch_m1_bb = _n_zeroch_lay.bounds(mask=metal1.mask)
            n_zeroch_y = tech.on_grid(
                canvas._m1_vssrail_width + metal1.min_space - _n_zeroch_m1_bb.bottom
            )
        _n_zeroch_impl_bb = _n_zeroch_lay.bounds(mask=nimplant.mask)
        _n_zeroch_cont_bb = _n_zeroch_lay.bounds(mask=contact.mask)

        _p_vddch_lay = layouter.wire_layout(
            net=vdd, well_net=vdd, wire=contact,
            bottom=active, bottom_implant=pimplant, bottom_well=nwell, bottom_height=p_w,
        )
        _p_vddch_impl_bb = _p_vddch_lay.bounds(mask=pimplant.mask)
        _p_vddch_cont_bb = _p_vddch_lay.bounds(mask=contact.mask)
        _p_vddch_m1_bb = _p_vddch_lay.bounds(mask=metal1.mask)
        p_vddch_y = p_y
        _p_onech_lay = layouter.wire_layout(
            net=one, well_net=vdd, wire=contact,
            bottom=active, bottom_implant=pimplant, bottom_well=nwell, bottom_height=p_w,
        )
        _p_onech_m1_bb = _p_onech_lay.bounds(mask=metal1.mask)
        # zeroch m1 needs to keep distance from vssrail
        d = (
            (canvas._cell_height - canvas._m1_vddrail_width - metal1.min_space)
            - (p_y + _p_onech_m1_bb.top)
        )
        if d > -0.5*tech.grid:
            p_onech_y = p_y
        else:
            h = tech.on_grid(_p_onech_m1_bb.height + d, mult=2, rounding="floor")
            _p_onech_lay = layouter.wire_layout(
                net=one, well_net=vdd, wire=contact,
                bottom=active, bottom_implant=pimplant, bottom_well=nwell,
                bottom_height=h, top_height=h,
            )
            _p_onech_m1_bb = _p_onech_lay.bounds(mask=metal1.mask)
            p_onech_y = tech.on_grid(
                canvas._cell_height - canvas._m1_vddrail_width - metal1.min_space
                - _p_onech_m1_bb.top
            )
        _p_onech_impl_bb = _p_onech_lay.bounds(mask=pimplant.mask)
        _p_onech_cont_bb = _p_onech_lay.bounds(mask=contact.mask)

        # Compute cell_width
        min_width_n = (
            _n_poly_bb.width + 2*nmos.computed.min_contactgate_space
            + (_n_vssch_cont_bb.right - _n_vssch_impl_bb.left)
            + (_n_zeroch_impl_bb.right - _n_zeroch_cont_bb.left)
            + nimplant.min_space
        )
        min_width_p = (
            _p_poly_bb.width + 2*pmos.computed.min_contactgate_space
            + (_p_onech_cont_bb.right - _p_onech_impl_bb.left)
            + (_p_vddch_impl_bb.right - _p_vddch_cont_bb.left)
            + pimplant.min_space
        )
        min_width_pin = 2*canvas._pin_width + 2*metal1.min_space
        cell_width = self.set_width(min_width=max(min_width_n, min_width_p, min_width_pin))

        # Place and connect the elements
        n_tap_x = p_tap_x = 0.5*cell_width
        layouter.place(object_=_n_tap_lay, x=n_tap_x, y=n_tap_y)
        layouter.place(object_=_p_tap_lay, x=p_tap_x, y=p_tap_y)

        n_x = p_x = 0.5*cell_width
        n_lay = layouter.place(_n_lay, x=n_x, y=n_y)
        n_act_bb = n_lay.bounds(mask=active.mask)
        n_poly_bb = n_lay.bounds(mask=poly.mask)
        p_lay = layouter.place(_p_lay, x=p_x, y=p_y)
        p_act_bb = p_lay.bounds(mask=active.mask)
        p_poly_bb = p_lay.bounds(mask=poly.mask)

        n_vssch_x = (
            n_poly_bb.left - nmos.computed.min_contactgate_space - _n_vssch_cont_bb.right
        )
        n_zeroch_x = (
            n_poly_bb.right + nmos.computed.min_contactgate_space - _n_zeroch_cont_bb.left
        )
        p_onech_x = (
            p_poly_bb.left - pmos.computed.min_contactgate_space - _p_onech_cont_bb.right
        )
        p_vddch_x = (
            p_poly_bb.right + pmos.computed.min_contactgate_space - _p_vddch_cont_bb.left
        )

        zero_polypad_x = (
            n_zeroch_x + _n_zeroch_m1_bb.left - _zero_polypad_m1_bb.left
        )
        zero_polypad_lay = layouter.place(object_=_zero_polypad_lay, x=zero_polypad_x, y=zero_polypad_y)
        zero_polypad_poly_bb = zero_polypad_lay.bounds(mask=poly.mask)
        zero_polypad_m1_bb = zero_polypad_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=zero, wire=poly, shape=_geo.Rect.from_rect(
            rect=zero_polypad_poly_bb, left=p_poly_bb.left,
        ))
        layouter.add_wire(net=zero, wire=poly, shape=_geo.Rect.from_rect(
            rect=p_poly_bb, bottom=zero_polypad_poly_bb.bottom,
        ))

        one_polypad_x = (
            p_onech_x + _p_onech_m1_bb.right - _one_polypad_m1_bb.right
        )
        one_polypad_lay = layouter.place(object_=_one_polypad_lay, x=one_polypad_x, y=one_polypad_y)
        one_polypad_poly_bb = one_polypad_lay.bounds(mask=poly.mask)
        one_polypad_m1_bb = one_polypad_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=one, wire=poly, shape=_geo.Rect.from_rect(
            rect=one_polypad_poly_bb, right=p_poly_bb.right,
        ))
        layouter.add_wire(net=one, wire=poly, shape=_geo.Rect.from_rect(
            rect=n_poly_bb, top=one_polypad_poly_bb.top,
        ))

        # Reduce # contacts for vss if m1 is too close too polypad m1
        d = one_polypad_m1_bb.bottom - (n_vssch_y + _n_vssch_m1_bb.top + metal1.min_space)
        if d < -0.5*tech.grid:
            h = tech.on_grid(_n_vssch_m1_bb.height + d, mult=2, rounding="floor")
            _n_vssch_lay = layouter.wire_layout(
                net=vss, wire=contact, bottom=active, bottom_implant=nimplant,
                bottom_height=h, top_height=h,
            )
            _n_vssch_act_bb = _n_vssch_lay.bounds(mask=active.mask)
            # Align active with active of transistor
            n_vssch_y = tech.on_grid(n_act_bb.bottom - _n_vssch_act_bb.bottom)
        n_vssch_lay = layouter.place(object_=_n_vssch_lay, x=n_vssch_x, y=n_vssch_y)
        n_vssch_act_bb = n_vssch_lay.bounds(mask=active.mask)
        n_vssch_m1_bb = n_vssch_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=vss, wire=active, implant=nimplant, shape=_geo.Rect.from_rect(
            rect=n_vssch_act_bb, bottom=n_act_bb.bottom, top=n_act_bb.top,
        ))
        layouter.add_wire(net=vss, wire=metal1, shape=_geo.Rect.from_rect(
            rect=n_vssch_m1_bb, bottom=0.0,
        ))
        n_zeroch_lay = layouter.place(object_=_n_zeroch_lay, x=n_zeroch_x, y=n_zeroch_y)
        n_zeroch_act_bb = n_zeroch_lay.bounds(mask=active.mask)
        n_zeroch_m1_bb = n_zeroch_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=zero, wire=active, implant=nimplant, shape=_geo.Rect.from_rect(
            rect=n_zeroch_act_bb, bottom=n_act_bb.bottom, top=n_act_bb.top,
        ))

        p_onech_lay = layouter.place(_p_onech_lay, x=p_onech_x, y=p_onech_y)
        p_onech_act_bb = p_onech_lay.bounds(mask=active.mask)
        p_onech_m1_bb = p_onech_lay.bounds(mask=metal1.mask)
        layouter.add_wire(
            net=one, well_net=vdd, wire=active, implant=pimplant, well=nwell,
            shape=_geo.Rect.from_rect(
                rect=p_onech_act_bb, bottom=p_act_bb.bottom, top=p_act_bb.top,
            ),
        )
        # Reduce # contacts for vdd if m1 is too close too polypad m1
        d = (p_vddch_y + _p_vddch_m1_bb.bottom - metal1.min_space) - zero_polypad_m1_bb.top
        if d < -0.5*tech.grid:
            h = tech.on_grid(_p_vddch_m1_bb.height + d, mult=2, rounding="floor")
            _p_vddch_lay = layouter.wire_layout(
                net=vss, well_net=vdd, wire=contact,
                bottom=active, bottom_implant=pimplant, bottom_well=nwell,
                bottom_height=h, top_height=h,
            )
            _p_vddch_act_bb = _p_vddch_lay.bounds(mask=active.mask)
            # Align active with active of transistor
            p_vddch_y = tech.on_grid(p_act_bb.top - _p_vddch_act_bb.top)
        p_vddch_lay = layouter.place(_p_vddch_lay, x=p_vddch_x, y=p_vddch_y)
        p_vddch_act_bb = p_vddch_lay.bounds(mask=active.mask)
        p_vddch_m1_bb = p_vddch_lay.bounds(mask=metal1.mask)
        layouter.add_wire(
            net=vdd, well_net=vdd, wire=active, implant=pimplant, well=nwell,
            shape=_geo.Rect.from_rect(
                rect=p_vddch_act_bb, bottom=p_act_bb.bottom, top=p_act_bb.top,
            ),
        )
        layouter.add_wire(net=vdd, wire=metal1, shape=_geo.Rect.from_rect(
            rect=p_vddch_m1_bb, top=canvas._cell_height,
        ))

        if (
            (cell_width - (n_zeroch_m1_bb.left + canvas._pin_width + 0.5*metal1.min_space))
            >= -0.5*tech.grid
        ):
            right = n_zeroch_x + _n_zeroch_m1_bb.left + canvas._pin_width
            top = zero_polypad_m1_bb.top
            shape=_geo.Rect.from_rect(rect=n_zeroch_m1_bb, right=right, top=top)
        else:
            left = 0.5*cell_width + 0.5*metal1.min_space
            right = left + canvas._pin_width
            bottom = n_zeroch_m1_bb.bottom
            top = zero_polypad_m1_bb.top
            shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
        pin = None if not zero_pin else metal1pin
        layouter.add_wire(net=zero, wire=metal1, pin=pin, shape=shape)
        if (p_onech_m1_bb.right - canvas._pin_width - 0.5*metal1.min_space) >= -0.5*tech.grid:
            left = p_onech_m1_bb.right - canvas._pin_width
            bottom = one_polypad_m1_bb.bottom
            shape = _geo.Rect.from_rect(rect=p_onech_m1_bb, left=left, bottom=bottom)
        else:
            right = 0.5*cell_width - 0.5*metal1.min_space
            left = right - canvas._pin_width
            bottom = p_onech_m1_bb.bottom
            top = one_polypad_m1_bb.top
            shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
        pin = None if not one_pin else metal1pin
        layouter.add_wire(net=one, wire=metal1, pin=pin, shape=shape)


class _Inv(_Cell):
    """Parameterized inverter.
    """
    def __init__(self, *,
        fab: "StdCellFactory", name: str,
        w_n: float, w_p: Optional[float]=None, fingers: int=1, balanced: bool=True,
    ):
        canvas = fab.canvas

        if w_p is None:
            if not balanced:
                raise ValueError(
                    "Either specify pmos transistor width or balanced has to be True"
                )
            w_p = w_n*canvas._balancedmos_w_ratio

        if fingers < 1:
            raise ValueError(f"finger has to greater than 0, not {fingers}")

        super().__init__(fab=fab, name=name)

        tech = fab.tech

        ckt = self.circuit
        layouter = self._layouter

        nmos = canvas.nmos
        pmos = canvas.pmos
        l = canvas.l
        active = canvas._active
        nimplant = canvas._nimplant
        pimplant = canvas._pimplant
        nwell = canvas._nwell
        poly = canvas._poly
        contact = canvas._contact
        metal1 = canvas._metal1
        metal1pin = canvas._metal1pin

        #
        # circuit
        #
        if fingers == 1:
            n_insts = (ckt.instantiate(nmos, name="n", l=l, w=w_n),)
            p_insts = (ckt.instantiate(pmos, name="p", l=l, w=w_p),)
        else:
            n_insts = tuple(
                ckt.instantiate(nmos, name=f"n{i}", l=l, w=w_n)
                for i in range(fingers)
            )
            p_insts = tuple(
                ckt.instantiate(pmos, name=f"p{i}", l=l, w=w_p)
                for i in range(fingers)
            )

        vdd = ckt.nets.vdd
        vdd.childports += (
            *(
                p_insts[i].ports.sourcedrain1 if i%2 == 0 else p_insts[i].ports.sourcedrain2
                for i in range(fingers)
            ),
            *(p_insts[i].ports.bulk for i in range(fingers)),
        )
        vss = ckt.nets.vss
        vss.childports += (
            *(
                n_insts[i].ports.sourcedrain1 if i%2 == 0 else n_insts[i].ports.sourcedrain2
                for i in range(fingers)
            ),
            *(n_insts[i].ports.bulk for i in range(fingers)),
        )

        i_ = ckt.new_net(name="i", external=True, childports=(
            *(n_insts[i].ports.gate for i in range(fingers)),
            *(p_insts[i].ports.gate for i in range(fingers)),
        ))
        nq = ckt.new_net(name="nq", external=True, childports=(
            *(
                n_insts[i].ports.sourcedrain2 if i%2 == 0 else n_insts[i].ports.sourcedrain1
                for i in range(fingers)
            ),
            *(
                p_insts[i].ports.sourcedrain2 if i%2 == 0 else p_insts[i].ports.sourcedrain1
                for i in range(fingers)
            ),
        ))

        #
        # layout
        #
        min_actpoly_space = tech.computed.min_space(primitive1=active, primitive2=poly)

        # i
        # m1 pin
        left = metal1.min_space # Leave a little more space than minimal
        right = left + canvas._pin_width
        bottom = canvas._m1_vssrail_width + metal1.min_space
        top = canvas._cell_height - canvas._m1_vddrail_width - metal1.min_space
        layouter.add_wire(net=i_, wire=metal1, pin=metal1pin, shape=_geo.Rect(
            left=left, bottom=bottom, right=right, top=top,
        ))
        x = right # Set x to edge of metal1 line
        y = canvas._well_edge_height
        # poly ch
        i_ch = layouter.add_wire(net=i_, wire=contact, bottom=poly, x=x, y=y)
        i_ch_poly_bb = i_ch.bounds(mask=poly.mask)
        i_ch_m1_bb = i_ch.bounds(mask=metal1.mask)

        # First vss contact
        l_ch = layouter.wire_layout(
            net=vss, wire=contact, bottom=active, bottom_implant=nimplant,
            top_enclosure="wide",
        )
        impl_bb = l_ch.bounds(mask=nimplant.mask)
        m1_bb = l_ch.bounds(mask=metal1.mask)
        n_vssch_x = 0.5*nimplant.min_space - impl_bb.left
        n_vssch_y = canvas._m1_vssrail_width - m1_bb.top
        n_vssch_lay = layouter.place(l_ch, x=n_vssch_x, y=n_vssch_y)
        n_vssch_act_bb = n_vssch_lay.bounds(mask=active.mask)

        # First vdd contact
        l_ch = layouter.wire_layout(
            net=vdd, well_net=vdd, wire=contact,
            bottom=active, bottom_implant=pimplant, bottom_well=nwell,
            top_enclosure="wide",
        )
        impl_bb = l_ch.bounds(mask=pimplant.mask)
        m1_bb = l_ch.bounds(mask=metal1.mask)
        p_vddch_x = 0.5*pimplant.min_space - impl_bb.left
        p_vddch_y = canvas._cell_height - canvas._m1_vddrail_width - m1_bb.bottom
        p_vddch_lay = layouter.place(l_ch, x=p_vddch_x, y=p_vddch_y)
        p_vddch_act_bb = p_vddch_lay.bounds(mask=active.mask)

        poly_left = max(
            n_vssch_act_bb.right + min_actpoly_space,
            p_vddch_act_bb.right + min_actpoly_space,
            i_ch_poly_bb.right,
        )
        poly_right = None
        min_cellwidth = None

        n_y = n_nqch_y = p_y = p_nqch_y = None
        n_nqch_m1_height = None
        p_nqch_m1_height = None
        nq_m1_left = nq_m1_right = None
        for i, n_inst in enumerate(n_insts):
            p_inst = p_insts[i]

            # transistor
            _n_lay = layouter.inst_layout(inst=n_inst)
            _p_lay = layouter.inst_layout(inst=p_inst)

            # Put all transistor at same height, compute height first time
            if i == 0:
                _n_nqch_lay = layouter.wire_layout(
                    net=nq, wire=contact, bottom=active, bottom_implant=nimplant,
                    bottom_height=w_n
                )
                _n_nqch_m1_bb = _n_nqch_lay.bounds(mask=metal1.mask)
                n_nqch_m1_height = _n_nqch_m1_bb.height
                _p_nqch_lay = layouter.wire_layout(
                    net=nq, well_net=vdd, wire=contact,
                    bottom=active, bottom_implant=pimplant, bottom_well=nwell,
                    bottom_height=w_p,
                )
                _p_nqch_m1_bb = _p_nqch_lay.bounds(mask=metal1.mask)
                p_nqch_m1_height = _p_nqch_m1_bb.height

                n_y = canvas._m1_vssrail_width + metal1.min_space - _n_nqch_m1_bb.bottom
                s = canvas._well_edge_height - (n_y + 0.5*w_n)
                min_s = tech.computed.min_space(primitive1=active, primitive2=nwell)
                assert (min_s is None) or (s >= min_s)
                n_nqch_y = n_y

                p_y = canvas._cell_height - (canvas._m1_vssrail_width + metal1.min_space) - _p_nqch_m1_bb.top
                # Check if nwell bottom is too low
                _p_nwell_bb = _p_lay.bounds(mask=nwell.mask)
                d = (_p_nwell_bb.bottom + p_y) - canvas._well_edge_height
                if d < 0.0:
                    # Move up and reduce number of contacts
                    p_y -= d
                # Check if metal1 of nqch top is too high
                d = (
                    (canvas._cell_height - canvas._m1_vddrail_width)
                    - (_p_nqch_m1_bb.top + p_y)
                    - metal1.min_space
                )
                if tech.on_grid(d) >= 0.0:
                    p_nqch_y = p_y
                else:
                    # Reduce number of contacts of p_nqch
                    p_nqch_m1_height = tech.on_grid(
                        _p_nqch_m1_bb.height + d, mult=2, rounding="floor",
                    )
                    p_nqch_y = (
                        canvas._cell_height - canvas._m1_vddrail_width - metal1.min_space
                        - 0.5*p_nqch_m1_height
                    )
            assert n_y is not None
            assert n_nqch_y is not None
            assert p_y is not None
            assert p_nqch_y is not None
            assert n_nqch_m1_height is not None
            assert p_nqch_m1_height is not None

            _n_poly_bb = _n_lay.bounds(mask=poly.mask)
            n_x = poly_left - _n_poly_bb.left
            n_lay = layouter.place(object_=_n_lay, x=n_x, y=n_y)
            n_act_bb = n_lay.bounds(mask=active.mask)
            n_poly_bb = n_lay.bounds(mask=poly.mask)

            _p_poly_bb = _p_lay.bounds(mask=poly.mask)
            p_x = poly_left - _p_poly_bb.left
            p_lay = layouter.place(object_=_p_lay, x=p_x, y=p_y)
            p_act_bb = p_lay.bounds(mask=active.mask)
            p_poly_bb = p_lay.bounds(mask=poly.mask)

            left = min(n_poly_bb.left, p_poly_bb.left)
            poly_right = right = max(n_poly_bb.right, p_poly_bb.right)
            bottom = n_poly_bb.top
            top = p_poly_bb.bottom
            layouter.add_wire(net=i_, wire=poly, shape=_geo.Rect(
                left=left, bottom=bottom, right=right, top=top,
            ))

            # For first transistor draw active for first vdd/vss contact
            if i == 0:
                bottom = min(n_vssch_act_bb.bottom, n_act_bb.bottom)
                top = max(n_vssch_act_bb.top, n_act_bb.top)
                layouter.add_wire(
                    net=vss, wire=active, implant=nimplant,
                    shape=_geo.Rect.from_rect(rect=n_vssch_act_bb, bottom=bottom, top=top),
                )

                bottom = min(p_vddch_act_bb.bottom, p_act_bb.bottom)
                top = max(p_vddch_act_bb.top, p_act_bb.top)
                layouter.add_wire(
                    net=vdd, well_net=vdd, wire=active, implant=pimplant, well=nwell,
                    shape=_geo.Rect.from_rect(rect=n_vssch_act_bb, bottom=bottom, top=top),
                )

            if i%2 == 0:
                # We regenerate n_nqch and p_nqch also for i == 0 on purpose
                # this is to treat all of them in the same way
                _n_nqch_lay = layouter.wire_layout(
                    net=nq, wire=contact, bottom=active, bottom_implant=nimplant,
                    top_height = n_nqch_m1_height,
                )
                _p_nqch_lay = layouter.wire_layout(
                    net=nq, well_net=vdd, wire=contact,
                    bottom=active, bottom_implant=pimplant, bottom_well=nwell,
                    top_height=p_nqch_m1_height,
                )

                _n_nqch_cont_bb = _n_nqch_lay.bounds(mask=contact.mask)
                n_nqch_x = n_poly_bb.right + nmos.computed.min_contactgate_space - _n_nqch_cont_bb.left
                n_nqch_lay = layouter.place(object_=_n_nqch_lay, x=n_nqch_x, y=n_nqch_y)
                n_nqch_act_bb = n_nqch_lay.bounds(mask=active.mask)
                n_nqch_impl_bb = n_nqch_lay.bounds(mask=nimplant.mask)
                n_nqch_cont_bb = n_nqch_lay.bounds(mask=contact.mask)
                n_nqch_m1_bb = n_nqch_lay.bounds(mask=metal1.mask)
                layouter.add_wire(
                    net=nq, wire=active, implant=nimplant, shape=_geo.Rect.from_rect(
                        rect=n_nqch_act_bb, bottom=n_act_bb.bottom, top=n_act_bb.top,
                    ),
                )

                _p_nqch_cont_bb = _p_nqch_lay.bounds(mask=contact.mask)
                p_nqch_x = p_poly_bb.right + pmos.computed.min_contactgate_space - _p_nqch_cont_bb.left
                p_nqch_lay = layouter.place(object_=_p_nqch_lay, x=p_nqch_x, y=p_nqch_y)
                p_nqch_act_bb = p_nqch_lay.bounds(mask=active.mask)
                p_nqch_impl_bb = p_nqch_lay.bounds(mask=pimplant.mask)
                p_nqch_cont_bb = p_nqch_lay.bounds(mask=contact.mask)
                p_nqch_m1_bb = p_nqch_lay.bounds(mask=metal1.mask)
                layouter.add_wire(
                    net=nq, well_net=vdd, wire=active, implant=pimplant, well=nwell,
                    shape=_geo.Rect.from_rect(
                        rect=p_nqch_act_bb, bottom=p_act_bb.bottom, top=p_act_bb.top,
                    ),
                )

                # nq
                bottom = n_nqch_m1_bb.bottom
                left = min(n_nqch_m1_bb.left, p_nqch_m1_bb.left)
                nq_m1_right = right = max(n_nqch_m1_bb.right, p_nqch_m1_bb.right)
                pin_args = {}
                if i == 0:
                    # Draw pin, keep distance from m1 on signal i
                    nq_m1_left = left = max(left, i_ch_m1_bb.right + metal1.min_space)
                    nq_m1_right = right = left + canvas._pin_width
                    pin_args = {"pin": metal1pin}
                top = p_nqch_m1_bb.top
                layouter.add_wire(net=nq, wire=metal1, **pin_args, shape=_geo.Rect(
                    left=left, bottom=bottom, right=right, top=top,
                ))

                poly_left = max(
                    n_nqch_cont_bb.right + nmos.computed.min_contactgate_space,
                    p_nqch_cont_bb.right + pmos.computed.min_contactgate_space,
                )
                min_cellwidth = max(
                    n_nqch_impl_bb.right + 0.5*nimplant.min_space,
                    p_nqch_impl_bb.right + 0.5*pimplant.min_space,
                )
            else:
                # vdd/vss contact
                l_ch = layouter.wire_layout(
                    net=vss, wire=contact, bottom=active, bottom_implant=nimplant,
                    top_enclosure="wide",
                )
                act_bb = l_ch.bounds(mask=active.mask)
                n_vssch_x = poly_right + min_actpoly_space - act_bb.left
                n_vssch_lay = layouter.place(l_ch, x=n_vssch_x, y=n_vssch_y)
                n_vssch_impl_bb = n_vssch_lay.bounds(mask=nimplant.mask)
                n_vssch_act_bb = n_vssch_lay.bounds(mask=active.mask)

                bottom = min(n_act_bb.bottom, n_vssch_act_bb.bottom)
                top= max(n_act_bb.top, n_vssch_act_bb.top)
                layouter.add_wire(
                    net=vss, wire=active, implant=nimplant,
                    shape=_geo.Rect.from_rect(rect=n_vssch_act_bb, bottom=bottom, top=top),
                )

                l_ch = layouter.wire_layout(
                    net=vdd, well_net=vdd, wire=contact,
                    bottom=active, bottom_implant=pimplant, bottom_well=nwell,
                    top_enclosure="wide",
                )
                act_bb = l_ch.bounds(mask=active.mask)
                p_vddch_x = poly_right + min_actpoly_space - act_bb.left
                p_vddch_lay = layouter.place(l_ch, x=p_vddch_x, y=p_vddch_y)
                p_vddch_impl_bb = p_vddch_lay.bounds(mask=active.mask)
                p_vddch_act_bb = p_vddch_lay.bounds(mask=active.mask)

                bottom = min(p_act_bb.bottom, p_vddch_act_bb.bottom)
                top= max(p_act_bb.top, p_vddch_act_bb.top)
                layouter.add_wire(
                    net=vdd, well_net=vdd, wire=active, implant=pimplant, well=nwell,
                    shape=_geo.Rect.from_rect(rect=p_vddch_act_bb, bottom=bottom, top=top),
                )

                poly_left = max(n_vssch_act_bb.right, p_vddch_act_bb.right) + min_actpoly_space
                min_cellwidth = max(
                    n_vssch_impl_bb.right + 0.5*nimplant.min_space,
                    p_vddch_impl_bb.right + 0.5*pimplant.min_space,
                )
        assert poly_right is not None
        assert min_cellwidth is not None

        # Determine cell_width
        cell_width = self.set_width(min_width=min_cellwidth)

        # Draw i horizontal poly connection
        if poly_right > i_ch_poly_bb.right:
            layouter.add_wire(net=i_, wire=poly, shape=_geo.Rect.from_rect(
                rect=i_ch_poly_bb, right=poly_right,
            ))

        # Draw nq horizontal metal1 connection
        if fingers > 2:
            assert nq_m1_left is not None
            assert nq_m1_right is not None
            left = nq_m1_left
            right = nq_m1_right
            bottom = canvas._well_edge_height - 0.5*canvas._pin_width
            top = bottom + canvas._pin_width
            layouter.add_wire(net=nq, wire=metal1, shape=_geo.Rect(
                left=left, bottom=bottom, right=right, top=top,
            ))

        # builk/well contacts
        l_ch = layouter.wire_layout(
            net=vss, wire=contact, bottom=active, bottom_implant=pimplant,
            columns=canvas._min_tap_chs, bottom_enclosure="wide",
        )
        impl_bb = l_ch.bounds(mask=pimplant.mask)
        x = cell_width - 0.5*pimplant.min_space - impl_bb.right
        y = 0.5*pimplant.min_space - impl_bb.bottom
        layouter.place(l_ch, x=x, y=y)

        l_ch = layouter.wire_layout(
            net=vdd, well_net=vdd, wire=contact,
            bottom=active, bottom_implant=nimplant, bottom_well=nwell,
            columns=canvas._min_tap_chs, bottom_enclosure="wide",
        )
        impl_bb = l_ch.bounds(mask=nimplant.mask)
        x = cell_width - 0.5*nimplant.min_space - impl_bb.right
        y = canvas._cell_height - 0.5*nimplant.min_space - impl_bb.top
        layouter.place(l_ch, x=x, y=y)


class _Buf(_Cell):
    """Parameterized buffer"""
    def __init__(self, *,
        fab: "StdCellFactory", name: str,
        w_ns: Tuple[float, Union[float, Tuple[float, int]]],
    ):
        if isinstance(w_ns[1], tuple):
            fingers = w_ns[1][1]
            w_ns = (w_ns[0], w_ns[1][0])
        else:
            fingers = 1
            w_ns = cast(Tuple[float, float], w_ns) # Help typing

        super().__init__(fab=fab, name=name)

        tech = fab.tech
        canvas = fab.canvas
        ckt = self.circuit
        layouter = self._layouter

        nmos = canvas._nmos
        pmos = canvas._pmos
        l = canvas.l

        nwell = canvas._nwell
        active = canvas._active
        nimplant = canvas._nimplant
        pimplant = canvas._pimplant
        poly = canvas._poly
        contact = canvas._contact
        metal1 = canvas._metal1
        metal1pin = canvas._metal1pin

        w_ps = tuple(canvas._balancedmos_w_ratio*w_n for w_n in w_ns)

        # Create the transistor instances
        n1 = ckt.instantiate(nmos, name="n1", l=l, w=w_ns[0])
        n2s = tuple(
            ckt.instantiate(nmos, name=f"n2_{i}", l=l, w=w_ns[1])
            for i in range(fingers)
        )
        p1 = ckt.instantiate(pmos, name="p1", l=l, w=w_ps[0])
        p2s = tuple(
            ckt.instantiate(pmos, name=f"p2_{i}", l=l, w=w_ps[1])
            for i in range(fingers)
        )

        # setup the nets
        vdd = ckt.nets.vdd
        vdd.childports += (
            p1.ports.bulk, p1.ports.sourcedrain2,
            *(p2.ports.bulk for p2 in p2s),
            *(
                p2.ports.sourcedrain1 if (i%2 == 0) else p2.ports.sourcedrain2
                for i, p2 in enumerate(p2s)
            ),
        )
        vss = ckt.nets.vss
        vss.childports += (
            n1.ports.bulk, n1.ports.sourcedrain2,
            *(n2.ports.bulk for n2 in n2s),
            *(
                n2.ports.sourcedrain1 if (i%2 == 0) else n2.ports.sourcedrain2
                for i, n2 in enumerate(n2s)
            ),
        )

        i_ = ckt.new_net(name="i", external=True, childports=(
            n1.ports.gate, p1.ports.gate,
        ))
        ni = ckt.new_net(name="ni", external=False, childports=(
            n1.ports.sourcedrain1, p1.ports.sourcedrain1,
            *(n2.ports.gate for n2 in n2s), *(p2.ports.gate for p2 in p2s),
        ))
        q = ckt.new_net(name="q", external=True, childports=(
            *(
                n2.ports.sourcedrain2 if (i%2 == 0) else n2.ports.sourcedrain1
                for i, n2 in enumerate(n2s)
            ),
            *(
                p2.ports.sourcedrain2 if (i%2 == 0) else p2.ports.sourcedrain1
                for i, p2 in enumerate(p2s)
            ),
        ))

        # layout
        min_actpoly_space = tech.computed.min_space(primitive1=active, primitive2=poly)

        # transistor layouts
        _n1_lay = layouter.inst_layout(inst=n1)
        _n1_act_bb = _n1_lay.bounds(mask=active.mask)
        _n1_poly_bb = _n1_lay.bounds(mask=poly.mask)
        _n2_lays = tuple(layouter.inst_layout(inst=n2) for n2 in n2s)
        _n2_act_bb = _n2_lays[0].bounds(mask=active.mask)
        _n2_poly_bb = _n2_lays[0].bounds(mask=poly.mask)
        _p1_lay = layouter.inst_layout(inst=p1)
        _p1_act_bb = _p1_lay.bounds(mask=active.mask)
        _p1_poly_bb = _p1_lay.bounds(mask=poly.mask)
        _p2_lays = tuple(layouter.inst_layout(inst=p2) for p2 in p2s)
        _p2_act_bb = _p2_lays[0].bounds(mask=active.mask)
        _p2_poly_bb = _p2_lays[0].bounds(mask=poly.mask)

        # Middle vss/vdd contact
        _n_vssch_lay = layouter.wire_layout(
            net=vss, wire=contact, bottom=active, bottom_implant=nimplant,
            top_enclosure="wide",
        )
        _n_vssch_act_bb = _n_vssch_lay.bounds(mask=active.mask)
        _n_vssch_m1_bb = _n_vssch_lay.bounds(mask=metal1.mask)
        _p_vddch_lay = layouter.wire_layout(
            net=vdd, well_net=vdd, wire=contact,
            bottom=active, bottom_implant=pimplant, bottom_well=nwell,
            top_enclosure="wide",
        )
        _p_vddch_act_bb = _p_vddch_lay.bounds(mask=active.mask)
        _p_vddch_m1_bb = _p_vddch_lay.bounds(mask=metal1.mask)

        # Compute vertical alignment
        n_vssch_y = canvas._m1_vssrail_width - _n_vssch_m1_bb.top
        n2_y = (_n_vssch_act_bb.bottom + n_vssch_y) - _n2_act_bb.bottom
        n1_y = (_n2_act_bb.top + n2_y) - _n1_act_bb.top

        p_vddch_y = (canvas._cell_height - canvas._m1_vddrail_width) - _p_vddch_m1_bb.bottom
        p2_y = (_p_vddch_act_bb.top + p_vddch_y) - _p2_act_bb.top
        p1_y = (_p2_act_bb.bottom + p2_y) - _p1_act_bb.bottom

        # Left ni contacts
        _n_nich_lay = layouter.wire_layout(
            net=ni, wire=contact, bottom=active, bottom_implant=nimplant,
            bottom_height=w_ns[0], top_height=w_ns[0],
        )
        _n_nich_nimpl_bb = _n_nich_lay.bounds(mask=nimplant.mask)
        _n_nich_act_bb = _n_nich_lay.bounds(mask=active.mask)
        _n_nich_m1_bb = _n_nich_lay.bounds(mask=metal1.mask)
        n_nich_x = 0.5*nimplant.min_space - _n_nich_nimpl_bb.left
        n_nich_y = (_n1_act_bb.top + n1_y) - _n_nich_act_bb.top
        d = tech.on_grid(
            (n_nich_y - 0.5*w_ns[0]) - (canvas._m1_vssrail_width + metal1.min_space),
            mult=2, rounding="floor"
        )
        if d < 0:
            h = w_ns[0] + d
            _n_nich_lay = layouter.wire_layout(
                net=ni, wire=contact, bottom=active, bottom_implant=nimplant,
                bottom_height=h, top_height=h,
            )
            _n_nich_act_bb = _n_nich_lay.bounds(mask=active.mask)
            n_nich_y = (_n1_act_bb.top + n1_y) - _n_nich_act_bb.top
        n_nich_lay = layouter.place(object_=_n_nich_lay, x=n_nich_x, y=n_nich_y)
        n_nich_cont_bb = n_nich_lay.bounds(mask=contact.mask)
        n_nich_m1_bb = n_nich_lay.bounds(mask=metal1.mask)


        _p_nich_lay = layouter.wire_layout(
            net=ni, well_net=vdd, wire=contact,
            bottom=active, bottom_implant=pimplant, bottom_well=nwell,
            bottom_height=w_ps[0], top_height=w_ps[0],
        )
        _p_nich_pimpl_bb = _p_nich_lay.bounds(mask=pimplant.mask)
        _p_nich_act_bb = _p_nich_lay.bounds(mask=active.mask)
        _p_nich_m1_bb = _p_nich_lay.bounds(mask=metal1.mask)
        p_nich_x = 0.5*pimplant.min_space - _p_nich_pimpl_bb.left
        p_nich_y = (_p1_act_bb.bottom + p1_y) - _p_nich_act_bb.bottom
        d = tech.on_grid(
            (canvas._cell_height - canvas._m1_vddrail_width - metal1.min_space)
            - (p_nich_y + 0.5*w_ps[0]),
            mult=2, rounding="floor",
        )
        if d < 0:
            h = w_ps[0] + d
            _p_nich_lay = layouter.wire_layout(
                net=ni, well_net=vdd, wire=contact,
                bottom=active, bottom_implant=pimplant, bottom_well=nwell,
                bottom_height=h, top_height=h,
            )
            _p_nich_act_bb = _p_nich_lay.bounds(mask=active.mask)
            p_nich_y = (_p1_act_bb.bottom + p1_y) - _p_nich_act_bb.bottom
        p_nich_lay = layouter.place(_p_nich_lay, x=p_nich_x, y=p_nich_y)
        p_nich_cont_bb = p_nich_lay.bounds(mask=contact.mask)
        p_nich_m1_bb = p_nich_lay.bounds(mask=metal1.mask)

        nim1_lay = layouter.add_wire(
            net=ni, wire=metal1, shape=_geo.Rect.from_rect(
                rect=n_nich_m1_bb, top=p_nich_m1_bb.top,
            )
        )
        nim1_bb = nim1_lay.bounds()

        # place n1/p1
        poly_left = max(
            n_nich_cont_bb.right + nmos.computed.min_contactgate_space,
            p_nich_cont_bb.right + pmos.computed.min_contactgate_space,
        )
        n1_x = poly_left - _n1_poly_bb.left
        n1_lay = layouter.place(object_=_n1_lay, x=n1_x, y=n1_y)
        n1_act_bb = n1_lay.bounds(mask=active.mask)
        n1_poly_bb = n1_lay.bounds(mask=poly.mask)
        p1_x = poly_left - _p1_poly_bb.left
        p1_lay = layouter.place(object_=_p1_lay, x=p1_x, y=p1_y)
        p1_act_bb = p1_lay.bounds(mask=active.mask)
        p1_poly_bb = p1_lay.bounds(mask=poly.mask)

        # draw i ch pads
        _n_ichppad_lay = layouter.wire_layout(
            net=i_, wire=contact, bottom=poly,
            bottom_enclosure="wide", top_enclosure="tall",
        )
        _n_ichppad_poly_bb = _n_ichppad_lay.bounds(mask=poly.mask)
        _n_ichppad_ch_bb = _n_ichppad_lay.bounds(mask=contact.mask)
        _n_ichppad_m1_bb = _n_ichppad_lay.bounds(mask=metal1.mask)
        n_ichppad_x = max(
            _n1_poly_bb.left - _n_ichppad_m1_bb.left,
            (nim1_bb.right + metal1.min_space) - _n_ichppad_m1_bb.left,
        )
        n_ichppad_y = n1_act_bb.top + min_actpoly_space - _n_ichppad_poly_bb.bottom
        if canvas._min_contact_active_space is not None:
            n_ichppad_y = max(
                n_ichppad_y,
                n1_act_bb.top + canvas._min_contact_active_space - _n_ichppad_ch_bb.bottom,
            )
        n_ichppad_lay = layouter.place(_n_ichppad_lay, x=n_ichppad_x, y=n_ichppad_y)
        n_ichppad_poly_bb = n_ichppad_lay.bounds(mask=poly.mask)
        n_ichppad_m1_bb = n_ichppad_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=i_, wire=poly, shape=_geo.Rect.from_rect(
            rect=n1_poly_bb, top=n_ichppad_poly_bb.top,
        ))
        if n_ichppad_poly_bb.left > n1_poly_bb.left:
            layouter.add_wire(net=i_, wire=poly, shape=_geo.Rect.from_rect(
                rect=n_ichppad_poly_bb, left=n1_poly_bb.left
            ))

        _p_ichppad_lay = layouter.wire_layout(
            net=i_, wire=contact, bottom=poly,
            bottom_enclosure="wide", top_enclosure="tall",
        )
        _p_ichppad_poly_bb = _p_ichppad_lay.bounds(mask=poly.mask)
        _p_ichppad_ch_bb = _p_ichppad_lay.bounds(mask=contact.mask)
        _p_ichppad_m1_bb = _p_ichppad_lay.bounds(mask=metal1.mask)
        p_ichppad_x = max(
            _p1_poly_bb.left - _p_ichppad_m1_bb.left,
            (nim1_bb.right + metal1.min_space) - _p_ichppad_m1_bb.left,
        )
        p_ichppad_y = p1_act_bb.bottom - min_actpoly_space - _p_ichppad_poly_bb.top
        if canvas._min_contact_active_space is not None:
            p_ichppad_y = min(
                p_ichppad_y,
                p1_act_bb.bottom - canvas._min_contact_active_space - _p_ichppad_ch_bb.top,
            )
        p_ichppad_lay = layouter.place(_p_ichppad_lay, x=p_ichppad_x, y=p_ichppad_y)
        p_ichppad_poly_bb = p_ichppad_lay.bounds(mask=poly.mask)
        p_ichppad_m1_bb = p_ichppad_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=i_, wire=poly, shape=_geo.Rect.from_rect(
            rect=p1_poly_bb, bottom=p_ichppad_poly_bb.bottom,
        ))
        if p_ichppad_poly_bb.left > p1_poly_bb.left:
            layouter.add_wire(net=i_, wire=poly, shape=_geo.Rect.from_rect(
                rect=p_ichppad_poly_bb, left=p1_poly_bb.left
            ))

        # Draw i m1 pin
        left = min(n_ichppad_m1_bb.left, p_ichppad_m1_bb.left)
        right = left + canvas._pin_width
        bottom = canvas._m1_vssrail_width + metal1.min_space
        top = canvas._cell_height - canvas._m1_vddrail_width - metal1.min_space
        layouter.add_wire(net=i_, wire=metal1, pin=metal1pin, shape=_geo.Rect(
            left=left, bottom=bottom, right=right, top=top,
        ))

        # place vss/vdd ch
        n_vssch_x = n1_poly_bb.right + min_actpoly_space - _n_vssch_act_bb.left
        n_vssch_lay = layouter.place(_n_vssch_lay, x=n_vssch_x, y=n_vssch_y)
        n_vssch_act_bb = n_vssch_lay.bounds(mask=active.mask)
        n_vssch_cont_bb = n_vssch_lay.bounds(mask=contact.mask)
        layouter.add_wire(
            net=vss, wire=active, implant=nimplant, shape=_geo.Rect.from_rect(
                rect=n_vssch_act_bb, top=n1_act_bb.top,
            )
        )

        p_vddch_x = p1_poly_bb.right + min_actpoly_space - _p_vddch_act_bb.left
        p_vddch_lay = layouter.place(_p_vddch_lay, x=p_vddch_x, y=p_vddch_y)
        p_vddch_act_bb = p_vddch_lay.bounds(mask=active.mask)
        p_vddch_cont_bb = p_vddch_lay.bounds(mask=contact.mask)
        layouter.add_wire(
            net=vdd, well_net=vdd, wire=active, implant=pimplant, well=nwell,
            shape=_geo.Rect.from_rect(rect=p_vddch_act_bb, bottom=p1_act_bb.bottom),
        )

        poly_left = max(
            n_vssch_cont_bb.right + nmos.computed.min_contactgate_space,
            p_vddch_cont_bb.right + pmos.computed.min_contactgate_space,
            max(n_ichppad_poly_bb.right, p_ichppad_poly_bb.right) + poly.min_space,
        )

        np2poly_bb = None
        for i in range(fingers):
            n2 = n2s[i]
            p2 = p2s[i]
            _n2_lay = _n2_lays[i]
            _p2_lay = _p2_lays[i]

            # place n2/p2 transistors
            n2_x = poly_left - _n2_poly_bb.left
            n2_lay = layouter.place(_n2_lay, x=n2_x, y=n2_y)
            n2_act_bb = n2_lay.bounds(mask=active.mask)
            n2_poly_bb = n2_lay.bounds(mask=poly.mask)
            p2_x = poly_left - _p2_poly_bb.left
            p2_lay = layouter.place(_p2_lay, x=p2_x, y=p2_y)
            p2_act_bb = p2_lay.bounds(mask=active.mask)
            p2_poly_bb = p2_lay.bounds(mask=poly.mask)

            # poly connection n2/p2
            left = min(n2_poly_bb.left, p2_poly_bb.left)
            right = max(n2_poly_bb.right, p2_poly_bb.right)
            bottom = n2_poly_bb.top
            top = p2_poly_bb.bottom
            np2poly_lay = layouter.add_wire(net=ni, wire=poly, shape=_geo.Rect(
                left=left, bottom=bottom, right=right, top=top,
            ))
            np2poly_bb = np2poly_lay.bounds()

            if i%2 == 0:
                # place n_qch/p_qch
                h = tech.on_grid(
                    n2_act_bb.top - (canvas._m1_vssrail_width + metal1.min_space),
                    mult=2, rounding="floor",
                )
                n_qch_x = n2_poly_bb.right + nmos.computed.min_contactgate_space + 0.5*contact.width
                n_qch_y = n2_act_bb.top - 0.5*h
                n_qch_lay = layouter.add_wire(
                    net=q, wire=contact, bottom=active, bottom_implant=nimplant,
                    x=n_qch_x, y=n_qch_y, bottom_height=h, top_height=h,
                )
                n_qch_act_bb = n_qch_lay.bounds(mask=active.mask)
                last_n_impl_bb = n_qch_lay.bounds(mask=nimplant.mask)
                n_qch_cont_bb = n_qch_lay.bounds(mask=contact.mask)
                n_qch_m1_bb = n_qch_lay.bounds(mask=metal1.mask)
                layouter.add_wire(net=q, wire=active, implant=nimplant, shape=_geo.Rect.from_rect(
                    rect=n_qch_act_bb, bottom=n2_act_bb.bottom, top=n2_act_bb.top,
                ))

                h = tech.on_grid(
                    (canvas._cell_height - canvas._m1_vddrail_width - metal1.min_space) - p2_act_bb.bottom,
                    mult=2, rounding="floor",
                )
                p_qch_x = p2_poly_bb.right + pmos.computed.min_contactgate_space + 0.5*contact.width
                p_qch_y = p2_act_bb.bottom + 0.5*h
                p_qch_lay = layouter.add_wire(
                    net=q, well_net=vdd, wire=contact,
                    bottom=active, bottom_implant=pimplant, bottom_well=nwell,
                    x=p_qch_x, y=p_qch_y, bottom_height=h, top_height=h,
                )
                p_qch_act_bb = p_qch_lay.bounds(mask=active.mask)
                last_p_impl_bb = p_qch_lay.bounds(mask=pimplant.mask)
                p_qch_cont_bb = p_qch_lay.bounds(mask=contact.mask)
                p_qch_m1_bb = p_qch_lay.bounds(mask=metal1.mask)
                layouter.add_wire(
                    net=q, well_net=vdd, wire=active, implant=pimplant, well=nwell,
                    shape=_geo.Rect.from_rect(
                        rect=p_qch_act_bb, bottom=p2_act_bb.bottom, top=p2_act_bb.top,
                    ),
                )

                # q m1, pin on first
                left = min(n_qch_m1_bb.left, p_qch_m1_bb.left)
                right = left + canvas._pin_width
                bottom = n_qch_m1_bb.bottom
                top = p_qch_m1_bb.top
                pin_args = {}
                if i == 0:
                    pin_args = {"pin": metal1pin}
                qm1_lay = layouter.add_wire(net=q, wire=metal1, **pin_args, shape=_geo.Rect(
                    left=left, bottom=bottom, right=right, top=top,
                ))
                qm1_bb = qm1_lay.bounds()
                if i == 0:
                    first_qm1_left = qm1_bb.left

                poly_left = max(
                    n_qch_cont_bb.right + nmos.computed.min_contactgate_space,
                    p_qch_cont_bb.right + pmos.computed.min_contactgate_space,
                )
            else:
                # place n_vssch, p_vddch
                _n_vssch_lay = layouter.wire_layout(
                    net=vss, wire=contact, bottom=active, bottom_implant=nimplant,
                    bottom_height=w_ns[1], top_height=w_ns[1],
                )
                _n_vssch_cont_bb = _n_vssch_lay.bounds(mask=contact.mask)
                _n_vssch_act_bb = _n_vssch_lay.bounds(mask=active.mask)
                n_vssch_x = (
                    (n2_poly_bb.right + nmos.computed.min_contactgate_space)
                    - _n_vssch_cont_bb.left
                )
                n_vssch_y = n2_act_bb.bottom - _n_vssch_act_bb.bottom
                n_vssch_lay = layouter.place(object_=_n_vssch_lay, x=n_vssch_x, y=n_vssch_y)
                n_vssch_act_bb = n_vssch_lay.bounds(mask=active.mask)
                last_n_impl_bb = n_vssch_lay.bounds(mask=nimplant.mask)
                n_vssch_cont_bb = n_vssch_lay.bounds(mask=contact.mask)
                n_vssch_m1_bb = n_vssch_lay.bounds(mask=metal1.mask)
                layouter.add_wire(net=vss, wire=active, implant=nimplant, shape=_geo.Rect.from_rect(
                    rect=n_vssch_act_bb, top=n2_act_bb.top,
                ))

                _p_vddch_lay = layouter.wire_layout(
                    net=vdd, well_net=vdd, wire=contact,
                    bottom=active, bottom_implant=pimplant, bottom_well=nwell,
                    bottom_height=w_ps[1], top_height=w_ps[1],
                )
                _p_vddch_cont_bb = _p_vddch_lay.bounds(mask=contact.mask)
                _p_vddch_act_bb = _p_vddch_lay.bounds(mask=active.mask)
                p_vddch_x = (
                    (p2_poly_bb.right + pmos.computed.min_contactgate_space)
                    - _p_vddch_cont_bb.left
                )
                p_vddch_y = p2_act_bb.top - _p_vddch_act_bb.top
                p_vddch_lay = layouter.place(object_=_p_vddch_lay, x=p_vddch_x, y=p_vddch_y)
                p_vddch_act_bb = p_vddch_lay.bounds(mask=active.mask)
                last_p_impl_bb = p_vddch_lay.bounds(mask=pimplant.mask)
                p_vddch_cont_bb = p_vddch_lay.bounds(mask=contact.mask)
                p_vddch_m1_bb = p_vddch_lay.bounds(mask=metal1.mask)
                layouter.add_wire(
                    net=vdd, well_net=vdd, wire=active, implant=pimplant, well=nwell,
                    shape=_geo.Rect.from_rect(rect=p_vddch_act_bb, bottom=p2_act_bb.bottom),
                )

                poly_left = max(
                    n_vssch_cont_bb.right + nmos.computed.min_contactgate_space,
                    p_vddch_cont_bb.right + pmos.computed.min_contactgate_space,
                )
        assert np2poly_bb is not None

        # ni polypad
        _nipppad_lay = layouter.wire_layout(net=ni, wire=contact, bottom=poly)
        _nippad_m1_bb = _nipppad_lay.bounds(mask=metal1.mask)
        nippad_x = nim1_bb.right - _nippad_m1_bb.right
        nippad_y = np2poly_bb.center.y
        nippad_lay = layouter.place(_nipppad_lay, x=nippad_x, y=nippad_y)
        nippad_poly_bb = nippad_lay.bounds(mask=poly.mask)
        layouter.add_wire(net=ni, wire=poly, shape=_geo.Rect.from_rect(
            rect=nippad_poly_bb, right=np2poly_bb.right,
        ))

        # hotizontal metal1 connection for q
        if fingers > 2:
            left = first_qm1_left
            bottom = n_vssch_m1_bb.top + metal1.min_space
            right = qm1_bb.right
            top = p_vddch_act_bb.bottom - metal1.min_space
            layouter.add_wire(net=q, wire=metal1, shape=_geo.Rect(
                left=left, bottom=bottom, right=right, top=top,
            ))

        # Set cell width
        cell_width = self.set_width(min_width=max(
            last_n_impl_bb.right + 0.5*nimplant.min_space,
            last_p_impl_bb.right + 0.5*pimplant.min_space,
            qm1_bb.right + metal1.min_space,
        ))

        # n/p taps
        idx = active.implant.index(pimplant)
        enc = active.min_implant_enclosure[idx].max()
        w = cell_width - pimplant.min_space - 2*enc
        _vsstap_lay = layouter.wire_layout(
            net=vss, wire=contact, bottom=active, bottom_implant=pimplant,
            bottom_width=w, bottom_enclosure="wide",
        )
        _vsstap_impl_bb = _vsstap_lay.bounds(mask=pimplant.mask)
        vsstap_x = 0.5*cell_width
        vsstap_y = 0.5*pimplant.min_space - _vsstap_impl_bb.bottom
        layouter.place(_vsstap_lay, x=vsstap_x, y=vsstap_y)

        idx = active.implant.index(nimplant)
        enc = active.min_implant_enclosure[idx].max()
        w = cell_width - nimplant.min_space - 2*enc
        _vddtap_lay = layouter.wire_layout(
            net=vdd, well_net=vdd, wire=contact,
            bottom=active, bottom_implant=nimplant, bottom_well=nwell,
            bottom_width=w, bottom_enclosure="wide",
        )
        _vddtap_impl_bb = _vddtap_lay.bounds(mask=nimplant.mask)
        vddtap_x = 0.5*cell_width
        vddtap_y = (canvas._cell_height - 0.5*nimplant.min_space) - _vddtap_impl_bb.top
        layouter.place(_vddtap_lay, x=vddtap_x, y=vddtap_y)


class _Nand(_Cell):
    def __init__(self, *, fab: "StdCellFactory", name: str, w_n: float, inputs: int):
        if inputs < 2:
            raise ValueError(
                f"A nand gate has to have at least 2 inputs, not '{inputs}'"
            )

        super().__init__(fab=fab, name=name)

        tech = fab.tech
        canvas = fab.canvas
        ckt = self.circuit
        layouter = self._layouter

        nmos = canvas._nmos
        pmos = canvas._pmos
        l = canvas.l
        active = canvas._active
        nimplant = canvas._nimplant
        pimplant = canvas._pimplant
        nwell = canvas._nwell
        contact = canvas._contact
        poly = canvas._poly
        metal1 = canvas._metal1
        metal1pin = canvas._metal1pin

        nets = ckt.nets
        insts = ckt.instances

        vdd = nets.vdd
        vss = nets.vss

        # Create nets and transistor instances
        w_p = tech.on_grid(canvas._balancedmos_w_ratio*w_n/2.0)
        min_actpoly_space = tech.computed.min_space(primitive1=active, primitive2=poly)

        nq = ckt.new_net(name="nq", external=True)
        int_net = None
        for i in range(inputs):
            net = ckt.new_net(name=f"i{i}", external=True)

            n_inst = ckt.instantiate(nmos, name=f"n{i}", l=l, w=w_n)
            p_inst = ckt.instantiate(pmos, name=f"p{i}", l=l, w=w_p)

            vss.childports += n_inst.ports.bulk
            vdd.childports += p_inst.ports.bulk

            if i == 0:
                vss.childports += n_inst.ports.sourcedrain1
            else:
                # Connect to previous net
                assert int_net is not None
                int_net.childports += n_inst.ports.sourcedrain1
            if i < inputs-1:
                int_net = ckt.new_net(name=f"int{i}", external=False)
                int_net.childports += n_inst.ports.sourcedrain2
            else:
                nq.childports += n_inst.ports.sourcedrain2

            if i%2 == 0:
                vdd.childports += p_inst.ports.sourcedrain1
                nq.childports += p_inst.ports.sourcedrain2
            else:
                nq.childports += p_inst.ports.sourcedrain1
                vdd.childports += p_inst.ports.sourcedrain2

            net.childports += (n_inst.ports.gate, p_inst.ports.gate)

        # Layout
        # First vss contact
        l_ch = layouter.wire_layout(
            net=vss, wire=contact, bottom=active, bottom_implant=nimplant,
        )
        impl_bb = l_ch.bounds(mask=nimplant.mask)
        m1_bb = l_ch.bounds(mask=metal1.mask)
        n_vssch_x = 0.5*nimplant.min_space - impl_bb.left
        n_vssch_y = canvas._m1_vssrail_width - m1_bb.top
        n_vssch_lay = layouter.place(l_ch, x=n_vssch_x, y=n_vssch_y)
        n_vssch_act_bb = n_vssch_lay.bounds(mask=active.mask)

        # First vdd contact
        l_ch = layouter.wire_layout(
            net=vdd, well_net=vdd, wire=contact,
            bottom=active, bottom_implant=pimplant, bottom_well=nwell,
        )
        impl_bb = l_ch.bounds(mask=pimplant.mask)
        m1_bb = l_ch.bounds(mask=metal1.mask)
        p_vddch_x = 0.5*pimplant.min_space - impl_bb.left
        p_vddch_y = canvas._cell_height - canvas._m1_vddrail_width - m1_bb.bottom
        p_vddch_lay = layouter.place(l_ch, x=p_vddch_x, y=p_vddch_y)
        p_vddch_act_bb = p_vddch_lay.bounds(mask=active.mask)

        poly_left = max(
            n_vssch_act_bb.right + min_actpoly_space,
            p_vddch_act_bb.right + min_actpoly_space,
        )
        min_cellwidth = None

        # Use same y for all transistors
        n_y = tech.on_grid(canvas._m1_vssrail_width + metal1.min_space + 0.5*w_n)
        p_y = tech.on_grid(
            canvas._cell_height - canvas._m1_vddrail_width - metal1.min_space - 0.5*w_p
        )

        n_act_bb = None
        p_nqch_m1_bb_first = None
        for i in range(inputs):
            n_inst = insts[f"n{i}"]
            p_inst = insts[f"p{i}"]

            # Place the transistors
            _n_lay = layouter.inst_layout(inst=n_inst)
            _n_poly_bb = _n_lay.bounds(mask=poly.mask)
            n_x = poly_left - _n_poly_bb.left
            n_lay = layouter.place(_n_lay, x=n_x, y=n_y)
            n_act_bb_prev = n_act_bb
            n_act_bb = n_lay.bounds(mask=active.mask)
            n_impl_bb = n_lay.bounds(mask=nimplant.mask)
            n_poly_bb = n_lay.bounds(mask=poly.mask)

            _p_lay = layouter.inst_layout(inst=p_inst)
            _p_poly_bb = _p_lay.bounds(mask=poly.mask)
            p_x = poly_left - _p_poly_bb.left
            p_lay = layouter.place(object_=_p_lay, x=p_x, y=p_y)
            p_act_bb = p_lay.bounds(mask=active.mask)
            p_impl_bb = p_lay.bounds(mask=pimplant.mask)
            p_poly_bb = p_lay.bounds(mask=poly.mask)

            min_cellwidth = max(
                n_impl_bb.right + 0.5*nimplant.min_space,
                p_impl_bb.right + 0.5*pimplant.min_space,
            )

            # Connect input signal with poly and metal pin
            net = nets[f"i{i}"]
            left = poly_left
            right = max(n_poly_bb.right, p_poly_bb.right)
            bottom = n_poly_bb.top
            top = p_poly_bb.bottom
            layouter.add_wire(net=net, wire=poly, shape=_geo.Rect(
                left=left, bottom=bottom, right=right, top=top,
            ))
            _i_polypad_lay = layouter.wire_layout(net=net, wire=contact, bottom=poly)
            _i_polypad_poly_bb = _i_polypad_lay.bounds(mask=poly.mask)
            i_polypad_x = (
                left - _i_polypad_poly_bb.right + tech.on_grid(
                    0.5*min(nmos.computed.min_l, pmos.computed.min_l), rounding="floor",
                )
            )
            i_polypad_y = canvas._well_edge_height
            i_polypad_lay = layouter.place(_i_polypad_lay, x=i_polypad_x, y=i_polypad_y)
            i_polypad_m1_bb = i_polypad_lay.bounds(mask=metal1.mask)
            right = i_polypad_m1_bb.right
            left = right - canvas._pin_width
            bottom = canvas._m1_vssrail_width + metal1.min_space
            top = canvas._cell_height - canvas._m1_vddrail_width - metal1.min_space
            if i > 0:
                # Lower top for nq m1 interconnect
                top -= w_p + metal1.min_space
            layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=_geo.Rect(
                left=left, bottom=bottom, right=right, top=top,
            ))
            poly_left_pad = (
                max(n_poly_bb.right, p_poly_bb.right)
                + poly.min_space + _i_polypad_poly_bb.width
                - tech.on_grid(
                    0.5*(min(nmos.computed.min_l, pmos.computed.min_l)),
                    rounding="floor",
                )
            )

            # Minimum left poly for next nmos
            poly_left_n = n_poly_bb.right + nmos.computed.min_gate_space

            if i == 0:
                # Connect first vdd, vss contact
                layouter.add_wire(
                    net=vss, wire=active, implant=nimplant, shape=_geo.Rect.from_rect(
                        rect=n_vssch_act_bb, top=n_act_bb.top,
                    ),
                )
                layouter.add_wire(
                    net=vdd, well_net=vdd, wire=active, implant=pimplant, well=nwell,
                    shape=_geo.Rect.from_rect(rect=p_vddch_act_bb, bottom=p_act_bb.bottom),
                )
            else:
                # connect to the previous n transistor active area
                assert n_act_bb_prev is not None
                if n_act_bb_prev.right < n_act_bb.left:
                    net = nets[f"int{i - 1}"]
                    left = n_act_bb_prev.right
                    bottom = n_act_bb_prev.bottom
                    right = n_act_bb.left
                    top = n_act_bb_prev.top
                    layouter.add_wire(net=net, wire=active, implant=nimplant, shape=_geo.Rect(
                        left=left, bottom=bottom, right=right, top=top,
                    ))

            # n last nq contact
            if i == (inputs - 1):
                n_nqch_x = (
                    n_poly_bb.right + nmos.computed.min_contactgate_space + 0.5*contact.width
                )
                n_nqch_lay = layouter.add_wire(
                    net=nq, wire=contact, bottom=active, bottom_implant=nimplant,
                    x=n_nqch_x, y=n_y, bottom_height=w_n, top_height=w_n,
                )
                n_nqch_nimpl_bb = n_nqch_lay.bounds(mask=nimplant.mask)
                n_nqch_m1_bb = n_nqch_lay.bounds(mask=metal1.mask)

                min_cellwidth = max(
                    min_cellwidth,
                    n_nqch_nimpl_bb.right + 0.5*nimplant.min_space,
                )

                right = n_nqch_m1_bb.left + canvas._pin_width
                top = canvas._cell_height - canvas._m1_vddrail_width - metal1.min_space
                layouter.add_wire(net=nq, wire=metal1, pin=metal1pin, shape=_geo.Rect.from_rect(
                    rect=n_nqch_m1_bb, right=right, top=top,
                ))
                assert p_nqch_m1_bb_first is not None, "Internal error"
                layouter.add_wire(net=nq, wire=metal1, shape=_geo.Rect.from_rect(
                    rect=p_nqch_m1_bb_first, right=right,
                ))

            # p contact
            if i%2 == 0:
                # nqch
                p_nqch_x = (
                    p_poly_bb.right + pmos.computed.min_contactgate_space + 0.5*contact.width
                )
                p_nqch_lay = layouter.add_wire(
                    net=nq, well_net=vdd, wire=contact,
                    bottom=active, bottom_implant=pimplant, bottom_well=nwell,
                    x=p_nqch_x, y=p_y, bottom_height=w_p, top_height=w_p,
                )
                p_nqch_pimpl_bb = p_nqch_lay.bounds(mask=pimplant.mask)

                min_cellwidth = max(
                    min_cellwidth,
                    p_nqch_pimpl_bb.right + 0.5*pimplant.min_space,
                )

                poly_left_p = p_nqch_x + 0.5*contact.width + pmos.computed.min_contactgate_space
                if i == 0:
                    p_nqch_m1_bb_first = p_nqch_lay.bounds(mask=metal1.mask)
            else:
                _p_vddch_lay = layouter.wire_layout(
                    net=vdd, well_net=vdd,
                    wire=contact, bottom=active, bottom_implant=pimplant, bottom_well=nwell,
                )
                _p_vddch_act_bb = _p_vddch_lay.bounds(mask=active.mask)
                p_vddch_x = p_poly_bb.right + min_actpoly_space - _p_vddch_act_bb.left
                p_vddch_lay = layouter.place(object_=_p_vddch_lay, x=p_vddch_x, y=p_vddch_y)
                p_vddch_act_bb = p_vddch_lay.bounds(mask=active.mask)
                p_vddch_pimpl_bb = p_vddch_lay.bounds(mask=pimplant.mask)
                layouter.add_wire(
                    net=vdd, well_net=vdd, wire=active, implant=pimplant, well=nwell,
                    shape=_geo.Rect.from_rect(rect=p_vddch_act_bb, bottom=p_act_bb.bottom),
                )

                min_cellwidth = max(
                    min_cellwidth,
                    p_vddch_pimpl_bb.right + 0.5*pimplant.min_space,
                )
                poly_left_p = p_vddch_act_bb.right + min_actpoly_space

            # n net
            poly_left = max(poly_left_n, poly_left_p, poly_left_pad)
        assert min_cellwidth is not None

        self.set_width(min_width=min_cellwidth)


class _Nor(_Cell):
    def __init__(self, *, fab: "StdCellFactory", name: str, w_n: float, inputs: int):
        if inputs < 2:
            raise ValueError(
                f"A nor gate has to have at least 2 inputs, not '{inputs}'"
            )

        super().__init__(fab=fab, name=name)

        tech = fab.tech
        canvas = fab.canvas
        ckt = self.circuit
        layouter = self._layouter

        nmos = canvas._nmos
        pmos = canvas._pmos
        l = canvas.l
        active = canvas._active
        nimplant = canvas._nimplant
        pimplant = canvas._pimplant
        nwell = canvas._nwell
        contact = canvas._contact
        poly = canvas._poly
        metal1 = canvas._metal1
        metal1pin = canvas._metal1pin

        nets = ckt.nets
        insts = ckt.instances

        vdd = nets.vdd
        vss = nets.vss

        # Create nets and transistor instances
        # TODO: Maximize transistor lengths
        w_p = tech.on_grid(1.5*canvas._balancedmos_w_ratio*w_n)
        min_actpoly_space = tech.computed.min_space(primitive1=active, primitive2=poly)
        min_actwell_space = tech.computed.min_space(primitive1=active, primitive2=nwell)

        nq = ckt.new_net(name="nq", external=True)
        int_net = None
        for i in range(inputs):
            net = ckt.new_net(name=f"i{i}", external=True)

            n_inst = ckt.instantiate(nmos, name=f"n{i}", l=l, w=w_n)
            p_inst = ckt.instantiate(pmos, name=f"p{i}", l=l, w=w_p)

            vss.childports += n_inst.ports.bulk
            vdd.childports += p_inst.ports.bulk

            if i%2 == 0:
                vss.childports += n_inst.ports.sourcedrain1
                nq.childports += n_inst.ports.sourcedrain2
            else:
                nq.childports += n_inst.ports.sourcedrain1
                vss.childports += n_inst.ports.sourcedrain2

            if i == 0:
                vdd.childports += p_inst.ports.sourcedrain1
            else:
                # Connect to previous net
                assert int_net is not None
                int_net.childports += p_inst.ports.sourcedrain1
            if i < inputs-1:
                int_net = ckt.new_net(name=f"int{i}", external=False)
                int_net.childports += p_inst.ports.sourcedrain2
            else:
                nq.childports += p_inst.ports.sourcedrain2

            net.childports += (n_inst.ports.gate, p_inst.ports.gate)

        # Layout
        # First vss contact
        l_ch = layouter.wire_layout(
            net=vss, wire=contact, bottom=active, bottom_implant=nimplant,
        )
        impl_bb = l_ch.bounds(mask=nimplant.mask)
        m1_bb = l_ch.bounds(mask=metal1.mask)
        n_vssch_x = 0.5*nimplant.min_space - impl_bb.left
        n_vssch_y = canvas._m1_vssrail_width - m1_bb.top
        n_vssch_lay = layouter.place(l_ch, x=n_vssch_x, y=n_vssch_y)
        n_vssch_act_bb = n_vssch_lay.bounds(mask=active.mask)

        # First vdd contact
        l_ch = layouter.wire_layout(
            net=vdd, well_net=vdd, wire=contact,
            bottom=active, bottom_implant=pimplant, bottom_well=nwell,
        )
        impl_bb = l_ch.bounds(mask=pimplant.mask)
        m1_bb = l_ch.bounds(mask=metal1.mask)
        p_vddch_x = 0.5*pimplant.min_space - impl_bb.left
        p_vddch_y = canvas._cell_height - canvas._m1_vddrail_width - m1_bb.bottom
        p_vddch_lay = layouter.place(l_ch, x=p_vddch_x, y=p_vddch_y)
        p_vddch_act_bb = p_vddch_lay.bounds(mask=active.mask)

        poly_left = max(
            n_vssch_act_bb.right + min_actpoly_space,
            p_vddch_act_bb.right + min_actpoly_space,
        )
        min_cellwidth = None

        # Use same y for all transistors
        n_y = tech.on_grid(canvas._m1_vssrail_width + metal1.min_space + 0.5*w_n)
        p_y = tech.on_grid(
            canvas._cell_height - canvas._m1_vddrail_width - metal1.min_space - 0.5*w_p
        )

        p_act_bb = None
        n_nqch_m1_bb_first = None
        for i in range(inputs):
            n_inst = insts[f"n{i}"]
            p_inst = insts[f"p{i}"]

            # Place the transistors
            _n_lay = layouter.inst_layout(inst=n_inst)
            _n_poly_bb = _n_lay.bounds(mask=poly.mask)
            n_x = poly_left - _n_poly_bb.left
            n_lay = layouter.place(_n_lay, x=n_x, y=n_y)
            n_act_bb = n_lay.bounds(mask=active.mask)
            n_impl_bb = n_lay.bounds(mask=nimplant.mask)
            n_poly_bb = n_lay.bounds(mask=poly.mask)

            _p_lay = layouter.inst_layout(inst=p_inst)
            _p_poly_bb = _p_lay.bounds(mask=poly.mask)
            p_x = poly_left - _p_poly_bb.left
            p_lay = layouter.place(object_=_p_lay, x=p_x, y=p_y)
            p_act_bb_prev = p_act_bb
            p_act_bb = p_lay.bounds(mask=active.mask)
            p_impl_bb = p_lay.bounds(mask=pimplant.mask)
            p_poly_bb = p_lay.bounds(mask=poly.mask)

            min_cellwidth = max(
                n_impl_bb.right + 0.5*nimplant.min_space,
                p_impl_bb.right + 0.5*pimplant.min_space,
            )

            # Connect input signal with poly and metal pin
            net = nets[f"i{i}"]
            left = poly_left
            right = max(n_poly_bb.right, p_poly_bb.right)
            bottom = n_poly_bb.top
            top = p_poly_bb.bottom
            layouter.add_wire(net=net, wire=poly, shape=_geo.Rect(
                left=left, bottom=bottom, right=right, top=top,
            ))
            _i_polypad_lay = layouter.wire_layout(net=net, wire=contact, bottom=poly)
            _i_polypad_poly_bb = _i_polypad_lay.bounds(mask=poly.mask)
            i_polypad_x = (
                left - _i_polypad_poly_bb.right + tech.on_grid(
                    0.5*min(nmos.computed.min_l, pmos.computed.min_l), rounding="floor",
                )
            )
            i_polypad_y = canvas._well_edge_height
            i_polypad_lay = layouter.place(_i_polypad_lay, x=i_polypad_x, y=i_polypad_y)
            i_polypad_m1_bb = i_polypad_lay.bounds(mask=metal1.mask)
            right = i_polypad_m1_bb.right
            left = right - canvas._pin_width
            bottom = canvas._m1_vssrail_width + metal1.min_space
            top = canvas._cell_height - canvas._m1_vddrail_width - metal1.min_space
            if i > 0:
                # Increase bottom for nq m1 interconnect
                bottom += w_n + metal1.min_space
            layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=_geo.Rect(
                left=left, bottom=bottom, right=right, top=top,
            ))
            poly_left_pad = (
                max(n_poly_bb.right, p_poly_bb.right)
                + poly.min_space + _i_polypad_poly_bb.width
                - tech.on_grid(
                    0.5*min(nmos.computed.min_l, pmos.computed.min_l), rounding="floor",
                )
            )

            # Minimum left poly for next nmos
            poly_left_p = p_poly_bb.right + pmos.computed.min_gate_space

            if i == 0:
                # Connect first vdd, vss contact
                layouter.add_wire(
                    net=vss, wire=active, implant=nimplant, shape=_geo.Rect.from_rect(
                        rect=n_vssch_act_bb, top=n_act_bb.top,
                    ),
                )
                layouter.add_wire(
                    net=vdd, well_net=vdd, wire=active, implant=pimplant, well=nwell,
                    shape=_geo.Rect.from_rect(rect=p_vddch_act_bb, bottom=p_act_bb.bottom),
                )
            else:
                # connect to the previous p transistor active area
                assert p_act_bb_prev is not None
                if p_act_bb_prev.right < p_act_bb.left:
                    net = nets[f"int{i - 1}"]
                    left = p_act_bb_prev.right
                    bottom = p_act_bb_prev.bottom
                    right = p_act_bb.left
                    top = p_act_bb_prev.top
                    layouter.add_wire(
                        net=net, well_net=vdd, wire=active,
                        implant=pimplant, well=nwell, shape=_geo.Rect(
                            left=left, bottom=bottom, right=right, top=top,
                        ),
                    )

            # p last nq contact
            if i == (inputs - 1):
                p_nqch_x = (
                    p_poly_bb.right + pmos.computed.min_contactgate_space + 0.5*contact.width
                )
                p_nqch_lay = layouter.add_wire(
                    net=nq, well_net=vdd, wire=contact,
                    bottom=active, bottom_implant=pimplant, bottom_well=nwell,
                    x=p_nqch_x, y=p_y, bottom_height=w_p, top_height=w_p,
                )
                p_nqch_pimpl_bb = p_nqch_lay.bounds(mask=pimplant.mask)
                p_nqch_m1_bb = p_nqch_lay.bounds(mask=metal1.mask)

                min_cellwidth = max(
                    min_cellwidth,
                    p_nqch_pimpl_bb.right + 0.5*pimplant.min_space,
                )
                right = p_nqch_m1_bb.left + canvas._pin_width
                bottom = canvas._m1_vssrail_width + metal1.min_space
                layouter.add_wire(net=nq, wire=metal1, pin=metal1pin, shape=_geo.Rect.from_rect(
                    rect=p_nqch_m1_bb, bottom=bottom, right=right,
                ))
                assert n_nqch_m1_bb_first is not None, "Internal error"
                layouter.add_wire(net=nq, wire=metal1, shape=_geo.Rect.from_rect(
                    rect=n_nqch_m1_bb_first, right=right,
                ))

            # n contact
            if i%2 == 0:
                # nqch
                n_nqch_x = (
                    n_poly_bb.right + nmos.computed.min_contactgate_space + 0.5*contact.width
                )
                n_nqch_lay = layouter.add_wire(
                    net=nq, wire=contact, bottom=active, bottom_implant=nimplant,
                    x=n_nqch_x, y=n_y, bottom_height=w_n, top_height=w_n,
                )
                n_nqch_nimpl_bb = n_nqch_lay.bounds(mask=nimplant.mask)

                min_cellwidth = max(
                    min_cellwidth,
                    n_nqch_nimpl_bb.right + 0.5*nimplant.min_space,
                )
                poly_left_n = n_nqch_x + 0.5*contact.width + nmos.computed.min_contactgate_space
                if i == 0:
                    n_nqch_m1_bb_first = n_nqch_lay.bounds(mask=metal1.mask)
            else:
                _n_vssch_lay = layouter.wire_layout(
                    net=vss, wire=contact, bottom=active, bottom_implant=nimplant,
                )
                _n_vssch_act_bb = _n_vssch_lay.bounds(mask=active.mask)
                n_vssch_x = n_poly_bb.right + min_actpoly_space - _n_vssch_act_bb.left
                n_vssch_lay = layouter.place(object_=_n_vssch_lay, x=n_vssch_x, y=n_vssch_y)
                n_vssch_act_bb = n_vssch_lay.bounds(mask=active.mask)
                n_vssch_nimpl_bb = n_vssch_lay.bounds(mask=nimplant.mask)
                layouter.add_wire(
                    net=vss, wire=active, implant=nimplant,
                    shape=_geo.Rect.from_rect(rect=n_vssch_act_bb, top=n_act_bb.top),
                )

                min_cellwidth = max(
                    min_cellwidth,
                    n_vssch_nimpl_bb.right + 0.5*nimplant.min_space,
                )
                poly_left_n = n_vssch_act_bb.right + min_actpoly_space

            # p net
            poly_left = max(poly_left_n, poly_left_p, poly_left_pad)
        assert min_cellwidth is not None

        self.set_width(min_width=min_cellwidth)


class StdCellFactory(_fab.CellFactory[_Cell]):
    def __init__(self, *,
        lib: _lbry.RoutingGaugeLibrary, cktfab: _ckt.CircuitFactory,
        layoutfab: _lay.LayoutFactory,
        name_prefix: str="", name_suffix: str="",
        canvas: StdCellCanvas,
    ):
        super().__init__(
            lib=lib, cktfab=cktfab, layoutfab=layoutfab, cell_class=_Cell,
            name_prefix=name_prefix, name_suffix=name_suffix,
        )
        self._lib: _lbry.RoutingGaugeLibrary
        self.lib: _lbry.RoutingGaugeLibrary

        self._canvas = canvas
        self._cktfab = cktfab
        self._layoutfab = layoutfab

    @property
    def canvas(self) -> StdCellCanvas:
        return self._canvas

    def add_default(self) -> None:
        self.add_lambdacells()
        self.add_fillers()
        self.add_diodes()
        self.add_logicconsts()
        self.add_inverters()
        self.add_buffers()
        self.add_nands()
        self.add_nors()

    def add_lambdacells(self, use_old: bool=False) -> None:
        canvas = self.canvas

        converter = _StdCellConverter(lib=self)
        for cell in (_oldcells if use_old else _cells):
            converter(src=cell, target=self.new_cell(name=cell.name))

        # Hack for minimum space for nimplant/pimplant for mx3_x2
        layout = self.lib.cells.mx3_x2.layout
        nimplant = canvas.nimplant
        pimplant = canvas.pimplant
        l = canvas.lambda_
        rect = _geo.Rect(left=10*l, bottom=30*l, right=210*l, top=70*l)
        layout.add_shape(layer=nimplant, net=None, shape=rect)
        rect = _geo.Rect(left=10*l, bottom=110*l, right=210*l, top=170*l)
        layout.add_shape(layer=pimplant, net=None, shape=rect)

    def add_fillers(self):
        """Add a set of fill cells to the library.
        """
        self.new_cell(name="fill", cell_class=_Fill)
        self.new_cell(name="tie", cell_class=_Tie)
        self.new_cell(name="tie_diff", cell_class=_Tie, max_diff=True)
        self.new_cell(name="tie_poly", cell_class=_Tie, max_poly=True)
        for i in (2, 4):
            self.new_cell(name=f"fill_w{i}", cell_class=_Fill, width=i)
            self.new_cell(name=f"tie_w{i}", cell_class=_Tie, width=i)
            self.new_cell(name=f"tie_diff_w{i}", cell_class=_Tie, max_diff=True, width=i)
            self.new_cell(name=f"tie_poly_w{i}", cell_class=_Tie, max_poly=True, width=i)

    def add_diodes(self):
        """Add an antenna diode cell to the library."""
        self.new_cell(name="diode_w1", cell_class=_Diode)

    def add_logicconsts(self):
        """Add logic 0 and 1 cells
        """
        self.new_cell(name="zero_x1", cell_class=_ZeroOneDecap, zero_pin=True, one_pin=False)
        self.new_cell(name="one_x1", cell_class=_ZeroOneDecap, zero_pin=False, one_pin=True)
        self.new_cell(name="zeroone_x1", cell_class=_ZeroOneDecap, zero_pin=True, one_pin=True)
        self.new_cell(name="decap_w0", cell_class=_ZeroOneDecap, zero_pin=False, one_pin=False)

    def add_inverters(self):
        """Add a set of inverters to the library.
        """
        self.new_cell(name="inv_x0", cell_class=_Inv, w_n=20*self.canvas.lambda_)
        self.new_cell(name="inv_x1", cell_class=_Inv, w_n=36*self.canvas.lambda_)
        self.new_cell(
            name="inv_x2", cell_class=_Inv, w_n=36*self.canvas.lambda_, fingers=2,
        )
        self.new_cell(
            name="inv_x4", cell_class=_Inv, w_n=36*self.canvas.lambda_, fingers=4,
        )

    def add_buffers(self):
        """Add a set of buffer to the library"""
        self.new_cell(
            name="buf_x1", cell_class=_Buf,
            w_ns=(10*self.canvas.lambda_, 36*self.canvas.lambda_),
        )
        self.new_cell(
            name="buf_x2", cell_class=_Buf,
            w_ns=(20*self.canvas.lambda_, (36*self.canvas.lambda_, 2)),
        )
        self.new_cell(
            name="buf_x4", cell_class=_Buf,
            w_ns=(36*self.canvas.lambda_, (36*self.canvas.lambda_, 4)),
        )

    def add_nands(self):
        """Add a set of nand gates to the library"""
        for i in range(2, 5):
            self.new_cell(
                name=f"nand{i}_x0", cell_class=_Nand,
                w_n=(40 if i==2 else 50)*self.canvas.lambda_, inputs=i,
            )

    def add_nors(self):
        """Add a set of nor gates to the library"""
        for i in range(2, 5):
            self.new_cell(
                name=f"nor{i}_x0", cell_class=_Nor,
                w_n=20*self.canvas.lambda_, inputs=i,
            )

    def write_spice(self, dirname=None):
        if dirname is None:
            raise ValueError("Please provide directory to write spice netlists to")

        for cell in _cells:
            with open(dirname + os.sep + cell.name + ".sp", "w") as f:
                f.write("* Spice netlist of {}\n\n".format(cell.name))
                f.write(cell.spice_netlist(lambda_=self.canvas.lambda_))
