# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack11_opy_ = 7
def bstackl_opy_ (bstack1l_opy_):
    global bstack1l1l_opy_
    stringNr = ord (bstack1l_opy_ [-1])
    bstack1ll1_opy_ = bstack1l_opy_ [:-1]
    bstack11l_opy_ = stringNr % len (bstack1ll1_opy_)
    bstack111_opy_ = bstack1ll1_opy_ [:bstack11l_opy_] + bstack1ll1_opy_ [bstack11l_opy_:]
    if bstack1_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1ll_opy_ + stringNr) % bstack11_opy_) for bstack1ll_opy_, char in enumerate (bstack111_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1ll_opy_ + stringNr) % bstack11_opy_) for bstack1ll_opy_, char in enumerate (bstack111_opy_)])
    return eval (bstack1l1_opy_)
import atexit
import os
import signal
import sys
import time
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
from multiprocessing import Pool
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
bstack11ll11l_opy_ = {
	bstackl_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧࠁ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࠪࠂ"),
  bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪࠃ"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡬ࡧࡼࠫࠄ"),
  bstackl_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬࠅ"): bstackl_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࠆ"),
  bstackl_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫࠇ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬࠈ"),
  bstackl_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫࠉ"): bstackl_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࠨࠊ"),
  bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࠋ"): bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨࠌ"),
  bstackl_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࠍ"): bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩࠎ"),
  bstackl_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࠏ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪࠫࠐ"),
  bstackl_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬࠑ"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡷࡴࡲࡥࠨࠒ"),
  bstackl_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠓ"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠔ"),
  bstackl_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠕ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠖ"),
  bstackl_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬࠗ"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡶࡪࡦࡨࡳࠬ࠘"),
  bstackl_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧ࠙"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧࠚ"),
  bstackl_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠛ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠜ"),
  bstackl_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠝ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠞ"),
  bstackl_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠟ"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠠ"),
  bstackl_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࠡ"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬࠢ"),
  bstackl_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠣ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠤ"),
  bstackl_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠥ"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠦ"),
  bstackl_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠧ"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠨ"),
  bstackl_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬࠩ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡴࡤࡌࡧࡼࡷࠬࠪ"),
  bstackl_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠫ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠬ"),
  bstackl_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭࠭"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡸ࠭࠮"),
  bstackl_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪ࠯"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡪࡨࡧࡣࡩࡧࠪ࠰"),
  bstackl_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠱"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠲"),
  bstackl_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠳"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠴"),
  bstackl_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ࠵"): bstackl_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ࠶"),
  bstackl_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧ࠷"): bstackl_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩ࠸"),
  bstackl_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ࠹"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭࠺"),
  bstackl_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠻"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠼"),
  bstackl_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠽"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠾"),
  bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࠿"): bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ࡀ"),
  bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡁ"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡂ"),
  bstackl_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨࡃ"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡲࡹࡷࡩࡥࠨࡄ"),
  bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡅ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡆ"),
  bstackl_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡇ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡈ"),
}
bstack11ll11l1_opy_ = [
  bstackl_opy_ (u"ࠧࡰࡵࠪࡉ"),
  bstackl_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫࡊ"),
  bstackl_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࡋ"),
  bstackl_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࡌ"),
  bstackl_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨࡍ"),
  bstackl_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩࡎ"),
  bstackl_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ࡏ"),
]
bstack1lll1l1l1_opy_ = {
  bstackl_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩࡐ"): [bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩࡑ"), bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡥࡎࡂࡏࡈࠫࡒ")],
  bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࡓ"): bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧࡔ"),
  bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨࡕ"): bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠩࡖ"),
  bstackl_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬࡗ"): bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊ࠭ࡘ"),
  bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࡙ࠫ"): bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ࡚ࠬ"),
  bstackl_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰ࡛ࠫ"): bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡇࡒࡂࡎࡏࡉࡑ࡙࡟ࡑࡇࡕࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭࡜"),
  bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ࡝"): bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࠬ࡞"),
  bstackl_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬ࡟"): bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ࡠ"),
  bstackl_opy_ (u"ࠪࡥࡵࡶࠧࡡ"): bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖࠧࡢ"),
  bstackl_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧࡣ"): bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࡤࡊࡅࡃࡗࡊࠫࡤ"),
  bstackl_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫࡥ"): bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫࡦ")
}
bstack1l11ll11_opy_ = {
  bstackl_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࡧ"): [bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸ࡟࡯ࡣࡰࡩࠬࡨ"), bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࡩ")],
  bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࡪ"): [bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡤࡱࡥࡺࠩ࡫"), bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ࡬")],
  bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡭"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡮"),
  bstackl_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ࡯"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨࡰ"),
  bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡱ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡲ"),
  bstackl_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧࡳ"): [bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡲࡳࠫࡴ"), bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࡵ")],
  bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࡶ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩࡷ"),
  bstackl_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡸ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡹ"),
  bstackl_opy_ (u"ࠧࡢࡲࡳࠫࡺ"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳࠫࡻ"),
  bstackl_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡼ"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡽ"),
  bstackl_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡾ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡿ")
}
bstack111111l_opy_ = {
  bstackl_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩࢀ"): bstackl_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫࢁ"),
  bstackl_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࢂ"): [bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫࢃ"), bstackl_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ࢄ")],
  bstackl_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢅ"): bstackl_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢆ"),
  bstackl_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪࢇ"): bstackl_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ࢈"),
  bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ࢉ"): [bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪࢊ"), bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩࢋ")],
  bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢌ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࢍ"),
  bstackl_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪࢎ"): bstackl_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬ࢏"),
  bstackl_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࢐"): [bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ࢑"), bstackl_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ࢒")],
  bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࢓"): [bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭࢔"), bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹ࠭࢕")]
}
bstack11l1l_opy_ = [
  bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭࢖"),
  bstackl_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫࢗ"),
  bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ࢘"),
  bstackl_opy_ (u"ࠪࡷࡪࡺࡗࡪࡰࡧࡳࡼࡘࡥࡤࡶ࢙ࠪ"),
  bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࢚࠭"),
  bstackl_opy_ (u"ࠬࡹࡴࡳ࡫ࡦࡸࡋ࡯࡬ࡦࡋࡱࡸࡪࡸࡡࡤࡶࡤࡦ࡮ࡲࡩࡵࡻ࢛ࠪ"),
  bstackl_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩ࢜"),
  bstackl_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ࢝"),
  bstackl_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭࢞"),
  bstackl_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ࢟"),
  bstackl_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢠ"),
  bstackl_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬࢡ"),
]
bstack1111l11l_opy_ = [
  bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢢ"),
  bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢣ"),
  bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢤ"),
  bstackl_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࢥ"),
  bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢦ"),
  bstackl_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬࢧ"),
  bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧࢨ"),
  bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩࢩ"),
  bstackl_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩࢪ"),
  bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬࢫ")
]
bstack1l1ll1l1_opy_ = [
  bstackl_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭ࢬ"),
  bstackl_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࢭ"),
  bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࢮ"),
  bstackl_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢯ"),
  bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡓࡶ࡮ࡵࡲࡪࡶࡼࠫࢰ"),
  bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩࢱ"),
  bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚ࡡࡨࠩࢲ"),
  bstackl_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ࢳ"),
  bstackl_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࢴ"),
  bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࢵ"),
  bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢶ"),
  bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫࢷ"),
  bstackl_opy_ (u"࠭࡯ࡴࠩࢸ"),
  bstackl_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪࢹ"),
  bstackl_opy_ (u"ࠨࡪࡲࡷࡹࡹࠧࢺ"),
  bstackl_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫࢻ"),
  bstackl_opy_ (u"ࠪࡶࡪ࡭ࡩࡰࡰࠪࢼ"),
  bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭ࢽ"),
  bstackl_opy_ (u"ࠬࡳࡡࡤࡪ࡬ࡲࡪ࠭ࢾ"),
  bstackl_opy_ (u"࠭ࡲࡦࡵࡲࡰࡺࡺࡩࡰࡰࠪࢿ"),
  bstackl_opy_ (u"ࠧࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸࠬࣀ"),
  bstackl_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬࣁ"),
  bstackl_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨࣂ"),
  bstackl_opy_ (u"ࠪࡲࡴࡖࡡࡨࡧࡏࡳࡦࡪࡔࡪ࡯ࡨࡳࡺࡺࠧࣃ"),
  bstackl_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬࣄ"),
  bstackl_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࣅ"),
  bstackl_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪࣆ"),
  bstackl_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡦࡰࡧࡏࡪࡿࡳࠨࣇ"),
  bstackl_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬࣈ"),
  bstackl_opy_ (u"ࠩࡱࡳࡕ࡯ࡰࡦ࡮࡬ࡲࡪ࠭ࣉ"),
  bstackl_opy_ (u"ࠪࡧ࡭࡫ࡣ࡬ࡗࡕࡐࠬ࣊"),
  bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣋"),
  bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡈࡵ࡯࡬࡫ࡨࡷࠬ࣌"),
  bstackl_opy_ (u"࠭ࡣࡢࡲࡷࡹࡷ࡫ࡃࡳࡣࡶ࡬ࠬ࣍"),
  bstackl_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ࣎"),
  bstackl_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࣏"),
  bstackl_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࡜ࡥࡳࡵ࡬ࡳࡳ࣐࠭"),
  bstackl_opy_ (u"ࠪࡲࡴࡈ࡬ࡢࡰ࡮ࡔࡴࡲ࡬ࡪࡰࡪ࣑ࠫ"),
  bstackl_opy_ (u"ࠫࡲࡧࡳ࡬ࡕࡨࡲࡩࡑࡥࡺࡵ࣒ࠪ"),
  bstackl_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡑࡵࡧࡴ࣓ࠩ"),
  bstackl_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡏࡤࠨࣔ"),
  bstackl_opy_ (u"ࠧࡥࡧࡧ࡭ࡨࡧࡴࡦࡦࡇࡩࡻ࡯ࡣࡦࠩࣕ"),
  bstackl_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡑࡣࡵࡥࡲࡹࠧࣖ"),
  bstackl_opy_ (u"ࠩࡳ࡬ࡴࡴࡥࡏࡷࡰࡦࡪࡸࠧࣗ"),
  bstackl_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨࣘ"),
  bstackl_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣙ"),
  bstackl_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪࣚ"),
  bstackl_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ࣛ"),
  bstackl_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫࣜ"),
  bstackl_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡃ࡫ࡲࡱࡪࡺࡲࡪࡥࠪࣝ"),
  bstackl_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࡗ࠴ࠪࣞ"),
  bstackl_opy_ (u"ࠪࡱ࡮ࡪࡓࡦࡵࡶ࡭ࡴࡴࡉ࡯ࡵࡷࡥࡱࡲࡁࡱࡲࡶࠫࣟ"),
  bstackl_opy_ (u"ࠫࡪࡹࡰࡳࡧࡶࡷࡴ࡙ࡥࡳࡸࡨࡶࠬ࣠"),
  bstackl_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫ࣡"),
  bstackl_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡄࡦࡳࠫ࣢"),
  bstackl_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࣣࠧ"),
  bstackl_opy_ (u"ࠨࡵࡼࡲࡨ࡚ࡩ࡮ࡧ࡚࡭ࡹ࡮ࡎࡕࡒࠪࣤ"),
  bstackl_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧࣥ"),
  bstackl_opy_ (u"ࠪ࡫ࡵࡹࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨࣦ"),
  bstackl_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬࣧ"),
  bstackl_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬࣨ"),
  bstackl_opy_ (u"࠭ࡦࡰࡴࡦࡩࡈ࡮ࡡ࡯ࡩࡨࡎࡦࡸࣩࠧ"),
  bstackl_opy_ (u"ࠧࡹ࡯ࡶࡎࡦࡸࠧ࣪"),
  bstackl_opy_ (u"ࠨࡺࡰࡼࡏࡧࡲࠨ࣫"),
  bstackl_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨ࣬"),
  bstackl_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪ࣭ࠪ"),
  bstackl_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸ࣮ࠬ"),
  bstackl_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ࣯"),
  bstackl_opy_ (u"࠭ࡡࡱࡲ࡙ࡩࡷࡹࡩࡰࡰࣰࠪ"),
  bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸࣱ࠭"),
  bstackl_opy_ (u"ࠨࡴࡨࡷ࡮࡭࡮ࡂࡲࡳࣲࠫ"),
  bstackl_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࡸ࠭ࣳ"),
  bstackl_opy_ (u"ࠪࡧࡦࡴࡡࡳࡻࠪࣴ"),
  bstackl_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬࣵ"),
  bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࣶࠬ"),
  bstackl_opy_ (u"࠭ࡩࡦࠩࣷ"),
  bstackl_opy_ (u"ࠧࡦࡦࡪࡩࠬࣸ"),
  bstackl_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨࣹ"),
  bstackl_opy_ (u"ࠩࡴࡹࡪࡻࡥࠨࣺ"),
  bstackl_opy_ (u"ࠪ࡭ࡳࡺࡥࡳࡰࡤࡰࠬࣻ"),
  bstackl_opy_ (u"ࠫࡦࡶࡰࡔࡶࡲࡶࡪࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠬࣼ"),
  bstackl_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡈࡧ࡭ࡦࡴࡤࡍࡲࡧࡧࡦࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫࣽ"),
  bstackl_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡉࡽࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩࣾ"),
  bstackl_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡎࡴࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪࣿ"),
  bstackl_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࠬऀ"),
  bstackl_opy_ (u"ࠩࡵࡩࡸ࡫ࡲࡷࡧࡇࡩࡻ࡯ࡣࡦࠩँ"),
  bstackl_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪं"),
  bstackl_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭ः"),
  bstackl_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡕࡧࡳࡴࡥࡲࡨࡪ࠭ऄ"),
  bstackl_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡏ࡯ࡴࡆࡨࡺ࡮ࡩࡥࡔࡧࡷࡸ࡮ࡴࡧࡴࠩअ"),
  bstackl_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡶࡦ࡬ࡳࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧआ"),
  bstackl_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡲࡳࡰࡪࡖࡡࡺࠩइ"),
  bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪई"),
  bstackl_opy_ (u"ࠪࡻࡩ࡯࡯ࡔࡧࡵࡺ࡮ࡩࡥࠨउ"),
  bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ऊ"),
  bstackl_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹࡉࡲࡰࡵࡶࡗ࡮ࡺࡥࡕࡴࡤࡧࡰ࡯࡮ࡨࠩऋ"),
  bstackl_opy_ (u"࠭ࡨࡪࡩ࡫ࡇࡴࡴࡴࡳࡣࡶࡸࠬऌ"),
  bstackl_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡐࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࡶࠫऍ"),
  bstackl_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫऎ"),
  bstackl_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ए"),
  bstackl_opy_ (u"ࠪࡶࡪࡳ࡯ࡷࡧࡌࡓࡘࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࡏࡳࡨࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨऐ"),
  bstackl_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ऑ"),
  bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ"),
  bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨओ"),
  bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭औ"),
  bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪक"),
  bstackl_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬख"),
  bstackl_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩग"),
  bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭घ"),
  bstackl_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨङ")
]
bstack1l1lllll_opy_ = {
  bstackl_opy_ (u"࠭ࡶࠨच"): bstackl_opy_ (u"ࠧࡷࠩछ"),
  bstackl_opy_ (u"ࠨࡨࠪज"): bstackl_opy_ (u"ࠩࡩࠫझ"),
  bstackl_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩञ"): bstackl_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪट"),
  bstackl_opy_ (u"ࠬࡵ࡮࡭ࡻࡤࡹࡹࡵ࡭ࡢࡶࡨࠫठ"): bstackl_opy_ (u"࠭࡯࡯࡮ࡼࡅࡺࡺ࡯࡮ࡣࡷࡩࠬड"),
  bstackl_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫढ"): bstackl_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬण"),
  bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬत"): bstackl_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭थ"),
  bstackl_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧद"): bstackl_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨध"),
  bstackl_opy_ (u"࠭ࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩन"): bstackl_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऩ"),
  bstackl_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫप"): bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬफ"),
  bstackl_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫब"): bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡉࡱࡶࡸࠬभ"),
  bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭म"): bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧय"),
  bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨर"): bstackl_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऱ"),
  bstackl_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫल"): bstackl_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬळ"),
  bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬऴ"): bstackl_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧव"),
  bstackl_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨश"): bstackl_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩष"),
  bstackl_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬस"): bstackl_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ह"),
  bstackl_opy_ (u"ࠪࡴࡦࡩࡦࡪ࡮ࡨࠫऺ"): bstackl_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧऻ"),
  bstackl_opy_ (u"ࠬࡶࡡࡤ࠯ࡩ࡭ࡱ࡫़ࠧ"): bstackl_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩऽ"),
  bstackl_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪा"): bstackl_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫि"),
  bstackl_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪी"): bstackl_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫु"),
  bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ू"): bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧृ"),
}
bstack1lll111l1_opy_ = bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡸࡦ࠲࡬ࡺࡨࠧॄ")
bstack1l1lll1_opy_ = bstackl_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠪॅ")
bstack1111ll11_opy_ = bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠬॆ")
bstack111111l1_opy_ = {
  bstackl_opy_ (u"ࠩࡦࡶ࡮ࡺࡩࡤࡣ࡯ࠫे"): 50,
  bstackl_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩै"): 40,
  bstackl_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬॉ"): 30,
  bstackl_opy_ (u"ࠬ࡯࡮ࡧࡱࠪॊ"): 20,
  bstackl_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬो"): 10
}
bstack1l11ll111_opy_ = bstack111111l1_opy_[bstackl_opy_ (u"ࠧࡪࡰࡩࡳࠬौ")]
bstack1lll11111_opy_ = bstackl_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵्ࠧ")
bstack1111111_opy_ = bstackl_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧॎ")
bstack1l11ll1l1_opy_ = bstackl_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩॏ")
bstack1llll1l_opy_ = bstackl_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪॐ")
bstack1llll1l1_opy_ = [bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭॑"), bstackl_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ॒࠭")]
bstack11111l_opy_ = [bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॓"), bstackl_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॔")]
bstack111l11l1_opy_ = [
  bstackl_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡔࡡ࡮ࡧࠪॕ"),
  bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬॖ"),
  bstackl_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨॗ"),
  bstackl_opy_ (u"ࠬࡴࡥࡸࡅࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࠩक़"),
  bstackl_opy_ (u"࠭ࡡࡱࡲࠪख़"),
  bstackl_opy_ (u"ࠧࡶࡦ࡬ࡨࠬग़"),
  bstackl_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪज़"),
  bstackl_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡦࠩड़"),
  bstackl_opy_ (u"ࠪࡳࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨढ़"),
  bstackl_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡨࡦࡻ࡯ࡥࡸࠩफ़"),
  bstackl_opy_ (u"ࠬࡴ࡯ࡓࡧࡶࡩࡹ࠭य़"), bstackl_opy_ (u"࠭ࡦࡶ࡮࡯ࡖࡪࡹࡥࡵࠩॠ"),
  bstackl_opy_ (u"ࠧࡤ࡮ࡨࡥࡷ࡙ࡹࡴࡶࡨࡱࡋ࡯࡬ࡦࡵࠪॡ"),
  bstackl_opy_ (u"ࠨࡧࡹࡩࡳࡺࡔࡪ࡯࡬ࡲ࡬ࡹࠧॢ"),
  bstackl_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡨࡶ࡫ࡵࡲ࡮ࡣࡱࡧࡪࡒ࡯ࡨࡩ࡬ࡲ࡬࠭ॣ"),
  bstackl_opy_ (u"ࠪࡳࡹ࡮ࡥࡳࡃࡳࡴࡸ࠭।"),
  bstackl_opy_ (u"ࠫࡵࡸࡩ࡯ࡶࡓࡥ࡬࡫ࡓࡰࡷࡵࡧࡪࡕ࡮ࡇ࡫ࡱࡨࡋࡧࡩ࡭ࡷࡵࡩࠬ॥"),
  bstackl_opy_ (u"ࠬࡧࡰࡱࡃࡦࡸ࡮ࡼࡩࡵࡻࠪ०"), bstackl_opy_ (u"࠭ࡡࡱࡲࡓࡥࡨࡱࡡࡨࡧࠪ१"), bstackl_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩ२"), bstackl_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡒࡤࡧࡰࡧࡧࡦࠩ३"), bstackl_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡇࡹࡷࡧࡴࡪࡱࡱࠫ४"),
  bstackl_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨ५"),
  bstackl_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡩࡸࡺࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠨ६"),
  bstackl_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࠧ७"), bstackl_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࡆࡰࡧࡍࡳࡺࡥ࡯ࡶࠪ८"),
  bstackl_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬ९"),
  bstackl_opy_ (u"ࠨࡣࡧࡦࡕࡵࡲࡵࠩ॰"),
  bstackl_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡕࡲࡧࡰ࡫ࡴࠨॱ"),
  bstackl_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡘ࡮ࡳࡥࡰࡷࡷࠫॲ"),
  bstackl_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡴࡩࠩॳ"),
  bstackl_opy_ (u"ࠬࡧࡶࡥࠩॴ"), bstackl_opy_ (u"࠭ࡡࡷࡦࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩॵ"), bstackl_opy_ (u"ࠧࡢࡸࡧࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩॶ"), bstackl_opy_ (u"ࠨࡣࡹࡨࡆࡸࡧࡴࠩॷ"),
  bstackl_opy_ (u"ࠩࡸࡷࡪࡑࡥࡺࡵࡷࡳࡷ࡫ࠧॸ"), bstackl_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡴࡩࠩॹ"), bstackl_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡴࡵࡺࡳࡷࡪࠧॺ"),
  bstackl_opy_ (u"ࠬࡱࡥࡺࡃ࡯࡭ࡦࡹࠧॻ"), bstackl_opy_ (u"࠭࡫ࡦࡻࡓࡥࡸࡹࡷࡰࡴࡧࠫॼ"),
  bstackl_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩॽ"), bstackl_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡁࡳࡩࡶࠫॾ"), bstackl_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࡈ࡮ࡸࠧॿ"), bstackl_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡅ࡫ࡶࡴࡳࡥࡎࡣࡳࡴ࡮ࡴࡧࡇ࡫࡯ࡩࠬঀ"), bstackl_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡘࡷࡪ࡙ࡹࡴࡶࡨࡱࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨঁ"),
  bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࠨং"), bstackl_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࡵࠪঃ"),
  bstackl_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡊࡩࡴࡣࡥࡰࡪࡈࡵࡪ࡮ࡧࡇ࡭࡫ࡣ࡬ࠩ঄"),
  bstackl_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡥࡣࡸ࡬ࡩࡼ࡚ࡩ࡮ࡧࡲࡹࡹ࠭অ"),
  bstackl_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡃࡦࡸ࡮ࡵ࡮ࠨআ"), bstackl_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡆࡥࡹ࡫ࡧࡰࡴࡼࠫই"), bstackl_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡊࡱࡧࡧࡴࠩঈ"), bstackl_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡦࡲࡉ࡯ࡶࡨࡲࡹࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨউ"),
  bstackl_opy_ (u"࠭ࡤࡰࡰࡷࡗࡹࡵࡰࡂࡲࡳࡓࡳࡘࡥࡴࡧࡷࠫঊ"),
  bstackl_opy_ (u"ࠧࡶࡰ࡬ࡧࡴࡪࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩঋ"), bstackl_opy_ (u"ࠨࡴࡨࡷࡪࡺࡋࡦࡻࡥࡳࡦࡸࡤࠨঌ"),
  bstackl_opy_ (u"ࠩࡱࡳࡘ࡯ࡧ࡯ࠩ঍"),
  bstackl_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࡘࡲ࡮ࡳࡰࡰࡴࡷࡥࡳࡺࡖࡪࡧࡺࡷࠬ঎"),
  bstackl_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡤࡳࡱ࡬ࡨ࡜ࡧࡴࡤࡪࡨࡶࡸ࠭এ"),
  bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬঐ"),
  bstackl_opy_ (u"࠭ࡲࡦࡥࡵࡩࡦࡺࡥࡄࡪࡵࡳࡲ࡫ࡄࡳ࡫ࡹࡩࡷ࡙ࡥࡴࡵ࡬ࡳࡳࡹࠧ঑"),
  bstackl_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭঒"),
  bstackl_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡕࡧࡴࡩࠩও"),
  bstackl_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡖࡴࡪ࡫ࡤࠨঔ"),
  bstackl_opy_ (u"ࠪ࡫ࡵࡹࡅ࡯ࡣࡥࡰࡪࡪࠧক"),
  bstackl_opy_ (u"ࠫ࡮ࡹࡈࡦࡣࡧࡰࡪࡹࡳࠨখ"),
  bstackl_opy_ (u"ࠬࡧࡤࡣࡇࡻࡩࡨ࡚ࡩ࡮ࡧࡲࡹࡹ࠭গ"),
  bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࡪ࡙ࡣࡳ࡫ࡳࡸࠬঘ"),
  bstackl_opy_ (u"ࠧࡴ࡭࡬ࡴࡉ࡫ࡶࡪࡥࡨࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫঙ"),
  bstackl_opy_ (u"ࠨࡣࡸࡸࡴࡍࡲࡢࡰࡷࡔࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠨচ"),
  bstackl_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡑࡥࡹࡻࡲࡢ࡮ࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧছ"),
  bstackl_opy_ (u"ࠪࡷࡾࡹࡴࡦ࡯ࡓࡳࡷࡺࠧজ"),
  bstackl_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡩࡨࡈࡰࡵࡷࠫঝ"),
  bstackl_opy_ (u"ࠬࡹ࡫ࡪࡲࡘࡲࡱࡵࡣ࡬ࠩঞ"), bstackl_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰ࡚ࡹࡱࡧࠪট"), bstackl_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡋࡦࡻࠪঠ"),
  bstackl_opy_ (u"ࠨࡣࡸࡸࡴࡒࡡࡶࡰࡦ࡬ࠬড"),
  bstackl_opy_ (u"ࠩࡶ࡯࡮ࡶࡌࡰࡩࡦࡥࡹࡉࡡࡱࡶࡸࡶࡪ࠭ঢ"),
  bstackl_opy_ (u"ࠪࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࡕࡴࡩࡧࡵࡔࡦࡩ࡫ࡢࡩࡨࡷࠬণ"),
  bstackl_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩ࡜࡯࡮ࡥࡱࡺࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳ࠭ত"),
  bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡴࡵ࡬ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩথ"),
  bstackl_opy_ (u"࠭ࡥ࡯ࡨࡲࡶࡨ࡫ࡁࡱࡲࡌࡲࡸࡺࡡ࡭࡮ࠪদ"),
  bstackl_opy_ (u"ࠧࡦࡰࡶࡹࡷ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡳࡉࡣࡹࡩࡕࡧࡧࡦࡵࠪধ"), bstackl_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡆࡨࡺࡹࡵ࡯࡭ࡵࡓࡳࡷࡺࠧন"), bstackl_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡆࡨࡸࡦ࡯࡬ࡴࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠬ঩"),
  bstackl_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡴࡵࡹࡃࡢࡥ࡫ࡩࡑ࡯࡭ࡪࡶࠪপ"),
  bstackl_opy_ (u"ࠫࡨࡧ࡬ࡦࡰࡧࡥࡷࡌ࡯ࡳ࡯ࡤࡸࠬফ"),
  bstackl_opy_ (u"ࠬࡨࡵ࡯ࡦ࡯ࡩࡎࡪࠧব"),
  bstackl_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ভ"),
  bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡈࡲࡦࡨ࡬ࡦࡦࠪম"), bstackl_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡅࡺࡺࡨࡰࡴ࡬ࡾࡪࡪࠧয"),
  bstackl_opy_ (u"ࠩࡤࡹࡹࡵࡁࡤࡥࡨࡴࡹࡇ࡬ࡦࡴࡷࡷࠬর"), bstackl_opy_ (u"ࠪࡥࡺࡺ࡯ࡅ࡫ࡶࡱ࡮ࡹࡳࡂ࡮ࡨࡶࡹࡹࠧ঱"),
  bstackl_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨࡍࡳࡹࡴࡳࡷࡰࡩࡳࡺࡳࡍ࡫ࡥࠫল"),
  bstackl_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡕࡣࡳࠫ঳"),
  bstackl_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏ࡮ࡪࡶ࡬ࡥࡱ࡛ࡲ࡭ࠩ঴"), bstackl_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡁ࡭࡮ࡲࡻࡕࡵࡰࡶࡲࡶࠫ঵"), bstackl_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡩࡱࡳࡷ࡫ࡆࡳࡣࡸࡨ࡜ࡧࡲ࡯࡫ࡱ࡫ࠬশ"), bstackl_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡩࡳࡒࡩ࡯࡭ࡶࡍࡳࡈࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥࠩষ"),
  bstackl_opy_ (u"ࠪ࡯ࡪ࡫ࡰࡌࡧࡼࡇ࡭ࡧࡩ࡯ࡵࠪস"),
  bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡾࡦࡨ࡬ࡦࡕࡷࡶ࡮ࡴࡧࡴࡆ࡬ࡶࠬহ"),
  bstackl_opy_ (u"ࠬࡶࡲࡰࡥࡨࡷࡸࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨ঺"),
  bstackl_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡐ࡫ࡹࡅࡧ࡯ࡥࡾ࠭঻"),
  bstackl_opy_ (u"ࠧࡴࡪࡲࡻࡎࡕࡓࡍࡱࡪ়ࠫ"),
  bstackl_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡕࡷࡶࡦࡺࡥࡨࡻࠪঽ"),
  bstackl_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡔࡨࡷࡵࡵ࡮ࡴࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪা"), bstackl_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡗࡢ࡫ࡷࡘ࡮ࡳࡥࡰࡷࡷࠫি"),
  bstackl_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡈࡪࡨࡵࡨࡒࡵࡳࡽࡿࠧী"),
  bstackl_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡹࡹ࡯ࡥࡈࡼࡪࡩࡵࡵࡧࡉࡶࡴࡳࡈࡵࡶࡳࡷࠬু"),
  bstackl_opy_ (u"࠭ࡳ࡬࡫ࡳࡐࡴ࡭ࡃࡢࡲࡷࡹࡷ࡫ࠧূ"),
  bstackl_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡄࡦࡤࡸ࡫ࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧৃ"),
  bstackl_opy_ (u"ࠨࡨࡸࡰࡱࡉ࡯࡯ࡶࡨࡼࡹࡒࡩࡴࡶࠪৄ"),
  bstackl_opy_ (u"ࠩࡺࡥ࡮ࡺࡆࡰࡴࡄࡴࡵ࡙ࡣࡳ࡫ࡳࡸࠬ৅"),
  bstackl_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡇࡴࡴ࡮ࡦࡥࡷࡖࡪࡺࡲࡪࡧࡶࠫ৆"),
  bstackl_opy_ (u"ࠫࡦࡶࡰࡏࡣࡰࡩࠬে"),
  bstackl_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡙ࡌࡄࡧࡵࡸࠬৈ"),
  bstackl_opy_ (u"࠭ࡴࡢࡲ࡚࡭ࡹ࡮ࡓࡩࡱࡵࡸࡕࡸࡥࡴࡵࡇࡹࡷࡧࡴࡪࡱࡱࠫ৉"),
  bstackl_opy_ (u"ࠧࡴࡥࡤࡰࡪࡌࡡࡤࡶࡲࡶࠬ৊"),
  bstackl_opy_ (u"ࠨࡹࡧࡥࡑࡵࡣࡢ࡮ࡓࡳࡷࡺࠧো"),
  bstackl_opy_ (u"ࠩࡶ࡬ࡴࡽࡘࡤࡱࡧࡩࡑࡵࡧࠨৌ"),
  bstackl_opy_ (u"ࠪ࡭ࡴࡹࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡷࡶࡩ্ࠬ"),
  bstackl_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡆࡳࡳ࡬ࡩࡨࡈ࡬ࡰࡪ࠭ৎ"),
  bstackl_opy_ (u"ࠬࡱࡥࡺࡥ࡫ࡥ࡮ࡴࡐࡢࡵࡶࡻࡴࡸࡤࠨ৏"),
  bstackl_opy_ (u"࠭ࡵࡴࡧࡓࡶࡪࡨࡵࡪ࡮ࡷ࡛ࡉࡇࠧ৐"),
  bstackl_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡘࡆࡄࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠨ৑"),
  bstackl_opy_ (u"ࠨࡹࡨࡦࡉࡸࡩࡷࡧࡵࡅ࡬࡫࡮ࡵࡗࡵࡰࠬ৒"),
  bstackl_opy_ (u"ࠩ࡮ࡩࡾࡩࡨࡢ࡫ࡱࡔࡦࡺࡨࠨ৓"),
  bstackl_opy_ (u"ࠪࡹࡸ࡫ࡎࡦࡹ࡚ࡈࡆ࠭৔"),
  bstackl_opy_ (u"ࠫࡼࡪࡡࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧ৕"), bstackl_opy_ (u"ࠬࡽࡤࡢࡅࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲ࡙࡯࡭ࡦࡱࡸࡸࠬ৖"),
  bstackl_opy_ (u"࠭ࡸࡤࡱࡧࡩࡔࡸࡧࡊࡦࠪৗ"), bstackl_opy_ (u"ࠧࡹࡥࡲࡨࡪ࡙ࡩࡨࡰ࡬ࡲ࡬ࡏࡤࠨ৘"),
  bstackl_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥ࡙ࡇࡅࡇࡻ࡮ࡥ࡮ࡨࡍࡩ࠭৙"),
  bstackl_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡐࡰࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡸࡴࡐࡰ࡯ࡽࠬ৚"),
  bstackl_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࡷࠬ৛"),
  bstackl_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶ࡮࡫ࡳࠨড়"), bstackl_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷࡿࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠨঢ়"),
  bstackl_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࡈࡢࡴࡧࡻࡦࡸࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩ৞"),
  bstackl_opy_ (u"ࠧ࡮ࡣࡻࡘࡾࡶࡩ࡯ࡩࡉࡶࡪࡷࡵࡦࡰࡦࡽࠬয়"),
  bstackl_opy_ (u"ࠨࡵ࡬ࡱࡵࡲࡥࡊࡵ࡙࡭ࡸ࡯ࡢ࡭ࡧࡆ࡬ࡪࡩ࡫ࠨৠ"),
  bstackl_opy_ (u"ࠩࡸࡷࡪࡉࡡࡳࡶ࡫ࡥ࡬࡫ࡓࡴ࡮ࠪৡ"),
  bstackl_opy_ (u"ࠪࡷ࡭ࡵࡵ࡭ࡦࡘࡷࡪ࡙ࡩ࡯ࡩ࡯ࡩࡹࡵ࡮ࡕࡧࡶࡸࡒࡧ࡮ࡢࡩࡨࡶࠬৢ"),
  bstackl_opy_ (u"ࠫࡸࡺࡡࡳࡶࡌ࡛ࡉࡖࠧৣ"),
  bstackl_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡴࡻࡣࡩࡋࡧࡉࡳࡸ࡯࡭࡮ࠪ৤"),
  bstackl_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪࡎࡩࡥࡦࡨࡲࡆࡶࡩࡑࡱ࡯࡭ࡨࡿࡅࡳࡴࡲࡶࠬ৥"),
  bstackl_opy_ (u"ࠧ࡮ࡱࡦ࡯ࡑࡵࡣࡢࡶ࡬ࡳࡳࡇࡰࡱࠩ০"),
  bstackl_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇࡱࡵࡱࡦࡺࠧ১"), bstackl_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈ࡬ࡰࡹ࡫ࡲࡔࡲࡨࡧࡸ࠭২"),
  bstackl_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡆࡨࡰࡦࡿࡁࡥࡤࠪ৩")
]
bstack1l1l11_opy_ = bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡹࡵࡲ࡯ࡢࡦࠪ৪")
bstack11111ll1_opy_ = [bstackl_opy_ (u"ࠬ࠴ࡡࡱ࡭ࠪ৫"), bstackl_opy_ (u"࠭࠮ࡢࡣࡥࠫ৬"), bstackl_opy_ (u"ࠧ࠯࡫ࡳࡥࠬ৭")]
bstack11ll111l_opy_ = [bstackl_opy_ (u"ࠨ࡫ࡧࠫ৮"), bstackl_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ৯"), bstackl_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ৰ"), bstackl_opy_ (u"ࠫࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦࠪৱ")]
bstack1lll1llll_opy_ = {
  bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ৲"): bstackl_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৳"),
  bstackl_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ৴"): bstackl_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭৵"),
  bstackl_opy_ (u"ࠩࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৶"): bstackl_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৷"),
  bstackl_opy_ (u"ࠫ࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৸"): bstackl_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৹"),
  bstackl_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡵ࡫ࡲࡲࡸ࠭৺"): bstackl_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ৻")
}
bstack1ll1111ll_opy_ = [
  bstackl_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ৼ"),
  bstackl_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ৽"),
  bstackl_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৾"),
  bstackl_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ৿"),
  bstackl_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭਀"),
]
bstack1l1l111_opy_ = bstack1111l11l_opy_ + bstack1l1ll1l1_opy_ + bstack111l11l1_opy_
bstack11l11_opy_ = [
  bstackl_opy_ (u"࠭࡞࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶࠧࠫਁ"),
  bstackl_opy_ (u"ࠧ࡟ࡤࡶ࠱ࡱࡵࡣࡢ࡮࠱ࡧࡴࡳࠤࠨਂ"),
  bstackl_opy_ (u"ࠨࡠ࠴࠶࠼࠴ࠧਃ"),
  bstackl_opy_ (u"ࠩࡡ࠵࠵࠴ࠧ਄"),
  bstackl_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠳࡞࠺࠲࠿࡝࠯ࠩਅ"),
  bstackl_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠵࡟࠵࠳࠹࡞࠰ࠪਆ"),
  bstackl_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠷ࡠ࠶࠭࠲࡟࠱ࠫਇ"),
  bstackl_opy_ (u"࠭࡞࠲࠻࠵࠲࠶࠼࠸࠯ࠩਈ")
]
bstack1l1111l1l_opy_ = bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀࠫਉ")
bstack11l11l1l_opy_ = bstackl_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡧࡹࡩࡳࡺࠧਊ")
bstack1l11l11_opy_ = [ bstackl_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ਋") ]
bstack1llll111l_opy_ = [ bstackl_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ਌") ]
bstack1lll1l11l_opy_ = [ bstackl_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ਍") ]
bstack11lll1l_opy_ = bstackl_opy_ (u"࡙ࠬࡄࡌࡕࡨࡸࡺࡶࠧ਎")
bstack1lll11l1_opy_ = bstackl_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩਏ")
bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠫਐ")
bstack1l1ll1_opy_ = bstackl_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧ਑")
bstack1l1l11ll_opy_ = [
  bstackl_opy_ (u"ࠩࡈࡖࡗࡥࡆࡂࡋࡏࡉࡉ࠭਒"),
  bstackl_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪਓ"),
  bstackl_opy_ (u"ࠫࡊࡘࡒࡠࡄࡏࡓࡈࡑࡅࡅࡡࡅ࡝ࡤࡉࡌࡊࡇࡑࡘࠬਔ"),
  bstackl_opy_ (u"ࠬࡋࡒࡓࡡࡑࡉ࡙࡝ࡏࡓࡍࡢࡇࡍࡇࡎࡈࡇࡇࠫਕ"),
  bstackl_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡆࡖࡢࡒࡔ࡚࡟ࡄࡑࡑࡒࡊࡉࡔࡆࡆࠪਖ"),
  bstackl_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡅࡏࡓࡘࡋࡄࠨਗ"),
  bstackl_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡘࡋࡔࠨਘ"),
  bstackl_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊࡌࡕࡔࡇࡇࠫਙ"),
  bstackl_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡆࡈࡏࡓࡖࡈࡈࠬਚ"),
  bstackl_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਛ"),
  bstackl_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭ਜ"),
  bstackl_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣࡎࡔࡖࡂࡎࡌࡈࠬਝ"),
  bstackl_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪਞ"),
  bstackl_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡕࡏࡐࡈࡐࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩਟ"),
  bstackl_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭ਠ"),
  bstackl_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪਡ"),
  bstackl_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡍࡕࡓࡕࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧਢ"),
  bstackl_opy_ (u"ࠬࡋࡒࡓࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਣ"),
  bstackl_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧਤ"),
  bstackl_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡕࡉࡘࡕࡌࡖࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ਥ"),
  bstackl_opy_ (u"ࠨࡇࡕࡖࡤࡓࡁࡏࡆࡄࡘࡔࡘ࡙ࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧਦ"),
]
def bstack1l11l11l1_opy_():
  global CONFIG
  headers = {
        bstackl_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨਧ"): bstackl_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ਨ"),
      }
  proxy = bstack11llll1_opy_(CONFIG)
  proxies = {}
  if CONFIG.get(bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ਩")) or CONFIG.get(bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩਪ")):
    proxies = {
      bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬਫ"): proxy
    }
  try:
    response = requests.get(bstack1111ll11_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1lll11ll1_opy_ = response.json()[bstackl_opy_ (u"ࠧࡩࡷࡥࡷࠬਬ")]
      logger.debug(bstack1l11lll1_opy_.format(response.json()))
      return bstack1lll11ll1_opy_
    else:
      logger.debug(bstack1l111l1l_opy_.format(bstackl_opy_ (u"ࠣࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡎࡘࡕࡎࠡࡲࡤࡶࡸ࡫ࠠࡦࡴࡵࡳࡷࠦࠢਭ")))
  except Exception as e:
    logger.debug(bstack1l111l1l_opy_.format(e))
def bstack111l11ll_opy_(hub_url):
  global CONFIG
  url = bstackl_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦਮ")+  hub_url + bstackl_opy_ (u"ࠥ࠳ࡨ࡮ࡥࡤ࡭ࠥਯ")
  headers = {
        bstackl_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪਰ"): bstackl_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ਱"),
      }
  proxy = bstack11llll1_opy_(CONFIG)
  proxies = {}
  if CONFIG.get(bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩਲ")) or CONFIG.get(bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫਲ਼")):
    proxies = {
      bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ਴"): proxy
    }
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1l11l1ll_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1l1ll1l_opy_.format(hub_url, e))
def bstack1ll11l_opy_():
  try:
    global bstack1l1l1_opy_
    bstack1lll11ll1_opy_ = bstack1l11l11l1_opy_()
    with Pool() as pool:
      results = pool.map(bstack111l11ll_opy_, bstack1lll11ll1_opy_)
    bstack1lll111l_opy_ = {}
    for item in results:
      hub_url = item[bstackl_opy_ (u"ࠩ࡫ࡹࡧࡥࡵࡳ࡮ࠪਵ")]
      latency = item[bstackl_opy_ (u"ࠪࡰࡦࡺࡥ࡯ࡥࡼࠫਸ਼")]
      bstack1lll111l_opy_[hub_url] = latency
    bstack1ll11ll1l_opy_ = min(bstack1lll111l_opy_, key= lambda x: bstack1lll111l_opy_[x])
    bstack1l1l1_opy_ = bstack1ll11ll1l_opy_
    logger.debug(bstack1llllll1l_opy_.format(bstack1ll11ll1l_opy_))
  except Exception as e:
    logger.debug(bstack1ll11l11l_opy_.format(e))
bstack11l1l1ll_opy_ = bstackl_opy_ (u"ࠫࡘ࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡰࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠰ࠥࡻࡳࡪࡰࡪࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠺ࠡࡽࢀࠫ਷")
bstack11ll1ll_opy_ = bstackl_opy_ (u"ࠬࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡࡵࡨࡸࡺࡶࠡࠨਸ")
bstack1l1l1ll11_opy_ = bstackl_opy_ (u"࠭ࡐࡢࡴࡶࡩࡩࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠨਹ")
bstack1ll111l1_opy_ = bstackl_opy_ (u"ࠧࡔࡣࡱ࡭ࡹ࡯ࡺࡦࡦࠣࡧࡴࡴࡦࡪࡩࠣࡪ࡮ࡲࡥ࠻ࠢࡾࢁࠬ਺")
bstack1ll1l1l1_opy_ = bstackl_opy_ (u"ࠨࡗࡶ࡭ࡳ࡭ࠠࡩࡷࡥࠤࡺࡸ࡬࠻ࠢࡾࢁࠬ਻")
bstack1l1ll11ll_opy_ = bstackl_opy_ (u"ࠩࡖࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡲࡵࡧࡧࠤࡼ࡯ࡴࡩࠢ࡬ࡨ࠿ࠦࡻࡾ਼ࠩ")
bstack1lll1l1_opy_ = bstackl_opy_ (u"ࠪࡖࡪࡩࡥࡪࡸࡨࡨࠥ࡯࡮ࡵࡧࡵࡶࡺࡶࡴ࠭ࠢࡨࡼ࡮ࡺࡩ࡯ࡩࠪ਽")
bstack11lllllll_opy_ = bstackl_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡡࠩਾ")
bstack1lll1111_opy_ = bstackl_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹࠦࡡ࡯ࡦࠣࡴࡾࡺࡥࡴࡶ࠰ࡷࡪࡲࡥ࡯࡫ࡸࡱࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺࠠࡱࡻࡷࡩࡸࡺ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡢࠪਿ")
bstack1l1l111l_opy_ = bstackl_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡳࡱࡥࡳࡹ࠲ࠠࡱࡣࡥࡳࡹࠦࡡ࡯ࡦࠣࡷࡪࡲࡥ࡯࡫ࡸࡱࡱ࡯ࡢࡳࡣࡵࡽࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡹࠠࡵࡱࠣࡶࡺࡴࠠࡳࡱࡥࡳࡹࠦࡴࡦࡵࡷࡷࠥ࡯࡮ࠡࡲࡤࡶࡦࡲ࡬ࡦ࡮࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡶࡴࡨ࡯ࡵࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡷࡵࡢࡰࡶࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠲ࡶࡡࡣࡱࡷࠤࡷࡵࡢࡰࡶࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡬ࡪࡤࡵࡥࡷࡿࡠࠨੀ")
bstack1l1l1lll_opy_ = bstackl_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡤࡨ࡬ࡦࡼࡥࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡣࡧ࡫ࡥࡻ࡫ࡠࠨੁ")
bstack1111111l_opy_ = bstackl_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡤࡴࡵ࡯ࡵ࡮࠯ࡦࡰ࡮࡫࡮ࡵࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡃࡳࡴ࡮ࡻ࡭࠮ࡒࡼࡸ࡭ࡵ࡮࠮ࡅ࡯࡭ࡪࡴࡴࡡࠩੂ")
bstack1l1l1l11_opy_ = bstackl_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡣࠫ੃")
bstack1ll1ll1_opy_ = bstackl_opy_ (u"ࠪࡇࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡦࡪࡰࡧࠤࡪ࡯ࡴࡩࡧࡵࠤࡘ࡫࡬ࡦࡰ࡬ࡹࡲࠦ࡯ࡳࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡶࡤࡰࡱࠦࡴࡩࡧࠣࡶࡪࡲࡥࡷࡣࡱࡸࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡹࠠࡶࡵ࡬ࡲ࡬ࠦࡰࡪࡲࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴ࠰ࠪ੄")
bstack1lll11l1l_opy_ = bstackl_opy_ (u"ࠫࡍࡧ࡮ࡥ࡮࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤ࡮ࡲࡷࡪ࠭੅")
bstack1l1lll_opy_ = bstackl_opy_ (u"ࠬࡇ࡬࡭ࠢࡧࡳࡳ࡫ࠡࠨ੆")
bstack1l1ll1l11_opy_ = bstackl_opy_ (u"࠭ࡃࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸࠥࡧࡴࠡࡣࡱࡽࠥࡶࡡࡳࡧࡱࡸࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡱࡩࠤࠧࢁࡽࠣ࠰ࠣࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡩ࡬ࡶࡦࡨࠤࡦࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭࠱ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡤࡱࡱࠦࡦࡪ࡮ࡨࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨࡲࡶࠥࡺࡥࡴࡶࡶ࠲ࠬੇ")
bstack1lllll11l_opy_ = bstackl_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡳࡧࡧࡩࡳࡺࡩࡢ࡮ࡶࠤࡳࡵࡴࠡࡲࡵࡳࡻ࡯ࡤࡦࡦ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡦࡪࡤࠡࡶ࡫ࡩࡲࠦࡩ࡯ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧࠣࡥࡸࠦࠢࡶࡵࡨࡶࡓࡧ࡭ࡦࠤࠣࡥࡳࡪࠠࠣࡣࡦࡧࡪࡹࡳࡌࡧࡼࠦࠥࡵࡲࠡࡵࡨࡸࠥࡺࡨࡦ࡯ࠣࡥࡸࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠤࡻࡧࡲࡪࡣࡥࡰࡪࡹ࠺ࠡࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠥࠤࡦࡴࡤࠡࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠧ࠭ੈ")
bstack1l11lllll_opy_ = bstackl_opy_ (u"ࠨࡏࡤࡰ࡫ࡵࡲ࡮ࡧࡧࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫࡯࡬ࡦ࠼ࠥࡿࢂࠨࠧ੉")
bstack1l11ll1l_opy_ = bstackl_opy_ (u"ࠩࡈࡲࡨࡵࡵ࡯ࡶࡨࡶࡪࡪࠠࡦࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡱࠢ࠰ࠤࢀࢃࠧ੊")
bstack11lll1l11_opy_ = bstackl_opy_ (u"ࠪࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡑࡵࡣࡢ࡮ࠪੋ")
bstack1l1l11l11_opy_ = bstackl_opy_ (u"ࠫࡘࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡒ࡯ࡤࡣ࡯ࠫੌ")
bstack1l111ll1l_opy_ = bstackl_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡑࡵࡣࡢ࡮ࠣ࡭ࡸࠦ࡮ࡰࡹࠣࡶࡺࡴ࡮ࡪࡰࡪ੍ࠥࠬ")
bstack1ll1l111_opy_ = bstackl_opy_ (u"࠭ࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡶࡸࡦࡸࡴࠡࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱࡀࠠࡼࡿࠪ੎")
bstack1111l1ll_opy_ = bstackl_opy_ (u"ࠧࡔࡶࡤࡶࡹ࡯࡮ࡨࠢ࡯ࡳࡨࡧ࡬ࠡࡤ࡬ࡲࡦࡸࡹࠡࡹ࡬ࡸ࡭ࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࡽࢀࠫ੏")
bstack111lll_opy_ = bstackl_opy_ (u"ࠨࡗࡳࡨࡦࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠩ੐")
bstack11lllll1l_opy_ = bstackl_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡰࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷࠥࢁࡽࠨੑ")
bstack111l11_opy_ = bstackl_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣࡴࡷࡵࡶࡪࡦࡨࠤࡦࡴࠠࡢࡲࡳࡶࡴࡶࡲࡪࡣࡷࡩࠥࡌࡗࠡࠪࡵࡳࡧࡵࡴ࠰ࡲࡤࡦࡴࡺࠩࠡ࡫ࡱࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫࡯࡬ࡦ࠮ࠣࡷࡰ࡯ࡰࠡࡶ࡫ࡩࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡭ࡨࡽࠥ࡯࡮ࠡࡥࡲࡲ࡫࡯ࡧࠡ࡫ࡩࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡹࡩ࡮ࡲ࡯ࡩࠥࡶࡹࡵࡪࡲࡲࠥࡹࡣࡳ࡫ࡳࡸࠥࡽࡩࡵࡪࡲࡹࡹࠦࡡ࡯ࡻࠣࡊ࡜࠴ࠧ੒")
bstack1l11l111_opy_ = bstackl_opy_ (u"ࠫࡘ࡫ࡴࡵ࡫ࡱ࡫ࠥ࡮ࡴࡵࡲࡓࡶࡴࡾࡹ࠰ࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡱࡱࠤࡨࡻࡲࡳࡧࡱࡸࡱࡿࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠣࡺࡪࡸࡳࡪࡱࡱࠤࡴ࡬ࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࠫࡿࢂ࠯ࠬࠡࡲ࡯ࡩࡦࡹࡥࠡࡷࡳ࡫ࡷࡧࡤࡦࠢࡷࡳ࡙ࠥࡥ࡭ࡧࡱ࡭ࡺࡳ࠾࠾࠶࠱࠴࠳࠶ࠠࡰࡴࠣࡶࡪ࡬ࡥࡳࠢࡷࡳࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡷࡸࡹ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡰࡥࡶ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠰ࡴࡸࡲ࠲ࡺࡥࡴࡶࡶ࠱ࡧ࡫ࡨࡪࡰࡧ࠱ࡵࡸ࡯ࡹࡻࠦࡴࡾࡺࡨࡰࡰࠣࡪࡴࡸࠠࡢࠢࡺࡳࡷࡱࡡࡳࡱࡸࡲࡩ࠴ࠧ੓")
bstack1l1lll11_opy_ = bstackl_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡻࡰࡰࠥ࡬ࡩ࡭ࡧ࠱࠲ࠬ੔")
bstack11111_opy_ = bstackl_opy_ (u"࠭ࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࡤࠡࡶ࡫ࡩࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠤࠫ੕")
bstack1llll11ll_opy_ = bstackl_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡺࡨࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨ࡬ࡰࡪ࠴ࠠࡼࡿࠪ੖")
bstack1111ll1_opy_ = bstackl_opy_ (u"ࠨࡇࡻࡴࡪࡩࡴࡦࡦࠣࡥࡹࠦ࡬ࡦࡣࡶࡸࠥ࠷ࠠࡪࡰࡳࡹࡹ࠲ࠠࡳࡧࡦࡩ࡮ࡼࡥࡥࠢ࠳ࠫ੗")
bstack1l1111_opy_ = bstackl_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡦࡸࡶ࡮ࡴࡧࠡࡃࡳࡴࠥࡻࡰ࡭ࡱࡤࡨ࠳ࠦࡻࡾࠩ੘")
bstack11llll1l_opy_ = bstackl_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱ࡮ࡲࡥࡩࠦࡁࡱࡲ࠱ࠤࡎࡴࡶࡢ࡮࡬ࡨࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨࠡࡲࡵࡳࡻ࡯ࡤࡦࡦࠣࡿࢂ࠴ࠧਖ਼")
bstack11l1llll_opy_ = bstackl_opy_ (u"ࠫࡐ࡫ࡹࡴࠢࡦࡥࡳࡴ࡯ࡵࠢࡦࡳ࠲࡫ࡸࡪࡵࡷࠤࡦࡹࠠࡢࡲࡳࠤࡻࡧ࡬ࡶࡧࡶ࠰ࠥࡻࡳࡦࠢࡤࡲࡾࠦ࡯࡯ࡧࠣࡴࡷࡵࡰࡦࡴࡷࡽࠥ࡬ࡲࡰ࡯ࠣࡿ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡳࡥࡹ࡮࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࡁࡹࡴࡳ࡫ࡱ࡫ࡃ࠲ࠠࡴࡪࡤࡶࡪࡧࡢ࡭ࡧࡢ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࡽ࠭ࠢࡲࡲࡱࡿࠠࠣࡲࡤࡸ࡭ࠨࠠࡢࡰࡧࠤࠧࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠣࠢࡦࡥࡳࠦࡣࡰ࠯ࡨࡼ࡮ࡹࡴࠡࡶࡲ࡫ࡪࡺࡨࡦࡴ࠱ࠫਗ਼")
bstack11l11lll_opy_ = bstackl_opy_ (u"ࠬࡡࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡢࡲࡳࠤࡵࡸ࡯ࡱࡧࡵࡸࡾࡣࠠࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠠࡢࡴࡨࠤࢀ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡴࡦࡺࡨ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡵ࡫ࡥࡷ࡫ࡡࡣ࡮ࡨࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾ࡾ࠰ࠣࡊࡴࡸࠠ࡮ࡱࡵࡩࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡰ࡭ࡧࡤࡷࡪࠦࡶࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡷࡸࡹ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡰࡥࡶ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵࡶࡩࡶ࡯࠲ࡷࡪࡺ࠭ࡶࡲ࠰ࡸࡪࡹࡴࡴ࠱ࡶࡴࡪࡩࡩࡧࡻ࠰ࡥࡵࡶࠧਜ਼")
bstack11lll1l1_opy_ = bstackl_opy_ (u"࡛࠭ࡊࡰࡹࡥࡱ࡯ࡤࠡࡣࡳࡴࠥࡶࡲࡰࡲࡨࡶࡹࡿ࡝ࠡࡕࡸࡴࡵࡵࡲࡵࡧࡧࠤࡻࡧ࡬ࡶࡧࡶࠤࡴ࡬ࠠࡢࡲࡳࠤࡦࡸࡥࠡࡱࡩࠤࢀ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡴࡦࡺࡨ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡵ࡫ࡥࡷ࡫ࡡࡣ࡮ࡨࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾ࡾ࠰ࠣࡊࡴࡸࠠ࡮ࡱࡵࡩࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡰ࡭ࡧࡤࡷࡪࠦࡶࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡷࡸࡹ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡰࡥࡶ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵࡶࡩࡶ࡯࠲ࡷࡪࡺ࠭ࡶࡲ࠰ࡸࡪࡹࡴࡴ࠱ࡶࡴࡪࡩࡩࡧࡻ࠰ࡥࡵࡶࠧੜ")
bstack1lllll1l1_opy_ = bstackl_opy_ (u"ࠧࡖࡵ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡣࡳࡴࠥ࡯ࡤࠡࡽࢀࠤ࡫ࡵࡲࠡࡪࡤࡷ࡭ࠦ࠺ࠡࡽࢀ࠲ࠬ੝")
bstack111111ll_opy_ = bstackl_opy_ (u"ࠨࡃࡳࡴ࡛ࠥࡰ࡭ࡱࡤࡨࡪࡪࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾ࠴ࠠࡊࡆࠣ࠾ࠥࢁࡽࠨਫ਼")
bstack11ll111_opy_ = bstackl_opy_ (u"ࠩࡘࡷ࡮ࡴࡧࠡࡃࡳࡴࠥࡀࠠࡼࡿ࠱ࠫ੟")
bstack1lll1ll_opy_ = bstackl_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡰࡴࠣࡺࡦࡴࡩ࡭࡮ࡤࠤࡵࡿࡴࡩࡱࡱࠤࡹ࡫ࡳࡵࡵ࠯ࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡽࡩࡵࡪࠣࡴࡦࡸࡡ࡭࡮ࡨࡰࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡀࠤ࠶࠭੠")
bstack1lllllll_opy_ = bstackl_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࠽ࠤࢀࢃࠧ੡")
bstack11111lll_opy_ = bstackl_opy_ (u"ࠬࡉ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡥ࡯ࡳࡸ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲ࠻ࠢࡾࢁࠬ੢")
bstack11111ll_opy_ = bstackl_opy_ (u"࠭ࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡪࡩࡹࠦࡲࡦࡣࡶࡳࡳࠦࡦࡰࡴࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡪࡧࡴࡶࡴࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩ࠳ࠦࡻࡾࠩ੣")
bstack1l11111ll_opy_ = bstackl_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡨࡵࡳࡲࠦࡡࡱ࡫ࠣࡧࡦࡲ࡬࠯ࠢࡈࡶࡷࡵࡲ࠻ࠢࡾࢁࠬ੤")
bstack111llll1_opy_ = bstackl_opy_ (u"ࠨࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡮࡯ࡸࠢࡥࡹ࡮ࡲࡤࠡࡗࡕࡐ࠱ࠦࡡࡴࠢࡥࡹ࡮ࡲࡤࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠥ࡯ࡳࠡࡰࡲࡸࠥࡻࡳࡦࡦ࠱ࠫ੥")
bstack1ll1ll1l_opy_ = bstackl_opy_ (u"ࠩࡖࡩࡷࡼࡥࡳࠢࡶ࡭ࡩ࡫ࠠࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠫࡿࢂ࠯ࠠࡪࡵࠣࡲࡴࡺࠠࡴࡣࡰࡩࠥࡧࡳࠡࡥ࡯࡭ࡪࡴࡴࠡࡵ࡬ࡨࡪࠦࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠪࡾࢁ࠮࠭੦")
bstack1ll1111_opy_ = bstackl_opy_ (u"࡚ࠪ࡮࡫ࡷࠡࡤࡸ࡭ࡱࡪࠠࡰࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡧࡥࡸ࡮ࡢࡰࡣࡵࡨ࠿ࠦࡻࡾࠩ੧")
bstack1l1l111l1_opy_ = bstackl_opy_ (u"࡚ࠫࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡢࡥࡦࡩࡸࡹࠠࡢࠢࡳࡶ࡮ࡼࡡࡵࡧࠣࡨࡴࡳࡡࡪࡰ࠽ࠤࢀࢃࠠ࠯ࠢࡖࡩࡹࠦࡴࡩࡧࠣࡪࡴࡲ࡬ࡰࡹ࡬ࡲ࡬ࠦࡣࡰࡰࡩ࡭࡬ࠦࡩ࡯ࠢࡼࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠣࡪ࡮ࡲࡥ࠻ࠢ࡟ࡲ࠲࠳࠭࠮࠯࠰࠱࠲࠳࠭࠮ࠢ࡟ࡲࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭࠼ࠣࡸࡷࡻࡥࠡ࡞ࡱ࠱࠲࠳࠭࠮࠯࠰࠱࠲࠳࠭ࠨ੨")
bstack11ll_opy_ = bstackl_opy_ (u"࡙ࠬ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡨࡧࡷࡣࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࡡࡨࡶࡷࡵࡲࠡ࠼ࠣࡿࢂ࠭੩")
bstack1111l11_opy_ = bstackl_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡲࡩࡥࡡ࡮ࡲ࡯࡭ࡹࡻࡤࡦࡡࡨࡺࡪࡴࡴࠡࡨࡲࡶ࡙ࠥࡄࡌࡕࡨࡸࡺࡶࠠࡼࡿࠥ੪")
bstack111ll11l_opy_ = bstackl_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡳࡪ࡟ࡢ࡯ࡳࡰ࡮ࡺࡵࡥࡧࡢࡩࡻ࡫࡮ࡵࠢࡩࡳࡷࠦࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠢࡾࢁࠧ੫")
bstack1ll1l1l_opy_ = bstackl_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡴࡤࡠࡣࡰࡴࡱ࡯ࡴࡶࡦࡨࡣࡪࡼࡥ࡯ࡶࠣࡪࡴࡸࠠࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠤࢀࢃࠢ੬")
bstack1ll111lll_opy_ = bstackl_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡫࡯ࡲࡦࡡࡵࡩࡶࡻࡥࡴࡶࠣࡿࢂࠨ੭")
bstack1l1l1l1ll_opy_ = bstackl_opy_ (u"ࠥࡔࡔ࡙ࡔࠡࡇࡹࡩࡳࡺࠠࡼࡿࠣࡶࡪࡹࡰࡰࡰࡶࡩࠥࡀࠠࡼࡿࠥ੮")
bstack1lll111_opy_ = bstackl_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࠣࡴࡷࡵࡸࡺࠢࡶࡩࡹࡺࡩ࡯ࡩࡶ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨ੯")
bstack1l11lll1_opy_ = bstackl_opy_ (u"ࠬࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡧࡴࡲࡱࠥ࠵࡮ࡦࡺࡷࡣ࡭ࡻࡢࡴࠢࡾࢁࠬੰ")
bstack1l111l1l_opy_ = bstackl_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠤ࡫ࡸ࡯࡮ࠢ࠲ࡲࡪࡾࡴࡠࡪࡸࡦࡸࡀࠠࡼࡿࠪੱ")
bstack1llllll1l_opy_ = bstackl_opy_ (u"ࠧࡏࡧࡤࡶࡪࡹࡴࠡࡪࡸࡦࠥࡧ࡬࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡶ࠾ࠥࢁࡽࠨੲ")
bstack1ll11l11l_opy_ = bstackl_opy_ (u"ࠨࡇࡕࡖࡔࡘࠠࡊࡐࠣࡅࡑࡒࡏࡄࡃࡗࡉࠥࡎࡕࡃࠢࡾࢁࠬੳ")
bstack1l11l1ll_opy_ = bstackl_opy_ (u"ࠩࡏࡥࡹ࡫࡮ࡤࡻࠣࡳ࡫ࠦࡨࡶࡤ࠽ࠤࢀࢃࠠࡪࡵ࠽ࠤࢀࢃࠧੴ")
bstack1l1ll1l_opy_ = bstackl_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦ࡬ࡢࡶࡨࡲࡨࡿࠠࡧࡱࡵࠤࢀࢃࠠࡩࡷࡥ࠾ࠥࢁࡽࠨੵ")
bstack1l1l1ll1l_opy_ = bstackl_opy_ (u"ࠫࡍࡻࡢࠡࡷࡵࡰࠥࡩࡨࡢࡰࡪࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦ࡯ࡱࡶ࡬ࡱࡦࡲࠠࡩࡷࡥ࠾ࠥࢁࡽࠨ੶")
bstack1l111111_opy_ = bstackl_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡹ࡮ࡥࠡࡱࡳࡸ࡮ࡳࡡ࡭ࠢ࡫ࡹࡧࠦࡵࡳ࡮࠽ࠤࢀࢃࠧ੷")
bstack1l11l1l1_opy_ = bstackl_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭੸")
bstack11l11ll_opy_ = bstackl_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭੹")
from ._version import __version__
bstack11l1111l_opy_ = None
CONFIG = {}
bstack1l111l111_opy_ = {}
bstack111l111_opy_ = {}
bstack1ll1ll11l_opy_ = None
bstack1ll11lll1_opy_ = None
bstack1l1l1ll_opy_ = None
bstack1l1ll1ll1_opy_ = -1
bstack1l1l1l1_opy_ = bstack1l11ll111_opy_
bstack1l11lll_opy_ = 1
bstack1l11l1lll_opy_ = False
bstack1l1ll11l_opy_ = bstackl_opy_ (u"ࠨࠩ੺")
bstack1l1111l_opy_ = bstackl_opy_ (u"ࠩࠪ੻")
bstack1l111l11_opy_ = False
bstack111l_opy_ = True
bstack1ll1l1lll_opy_ = bstackl_opy_ (u"ࠪࠫ੼")
bstack1ll1ll_opy_ = []
bstack1l1l1_opy_ = bstackl_opy_ (u"ࠫࠬ੽")
bstack1lll11l11_opy_ = False
bstack1l1l11111_opy_ = None
bstack111lll1_opy_ = False
bstack1l1ll1l1l_opy_ = None
bstack1l1111ll_opy_ = None
bstack1ll1llll_opy_ = None
bstack1l11111l1_opy_ = None
bstack1l11l1l11_opy_ = None
bstack11l1l1l_opy_ = None
bstack1l1llll1l_opy_ = None
bstack1l11111l_opy_ = None
bstack1l11llll1_opy_ = None
bstack1llllll11_opy_ = None
bstack1l111lll_opy_ = None
bstack1l111l1_opy_ = None
bstack11l1111_opy_ = None
bstack1ll111l11_opy_ = None
bstack1ll11_opy_ = bstackl_opy_ (u"ࠧࠨ੾")
class bstack1l11l1l1l_opy_(threading.Thread):
  def run(self):
    self.exc = None
    try:
      self.ret = self._target(*self._args, **self._kwargs)
    except Exception as e:
      self.exc = e
  def join(self, timeout=None):
    super(bstack1l11l1l1l_opy_, self).join(timeout)
    if self.exc:
      raise self.exc
    return self.ret
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1l1l1l1_opy_,
                    format=bstackl_opy_ (u"࠭࡜࡯ࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫ੿"),
                    datefmt=bstackl_opy_ (u"ࠧࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ઀"))
def bstack1llll1111_opy_():
  global CONFIG
  global bstack1l1l1l1_opy_
  if bstackl_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪઁ") in CONFIG:
    bstack1l1l1l1_opy_ = bstack111111l1_opy_[CONFIG[bstackl_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫં")]]
    logging.getLogger().setLevel(bstack1l1l1l1_opy_)
def bstack111l1ll_opy_():
  global CONFIG
  global bstack111lll1_opy_
  bstack1ll11ll_opy_ = bstack1llll11l_opy_(CONFIG)
  if(bstackl_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬઃ") in bstack1ll11ll_opy_ and str(bstack1ll11ll_opy_[bstackl_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭઄")]).lower() == bstackl_opy_ (u"ࠬࡺࡲࡶࡧࠪઅ")):
    bstack111lll1_opy_ = True
def bstack111ll1l1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1ll111111_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll1l11l_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstackl_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡣࡰࡰࡩ࡭࡬࡬ࡩ࡭ࡧࠥઆ") == args[i].lower() or bstackl_opy_ (u"ࠢ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡲ࡫࡯ࡧࠣઇ") == args[i].lower():
      path = args[i+1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1ll1l1lll_opy_
      bstack1ll1l1lll_opy_ += bstackl_opy_ (u"ࠨ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡅࡲࡲ࡫࡯ࡧࡇ࡫࡯ࡩࠥ࠭ઈ") + path
      return path
  return None
def bstack1l1l1l1l_opy_():
  bstack11lllll1_opy_ = bstack1ll1l11l_opy_()
  if bstack11lllll1_opy_ and os.path.exists(os.path.abspath(bstack11lllll1_opy_)):
    fileName = bstack11lllll1_opy_
  if bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࠭ઉ") in os.environ and os.path.exists(os.path.abspath(os.environ[bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋࠧઊ")])) and not bstackl_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࠭ઋ") in locals():
    fileName = os.environ[bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆࠩઌ")]
  if bstackl_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨઍ") in locals():
    bstack1111l111_opy_ = os.path.abspath(fileName)
  else:
    bstack1111l111_opy_ = bstackl_opy_ (u"ࠧࠨ઎")
  bstack1lll1_opy_ = os.getcwd()
  bstack1ll11111l_opy_ = bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫએ")
  bstack1lllll1ll_opy_ = bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡤࡱࡱ࠭ઐ")
  while (not os.path.exists(bstack1111l111_opy_)) and bstack1lll1_opy_ != bstackl_opy_ (u"ࠥࠦઑ"):
    bstack1111l111_opy_ = os.path.join(bstack1lll1_opy_, bstack1ll11111l_opy_)
    if not os.path.exists(bstack1111l111_opy_):
      bstack1111l111_opy_ = os.path.join(bstack1lll1_opy_, bstack1lllll1ll_opy_)
    if bstack1lll1_opy_ != os.path.dirname(bstack1lll1_opy_):
      bstack1lll1_opy_ = os.path.dirname(bstack1lll1_opy_)
    else:
      bstack1lll1_opy_ = bstackl_opy_ (u"ࠦࠧ઒")
  if not os.path.exists(bstack1111l111_opy_):
    bstack1lllll111_opy_(
      bstack1l1ll1l11_opy_.format(os.getcwd()))
  with open(bstack1111l111_opy_, bstackl_opy_ (u"ࠬࡸࠧઓ")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack1lllll111_opy_(bstack1l11lllll_opy_.format(str(exc)))
def bstack11ll1lll_opy_(config):
  bstack1111llll_opy_ = bstack1l1lll111_opy_(config)
  for option in list(bstack1111llll_opy_):
    if option.lower() in bstack1l1lllll_opy_ and option != bstack1l1lllll_opy_[option.lower()]:
      bstack1111llll_opy_[bstack1l1lllll_opy_[option.lower()]] = bstack1111llll_opy_[option]
      del bstack1111llll_opy_[option]
  return config
def bstack1l11ll11l_opy_():
  global bstack111l111_opy_
  for key, bstack11lll111l_opy_ in bstack1lll1l1l1_opy_.items():
    if isinstance(bstack11lll111l_opy_, list):
      for var in bstack11lll111l_opy_:
        if var in os.environ:
          bstack111l111_opy_[key] = os.environ[var]
          break
    elif bstack11lll111l_opy_ in os.environ:
      bstack111l111_opy_[key] = os.environ[bstack11lll111l_opy_]
  if bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨઔ") in os.environ:
    bstack111l111_opy_[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫક")] = {}
    bstack111l111_opy_[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬખ")][bstackl_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫગ")] = os.environ[bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬઘ")]
def bstack11lll11_opy_():
  global bstack1l111l111_opy_
  global bstack1ll1l1lll_opy_
  for idx, val in enumerate(sys.argv):
    if idx<len(sys.argv) and bstackl_opy_ (u"ࠫ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧઙ").lower() == val.lower():
      bstack1l111l111_opy_[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩચ")] = {}
      bstack1l111l111_opy_[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪછ")][bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩજ")] = sys.argv[idx+1]
      del sys.argv[idx:idx+2]
      break
  for key, bstack11llll_opy_ in bstack1l11ll11_opy_.items():
    if isinstance(bstack11llll_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack11llll_opy_:
          if idx<len(sys.argv) and bstackl_opy_ (u"ࠨ࠯࠰ࠫઝ") + var.lower() == val.lower() and not key in bstack1l111l111_opy_:
            bstack1l111l111_opy_[key] = sys.argv[idx+1]
            bstack1ll1l1lll_opy_ += bstackl_opy_ (u"ࠩࠣ࠱࠲࠭ઞ") + var + bstackl_opy_ (u"ࠪࠤࠬટ") + sys.argv[idx+1]
            del sys.argv[idx:idx+2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx<len(sys.argv) and bstackl_opy_ (u"ࠫ࠲࠳ࠧઠ") + bstack11llll_opy_.lower() == val.lower() and not key in bstack1l111l111_opy_:
          bstack1l111l111_opy_[key] = sys.argv[idx+1]
          bstack1ll1l1lll_opy_ += bstackl_opy_ (u"ࠬࠦ࠭࠮ࠩડ") + bstack11llll_opy_ + bstackl_opy_ (u"࠭ࠠࠨઢ") + sys.argv[idx+1]
          del sys.argv[idx:idx+2]
def bstack1llll1l1l_opy_(config):
  bstack1l11l_opy_ = config.keys()
  for bstack1ll1lll1_opy_, bstack1l11l1l_opy_ in bstack11ll11l_opy_.items():
    if bstack1l11l1l_opy_ in bstack1l11l_opy_:
      config[bstack1ll1lll1_opy_] = config[bstack1l11l1l_opy_]
      del config[bstack1l11l1l_opy_]
  for bstack1ll1lll1_opy_, bstack1l11l1l_opy_ in bstack111111l_opy_.items():
    if isinstance(bstack1l11l1l_opy_, list):
      for bstack1l1l1111_opy_ in bstack1l11l1l_opy_:
        if bstack1l1l1111_opy_ in bstack1l11l_opy_:
          config[bstack1ll1lll1_opy_] = config[bstack1l1l1111_opy_]
          del config[bstack1l1l1111_opy_]
          break
    elif bstack1l11l1l_opy_ in bstack1l11l_opy_:
        config[bstack1ll1lll1_opy_] = config[bstack1l11l1l_opy_]
        del config[bstack1l11l1l_opy_]
  for bstack1l1l1111_opy_ in list(config):
    for bstack1ll1ll111_opy_ in bstack1l1l111_opy_:
      if bstack1l1l1111_opy_.lower() == bstack1ll1ll111_opy_.lower() and bstack1l1l1111_opy_ != bstack1ll1ll111_opy_:
        config[bstack1ll1ll111_opy_] = config[bstack1l1l1111_opy_]
        del config[bstack1l1l1111_opy_]
  bstack1l1llll11_opy_ = []
  if bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪણ") in config:
    bstack1l1llll11_opy_ = config[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫત")]
  for platform in bstack1l1llll11_opy_:
    for bstack1l1l1111_opy_ in list(platform):
      for bstack1ll1ll111_opy_ in bstack1l1l111_opy_:
        if bstack1l1l1111_opy_.lower() == bstack1ll1ll111_opy_.lower() and bstack1l1l1111_opy_ != bstack1ll1ll111_opy_:
          platform[bstack1ll1ll111_opy_] = platform[bstack1l1l1111_opy_]
          del platform[bstack1l1l1111_opy_]
  for bstack1ll1lll1_opy_, bstack1l11l1l_opy_ in bstack111111l_opy_.items():
    for platform in bstack1l1llll11_opy_:
      if isinstance(bstack1l11l1l_opy_, list):
        for bstack1l1l1111_opy_ in bstack1l11l1l_opy_:
          if bstack1l1l1111_opy_ in platform:
            platform[bstack1ll1lll1_opy_] = platform[bstack1l1l1111_opy_]
            del platform[bstack1l1l1111_opy_]
            break
      elif bstack1l11l1l_opy_ in platform:
        platform[bstack1ll1lll1_opy_] = platform[bstack1l11l1l_opy_]
        del platform[bstack1l11l1l_opy_]
  for bstack1l1lll1ll_opy_ in bstack1lll1llll_opy_:
    if bstack1l1lll1ll_opy_ in config:
      if not bstack1lll1llll_opy_[bstack1l1lll1ll_opy_] in config:
        config[bstack1lll1llll_opy_[bstack1l1lll1ll_opy_]] = {}
      config[bstack1lll1llll_opy_[bstack1l1lll1ll_opy_]].update(config[bstack1l1lll1ll_opy_])
      del config[bstack1l1lll1ll_opy_]
  for platform in bstack1l1llll11_opy_:
    for bstack1l1lll1ll_opy_ in bstack1lll1llll_opy_:
      if bstack1l1lll1ll_opy_ in list(platform):
        if not bstack1lll1llll_opy_[bstack1l1lll1ll_opy_] in platform:
          platform[bstack1lll1llll_opy_[bstack1l1lll1ll_opy_]] = {}
        platform[bstack1lll1llll_opy_[bstack1l1lll1ll_opy_]].update(platform[bstack1l1lll1ll_opy_])
        del platform[bstack1l1lll1ll_opy_]
  config = bstack11ll1lll_opy_(config)
  return config
def bstack1l1ll11l1_opy_(config):
  global bstack1l1111l_opy_
  if bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭થ") in config and str(config[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧદ")]).lower() != bstackl_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪધ"):
    if not bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩન") in config:
      config[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ઩")] = {}
    if not bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩપ") in config[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬફ")]:
      bstack11l11l_opy_ = datetime.datetime.now()
      bstack1l11lll11_opy_ = bstack11l11l_opy_.strftime(bstackl_opy_ (u"ࠩࠨࡨࡤࠫࡢࡠࠧࡋࠩࡒ࠭બ"))
      hostname = socket.gethostname()
      bstack11ll1l1_opy_ = bstackl_opy_ (u"ࠪࠫભ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstackl_opy_ (u"ࠫࢀࢃ࡟ࡼࡿࡢࡿࢂ࠭મ").format(bstack1l11lll11_opy_, hostname, bstack11ll1l1_opy_)
      config[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩય")][bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨર")] = identifier
    bstack1l1111l_opy_ = config[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ઱")][bstackl_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪલ")]
  return config
def bstack1l111l1l1_opy_():
  if (
    isinstance(os.getenv(bstackl_opy_ (u"ࠩࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠧળ")), str) and len(os.getenv(bstackl_opy_ (u"ࠪࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠨ઴"))) > 0
  ) or (
    isinstance(os.getenv(bstackl_opy_ (u"ࠫࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠪવ")), str) and len(os.getenv(bstackl_opy_ (u"ࠬࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠫશ"))) > 0
  ):
    return os.getenv(bstackl_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠬષ"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠧࡄࡋࠪસ"))).lower() == bstackl_opy_ (u"ࠨࡶࡵࡹࡪ࠭હ") and str(os.getenv(bstackl_opy_ (u"ࠩࡆࡍࡗࡉࡌࡆࡅࡌࠫ઺"))).lower() == bstackl_opy_ (u"ࠪࡸࡷࡻࡥࠨ઻"):
    return os.getenv(bstackl_opy_ (u"ࠫࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓ઼ࠧ"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠬࡉࡉࠨઽ"))).lower() == bstackl_opy_ (u"࠭ࡴࡳࡷࡨࠫા") and str(os.getenv(bstackl_opy_ (u"ࠧࡕࡔࡄ࡚ࡎ࡙ࠧિ"))).lower() == bstackl_opy_ (u"ࠨࡶࡵࡹࡪ࠭ી"):
    return os.getenv(bstackl_opy_ (u"ࠩࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠨુ"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠪࡇࡎ࠭ૂ"))).lower() == bstackl_opy_ (u"ࠫࡹࡸࡵࡦࠩૃ") and str(os.getenv(bstackl_opy_ (u"ࠬࡉࡉࡠࡐࡄࡑࡊ࠭ૄ"))).lower() == bstackl_opy_ (u"࠭ࡣࡰࡦࡨࡷ࡭࡯ࡰࠨૅ"):
    return 0 # bstack1l111ll_opy_ bstack1l1111l11_opy_ not set build number env
  if os.getenv(bstackl_opy_ (u"ࠧࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆࡗࡇࡎࡄࡊࠪ૆")) and os.getenv(bstackl_opy_ (u"ࠨࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡈࡕࡍࡎࡋࡗࠫે")):
    return os.getenv(bstackl_opy_ (u"ࠩࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠫૈ"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠪࡇࡎ࠭ૉ"))).lower() == bstackl_opy_ (u"ࠫࡹࡸࡵࡦࠩ૊") and str(os.getenv(bstackl_opy_ (u"ࠬࡊࡒࡐࡐࡈࠫો"))).lower() == bstackl_opy_ (u"࠭ࡴࡳࡷࡨࠫૌ"):
    return os.getenv(bstackl_opy_ (u"ࠧࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖ્ࠬ"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠨࡅࡌࠫ૎"))).lower() == bstackl_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ૏") and str(os.getenv(bstackl_opy_ (u"ࠪࡗࡊࡓࡁࡑࡊࡒࡖࡊ࠭ૐ"))).lower() == bstackl_opy_ (u"ࠫࡹࡸࡵࡦࠩ૑"):
    return os.getenv(bstackl_opy_ (u"࡙ࠬࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡏࡄࠨ૒"), 0)
  if str(os.getenv(bstackl_opy_ (u"࠭ࡃࡊࠩ૓"))).lower() == bstackl_opy_ (u"ࠧࡵࡴࡸࡩࠬ૔") and str(os.getenv(bstackl_opy_ (u"ࠨࡉࡌࡘࡑࡇࡂࡠࡅࡌࠫ૕"))).lower() == bstackl_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ૖"):
    return os.getenv(bstackl_opy_ (u"ࠪࡇࡎࡥࡊࡐࡄࡢࡍࡉ࠭૗"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠫࡈࡏࠧ૘"))).lower() == bstackl_opy_ (u"ࠬࡺࡲࡶࡧࠪ૙") and str(os.getenv(bstackl_opy_ (u"࠭ࡂࡖࡋࡏࡈࡐࡏࡔࡆࠩ૚"))).lower() == bstackl_opy_ (u"ࠧࡵࡴࡸࡩࠬ૛"):
    return os.getenv(bstackl_opy_ (u"ࠨࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠪ૜"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠩࡗࡊࡤࡈࡕࡊࡎࡇࠫ૝"))).lower() == bstackl_opy_ (u"ࠪࡸࡷࡻࡥࠨ૞"):
    return os.getenv(bstackl_opy_ (u"ࠫࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠫ૟"), 0)
  return -1
def bstack111llll_opy_(bstack11111l1_opy_):
  global CONFIG
  if not bstackl_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧૠ") in CONFIG[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨૡ")]:
    return
  CONFIG[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩૢ")] = CONFIG[bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪૣ")].replace(
    bstackl_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫ૤"),
    str(bstack11111l1_opy_)
  )
def bstack1ll11lll_opy_():
  global CONFIG
  if not bstackl_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩ૥") in CONFIG[bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૦")]:
    return
  bstack11l11l_opy_ = datetime.datetime.now()
  bstack1l11lll11_opy_ = bstack11l11l_opy_.strftime(bstackl_opy_ (u"ࠬࠫࡤ࠮ࠧࡥ࠱ࠪࡎ࠺ࠦࡏࠪ૧"))
  CONFIG[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૨")] = CONFIG[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૩")].replace(
    bstackl_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧ૪"),
    bstack1l11lll11_opy_
  )
def bstack11l1l11_opy_():
  global CONFIG
  if bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૫") in CONFIG and not bool(CONFIG[bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૬")]):
    del CONFIG[bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૭")]
    return
  if not bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૮") in CONFIG:
    CONFIG[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૯")] = bstackl_opy_ (u"ࠧࠤࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪ૰")
  if bstackl_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧ૱") in CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૲")]:
    bstack1ll11lll_opy_()
    os.environ[bstackl_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧ૳")] = CONFIG[bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૴")]
  if not bstackl_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧ૵") in CONFIG[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૶")]:
    return
  bstack11111l1_opy_ = bstackl_opy_ (u"ࠧࠨ૷")
  bstack1lll1ll11_opy_ = bstack1l111l1l1_opy_()
  if bstack1lll1ll11_opy_ != -1:
    bstack11111l1_opy_ = bstackl_opy_ (u"ࠨࡅࡌࠤࠬ૸") + str(bstack1lll1ll11_opy_)
  if bstack11111l1_opy_ == bstackl_opy_ (u"ࠩࠪૹ"):
    bstack1lll11lll_opy_ = bstack1llll1lll_opy_(CONFIG[bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ૺ")])
    if bstack1lll11lll_opy_ != -1:
      bstack11111l1_opy_ = str(bstack1lll11lll_opy_)
  if bstack11111l1_opy_:
    bstack111llll_opy_(bstack11111l1_opy_)
    os.environ[bstackl_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨૻ")] = CONFIG[bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧૼ")]
def bstack1ll1ll1l1_opy_(bstack11ll1l1l_opy_, bstack1lllll1l_opy_, path):
  bstack111l11l_opy_ = {
    bstackl_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૽"): bstack1lllll1l_opy_
  }
  if os.path.exists(path):
    bstack1lll11l_opy_ = json.load(open(path, bstackl_opy_ (u"ࠧࡳࡤࠪ૾")))
  else:
    bstack1lll11l_opy_ = {}
  bstack1lll11l_opy_[bstack11ll1l1l_opy_] = bstack111l11l_opy_
  with open(path, bstackl_opy_ (u"ࠣࡹ࠮ࠦ૿")) as outfile:
    json.dump(bstack1lll11l_opy_, outfile)
def bstack1llll1lll_opy_(bstack11ll1l1l_opy_):
  bstack11ll1l1l_opy_ = str(bstack11ll1l1l_opy_)
  bstack111l1l1l_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠩࢁࠫ଀")), bstackl_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪଁ"))
  try:
    if not os.path.exists(bstack111l1l1l_opy_):
      os.makedirs(bstack111l1l1l_opy_)
    file_path = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠫࢃ࠭ଂ")), bstackl_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬଃ"), bstackl_opy_ (u"࠭࠮ࡣࡷ࡬ࡰࡩ࠳࡮ࡢ࡯ࡨ࠱ࡨࡧࡣࡩࡧ࠱࡮ࡸࡵ࡮ࠨ଄"))
    if not os.path.isfile(file_path):
      with open(file_path, bstackl_opy_ (u"ࠧࡸࠩଅ")):
        pass
      with open(file_path, bstackl_opy_ (u"ࠣࡹ࠮ࠦଆ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstackl_opy_ (u"ࠩࡵࠫଇ")) as bstack1l111_opy_:
      bstack11l111ll_opy_ = json.load(bstack1l111_opy_)
    if bstack11ll1l1l_opy_ in bstack11l111ll_opy_:
      bstack1l111llll_opy_ = bstack11l111ll_opy_[bstack11ll1l1l_opy_][bstackl_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧଈ")]
      bstack1ll1l1ll1_opy_ = int(bstack1l111llll_opy_) + 1
      bstack1ll1ll1l1_opy_(bstack11ll1l1l_opy_, bstack1ll1l1ll1_opy_, file_path)
      return bstack1ll1l1ll1_opy_
    else:
      bstack1ll1ll1l1_opy_(bstack11ll1l1l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1lllllll_opy_.format(str(e)))
    return -1
def bstack1ll1lll1l_opy_(config):
  if not config[bstackl_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ଉ")] or not config[bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨଊ")]:
    return True
  else:
    return False
def bstack1ll11ll11_opy_(config):
  if bstackl_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬଋ") in config:
    del(config[bstackl_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ଌ")])
    return False
  if bstack1ll111111_opy_() < version.parse(bstackl_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧ଍")):
    return False
  if bstack1ll111111_opy_() >= version.parse(bstackl_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨ଎")):
    return True
  if bstackl_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪଏ") in config and config[bstackl_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫଐ")] == False:
    return False
  else:
    return True
def bstack1ll111ll_opy_(config, index = 0):
  global bstack1l111l11_opy_
  bstack1l1l1l111_opy_ = {}
  caps = bstack1111l11l_opy_ + bstack11l1l_opy_
  if bstack1l111l11_opy_:
    caps += bstack111l11l1_opy_
  for key in config:
    if key in caps + [bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ଑")]:
      continue
    bstack1l1l1l111_opy_[key] = config[key]
  if bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ଒") in config:
    for bstack1llllll1_opy_ in config[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଓ")][index]:
      if bstack1llllll1_opy_ in caps + [bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ଔ"), bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪକ")]:
        continue
      bstack1l1l1l111_opy_[bstack1llllll1_opy_] = config[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଖ")][index][bstack1llllll1_opy_]
  bstack1l1l1l111_opy_[bstackl_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ଗ")] = socket.gethostname()
  if bstackl_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ଘ") in bstack1l1l1l111_opy_:
    del(bstack1l1l1l111_opy_[bstackl_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧଙ")])
  return bstack1l1l1l111_opy_
def bstack1l1l1l_opy_(config):
  global bstack1l111l11_opy_
  bstack1ll11llll_opy_ = {}
  caps = bstack11l1l_opy_
  if bstack1l111l11_opy_:
    caps+= bstack111l11l1_opy_
  for key in caps:
    if key in config:
      bstack1ll11llll_opy_[key] = config[key]
  return bstack1ll11llll_opy_
def bstack1llll1ll_opy_(bstack1l1l1l111_opy_, bstack1ll11llll_opy_):
  bstack11ll11ll_opy_ = {}
  for key in bstack1l1l1l111_opy_.keys():
    if key in bstack11ll11l_opy_:
      bstack11ll11ll_opy_[bstack11ll11l_opy_[key]] = bstack1l1l1l111_opy_[key]
    else:
      bstack11ll11ll_opy_[key] = bstack1l1l1l111_opy_[key]
  for key in bstack1ll11llll_opy_:
    if key in bstack11ll11l_opy_:
      bstack11ll11ll_opy_[bstack11ll11l_opy_[key]] = bstack1ll11llll_opy_[key]
    else:
      bstack11ll11ll_opy_[key] = bstack1ll11llll_opy_[key]
  return bstack11ll11ll_opy_
def bstack1l1111111_opy_(config, index = 0):
  global bstack1l111l11_opy_
  caps = {}
  bstack1ll11llll_opy_ = bstack1l1l1l_opy_(config)
  bstack11l11l1_opy_ = bstack11l1l_opy_
  bstack11l11l1_opy_ += bstack1ll1111ll_opy_
  if bstack1l111l11_opy_:
    bstack11l11l1_opy_ += bstack111l11l1_opy_
  if bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଚ") in config:
    if bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ଛ") in config[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬଜ")][index]:
      caps[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨଝ")] = config[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଞ")][index][bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪଟ")]
    if bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧଠ") in config[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଡ")][index]:
      caps[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩଢ")] = str(config[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬଣ")][index][bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫତ")])
    bstack11llllll_opy_ = {}
    for bstack1lll1ll1l_opy_ in bstack11l11l1_opy_:
      if bstack1lll1ll1l_opy_ in config[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଥ")][index]:
        if bstack1lll1ll1l_opy_ == bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧଦ"):
          bstack11llllll_opy_[bstack1lll1ll1l_opy_] = str(config[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଧ")][index][bstack1lll1ll1l_opy_] * 1.0)
        else:
          bstack11llllll_opy_[bstack1lll1ll1l_opy_] = config[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪନ")][index][bstack1lll1ll1l_opy_]
        del(config[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ଩")][index][bstack1lll1ll1l_opy_])
    bstack1ll11llll_opy_ = update(bstack1ll11llll_opy_, bstack11llllll_opy_)
  bstack1l1l1l111_opy_ = bstack1ll111ll_opy_(config, index)
  for bstack1l1l1111_opy_ in bstack11l1l_opy_ + [bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧପ"), bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫଫ")]:
    if bstack1l1l1111_opy_ in bstack1l1l1l111_opy_:
      bstack1ll11llll_opy_[bstack1l1l1111_opy_] = bstack1l1l1l111_opy_[bstack1l1l1111_opy_]
      del(bstack1l1l1l111_opy_[bstack1l1l1111_opy_])
  if bstack1ll11ll11_opy_(config):
    bstack1l1l1l111_opy_[bstackl_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫବ")] = True
    caps.update(bstack1ll11llll_opy_)
    caps[bstackl_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ଭ")] = bstack1l1l1l111_opy_
  else:
    bstack1l1l1l111_opy_[bstackl_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ମ")] = False
    caps.update(bstack1llll1ll_opy_(bstack1l1l1l111_opy_, bstack1ll11llll_opy_))
    if bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬଯ") in caps:
      caps[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩର")] = caps[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ଱")]
      del(caps[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨଲ")])
    if bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬଳ") in caps:
      caps[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ଴")] = caps[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧଵ")]
      del(caps[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨଶ")])
  return caps
def bstack11l11ll1_opy_():
  global bstack1l1l1_opy_
  if bstack1ll111111_opy_() <= version.parse(bstackl_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨଷ")):
    if bstack1l1l1_opy_ != bstackl_opy_ (u"ࠩࠪସ"):
      return bstackl_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦହ") + bstack1l1l1_opy_ + bstackl_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ଺")
    return bstack1l1lll1_opy_
  if  bstack1l1l1_opy_ != bstackl_opy_ (u"ࠬ࠭଻"):
    return bstackl_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯଼ࠣ") + bstack1l1l1_opy_ + bstackl_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣଽ")
  return bstack1lll111l1_opy_
def bstack11ll11_opy_(options):
  return hasattr(options, bstackl_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩା"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11lll1ll1_opy_(options, bstack1l1111l1_opy_):
  for bstack1ll111ll1_opy_ in bstack1l1111l1_opy_:
    if bstack1ll111ll1_opy_ in [bstackl_opy_ (u"ࠩࡤࡶ࡬ࡹࠧି"), bstackl_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧୀ")]:
      next
    if bstack1ll111ll1_opy_ in options._experimental_options:
      options._experimental_options[bstack1ll111ll1_opy_]= update(options._experimental_options[bstack1ll111ll1_opy_], bstack1l1111l1_opy_[bstack1ll111ll1_opy_])
    else:
      options.add_experimental_option(bstack1ll111ll1_opy_, bstack1l1111l1_opy_[bstack1ll111ll1_opy_])
  if bstackl_opy_ (u"ࠫࡦࡸࡧࡴࠩୁ") in bstack1l1111l1_opy_:
    for arg in bstack1l1111l1_opy_[bstackl_opy_ (u"ࠬࡧࡲࡨࡵࠪୂ")]:
      options.add_argument(arg)
    del(bstack1l1111l1_opy_[bstackl_opy_ (u"࠭ࡡࡳࡩࡶࠫୃ")])
  if bstackl_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫୄ") in bstack1l1111l1_opy_:
    for ext in bstack1l1111l1_opy_[bstackl_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ୅")]:
      options.add_extension(ext)
    del(bstack1l1111l1_opy_[bstackl_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭୆")])
def bstack1111l1_opy_(options, bstack1l1111lll_opy_):
  if bstackl_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩେ") in bstack1l1111lll_opy_:
    for bstack11llll111_opy_ in bstack1l1111lll_opy_[bstackl_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪୈ")]:
      if bstack11llll111_opy_ in options._preferences:
        options._preferences[bstack11llll111_opy_] = update(options._preferences[bstack11llll111_opy_], bstack1l1111lll_opy_[bstackl_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ୉")][bstack11llll111_opy_])
      else:
        options.set_preference(bstack11llll111_opy_, bstack1l1111lll_opy_[bstackl_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ୊")][bstack11llll111_opy_])
  if bstackl_opy_ (u"ࠧࡢࡴࡪࡷࠬୋ") in bstack1l1111lll_opy_:
    for arg in bstack1l1111lll_opy_[bstackl_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ୌ")]:
      options.add_argument(arg)
def bstack1l11_opy_(options, bstack11l1l11l_opy_):
  if bstackl_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹ୍ࠪ") in bstack11l1l11l_opy_:
    options.use_webview(bool(bstack11l1l11l_opy_[bstackl_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫ୎")]))
  bstack11lll1ll1_opy_(options, bstack11l1l11l_opy_)
def bstack11lll1lll_opy_(options, bstack1lll1lll_opy_):
  for bstack1l1ll_opy_ in bstack1lll1lll_opy_:
    if bstack1l1ll_opy_ in [bstackl_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨ୏"), bstackl_opy_ (u"ࠬࡧࡲࡨࡵࠪ୐")]:
      next
    options.set_capability(bstack1l1ll_opy_, bstack1lll1lll_opy_[bstack1l1ll_opy_])
  if bstackl_opy_ (u"࠭ࡡࡳࡩࡶࠫ୑") in bstack1lll1lll_opy_:
    for arg in bstack1lll1lll_opy_[bstackl_opy_ (u"ࠧࡢࡴࡪࡷࠬ୒")]:
      options.add_argument(arg)
  if bstackl_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬ୓") in bstack1lll1lll_opy_:
    options.use_technology_preview(bool(bstack1lll1lll_opy_[bstackl_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭୔")]))
def bstack1ll111l1l_opy_(options, bstack1l1l11l_opy_):
  for bstack11lllll_opy_ in bstack1l1l11l_opy_:
    if bstack11lllll_opy_ in [bstackl_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ୕"), bstackl_opy_ (u"ࠫࡦࡸࡧࡴࠩୖ")]:
      next
    options._options[bstack11lllll_opy_] = bstack1l1l11l_opy_[bstack11lllll_opy_]
  if bstackl_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩୗ") in bstack1l1l11l_opy_:
    for bstack1ll1llll1_opy_ in bstack1l1l11l_opy_[bstackl_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ୘")]:
      options.add_additional_option(
          bstack1ll1llll1_opy_, bstack1l1l11l_opy_[bstackl_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ୙")][bstack1ll1llll1_opy_])
  if bstackl_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭୚") in bstack1l1l11l_opy_:
    for arg in bstack1l1l11l_opy_[bstackl_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ୛")]:
      options.add_argument(arg)
def bstack1llll1l11_opy_(options, caps):
  if not hasattr(options, bstackl_opy_ (u"ࠪࡏࡊ࡟ࠧଡ଼")):
    return
  if options.KEY == bstackl_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩଢ଼") and options.KEY in caps:
    bstack11lll1ll1_opy_(options, caps[bstackl_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ୞")])
  elif options.KEY == bstackl_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫୟ") and options.KEY in caps:
    bstack1111l1_opy_(options, caps[bstackl_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬୠ")])
  elif options.KEY == bstackl_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩୡ") and options.KEY in caps:
    bstack11lll1lll_opy_(options, caps[bstackl_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪୢ")])
  elif options.KEY == bstackl_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫୣ") and options.KEY in caps:
    bstack1l11_opy_(options, caps[bstackl_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬ୤")])
  elif options.KEY == bstackl_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ୥") and options.KEY in caps:
    bstack1ll111l1l_opy_(options, caps[bstackl_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬ୦")])
def bstack1l111ll11_opy_(caps):
  global bstack1l111l11_opy_
  if bstack1l111l11_opy_:
    if bstack111ll1l1_opy_() < version.parse(bstackl_opy_ (u"ࠧ࠳࠰࠶࠲࠵࠭୧")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstackl_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ୨")
    if bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ୩") in caps:
      browser = caps[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ୪")]
    elif bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ୫") in caps:
      browser = caps[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭୬")]
    browser = str(browser).lower()
    if browser == bstackl_opy_ (u"࠭ࡩࡱࡪࡲࡲࡪ࠭୭") or browser == bstackl_opy_ (u"ࠧࡪࡲࡤࡨࠬ୮"):
      browser = bstackl_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨ୯")
    if browser == bstackl_opy_ (u"ࠩࡶࡥࡲࡹࡵ࡯ࡩࠪ୰"):
      browser = bstackl_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪୱ")
    if browser not in [bstackl_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ୲"), bstackl_opy_ (u"ࠬ࡫ࡤࡨࡧࠪ୳"), bstackl_opy_ (u"࠭ࡩࡦࠩ୴"), bstackl_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧ୵"), bstackl_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩ୶")]:
      return None
    try:
      package = bstackl_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡼࡿ࠱ࡳࡵࡺࡩࡰࡰࡶࠫ୷").format(browser)
      name = bstackl_opy_ (u"ࠪࡓࡵࡺࡩࡰࡰࡶࠫ୸")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11ll11_opy_(options):
        return None
      for bstack1l1l1111_opy_ in caps.keys():
        options.set_capability(bstack1l1l1111_opy_, caps[bstack1l1l1111_opy_])
      bstack1llll1l11_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1ll11ll1_opy_(options, bstack11l1_opy_):
  if not bstack11ll11_opy_(options):
    return
  for bstack1l1l1111_opy_ in bstack11l1_opy_.keys():
    if bstack1l1l1111_opy_ in bstack1ll1111ll_opy_:
      next
    if bstack1l1l1111_opy_ in options._caps and type(options._caps[bstack1l1l1111_opy_]) in [dict, list]:
      options._caps[bstack1l1l1111_opy_] = update(options._caps[bstack1l1l1111_opy_], bstack11l1_opy_[bstack1l1l1111_opy_])
    else:
      options.set_capability(bstack1l1l1111_opy_, bstack11l1_opy_[bstack1l1l1111_opy_])
  bstack1llll1l11_opy_(options, bstack11l1_opy_)
  if bstackl_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪ୹") in options._caps:
    if options._caps[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ୺")] and options._caps[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ୻")].lower() != bstackl_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨ୼"):
      del options._caps[bstackl_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧ୽")]
def bstack1llll1ll1_opy_(proxy_config):
  if bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭୾") in proxy_config:
    proxy_config[bstackl_opy_ (u"ࠪࡷࡸࡲࡐࡳࡱࡻࡽࠬ୿")] = proxy_config[bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ஀")]
    del(proxy_config[bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ஁")])
  if bstackl_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩஂ") in proxy_config and proxy_config[bstackl_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪஃ")].lower() != bstackl_opy_ (u"ࠨࡦ࡬ࡶࡪࡩࡴࠨ஄"):
    proxy_config[bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬஅ")] = bstackl_opy_ (u"ࠪࡱࡦࡴࡵࡢ࡮ࠪஆ")
  if bstackl_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡄࡹࡹࡵࡣࡰࡰࡩ࡭࡬࡛ࡲ࡭ࠩஇ") in proxy_config:
    proxy_config[bstackl_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨஈ")] = bstackl_opy_ (u"࠭ࡰࡢࡥࠪஉ")
  return proxy_config
def bstack1l11ll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstackl_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ஊ") in config:
    return proxy
  config[bstackl_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧ஋")] = bstack1llll1ll1_opy_(config[bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ஌")])
  if proxy == None:
    proxy = Proxy(config[bstackl_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ஍")])
  return proxy
def bstack1l1llll_opy_(self):
  global CONFIG
  global bstack1l11llll1_opy_
  if bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧஎ") in CONFIG:
    return CONFIG[bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨஏ")]
  elif bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪஐ") in CONFIG:
    return CONFIG[bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ஑")]
  else:
    return bstack1l11llll1_opy_(self)
def bstack1ll11l11_opy_():
  global CONFIG
  return bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫஒ") in CONFIG or bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ஓ") in CONFIG
def bstack11llll1_opy_(config):
  if not bstack1ll11l11_opy_():
    return
  if config.get(bstackl_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ஔ")):
    return config.get(bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧக"))
  if config.get(bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ஖")):
    return config.get(bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ஗"))
def bstack111111_opy_():
  return bstack1ll11l11_opy_() and bstack1ll111111_opy_() >= version.parse(bstack1l1ll1_opy_)
def bstack1l1lll111_opy_(config):
  if bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ஘") in config:
    return config[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬங")]
  if bstackl_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨச") in config:
    return config[bstackl_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ஛")]
  return {}
def bstack1llll11l_opy_(config):
  if bstackl_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩஜ") in config:
    return config[bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ஝")]
  return {}
def bstack1lllll_opy_(caps):
  global bstack1l1111l_opy_
  if bstackl_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧஞ") in caps:
    caps[bstackl_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨட")][bstackl_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ஠")] = True
    if bstack1l1111l_opy_:
      caps[bstackl_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ஡")][bstackl_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ஢")] = bstack1l1111l_opy_
  else:
    caps[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩண")] = True
    if bstack1l1111l_opy_:
      caps[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭த")] = bstack1l1111l_opy_
def bstack11l111_opy_():
  global CONFIG
  if bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ஥") in CONFIG and CONFIG[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ஦")]:
    bstack1111llll_opy_ = bstack1l1lll111_opy_(CONFIG)
    bstack11lll11ll_opy_(CONFIG[bstackl_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ஧")], bstack1111llll_opy_)
def bstack11lll11ll_opy_(key, bstack1111llll_opy_):
  global bstack11l1111l_opy_
  logger.info(bstack11lll1l11_opy_)
  try:
    bstack11l1111l_opy_ = Local()
    bstack1111lll1_opy_ = {bstackl_opy_ (u"ࠩ࡮ࡩࡾ࠭ந"): key}
    bstack1111lll1_opy_.update(bstack1111llll_opy_)
    logger.debug(bstack1111l1ll_opy_.format(str(bstack1111lll1_opy_)))
    bstack11l1111l_opy_.start(**bstack1111lll1_opy_)
    if bstack11l1111l_opy_.isRunning():
      logger.info(bstack1l111ll1l_opy_)
  except Exception as e:
    bstack1lllll111_opy_(bstack1ll1l111_opy_.format(str(e)))
def bstack1l11l1ll1_opy_():
  global bstack11l1111l_opy_
  if bstack11l1111l_opy_.isRunning():
    logger.info(bstack1l1l11l11_opy_)
    bstack11l1111l_opy_.stop()
  bstack11l1111l_opy_ = None
def bstack11111111_opy_():
  global bstack1ll11_opy_
  global bstack1ll1ll_opy_
  if bstack1ll11_opy_:
    logger.warning(bstack1l1l111l1_opy_.format(str(bstack1ll11_opy_)))
  logger.info(bstack1lll11l1l_opy_)
  global bstack11l1111l_opy_
  if bstack11l1111l_opy_:
    bstack1l11l1ll1_opy_()
  try:
    for driver in bstack1ll1ll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l1lll_opy_)
  bstack111l1lll_opy_()
def bstack1lll111ll_opy_(self, *args):
  logger.error(bstack1lll1l1_opy_)
  bstack11111111_opy_()
  sys.exit(1)
def bstack1lllll111_opy_(err):
  logger.critical(bstack1l11ll1l_opy_.format(str(err)))
  bstack111l1lll_opy_(bstack1l11ll1l_opy_.format(str(err)))
  atexit.unregister(bstack11111111_opy_)
  sys.exit(1)
def bstack111lllll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack111l1lll_opy_(message)
  atexit.unregister(bstack11111111_opy_)
  sys.exit(1)
def bstack1l11ll1_opy_():
  global CONFIG
  global bstack1l111l111_opy_
  global bstack111l111_opy_
  global bstack111l_opy_
  CONFIG = bstack1l1l1l1l_opy_()
  bstack1l11ll11l_opy_()
  bstack11lll11_opy_()
  CONFIG = bstack1llll1l1l_opy_(CONFIG)
  update(CONFIG, bstack111l111_opy_)
  update(CONFIG, bstack1l111l111_opy_)
  CONFIG = bstack1l1ll11l1_opy_(CONFIG)
  if bstackl_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧன") in CONFIG and str(CONFIG[bstackl_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨப")]).lower() == bstackl_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ஫"):
    bstack111l_opy_ = False
  if (bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ஬") in CONFIG and bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ஭") in bstack1l111l111_opy_) or (bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫம") in CONFIG and bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬய") not in bstack111l111_opy_):
    if os.getenv(bstackl_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧர")):
      CONFIG[bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ற")] = os.getenv(bstackl_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩல"))
    else:
      bstack11l1l11_opy_()
  elif (bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩள") not in CONFIG and bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩழ") in CONFIG) or (bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫவ") in bstack111l111_opy_ and bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬஶ") not in bstack1l111l111_opy_):
    del(CONFIG[bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬஷ")])
  if bstack1ll1lll1l_opy_(CONFIG):
    bstack1lllll111_opy_(bstack1lllll11l_opy_)
  bstack1ll111l_opy_()
  bstack1l11ll1ll_opy_()
  if bstack1l111l11_opy_:
    CONFIG[bstackl_opy_ (u"ࠫࡦࡶࡰࠨஸ")] = bstack1l111l11l_opy_(CONFIG)
    logger.info(bstack11ll111_opy_.format(CONFIG[bstackl_opy_ (u"ࠬࡧࡰࡱࠩஹ")]))
def bstack1l11ll1ll_opy_():
  global CONFIG
  global bstack1l111l11_opy_
  if bstackl_opy_ (u"࠭ࡡࡱࡲࠪ஺") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack111lllll_opy_(e, bstack1111111l_opy_)
    bstack1l111l11_opy_ = True
def bstack1l111l11l_opy_(config):
  bstack11ll1111_opy_ = bstackl_opy_ (u"ࠧࠨ஻")
  app = config[bstackl_opy_ (u"ࠨࡣࡳࡴࠬ஼")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack11111ll1_opy_:
      if os.path.exists(app):
        bstack11ll1111_opy_ = bstack111ll111_opy_(config, app)
      elif bstack1l111l_opy_(app):
        bstack11ll1111_opy_ = app
      else:
        bstack1lllll111_opy_(bstack11llll1l_opy_.format(app))
    else:
      if bstack1l111l_opy_(app):
        bstack11ll1111_opy_ = app
      elif os.path.exists(app):
        bstack11ll1111_opy_ = bstack111ll111_opy_(app)
      else:
        bstack1lllll111_opy_(bstack11lll1l1_opy_)
  else:
    if len(app) > 2:
      bstack1lllll111_opy_(bstack11l1llll_opy_)
    elif len(app) == 2:
      if bstackl_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ஽") in app and bstackl_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ா") in app:
        if os.path.exists(app[bstackl_opy_ (u"ࠫࡵࡧࡴࡩࠩி")]):
          bstack11ll1111_opy_ = bstack111ll111_opy_(config, app[bstackl_opy_ (u"ࠬࡶࡡࡵࡪࠪீ")], app[bstackl_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩு")])
        else:
          bstack1lllll111_opy_(bstack11llll1l_opy_.format(app))
      else:
        bstack1lllll111_opy_(bstack11l1llll_opy_)
    else:
      for key in app:
        if key in bstack11ll111l_opy_:
          if key == bstackl_opy_ (u"ࠧࡱࡣࡷ࡬ࠬூ"):
            if os.path.exists(app[key]):
              bstack11ll1111_opy_ = bstack111ll111_opy_(config, app[key])
            else:
              bstack1lllll111_opy_(bstack11llll1l_opy_.format(app))
          else:
            bstack11ll1111_opy_ = app[key]
        else:
          bstack1lllll111_opy_(bstack11l11lll_opy_)
  return bstack11ll1111_opy_
def bstack1l111l_opy_(bstack11ll1111_opy_):
  import re
  bstack11l1lll1_opy_ = re.compile(bstackl_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣ௃"))
  bstack1l1ll1ll_opy_ = re.compile(bstackl_opy_ (u"ࡴࠥࡢࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪ࠰࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮ࠩࠨ௄"))
  if bstackl_opy_ (u"ࠪࡦࡸࡀ࠯࠰ࠩ௅") in bstack11ll1111_opy_ or re.fullmatch(bstack11l1lll1_opy_, bstack11ll1111_opy_) or re.fullmatch(bstack1l1ll1ll_opy_, bstack11ll1111_opy_):
    return True
  else:
    return False
def bstack111ll111_opy_(config, path, bstack1lll1l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstackl_opy_ (u"ࠫࡷࡨࠧெ")).read()).hexdigest()
  bstack1l1ll1lll_opy_ = bstack1lll11ll_opy_(md5_hash)
  bstack11ll1111_opy_ = None
  if bstack1l1ll1lll_opy_:
    logger.info(bstack1lllll1l1_opy_.format(bstack1l1ll1lll_opy_, md5_hash))
    return bstack1l1ll1lll_opy_
  bstack1llllllll_opy_ = MultipartEncoder(
    fields={
        bstackl_opy_ (u"ࠬ࡬ࡩ࡭ࡧࠪே"): (os.path.basename(path), open(os.path.abspath(path), bstackl_opy_ (u"࠭ࡲࡣࠩை")), bstackl_opy_ (u"ࠧࡵࡧࡻࡸ࠴ࡶ࡬ࡢ࡫ࡱࠫ௉")),
        bstackl_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫொ"): bstack1lll1l_opy_
    }
  )
  response = requests.post(bstack1l1l11_opy_, data=bstack1llllllll_opy_,
                         headers={bstackl_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨோ"): bstack1llllllll_opy_.content_type}, auth=(config[bstackl_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬௌ")], config[bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿ்ࠧ")]))
  try:
    res = json.loads(response.text)
    bstack11ll1111_opy_ = res[bstackl_opy_ (u"ࠬࡧࡰࡱࡡࡸࡶࡱ࠭௎")]
    logger.info(bstack111111ll_opy_.format(bstack11ll1111_opy_))
    bstack1ll1l1l1l_opy_(md5_hash, bstack11ll1111_opy_)
  except ValueError as err:
    bstack1lllll111_opy_(bstack1l1111_opy_.format(str(err)))
  return bstack11ll1111_opy_
def bstack1ll111l_opy_():
  global CONFIG
  global bstack1l11lll_opy_
  bstack111ll_opy_ = 0
  bstack1111l1l_opy_ = 1
  if bstackl_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭௏") in CONFIG:
    bstack1111l1l_opy_ = CONFIG[bstackl_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧௐ")]
  if bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௑") in CONFIG:
    bstack111ll_opy_ = len(CONFIG[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௒")])
  bstack1l11lll_opy_ = int(bstack1111l1l_opy_) * int(bstack111ll_opy_)
def bstack1lll11ll_opy_(md5_hash):
  bstack1lllll11_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠪࢂࠬ௓")), bstackl_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ௔"), bstackl_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭௕"))
  if os.path.exists(bstack1lllll11_opy_):
    bstack1l1l1l11l_opy_ = json.load(open(bstack1lllll11_opy_,bstackl_opy_ (u"࠭ࡲࡣࠩ௖")))
    if md5_hash in bstack1l1l1l11l_opy_:
      bstack1lll1lll1_opy_ = bstack1l1l1l11l_opy_[md5_hash]
      bstack1llll1_opy_ = datetime.datetime.now()
      bstack111lll11_opy_ = datetime.datetime.strptime(bstack1lll1lll1_opy_[bstackl_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪௗ")], bstackl_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬ௘"))
      if (bstack1llll1_opy_ - bstack111lll11_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1lll1lll1_opy_[bstackl_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ௙")]):
        return None
      return bstack1lll1lll1_opy_[bstackl_opy_ (u"ࠪ࡭ࡩ࠭௚")]
  else:
    return None
def bstack1ll1l1l1l_opy_(md5_hash, bstack11ll1111_opy_):
  bstack111l1l1l_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠫࢃ࠭௛")), bstackl_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ௜"))
  if not os.path.exists(bstack111l1l1l_opy_):
    os.makedirs(bstack111l1l1l_opy_)
  bstack1lllll11_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"࠭ࡾࠨ௝")), bstackl_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ௞"), bstackl_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩ௟"))
  bstack1lll11_opy_ = {
    bstackl_opy_ (u"ࠩ࡬ࡨࠬ௠"): bstack11ll1111_opy_,
    bstackl_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭௡"): datetime.datetime.strftime(datetime.datetime.now(), bstackl_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ௢")),
    bstackl_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ௣"): str(__version__)
  }
  if os.path.exists(bstack1lllll11_opy_):
    bstack1l1l1l11l_opy_ = json.load(open(bstack1lllll11_opy_,bstackl_opy_ (u"࠭ࡲࡣࠩ௤")))
  else:
    bstack1l1l1l11l_opy_ = {}
  bstack1l1l1l11l_opy_[md5_hash] = bstack1lll11_opy_
  with open(bstack1lllll11_opy_, bstackl_opy_ (u"ࠢࡸ࠭ࠥ௥")) as outfile:
    json.dump(bstack1l1l1l11l_opy_, outfile)
def bstack1ll1lll11_opy_(self):
  return
def bstack11lll1l1l_opy_(self):
  return
def bstack1l1l11ll1_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack11llllll1_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1ll1ll11l_opy_
  global bstack1l1ll1ll1_opy_
  global bstack1l1l1ll_opy_
  global bstack1l11l1lll_opy_
  global bstack1l1ll11l_opy_
  global bstack1l1ll1l1l_opy_
  global bstack1ll1ll_opy_
  CONFIG[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ௦")] = str(bstack1l1ll11l_opy_) + str(__version__)
  command_executor = bstack11l11ll1_opy_()
  logger.debug(bstack1ll1l1l1_opy_.format(command_executor))
  proxy = bstack1l11ll_opy_(CONFIG, proxy)
  bstack1ll1l11ll_opy_ = 0 if bstack1l1ll1ll1_opy_ < 0 else bstack1l1ll1ll1_opy_
  if bstack1l11l1lll_opy_ is True:
    bstack1ll1l11ll_opy_ = int(threading.current_thread().getName())
  bstack11l1_opy_ = bstack1l1111111_opy_(CONFIG, bstack1ll1l11ll_opy_)
  logger.debug(bstack1l1l1ll11_opy_.format(str(bstack11l1_opy_)))
  if bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭௧") in CONFIG and CONFIG[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ௨")]:
    bstack1lllll_opy_(bstack11l1_opy_)
  if desired_capabilities:
    bstack11llll11l_opy_ = bstack1llll1l1l_opy_(desired_capabilities)
    bstack11llll11l_opy_[bstackl_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ௩")] = bstack1ll11ll11_opy_(CONFIG)
    bstack1llll111_opy_ = bstack1l1111111_opy_(bstack11llll11l_opy_)
    if bstack1llll111_opy_:
      bstack11l1_opy_ = update(bstack1llll111_opy_, bstack11l1_opy_)
    desired_capabilities = None
  if options:
    bstack1ll11ll1_opy_(options, bstack11l1_opy_)
  if not options:
    options = bstack1l111ll11_opy_(bstack11l1_opy_)
  if proxy and bstack1ll111111_opy_() >= version.parse(bstackl_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ௪")):
    options.proxy(proxy)
  if options and bstack1ll111111_opy_() >= version.parse(bstackl_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ௫")):
    desired_capabilities = None
  if (
      not options and not desired_capabilities
  ) or (
      bstack1ll111111_opy_() < version.parse(bstackl_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭௬")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11l1_opy_)
  logger.info(bstack11ll1ll_opy_)
  if bstack1ll111111_opy_() >= version.parse(bstackl_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ௭")):
    bstack1l1ll1l1l_opy_(self, command_executor=command_executor,
          options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1ll111111_opy_() >= version.parse(bstackl_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ௮")):
    bstack1l1ll1l1l_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1ll111111_opy_() >= version.parse(bstackl_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪ௯")):
    bstack1l1ll1l1l_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1l1ll1l1l_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  try:
    bstack11lll1_opy_ = bstackl_opy_ (u"ࠫࠬ௰")
    if bstack1ll111111_opy_() >= version.parse(bstackl_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭௱")):
      bstack11lll1_opy_ = self.caps.get(bstackl_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ௲"))
    else:
      bstack11lll1_opy_ = self.capabilities.get(bstackl_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ௳"))
    if bstack11lll1_opy_:
      if bstack1ll111111_opy_() <= version.parse(bstackl_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ௴")):
        self.command_executor._url = bstackl_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ௵") + bstack1l1l1_opy_ + bstackl_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢ௶")
      else:
        self.command_executor._url = bstackl_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ௷") + bstack11lll1_opy_ + bstackl_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ௸")
      logger.debug(bstack1l1l1ll1l_opy_.format(bstack11lll1_opy_))
    else:
      logger.debug(bstack1l111111_opy_.format(bstackl_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢ௹")))
  except Exception as e:
    logger.debug(bstack1l111111_opy_.format(e))
  bstack1ll1ll11l_opy_ = self.session_id
  bstack1ll1ll_opy_.append(self)
  if bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ௺") in CONFIG and bstackl_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭௻") in CONFIG[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௼")][bstack1ll1l11ll_opy_]:
    bstack1l1l1ll_opy_ = CONFIG[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭௽")][bstack1ll1l11ll_opy_][bstackl_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ௾")]
  logger.debug(bstack1l1ll11ll_opy_.format(bstack1ll1ll11l_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1l1l11l1_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1lll11l11_opy_
      if(bstackl_opy_ (u"ࠧ࡯࡮ࡥࡧࡻ࠲࡯ࡹࠢ௿") in args[1]):
        with open(os.path.join(os.path.expanduser(bstackl_opy_ (u"࠭ࡾࠨఀ")), bstackl_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧఁ"), bstackl_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪం")), bstackl_opy_ (u"ࠩࡺࠫః")) as fp:
          fp.write(bstackl_opy_ (u"ࠥࠦఄ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstackl_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨఅ")))):
          with open(args[1], bstackl_opy_ (u"ࠬࡸࠧఆ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstackl_opy_ (u"࠭ࡡࡴࡻࡱࡧࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡠࡰࡨࡻࡕࡧࡧࡦࠪࡦࡳࡳࡺࡥࡹࡶ࠯ࠤࡵࡧࡧࡦࠢࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠬఇ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l11l1l1_opy_)
            lines.insert(1, bstack11l11ll_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstackl_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤఈ")), bstackl_opy_ (u"ࠨࡹࠪఉ")) as bstack1ll1ll11_opy_:
              bstack1ll1ll11_opy_.writelines(lines)
        CONFIG[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫఊ")] = str(bstack1l1ll11l_opy_) + str(__version__)
        bstack1ll1l11ll_opy_ = 0 if bstack1l1ll1ll1_opy_ < 0 else bstack1l1ll1ll1_opy_
        if bstack1l11l1lll_opy_ is True:
          bstack1ll1l11ll_opy_ = int(threading.current_thread().getName())
        CONFIG[bstackl_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥఋ")] = False
        CONFIG[bstackl_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥఌ")] = True
        bstack11l1_opy_ = bstack1l1111111_opy_(CONFIG, bstack1ll1l11ll_opy_)
        logger.debug(bstack1l1l1ll11_opy_.format(str(bstack11l1_opy_)))
        if CONFIG[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ఍")]:
          bstack1lllll_opy_(bstack11l1_opy_)
        if bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩఎ") in CONFIG and bstackl_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬఏ") in CONFIG[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫఐ")][bstack1ll1l11ll_opy_]:
          bstack1l1l1ll_opy_ = CONFIG[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ఑")][bstack1ll1l11ll_opy_][bstackl_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨఒ")]
        args.append(os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠫࢃ࠭ఓ")), bstackl_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬఔ"), bstackl_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨక")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11l1_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstackl_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤఖ"))
      bstack1lll11l11_opy_ = True
      return bstack1l111l1_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack11lll1ll_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1ll1ll11l_opy_
    global bstack1l1ll1ll1_opy_
    global bstack1l1l1ll_opy_
    global bstack1l11l1lll_opy_
    global bstack1l1ll11l_opy_
    global bstack1l1ll1l1l_opy_
    CONFIG[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪగ")] = str(bstack1l1ll11l_opy_) + str(__version__)
    bstack1ll1l11ll_opy_ = 0 if bstack1l1ll1ll1_opy_ < 0 else bstack1l1ll1ll1_opy_
    if bstack1l11l1lll_opy_ is True:
      bstack1ll1l11ll_opy_ = int(threading.current_thread().getName())
    CONFIG[bstackl_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣఘ")] = True
    bstack11l1_opy_ = bstack1l1111111_opy_(CONFIG, bstack1ll1l11ll_opy_)
    logger.debug(bstack1l1l1ll11_opy_.format(str(bstack11l1_opy_)))
    if CONFIG[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧఙ")]:
      bstack1lllll_opy_(bstack11l1_opy_)
    if bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧచ") in CONFIG and bstackl_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪఛ") in CONFIG[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩజ")][bstack1ll1l11ll_opy_]:
      bstack1l1l1ll_opy_ = CONFIG[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪఝ")][bstack1ll1l11ll_opy_][bstackl_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ఞ")]
    import urllib
    import json
    bstack1ll1111l_opy_ = bstackl_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫట") + urllib.parse.quote(json.dumps(bstack11l1_opy_))
    browser = self.connect(bstack1ll1111l_opy_)
    return browser
except Exception as e:
    pass
def bstack1l11111_opy_():
    global bstack1lll11l11_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack11lll1ll_opy_
        bstack1lll11l11_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1l1l11l1_opy_
      bstack1lll11l11_opy_ = True
    except Exception as e:
      pass
def bstack1ll1l111l_opy_(context, bstack11lll111_opy_):
  try:
    context.page.evaluate(bstackl_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦఠ"), bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨడ")+ json.dumps(bstack11lll111_opy_) + bstackl_opy_ (u"ࠧࢃࡽࠣఢ"))
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀࠦణ"), e)
def bstack1l1ll111_opy_(context, message, level):
  try:
    context.page.evaluate(bstackl_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣత"), bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭థ") + json.dumps(message) + bstackl_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬద") + json.dumps(level) + bstackl_opy_ (u"ࠪࢁࢂ࠭ధ"))
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃࠢన"), e)
def bstack1l11l111l_opy_(context, status, message = bstackl_opy_ (u"ࠧࠨ఩")):
  try:
    if(status == bstackl_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨప")):
      context.page.evaluate(bstackl_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣఫ"), bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡳࡧࡤࡷࡴࡴࠢ࠻ࠩబ") + json.dumps(bstackl_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࠦభ") + str(message)) + bstackl_opy_ (u"ࠪ࠰ࠧࡹࡴࡢࡶࡸࡷࠧࡀࠧమ") + json.dumps(status) + bstackl_opy_ (u"ࠦࢂࢃࠢయ"))
    else:
      context.page.evaluate(bstackl_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨర"), bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠧఱ") + json.dumps(status) + bstackl_opy_ (u"ࠢࡾࡿࠥల"))
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡾࢁࠧళ"), e)
def bstack1l1llllll_opy_(self, url):
  global bstack1l111lll_opy_
  try:
    bstack1l111lll1_opy_(url)
  except Exception as err:
    logger.debug(bstack11ll_opy_.format(str(err)))
  try:
    bstack1l111lll_opy_(self, url)
  except Exception as e:
    try:
      bstack1llll11l1_opy_ = str(e)
      if any(err_msg in bstack1llll11l1_opy_ for err_msg in bstack1l1l11ll_opy_):
        bstack1l111lll1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack11ll_opy_.format(str(err)))
    raise e
def bstack1l11lll1l_opy_(self):
  global bstack1l1l11111_opy_
  bstack1l1l11111_opy_ = self
  return
def bstack1111l_opy_(self, test):
  global CONFIG
  global bstack1l1l11111_opy_
  global bstack1ll1ll11l_opy_
  global bstack1ll11lll1_opy_
  global bstack1l1l1ll_opy_
  global bstack1l1111ll_opy_
  global bstack1ll1llll_opy_
  global bstack1ll1ll_opy_
  try:
    if not bstack1ll1ll11l_opy_:
      with open(os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠩࢁࠫఴ")), bstackl_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪవ"), bstackl_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭శ"))) as f:
        bstack1ll111_opy_ = json.loads(bstackl_opy_ (u"ࠧࢁࠢష") + f.read().strip() + bstackl_opy_ (u"࠭ࠢࡹࠤ࠽ࠤࠧࡿࠢࠨస") + bstackl_opy_ (u"ࠢࡾࠤహ"))
        bstack1ll1ll11l_opy_ = bstack1ll111_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1ll1ll_opy_:
    for driver in bstack1ll1ll_opy_:
      if bstack1ll1ll11l_opy_ == driver.session_id:
        if test:
          bstack11l1l111_opy_ = str(test.data)
        if not bstack111lll1_opy_ and bstack11l1l111_opy_:
          bstack1l111111l_opy_ = {
            bstackl_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ఺"): bstackl_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ఻"),
            bstackl_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ఼࠭"): {
              bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩఽ"): bstack11l1l111_opy_
            }
          }
          bstack1l1lllll1_opy_ = bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪా").format(json.dumps(bstack1l111111l_opy_))
          driver.execute_script(bstack1l1lllll1_opy_)
        if bstack1ll11lll1_opy_:
          bstack111l1l1_opy_ = {
            bstackl_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ి"): bstackl_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩీ"),
            bstackl_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫు"): {
              bstackl_opy_ (u"ࠩࡧࡥࡹࡧࠧూ"): bstack11l1l111_opy_ + bstackl_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬృ"),
              bstackl_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪౄ"): bstackl_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ౅")
            }
          }
          bstack1l111111l_opy_ = {
            bstackl_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ె"): bstackl_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪే"),
            bstackl_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫై"): {
              bstackl_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ౉"): bstackl_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪొ")
            }
          }
          if bstack1ll11lll1_opy_.status == bstackl_opy_ (u"ࠫࡕࡇࡓࡔࠩో"):
            bstack1l1l11lll_opy_ = bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪౌ").format(json.dumps(bstack111l1l1_opy_))
            driver.execute_script(bstack1l1l11lll_opy_)
            bstack1l1lllll1_opy_ = bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀ్ࠫ").format(json.dumps(bstack1l111111l_opy_))
            driver.execute_script(bstack1l1lllll1_opy_)
          elif bstack1ll11lll1_opy_.status == bstackl_opy_ (u"ࠧࡇࡃࡌࡐࠬ౎"):
            reason = bstackl_opy_ (u"ࠣࠤ౏")
            bstack11l11l11_opy_ = bstack11l1l111_opy_ + bstackl_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠪ౐")
            if bstack1ll11lll1_opy_.message:
              reason = str(bstack1ll11lll1_opy_.message)
              bstack11l11l11_opy_ = bstack11l11l11_opy_ + bstackl_opy_ (u"ࠪࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࠪ౑") + reason
            bstack111l1l1_opy_[bstackl_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ౒")] = {
              bstackl_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ౓"): bstackl_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ౔"),
              bstackl_opy_ (u"ࠧࡥࡣࡷࡥౕࠬ"): bstack11l11l11_opy_
            }
            bstack1l111111l_opy_[bstackl_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶౖࠫ")] = {
              bstackl_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ౗"): bstackl_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪౘ"),
              bstackl_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫౙ"): reason
            }
            bstack1l1l11lll_opy_ = bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪౚ").format(json.dumps(bstack111l1l1_opy_))
            driver.execute_script(bstack1l1l11lll_opy_)
            bstack1l1lllll1_opy_ = bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ౛").format(json.dumps(bstack1l111111l_opy_))
            driver.execute_script(bstack1l1lllll1_opy_)
  elif bstack1ll1ll11l_opy_:
    try:
      data = {}
      bstack11l1l111_opy_ = None
      if test:
        bstack11l1l111_opy_ = str(test.data)
      if not bstack111lll1_opy_ and bstack11l1l111_opy_:
        data[bstackl_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ౜")] = bstack11l1l111_opy_
      if bstack1ll11lll1_opy_:
        if bstack1ll11lll1_opy_.status == bstackl_opy_ (u"ࠨࡒࡄࡗࡘ࠭ౝ"):
          data[bstackl_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ౞")] = bstackl_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ౟")
        elif bstack1ll11lll1_opy_.status == bstackl_opy_ (u"ࠫࡋࡇࡉࡍࠩౠ"):
          data[bstackl_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬౡ")] = bstackl_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ౢ")
          if bstack1ll11lll1_opy_.message:
            data[bstackl_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧౣ")] = str(bstack1ll11lll1_opy_.message)
      user = CONFIG[bstackl_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ౤")]
      key = CONFIG[bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ౥")]
      url = bstackl_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠯ࡼࡿ࠱࡮ࡸࡵ࡮ࠨ౦").format(user, key, bstack1ll1ll11l_opy_)
      headers = {
        bstackl_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪ౧"): bstackl_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ౨"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack11lllll1l_opy_.format(str(e)))
  if bstack1l1l11111_opy_:
    bstack1ll1llll_opy_(bstack1l1l11111_opy_)
  bstack1l1111ll_opy_(self, test)
def bstack11l1lll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1l11111l1_opy_
  bstack1l11111l1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1ll11lll1_opy_
  bstack1ll11lll1_opy_ = self._test
def bstack1lll1ll1_opy_(outs_dir, options, tests_root_name, stats, copied_artifacts, outputfile=None):
  from pabot import pabot
  outputfile = outputfile or options.get(bstackl_opy_ (u"ࠨ࡯ࡶࡶࡳࡹࡹࠨ౩"), bstackl_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺ࠮ࡹ࡯࡯ࠦ౪"))
  output_path = os.path.abspath(
    os.path.join(options.get(bstackl_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴࡥ࡫ࡵࠦ౫"), bstackl_opy_ (u"ࠤ࠱ࠦ౬")), outputfile)
  )
  files = sorted(pabot.glob(os.path.join(pabot._glob_escape(outs_dir), bstackl_opy_ (u"ࠥ࠮࠳ࡾ࡭࡭ࠤ౭"))))
  if not files:
    pabot._write(bstackl_opy_ (u"ࠫ࡜ࡇࡒࡏ࠼ࠣࡒࡴࠦ࡯ࡶࡶࡳࡹࡹࠦࡦࡪ࡮ࡨࡷࠥ࡯࡮ࠡࠤࠨࡷࠧ࠭౮") % outs_dir, pabot.Color.YELLOW)
    return bstackl_opy_ (u"ࠧࠨ౯")
  def invalid_xml_callback():
    global _ABNORMAL_EXIT_HAPPENED
    _ABNORMAL_EXIT_HAPPENED = True
  resu = pabot.merge(
    files, options, tests_root_name, copied_artifacts, invalid_xml_callback
  )
  pabot._update_stats(resu, stats)
  resu.save(output_path)
  return output_path
def bstack1lll1l11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  from pabot import pabot
  from robot import __version__ as ROBOT_VERSION
  from robot import rebot
  if bstackl_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡶࡡࡵࡪࠥ౰") in options:
    del options[bstackl_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦ౱")]
  if ROBOT_VERSION < bstackl_opy_ (u"ࠣ࠶࠱࠴ࠧ౲"):
    stats = {
      bstackl_opy_ (u"ࠤࡦࡶ࡮ࡺࡩࡤࡣ࡯ࠦ౳"): {bstackl_opy_ (u"ࠥࡸࡴࡺࡡ࡭ࠤ౴"): 0, bstackl_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ౵"): 0, bstackl_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ౶"): 0},
      bstackl_opy_ (u"ࠨࡡ࡭࡮ࠥ౷"): {bstackl_opy_ (u"ࠢࡵࡱࡷࡥࡱࠨ౸"): 0, bstackl_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ౹"): 0, bstackl_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ౺"): 0},
    }
  else:
    stats = {
      bstackl_opy_ (u"ࠥࡸࡴࡺࡡ࡭ࠤ౻"): 0,
      bstackl_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ౼"): 0,
      bstackl_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ౽"): 0,
      bstackl_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢ౾"): 0,
    }
  if pabot_args[bstackl_opy_ (u"ࠢࡃࡕࡗࡅࡈࡑ࡟ࡑࡃࡕࡅࡑࡒࡅࡍࡡࡕ࡙ࡓࠨ౿")]:
    outputs = []
    for index, _ in enumerate(pabot_args[bstackl_opy_ (u"ࠣࡄࡖࡘࡆࡉࡋࡠࡒࡄࡖࡆࡒࡌࡆࡎࡢࡖ࡚ࡔࠢಀ")]):
      copied_artifacts = pabot._copy_output_artifacts(
        options, pabot_args[bstackl_opy_ (u"ࠤࡤࡶࡹ࡯ࡦࡢࡥࡷࡷࠧಁ")], pabot_args[bstackl_opy_ (u"ࠥࡥࡷࡺࡩࡧࡣࡦࡸࡸ࡯࡮ࡴࡷࡥࡪࡴࡲࡤࡦࡴࡶࠦಂ")]
      )
      outputs += [
        bstack1lll1ll1_opy_(
          os.path.join(outs_dir, str(index)+ bstackl_opy_ (u"ࠦ࠴ࠨಃ")),
          options,
          tests_root_name,
          stats,
          copied_artifacts,
          outputfile=os.path.join(bstackl_opy_ (u"ࠧࡶࡡࡣࡱࡷࡣࡷ࡫ࡳࡶ࡮ࡷࡷࠧ಄"), bstackl_opy_ (u"ࠨ࡯ࡶࡶࡳࡹࡹࠫࡳ࠯ࡺࡰࡰࠧಅ") % index),
        )
      ]
    if bstackl_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺࠢಆ") not in options:
      options[bstackl_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴࠣಇ")] = bstackl_opy_ (u"ࠤࡲࡹࡹࡶࡵࡵ࠰ࡻࡱࡱࠨಈ")
    pabot._write_stats(stats)
    return rebot(*outputs, **pabot._options_for_rebot(options, start_time_string, pabot._now()))
  else:
    return pabot._report_results(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1ll11l1ll_opy_(self, ff_profile_dir):
  global bstack1l11l1l11_opy_
  if not ff_profile_dir:
    return None
  return bstack1l11l1l11_opy_(self, ff_profile_dir)
def bstack1l1lll1l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l1111l_opy_
  bstack1ll11111_opy_ = []
  if bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ಉ") in CONFIG:
    bstack1ll11111_opy_ = CONFIG[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧಊ")]
  bstack11l111l1_opy_ = len(suite_group) * len(pabot_args[bstackl_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡦࡪ࡮ࡨࡷࠧಋ")] or [(bstackl_opy_ (u"ࠨࠢಌ"), None)]) * len(bstack1ll11111_opy_)
  pabot_args[bstackl_opy_ (u"ࠢࡃࡕࡗࡅࡈࡑ࡟ࡑࡃࡕࡅࡑࡒࡅࡍࡡࡕ࡙ࡓࠨ಍")] = []
  for q in range(bstack11l111l1_opy_):
    pabot_args[bstackl_opy_ (u"ࠣࡄࡖࡘࡆࡉࡋࡠࡒࡄࡖࡆࡒࡌࡆࡎࡢࡖ࡚ࡔࠢಎ")].append(str(q))
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstackl_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࠥಏ")],
      pabot_args[bstackl_opy_ (u"ࠥࡺࡪࡸࡢࡰࡵࡨࠦಐ")],
      argfile,
      pabot_args.get(bstackl_opy_ (u"ࠦ࡭࡯ࡶࡦࠤ಑")),
      pabot_args[bstackl_opy_ (u"ࠧࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠣಒ")],
      platform[0],
      bstack1l1111l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstackl_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡧ࡫࡯ࡩࡸࠨಓ")] or [(bstackl_opy_ (u"ࠢࠣಔ"), None)]
    for platform in enumerate(bstack1ll11111_opy_)
  ]
def bstack11lll11l_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack11l1ll1_opy_=bstackl_opy_ (u"ࠨࠩಕ")):
  global bstack1l1llll1l_opy_
  self.platform_index = platform_index
  self.bstack1l1lll1l1_opy_ = bstack11l1ll1_opy_
  bstack1l1llll1l_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack111l1ll1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l11111l_opy_
  global bstack1ll1l1lll_opy_
  if not bstackl_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫಖ") in item.options:
    item.options[bstackl_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬಗ")] = []
  for v in item.options[bstackl_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ಘ")]:
    if bstackl_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛ࠫಙ") in v:
      item.options[bstackl_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨಚ")].remove(v)
    if bstackl_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧಛ") in v:
      item.options[bstackl_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪಜ")].remove(v)
  item.options[bstackl_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫಝ")].insert(0, bstackl_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙࠼ࡾࢁࠬಞ").format(item.platform_index))
  item.options[bstackl_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ಟ")].insert(0, bstackl_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓ࠼ࡾࢁࠬಠ").format(item.bstack1l1lll1l1_opy_))
  if bstack1ll1l1lll_opy_:
    item.options[bstackl_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨಡ")].insert(0, bstackl_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙࠺ࡼࡿࠪಢ").format(bstack1ll1l1lll_opy_))
  return bstack1l11111l_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1l111ll1_opy_(command):
  global bstack1ll1l1lll_opy_
  if bstack1ll1l1lll_opy_:
    command[0] = command[0].replace(bstackl_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧಣ"), bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡵࡧ࡯ࠥࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠦࠧತ") + bstack1ll1l1lll_opy_, 1)
  else:
    command[0] = command[0].replace(bstackl_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩಥ"), bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡷࡩࡱࠠࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨದ"), 1)
def bstack1l1l1lll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11l1l1l_opy_
  bstack1l111ll1_opy_(command)
  return bstack11l1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l1ll1111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11l1l1l_opy_
  bstack1l111ll1_opy_(command)
  return bstack11l1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1l1l1l1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11l1l1l_opy_
  bstack1l111ll1_opy_(command)
  return bstack11l1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1l111l1ll_opy_(self, runner, quiet=False, capture=True):
  global bstack1l1ll111l_opy_
  bstack1l1llll1_opy_ = bstack1l1ll111l_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstackl_opy_ (u"ࠬ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࡠࡣࡵࡶࠬಧ")):
      runner.exception_arr = []
    if not hasattr(runner, bstackl_opy_ (u"࠭ࡥࡹࡥࡢࡸࡷࡧࡣࡦࡤࡤࡧࡰࡥࡡࡳࡴࠪನ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l1llll1_opy_
def bstack11l1ll_opy_(self, name, context, *args):
  global bstack1ll1l1l11_opy_
  if name in [bstackl_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠨ಩"), bstackl_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪಪ")]:
    bstack1ll1l1l11_opy_(self, name, context, *args)
  if name == bstackl_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠪಫ"):
    try:
      if(not bstack111lll1_opy_):
        bstack11lll111_opy_ = str(self.feature.name)
        bstack1ll1l111l_opy_(context, bstack11lll111_opy_)
        context.browser.execute_script(bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨಬ") + json.dumps(bstack11lll111_opy_) + bstackl_opy_ (u"ࠫࢂࢃࠧಭ"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤ࡮ࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬಮ").format(str(e)))
  if name == bstackl_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨಯ"):
    try:
      if not hasattr(self, bstackl_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩರ")):
        self.driver_before_scenario = True
      if(not bstack111lll1_opy_):
        bstack1l1111ll1_opy_ = args[0].name
        bstack1111lll_opy_ = bstack11lll111_opy_ = str(self.feature.name)
        bstack11lll111_opy_ = bstack1111lll_opy_ + bstackl_opy_ (u"ࠨࠢ࠰ࠤࠬಱ") + bstack1l1111ll1_opy_
        if self.driver_before_scenario:
          bstack1ll1l111l_opy_(context, bstack11lll111_opy_)
          context.browser.execute_script(bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧಲ") + json.dumps(bstack11lll111_opy_) + bstackl_opy_ (u"ࠪࢁࢂ࠭ಳ"))
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡧࡱࡥࡷ࡯࡯࠻ࠢࡾࢁࠬ಴").format(str(e)))
  if name == bstackl_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ವ"):
    try:
      bstack1l1l11l1l_opy_ = args[0].status.name
      if str(bstack1l1l11l1l_opy_).lower() == bstackl_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ಶ"):
        bstack1l1lll11l_opy_ = bstackl_opy_ (u"ࠧࠨಷ")
        bstack1111l1l1_opy_ = bstackl_opy_ (u"ࠨࠩಸ")
        bstack111l111l_opy_ = bstackl_opy_ (u"ࠩࠪಹ")
        try:
          import traceback
          bstack1l1lll11l_opy_ = self.exception.__class__.__name__
          bstack11llll1ll_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1111l1l1_opy_ = bstackl_opy_ (u"ࠪࠤࠬ಺").join(bstack11llll1ll_opy_)
          bstack111l111l_opy_ = bstack11llll1ll_opy_[-1]
        except Exception as e:
          logger.debug(bstack11111ll_opy_.format(str(e)))
        bstack1l1lll11l_opy_ += bstack111l111l_opy_
        bstack1l1ll111_opy_(context, json.dumps(str(args[0].name) + bstackl_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥ಻") + str(bstack1111l1l1_opy_)), bstackl_opy_ (u"ࠧ࡫ࡲࡳࡱࡵ಼ࠦ"))
        if self.driver_before_scenario:
          bstack1l11l111l_opy_(context, bstackl_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨಽ"), bstack1l1lll11l_opy_)
        context.browser.execute_script(bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬಾ") + json.dumps(str(args[0].name) + bstackl_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢಿ") + str(bstack1111l1l1_opy_)) + bstackl_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩೀ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ࠱ࠦࠢࡳࡧࡤࡷࡴࡴࠢ࠻ࠢࠪು") + json.dumps(bstackl_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣೂ") + str(bstack1l1lll11l_opy_)) + bstackl_opy_ (u"ࠬࢃࡽࠨೃ"))
      else:
        bstack1l1ll111_opy_(context, bstackl_opy_ (u"ࠨࡐࡢࡵࡶࡩࡩࠧࠢೄ"), bstackl_opy_ (u"ࠢࡪࡰࡩࡳࠧ೅"))
        if self.driver_before_scenario:
          bstack1l11l111l_opy_(context, bstackl_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣೆ"))
        context.browser.execute_script(bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧೇ") + json.dumps(str(args[0].name) + bstackl_opy_ (u"ࠥࠤ࠲ࠦࡐࡢࡵࡶࡩࡩࠧࠢೈ")) + bstackl_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢࡾࡿࠪ೉"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡸࡺࡡࡵࡷࡶࠦ࠿ࠨࡰࡢࡵࡶࡩࡩࠨࡽࡾࠩೊ"))
    except Exception as e:
      logger.debug(bstackl_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨೋ").format(str(e)))
  if name == bstackl_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧೌ"):
    try:
      if context.failed is True:
        bstack1ll1l11l1_opy_ = []
        bstack1lll1111l_opy_ = []
        bstack1l11l11l_opy_ = []
        bstack1l11l11ll_opy_ = bstackl_opy_ (u"ࠨ್ࠩ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1ll1l11l1_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack11llll1ll_opy_ = traceback.format_tb(exc_tb)
            bstack111ll1_opy_ = bstackl_opy_ (u"ࠩࠣࠫ೎").join(bstack11llll1ll_opy_)
            bstack1lll1111l_opy_.append(bstack111ll1_opy_)
            bstack1l11l11l_opy_.append(bstack11llll1ll_opy_[-1])
        except Exception as e:
          logger.debug(bstack11111ll_opy_.format(str(e)))
        bstack1l1lll11l_opy_ = bstackl_opy_ (u"ࠪࠫ೏")
        for i in range(len(bstack1ll1l11l1_opy_)):
          bstack1l1lll11l_opy_ += bstack1ll1l11l1_opy_[i] + bstack1l11l11l_opy_[i] + bstackl_opy_ (u"ࠫࡡࡴࠧ೐")
        bstack1l11l11ll_opy_ = bstackl_opy_ (u"ࠬࠦࠧ೑").join(bstack1lll1111l_opy_)
        if not self.driver_before_scenario:
          bstack1l1ll111_opy_(context, bstack1l11l11ll_opy_, bstackl_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ೒"))
          bstack1l11l111l_opy_(context, bstackl_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ೓"), bstack1l1lll11l_opy_)
          context.browser.execute_script(bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭೔") + json.dumps(bstack1l11l11ll_opy_) + bstackl_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩೕ"))
          context.browser.execute_script(bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ࠱ࠦࠢࡳࡧࡤࡷࡴࡴࠢ࠻ࠢࠪೖ") + json.dumps(bstackl_opy_ (u"ࠦࡘࡵ࡭ࡦࠢࡶࡧࡪࡴࡡࡳ࡫ࡲࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦ࡜࡯ࠤ೗") + str(bstack1l1lll11l_opy_)) + bstackl_opy_ (u"ࠬࢃࡽࠨ೘"))
      else:
        if not self.driver_before_scenario:
          bstack1l1ll111_opy_(context, bstackl_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤ೙") + str(self.feature.name) + bstackl_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤ೚"), bstackl_opy_ (u"ࠣ࡫ࡱࡪࡴࠨ೛"))
          bstack1l11l111l_opy_(context, bstackl_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ೜"))
          context.browser.execute_script(bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨೝ") + json.dumps(bstackl_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩ࠿ࠦࠢೞ") + str(self.feature.name) + bstackl_opy_ (u"ࠧࠦࡰࡢࡵࡶࡩࡩࠧࠢ೟")) + bstackl_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬೠ"))
          context.browser.execute_script(bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠣࡲࡤࡷࡸ࡫ࡤࠣࡿࢀࠫೡ"))
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪೢ").format(str(e)))
  if name in [bstackl_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩೣ"), bstackl_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ೤")]:
    bstack1ll1l1l11_opy_(self, name, context, *args)
    if (name == bstackl_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ೥") and self.driver_before_scenario) or (name == bstackl_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ೦") and not self.driver_before_scenario):
      try:
        context.browser.quit()
      except Exception:
        pass
def bstack1ll1ll1ll_opy_(config, startdir):
  return bstackl_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࠲ࢀࠦ೧").format(bstackl_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨ೨"))
class Notset:
  def __repr__(self):
    return bstackl_opy_ (u"ࠣ࠾ࡑࡓ࡙࡙ࡅࡕࡀࠥ೩")
notset = Notset()
def bstack1ll11l1l1_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack11l1111_opy_
  if str(name).lower() == bstackl_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩ೪"):
    return bstackl_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤ೫")
  else:
    return bstack11l1111_opy_(self, name, default, skip)
def bstack11ll1l11_opy_(item, when):
  global bstack1ll111l11_opy_
  try:
    bstack1ll111l11_opy_(item, when)
  except Exception as e:
    pass
def bstack1l11l1_opy_():
  return
def bstack111ll1l_opy_(bstack1ll1111l1_opy_):
  global bstack1l1ll11l_opy_
  global bstack1lll11l11_opy_
  bstack1l1ll11l_opy_ = bstack1ll1111l1_opy_
  logger.info(bstack11l1l1ll_opy_.format(bstack1l1ll11l_opy_.split(bstackl_opy_ (u"ࠫ࠲࠭೬"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    Service.start = bstack1ll1lll11_opy_
    Service.stop = bstack11lll1l1l_opy_
    webdriver.Remote.__init__ = bstack11llllll1_opy_
    webdriver.Remote.get = bstack1l1llllll_opy_
    WebDriver.close = bstack1l1l11ll1_opy_
    bstack1lll11l11_opy_ = True
  except Exception as e:
    pass
  bstack1l11111_opy_()
  if not bstack1lll11l11_opy_:
    bstack111lllll_opy_(bstackl_opy_ (u"ࠧࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠢ೭"), bstack1ll1ll1_opy_)
  if bstack111111_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1l1llll_opy_
    except Exception as e:
      logger.error(bstack1lll111_opy_.format(str(e)))
  if (bstackl_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ೮") in str(bstack1ll1111l1_opy_).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1ll11l1ll_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1l11lll1l_opy_
      except Exception as e:
        logger.warn(bstack1l1l111l_opy_ + str(e))
    except Exception as e:
      bstack111lllll_opy_(e, bstack1l1l111l_opy_)
    Output.end_test = bstack1111l_opy_
    TestStatus.__init__ = bstack11l1lll_opy_
    QueueItem.__init__ = bstack11lll11l_opy_
    pabot._create_items = bstack1l1lll1l_opy_
    try:
      from pabot import __version__ as bstack111l1111_opy_
      if version.parse(bstack111l1111_opy_) >= version.parse(bstackl_opy_ (u"ࠧ࠳࠰࠴࠹࠳࠶ࠧ೯")):
        pabot._run = bstack1l1l1l1l1_opy_
      elif version.parse(bstack111l1111_opy_) >= version.parse(bstackl_opy_ (u"ࠨ࠴࠱࠵࠸࠴࠰ࠨ೰")):
        pabot._run = bstack1l1ll1111_opy_
      else:
        pabot._run = bstack1l1l1lll1_opy_
    except Exception as e:
      pabot._run = bstack1l1l1lll1_opy_
    pabot._create_command_for_execution = bstack111l1ll1_opy_
    pabot._report_results = bstack1lll1l11_opy_
  if bstackl_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩೱ") in str(bstack1ll1111l1_opy_).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack111lllll_opy_(e, bstack1l1l1lll_opy_)
    Runner.run_hook = bstack11l1ll_opy_
    Step.run = bstack1l111l1ll_opy_
  if bstackl_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪೲ") in str(bstack1ll1111l1_opy_).lower():
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      from _pytest import runner
      pytest_selenium.pytest_report_header = bstack1ll1ll1ll_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l11l1_opy_
      Config.getoption = bstack1ll11l1l1_opy_
      runner._update_current_test_var = bstack11ll1l11_opy_
    except Exception as e:
      pass
def bstack11ll1l_opy_():
  global CONFIG
  if bstackl_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫೳ") in CONFIG and int(CONFIG[bstackl_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ೴")]) > 1:
    logger.warn(bstack1lll1ll_opy_)
def bstack111l1_opy_(bstack1ll1l_opy_, index):
  bstack111ll1l_opy_(bstack1lll11111_opy_)
  exec(open(bstack1ll1l_opy_).read())
def bstack1l1l111ll_opy_(arg):
  arg.append(bstackl_opy_ (u"ࠨ࠭࠮ࡥࡤࡴࡹࡻࡲࡦ࠿ࡶࡽࡸࠨ೵"))
  arg.append(bstackl_opy_ (u"ࠢ࠮࡙ࠥ೶"))
  arg.append(bstackl_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥ࠻ࡏࡲࡨࡺࡲࡥࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡬ࡱࡵࡵࡲࡵࡧࡧ࠾ࡵࡿࡴࡦࡵࡷ࠲ࡕࡿࡴࡦࡵࡷ࡛ࡦࡸ࡮ࡪࡰࡪࠦ೷"))
  global CONFIG
  bstack111ll1l_opy_(bstack1llll1l_opy_)
  os.environ[bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪ೸")] = CONFIG[bstackl_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ೹")]
  os.environ[bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧ೺")] = CONFIG[bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ೻")]
  from _pytest.config import main as bstack1l1l1ll1_opy_
  bstack1l1l1ll1_opy_(arg)
def bstack11lll11l1_opy_(arg):
  bstack111ll1l_opy_(bstack1l11ll1l1_opy_)
  from behave.__main__ import main as bstack1ll1l1111_opy_
  bstack1ll1l1111_opy_(arg)
def bstack11ll1ll1_opy_():
  logger.info(bstack1l1lll11_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstackl_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ೼"), help=bstackl_opy_ (u"ࠧࡈࡧࡱࡩࡷࡧࡴࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡲࡲ࡫࡯ࡧࠨ೽"))
  parser.add_argument(bstackl_opy_ (u"ࠨ࠯ࡸࠫ೾"), bstackl_opy_ (u"ࠩ࠰࠱ࡺࡹࡥࡳࡰࡤࡱࡪ࠭೿"), help=bstackl_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡶࡵࡨࡶࡳࡧ࡭ࡦࠩഀ"))
  parser.add_argument(bstackl_opy_ (u"ࠫ࠲ࡱࠧഁ"), bstackl_opy_ (u"ࠬ࠳࠭࡬ࡧࡼࠫം"), help=bstackl_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠧഃ"))
  parser.add_argument(bstackl_opy_ (u"ࠧ࠮ࡨࠪഄ"), bstackl_opy_ (u"ࠨ࠯࠰ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭അ"), help=bstackl_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨആ"))
  bstack11ll1_opy_ = parser.parse_args()
  try:
    bstack111l1l_opy_ = bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡪࡩࡳ࡫ࡲࡪࡥ࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧഇ")
    if bstack11ll1_opy_.framework and bstack11ll1_opy_.framework not in (bstackl_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫഈ"), bstackl_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭ഉ")):
      bstack111l1l_opy_ = bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬഊ")
    bstack1ll1lll_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111l1l_opy_)
    bstack1111ll1l_opy_ = open(bstack1ll1lll_opy_, bstackl_opy_ (u"ࠧࡳࠩഋ"))
    bstack1llll_opy_ = bstack1111ll1l_opy_.read()
    bstack1111ll1l_opy_.close()
    if bstack11ll1_opy_.username:
      bstack1llll_opy_ = bstack1llll_opy_.replace(bstackl_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨഌ"), bstack11ll1_opy_.username)
    if bstack11ll1_opy_.key:
      bstack1llll_opy_ = bstack1llll_opy_.replace(bstackl_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫ഍"), bstack11ll1_opy_.key)
    if bstack11ll1_opy_.framework:
      bstack1llll_opy_ = bstack1llll_opy_.replace(bstackl_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫഎ"), bstack11ll1_opy_.framework)
    file_name = bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧഏ")
    file_path = os.path.abspath(file_name)
    bstack111ll1ll_opy_ = open(file_path, bstackl_opy_ (u"ࠬࡽࠧഐ"))
    bstack111ll1ll_opy_.write(bstack1llll_opy_)
    bstack111ll1ll_opy_.close()
    logger.info(bstack11111_opy_)
    try:
      os.environ[bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ഑")] = bstack11ll1_opy_.framework if bstack11ll1_opy_.framework != None else bstackl_opy_ (u"ࠢࠣഒ")
      config = yaml.safe_load(bstack1llll_opy_)
      config[bstackl_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨഓ")] = bstackl_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡶࡩࡹࡻࡰࠨഔ")
      bstack1l1ll11_opy_(bstack11lll1l_opy_, config)
    except Exception as e:
      logger.debug(bstack1111l11_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1llll11ll_opy_.format(str(e)))
def bstack1l1ll11_opy_(bstack11lll_opy_, config, bstack1ll11l1l_opy_ = {}):
  global bstack111l_opy_
  if not config:
    return
  bstack11l1ll11_opy_ = bstack1lll1l11l_opy_ if not bstack111l_opy_ else ( bstack1llll111l_opy_ if bstackl_opy_ (u"ࠪࡥࡵࡶࠧക") in config else bstack1l11l11_opy_ )
  data = {
    bstackl_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ഖ"): config[bstackl_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧഗ")],
    bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩഘ"): config[bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪങ")],
    bstackl_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬച"): bstack11lll_opy_,
    bstackl_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬഛ"): {
      bstackl_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨജ"): str(config[bstackl_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫഝ")]) if bstackl_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬഞ") in config else bstackl_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢട"),
      bstackl_opy_ (u"ࠧࡳࡧࡩࡩࡷࡸࡥࡳࠩഠ"): bstack1l1l1111l_opy_(os.getenv(bstackl_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠥഡ"), bstackl_opy_ (u"ࠤࠥഢ"))),
      bstackl_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬണ"): bstackl_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫത"),
      bstackl_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ഥ"): bstack11l1ll11_opy_,
      bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩദ"): config[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪധ")]if config[bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫന")] else bstackl_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥഩ"),
      bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬപ"): str(config[bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ഫ")]) if bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧബ") in config else bstackl_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢഭ"),
      bstackl_opy_ (u"ࠧࡰࡵࠪമ"): sys.platform,
      bstackl_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪയ"): socket.gethostname()
    }
  }
  update(data[bstackl_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬര")], bstack1ll11l1l_opy_)
  try:
    response = bstack1111ll_opy_(bstackl_opy_ (u"ࠪࡔࡔ࡙ࡔࠨറ"), bstack11l11l1l_opy_, data, config)
    if response:
      logger.debug(bstack1l1l1l1ll_opy_.format(bstack11lll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1ll111lll_opy_.format(str(e)))
def bstack1111ll_opy_(type, url, data, config):
  bstack1ll11l111_opy_ = bstack1l1111l1l_opy_.format(url)
  proxy = bstack11llll1_opy_(config)
  proxies = {}
  response = {}
  if config.get(bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧല")) or config.get(bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩള")):
    proxies = {
      bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬഴ"): proxy
    }
  if type == bstackl_opy_ (u"ࠧࡑࡑࡖࡘࠬവ"):
    response = requests.post(bstack1ll11l111_opy_, json=data,
                    headers={bstackl_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧശ"): bstackl_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬഷ")}, auth=(config[bstackl_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬസ")], config[bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧഹ")]), proxies=proxies)
  return response
def bstack1l1l1111l_opy_(framework):
  return bstackl_opy_ (u"ࠧࢁࡽ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤഺ").format(str(framework), __version__) if framework else bstackl_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃ഻ࠢ").format(__version__)
def bstack1lll1l1l_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack1l11ll1_opy_()
    logger.debug(bstack1ll111l1_opy_.format(str(CONFIG)))
    bstack1llll1111_opy_()
    bstack111l1ll_opy_()
  except Exception as e:
    logger.error(bstackl_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱ࠮ࠣࡩࡷࡸ࡯ࡳ࠼഼ࠣࠦ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack111ll11_opy_
  atexit.register(bstack11111111_opy_)
  signal.signal(signal.SIGINT, bstack1lll111ll_opy_)
  signal.signal(signal.SIGTERM, bstack1lll111ll_opy_)
def bstack111ll11_opy_(exctype, value, traceback):
  global bstack1ll1ll_opy_
  try:
    for driver in bstack1ll1ll_opy_:
      driver.execute_script(
        bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠤࡩࡥ࡮ࡲࡥࡥࠤ࠯ࠤࠧࡸࡥࡢࡵࡲࡲࠧࡀࠠࠨഽ") + json.dumps(bstackl_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧാ") + str(value)) + bstackl_opy_ (u"ࠪࢁࢂ࠭ി"))
  except Exception:
    pass
  bstack111l1lll_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack111l1lll_opy_(message = bstackl_opy_ (u"ࠫࠬീ")):
  global CONFIG
  try:
    if message:
      bstack1ll11l1l_opy_ = {
        bstackl_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫു"): str(message)
      }
      bstack1l1ll11_opy_(bstack11l1l1l1_opy_, CONFIG, bstack1ll11l1l_opy_)
    else:
      bstack1l1ll11_opy_(bstack11l1l1l1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1ll1l1l_opy_.format(str(e)))
def bstack11l1l1_opy_(bstack11lllll11_opy_, size):
  bstack11l111l_opy_ = []
  while len(bstack11lllll11_opy_) > size:
    bstack1llllll_opy_ = bstack11lllll11_opy_[:size]
    bstack11l111l_opy_.append(bstack1llllll_opy_)
    bstack11lllll11_opy_   = bstack11lllll11_opy_[size:]
  bstack11l111l_opy_.append(bstack11lllll11_opy_)
  return bstack11l111l_opy_
def run_on_browserstack():
  if len(sys.argv) <= 1:
    logger.critical(bstack1111ll1_opy_)
    return
  if sys.argv[1] == bstackl_opy_ (u"࠭࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩൂ")  or sys.argv[1] == bstackl_opy_ (u"ࠧ࠮ࡸࠪൃ"):
    logger.info(bstackl_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡑࡻࡷ࡬ࡴࡴࠠࡔࡆࡎࠤࡻࢁࡽࠨൄ").format(__version__))
    return
  if sys.argv[1] == bstackl_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ൅"):
    bstack11ll1ll1_opy_()
    return
  args = sys.argv
  bstack1lll1l1l_opy_()
  global CONFIG
  global bstack1l11lll_opy_
  global bstack1l11l1lll_opy_
  global bstack1l1ll1ll1_opy_
  global bstack1l1111l_opy_
  global bstack1ll1l1lll_opy_
  bstack1llll11_opy_ = bstackl_opy_ (u"ࠪࠫെ")
  if args[1] == bstackl_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫേ") or args[1] == bstackl_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭ൈ"):
    bstack1llll11_opy_ = bstackl_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭൉")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ൊ"):
    bstack1llll11_opy_ = bstackl_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧോ")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨൌ"):
    bstack1llll11_opy_ = bstackl_opy_ (u"ࠪࡴࡦࡨ࡯ࡵ്ࠩ")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬൎ"):
    bstack1llll11_opy_ = bstackl_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭൏")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭൐"):
    bstack1llll11_opy_ = bstackl_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ൑")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ൒"):
    bstack1llll11_opy_ = bstackl_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ൓")
    args = args[2:]
  else:
    if not bstackl_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ൔ") in CONFIG or str(CONFIG[bstackl_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧൕ")]).lower() in [bstackl_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬൖ"), bstackl_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧൗ")]:
      bstack1llll11_opy_ = bstackl_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ൘")
      args = args[1:]
    elif str(CONFIG[bstackl_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ൙")]).lower() == bstackl_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ൚"):
      bstack1llll11_opy_ = bstackl_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ൛")
      args = args[1:]
    elif str(CONFIG[bstackl_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ൜")]).lower() == bstackl_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ൝"):
      bstack1llll11_opy_ = bstackl_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ൞")
      args = args[1:]
    elif str(CONFIG[bstackl_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪൟ")]).lower() == bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨൠ"):
      bstack1llll11_opy_ = bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩൡ")
      args = args[1:]
    elif str(CONFIG[bstackl_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ൢ")]).lower() == bstackl_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫൣ"):
      bstack1llll11_opy_ = bstackl_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ൤")
      args = args[1:]
    else:
      os.environ[bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ൥")] = bstack1llll11_opy_
      bstack1lllll111_opy_(bstack111l11_opy_)
  global bstack1l111l1_opy_
  try:
    os.environ[bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ൦")] = bstack1llll11_opy_
    bstack1l1ll11_opy_(bstack1lll11l1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1ll1l1l_opy_.format(str(e)))
  global bstack1l1ll1l1l_opy_
  global bstack1l1111ll_opy_
  global bstack1ll1llll_opy_
  global bstack1l11111l1_opy_
  global bstack1l11l1l11_opy_
  global bstack11l1l1l_opy_
  global bstack1l1llll1l_opy_
  global bstack1l11111l_opy_
  global bstack1llllll11_opy_
  global bstack1ll1l1l11_opy_
  global bstack1l1ll111l_opy_
  global bstack1l111lll_opy_
  global bstack1l11llll1_opy_
  global bstack11l1111_opy_
  global bstack1ll111l11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1ll1l1l_opy_ = webdriver.Remote.__init__
    bstack1llllll11_opy_ = WebDriver.close
    bstack1l111lll_opy_ = WebDriver.get
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l111l1_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack1ll11l11_opy_():
    if bstack1ll111111_opy_() < version.parse(bstack1l1ll1_opy_):
      logger.error(bstack1l11l111_opy_.format(bstack1ll111111_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l11llll1_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1lll111_opy_.format(str(e)))
  bstack1ll11l_opy_()
  if (bstack1llll11_opy_ in [bstackl_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ൧"), bstackl_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ൨"), bstackl_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ൩")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1ll11l1ll_opy_
        bstack1ll1llll_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1l1l111l_opy_ + str(e))
    except Exception as e:
      bstack111lllll_opy_(e, bstack1l1l111l_opy_)
    bstack1l1111ll_opy_ = Output.end_test
    bstack1l11111l1_opy_ = TestStatus.__init__
    bstack11l1l1l_opy_ = pabot._run
    bstack1l1llll1l_opy_ = QueueItem.__init__
    bstack1l11111l_opy_ = pabot._create_command_for_execution
  if bstack1llll11_opy_ == bstackl_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ൪"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack111lllll_opy_(e, bstack1l1l1lll_opy_)
    bstack1ll1l1l11_opy_ = Runner.run_hook
    bstack1l1ll111l_opy_ = Step.run
  if bstack1llll11_opy_ == bstackl_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ൫"):
    try:
      from _pytest.config import Config
      bstack11l1111_opy_ = Config.getoption
      from _pytest import runner
      bstack1ll111l11_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1lll1111_opy_)
  if bstack1llll11_opy_ == bstackl_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭൬"):
    bstack11l111_opy_()
    bstack11ll1l_opy_()
    if bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ൭") in CONFIG:
      bstack1l11l1lll_opy_ = True
      bstack111l1l11_opy_ = []
      for index, platform in enumerate(CONFIG[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ൮")]):
        bstack111l1l11_opy_.append(bstack1l11l1l1l_opy_(name=str(index),
                                      target=bstack111l1_opy_, args=(args[0], index)))
      for t in bstack111l1l11_opy_:
        t.start()
      for t in bstack111l1l11_opy_:
        t.join()
    else:
      bstack111ll1l_opy_(bstack1lll11111_opy_)
      exec(open(args[0]).read())
  elif bstack1llll11_opy_ == bstackl_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ൯") or bstack1llll11_opy_ == bstackl_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ൰"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack111lllll_opy_(e, bstack1l1l111l_opy_)
    bstack11l111_opy_()
    bstack111ll1l_opy_(bstack1111111_opy_)
    if bstackl_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ൱") in args:
      i = args.index(bstackl_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ൲"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1l11lll_opy_))
    args.insert(0, str(bstackl_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ൳")))
    pabot.main(args)
  elif bstack1llll11_opy_ == bstackl_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ൴"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack111lllll_opy_(e, bstack1l1l111l_opy_)
    for a in args:
      if bstackl_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞ࠧ൵") in a:
        bstack1l1ll1ll1_opy_ = int(a.split(bstackl_opy_ (u"ࠩ࠽ࠫ൶"))[1])
      if bstackl_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ൷") in a:
        bstack1l1111l_opy_ = str(a.split(bstackl_opy_ (u"ࠫ࠿࠭൸"))[1])
      if bstackl_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗࠬ൹") in a:
        bstack1ll1l1lll_opy_ = str(a.split(bstackl_opy_ (u"࠭࠺ࠨൺ"))[1])
    bstack111ll1l_opy_(bstack1111111_opy_)
    run_cli(args)
  elif bstack1llll11_opy_ == bstackl_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧൻ"):
    try:
      from _pytest.config import _prepareconfig
      from _pytest.config import Config
      from _pytest import runner
      import importlib
      bstack11l1ll1l_opy_ = importlib.find_loader(bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪർ"))
    except Exception as e:
      logger.warn(e, bstack1lll1111_opy_)
    bstack11l111_opy_()
    try:
      if bstackl_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫൽ") in args:
        i = args.index(bstackl_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬൾ"))
        args.pop(i+1)
        args.pop(i)
      if bstackl_opy_ (u"ࠫ࠲࠳ࡰ࡭ࡷࡪ࡭ࡳࡹࠧൿ") in args:
        i = args.index(bstackl_opy_ (u"ࠬ࠳࠭ࡱ࡮ࡸ࡫࡮ࡴࡳࠨ඀"))
        args.pop(i+1)
        args.pop(i)
      if bstackl_opy_ (u"࠭࠭ࡱࠩඁ") in args:
        i = args.index(bstackl_opy_ (u"ࠧ࠮ࡲࠪං"))
        args.pop(i+1)
        args.pop(i)
      if bstackl_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩඃ") in args:
        i = args.index(bstackl_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ඄"))
        args.pop(i+1)
        args.pop(i)
      if bstackl_opy_ (u"ࠪ࠱ࡳ࠭අ") in args:
        i = args.index(bstackl_opy_ (u"ࠫ࠲ࡴࠧආ"))
        args.pop(i+1)
        args.pop(i)
    except Exception as exc:
      logger.error(str(exc))
    config = _prepareconfig(args)
    bstack1l11l1111_opy_ = config.args
    bstack11111l1l_opy_ = config.invocation_params.args
    bstack11111l1l_opy_ = list(bstack11111l1l_opy_)
    bstack11111l11_opy_ = []
    for arg in bstack11111l1l_opy_:
      for spec in bstack1l11l1111_opy_:
        if os.path.normpath(arg) != os.path.normpath(spec):
          bstack11111l11_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstackl_opy_ (u"ࠬࡽࡩ࡯ࡦࡲࡻࡸ࠭ඇ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l11l1111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1ll11l1_opy_)))
                    for bstack1ll11l1_opy_ in bstack1l11l1111_opy_]
    if (bstack111lll1_opy_):
      bstack11111l11_opy_.append(bstackl_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪඈ"))
      bstack11111l11_opy_.append(bstackl_opy_ (u"ࠧࡕࡴࡸࡩࠬඉ"))
    bstack11111l11_opy_.append(bstackl_opy_ (u"ࠨ࠯ࡳࠫඊ"))
    bstack11111l11_opy_.append(bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠧඋ"))
    bstack11111l11_opy_.append(bstackl_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬඌ"))
    bstack11111l11_opy_.append(bstackl_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫඍ"))
    bstack1111_opy_ = []
    for spec in bstack1l11l1111_opy_:
      bstack1lllll1_opy_ = []
      bstack1lllll1_opy_.append(spec)
      bstack1lllll1_opy_ += bstack11111l11_opy_
      bstack1111_opy_.append(bstack1lllll1_opy_)
    bstack1l11l1lll_opy_ = True
    bstack11llll1l1_opy_ = 1
    if bstackl_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬඎ") in CONFIG:
      bstack11llll1l1_opy_ = CONFIG[bstackl_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ඏ")]
    bstack1ll1l1_opy_ = int(bstack11llll1l1_opy_)*int(len(CONFIG[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪඐ")]))
    execution_items = []
    for index, _ in enumerate(CONFIG[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫඑ")]):
      for bstack1lllll1_opy_ in bstack1111_opy_:
        item = {}
        item[bstackl_opy_ (u"ࠩࡤࡶ࡬࠭ඒ")] = bstack1lllll1_opy_
        item[bstackl_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩඓ")] = index
        execution_items.append(item)
    bstack11llll11_opy_ = bstack11l1l1_opy_(execution_items, bstack1ll1l1_opy_)
    for execution_item in bstack11llll11_opy_:
      bstack111l1l11_opy_ = []
      for item in execution_item:
        bstack111l1l11_opy_.append(bstack1l11l1l1l_opy_(name=str(item[bstackl_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪඔ")]),
                                            target=bstack1l1l111ll_opy_,
                                            args=(item[bstackl_opy_ (u"ࠬࡧࡲࡨࠩඕ")],)))
      for t in bstack111l1l11_opy_:
        t.start()
      for t in bstack111l1l11_opy_:
        t.join()
  elif bstack1llll11_opy_ == bstackl_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ඖ"):
    try:
      from behave.__main__ import main as bstack1ll1l1111_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack111lllll_opy_(e, bstack1l1l1lll_opy_)
    bstack11l111_opy_()
    bstack1l11l1lll_opy_ = True
    bstack11llll1l1_opy_ = 1
    if bstackl_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ඗") in CONFIG:
      bstack11llll1l1_opy_ = CONFIG[bstackl_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ඘")]
    bstack1ll1l1_opy_ = int(bstack11llll1l1_opy_)*int(len(CONFIG[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ඙")]))
    config = Configuration(args)
    bstack1l11l1111_opy_ = config.paths
    bstack1lll1l111_opy_ = []
    for arg in args:
      if os.path.normpath(arg) not in bstack1l11l1111_opy_:
        bstack1lll1l111_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstackl_opy_ (u"ࠪࡻ࡮ࡴࡤࡰࡹࡶࠫක"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l11l1111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1ll11l1_opy_)))
                    for bstack1ll11l1_opy_ in bstack1l11l1111_opy_]
    bstack1111_opy_ = []
    for spec in bstack1l11l1111_opy_:
      bstack1lllll1_opy_ = []
      bstack1lllll1_opy_ += bstack1lll1l111_opy_
      bstack1lllll1_opy_.append(spec)
      bstack1111_opy_.append(bstack1lllll1_opy_)
    execution_items = []
    for index, _ in enumerate(CONFIG[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧඛ")]):
      for bstack1lllll1_opy_ in bstack1111_opy_:
        item = {}
        item[bstackl_opy_ (u"ࠬࡧࡲࡨࠩග")] = bstackl_opy_ (u"࠭ࠠࠨඝ").join(bstack1lllll1_opy_)
        item[bstackl_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ඞ")] = index
        execution_items.append(item)
    bstack11llll11_opy_ = bstack11l1l1_opy_(execution_items, bstack1ll1l1_opy_)
    for execution_item in bstack11llll11_opy_:
      bstack111l1l11_opy_ = []
      for item in execution_item:
        bstack111l1l11_opy_.append(bstack1l11l1l1l_opy_(name=str(item[bstackl_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧඟ")]),
                                            target=bstack11lll11l1_opy_,
                                            args=(item[bstackl_opy_ (u"ࠩࡤࡶ࡬࠭ච")],)))
      for t in bstack111l1l11_opy_:
        t.start()
      for t in bstack111l1l11_opy_:
        t.join()
  else:
    bstack1lllll111_opy_(bstack111l11_opy_)
  bstack1ll1l1ll_opy_()
def bstack1ll1l1ll_opy_():
  global CONFIG
  try:
    if bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ඡ") in CONFIG:
      host = bstackl_opy_ (u"ࠫࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪࠧජ") if bstackl_opy_ (u"ࠬࡧࡰࡱࠩඣ") in CONFIG else bstackl_opy_ (u"࠭ࡡࡱ࡫ࠪඤ")
      user = CONFIG[bstackl_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩඥ")]
      key = CONFIG[bstackl_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫඦ")]
      bstack1lllllll1_opy_ = bstackl_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨට") if bstackl_opy_ (u"ࠪࡥࡵࡶࠧඨ") in CONFIG else bstackl_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ඩ")
      url = bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࢁࡽ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠮࡫ࡵࡲࡲࠬඪ").format(user, key, host, bstack1lllllll1_opy_)
      headers = {
        bstackl_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬණ"): bstackl_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪඬ"),
      }
      if bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪත") in CONFIG:
        params = {bstackl_opy_ (u"ࠩࡱࡥࡲ࡫ࠧථ"):CONFIG[bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ද")], bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧධ"):CONFIG[bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧන")]}
      else:
        params = {bstackl_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ඲"):CONFIG[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪඳ")]}
      response = requests.get(url, params=params, headers=headers)
      if response.json():
        bstack1ll1l11_opy_ = response.json()[0][bstackl_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡨࡵࡪ࡮ࡧࠫප")]
        if bstack1ll1l11_opy_:
          bstack1ll1lllll_opy_ = bstack1ll1l11_opy_[bstackl_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭ඵ")].split(bstackl_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥ࠰ࡦࡺ࡯࡬ࡥࠩබ"))[0] + bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡶ࠳ࠬභ") + bstack1ll1l11_opy_[bstackl_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨම")]
          logger.info(bstack1ll1111_opy_.format(bstack1ll1lllll_opy_))
          bstack1l11llll_opy_ = CONFIG[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩඹ")]
          if bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩය") in CONFIG:
            bstack1l11llll_opy_ += bstackl_opy_ (u"ࠨࠢࠪර") + CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ඼")]
          if bstack1l11llll_opy_!= bstack1ll1l11_opy_[bstackl_opy_ (u"ࠪࡲࡦࡳࡥࠨල")]:
            logger.debug(bstack1ll1ll1l_opy_.format(bstack1ll1l11_opy_[bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ඾")], bstack1l11llll_opy_))
    else:
      logger.warn(bstack111llll1_opy_)
  except Exception as e:
    logger.debug(bstack1l11111ll_opy_.format(str(e)))
def bstack1l111lll1_opy_(url, bstack1lll1l1ll_opy_=False):
  global CONFIG
  global bstack1ll11_opy_
  if not bstack1ll11_opy_:
    hostname = bstack111lll1l_opy_(url)
    is_private = bstack1l1l1llll_opy_(hostname)
    if (bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ඿") in CONFIG and not CONFIG[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪව")]) and (is_private or bstack1lll1l1ll_opy_):
      bstack1ll11_opy_ = hostname
def bstack111lll1l_opy_(url):
  return urlparse(url).hostname
def bstack1l1l1llll_opy_(hostname):
  for bstack11l11111_opy_ in bstack11l11_opy_:
    regex = re.compile(bstack11l11111_opy_)
    if regex.match(hostname):
      return True
  return False