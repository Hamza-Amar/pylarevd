"""Tests for the 8 event display enhancements."""

import io
import os
import numpy as np
import pytest

from pylarevd import EventFile
from pylarevd.app import build_app, render
from pylarevd.display import Display3D

SAMPLE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "samples")
ATMNU_PATH = os.path.join(SAMPLE_DIR, "atmnu_max_weighted_HD_w19433s1_job000100_20260829T125152Z_reco2.root")
NDK_PATH = os.path.join(SAMPLE_DIR, "ndk_n_to_eminus_Kplus_HD_w19409s1_job000001_20260828T150556Z_reco2.root")
MUSUN_PATH = os.path.join(SAMPLE_DIR, "musun_HD_w19435s1_job003240_20260829T170934Z_reco2.root")

needs_ndk = pytest.mark.skipif(not os.path.exists(NDK_PATH), reason="NDK sample file absent")
needs_atmnu = pytest.mark.skipif(not os.path.exists(ATMNU_PATH), reason="Atmospheric neutrino sample file absent")
needs_musun = pytest.mark.skipif(not os.path.exists(MUSUN_PATH), reason="Cosmic sample file absent")
needs_all = pytest.mark.skipif(
    not (os.path.exists(NDK_PATH) and os.path.exists(ATMNU_PATH) and os.path.exists(MUSUN_PATH)),
    reason="All sample files required"
)


@needs_all
def test_true_vertex_universal():
    """True vertex should be available for neutrino, NDK, and cosmic events."""
    ev_atmnu = EventFile(ATMNU_PATH)[0]
    tv_atmnu = ev_atmnu.true_vertex()
    assert tv_atmnu is not None
    assert len(tv_atmnu) == 3
    assert np.isfinite(tv_atmnu).all()

    ev_ndk = EventFile(NDK_PATH)[0]
    tv_ndk = ev_ndk.true_vertex()
    assert tv_ndk is not None
    assert len(tv_ndk) == 3
    assert np.isfinite(tv_ndk).all()

    ti_ndk = ev_ndk.true_interaction()
    assert ti_ndk is not None
    assert "n -> e⁻ + K⁺" in ti_ndk.headline() or "n -> e- + K+" in ti_ndk.headline()
    assert ti_ndk.latex in ("$n \\to e^- + K^+$", "$n \\to e^- K^+$")

    ev_musun = EventFile(MUSUN_PATH)[0]
    tv_musun = ev_musun.true_vertex()
    assert tv_musun is not None
    assert len(tv_musun) == 3
    assert np.isfinite(tv_musun).all()
