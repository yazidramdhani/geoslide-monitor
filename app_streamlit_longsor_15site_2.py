"""
SISTEM MONITORING POTENSI LONGSOR INTERAKTIF — 15 DAS & 15 LOKASI SITE
Fitur:
- Droplist Terpisah: 15 Lokasi Batas DAS/Catchment Area & 15 Lokasi Batas Site
- Detail Tanggal Prakiraan Hujan 7 Hari ke Depan (Sabtu, 17 Okt 2026 s/d Jumat, 23 Okt 2026)
- Integrasi Real-Time Cloud / Google Drive & Google Sheets (Tanpa Upload Ulang Manual)

Cara menjalankan lokal:
  pip install streamlit folium streamlit-folium geopandas rasterio numpy pandas openpyxl
  streamlit run app_streamlit_longsor_15site.py

Cara deploy gratis agar bisa diakses real-time oleh orang lain:
  Unggah script ini + requirements.txt ke GitHub, lalu hubungkan ke https://share.streamlit.io
"""

import math
import numpy as np
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

LOCATIONS_DB = {
  "DAS_01": {
    "dasId": "DAS_01",
    "dasName": "DAS_01 \u2014 DAS Ciliwung Hulu (Jawa Barat)",
    "siteId": "SITE_01",
    "siteName": "SITE_01 \u2014 Site 01 - Cibanteng Bogor",
    "prov": "Jawa Barat",
    "center": [
      -6.685,
      106.935
    ],
    "zoom": 13,
    "dasAreaHa": 1450,
    "siteAreaHa": 320,
    "weeklyRain": [
      85,
      115,
      40,
      25,
      160,
      95,
      30
    ],
    "dasBoundary": [
      [
        -6.65,
        106.9
      ],
      [
        -6.648,
        106.965
      ],
      [
        -6.675,
        106.982
      ],
      [
        -6.718,
        106.97
      ],
      [
        -6.722,
        106.915
      ],
      [
        -6.69,
        106.892
      ]
    ],
    "siteBoundary": [
      [
        -6.668,
        106.92
      ],
      [
        -6.666,
        106.952
      ],
      [
        -6.698,
        106.956
      ],
      [
        -6.702,
        106.918
      ]
    ],
    "gridBounds": {
      "latMin": -6.718,
      "latMax": -6.652,
      "lngMin": 106.898,
      "lngMax": 106.978,
      "rows": 12,
      "cols": 14
    },
    "seed": 1
  },
  "DAS_02": {
    "dasId": "DAS_02",
    "dasName": "DAS_02 \u2014 Sub-DAS Keduang (Jawa Tengah)",
    "siteId": "SITE_02",
    "siteName": "SITE_02 \u2014 Site 02 - Ngadirojo Wonogiri",
    "prov": "Jawa Tengah",
    "center": [
      -7.805,
      111.045
    ],
    "zoom": 13,
    "dasAreaHa": 1820,
    "siteAreaHa": 410,
    "weeklyRain": [
      45,
      75,
      130,
      165,
      90,
      35,
      15
    ],
    "dasBoundary": [
      [
        -7.77,
        111.01
      ],
      [
        -7.768,
        111.075
      ],
      [
        -7.795,
        111.092
      ],
      [
        -7.838,
        111.08
      ],
      [
        -7.842,
        111.025
      ],
      [
        -7.81,
        111.002
      ]
    ],
    "siteBoundary": [
      [
        -7.788,
        111.03
      ],
      [
        -7.786,
        111.062
      ],
      [
        -7.818,
        111.066
      ],
      [
        -7.822,
        111.028
      ]
    ],
    "gridBounds": {
      "latMin": -7.838,
      "latMax": -7.772,
      "lngMin": 111.008,
      "lngMax": 111.088,
      "rows": 12,
      "cols": 14
    },
    "seed": 2
  },
  "DAS_03": {
    "dasId": "DAS_03",
    "dasName": "DAS_03 \u2014 DAS Gumbasa (Sulawesi Tengah)",
    "siteId": "SITE_03",
    "siteName": "SITE_03 \u2014 Site 03 - Gumbasa Hulu",
    "prov": "Sulawesi Tengah",
    "center": [
      -1.185,
      119.945
    ],
    "zoom": 13,
    "dasAreaHa": 2100,
    "siteAreaHa": 480,
    "weeklyRain": [
      60,
      95,
      145,
      180,
      120,
      55,
      40
    ],
    "dasBoundary": [
      [
        -1.15,
        119.91
      ],
      [
        -1.148,
        119.975
      ],
      [
        -1.175,
        119.992
      ],
      [
        -1.218,
        119.98
      ],
      [
        -1.222,
        119.925
      ],
      [
        -1.19,
        119.902
      ]
    ],
    "siteBoundary": [
      [
        -1.168,
        119.93
      ],
      [
        -1.166,
        119.962
      ],
      [
        -1.198,
        119.966
      ],
      [
        -1.202,
        119.928
      ]
    ],
    "gridBounds": {
      "latMin": -1.218,
      "latMax": -1.152,
      "lngMin": 119.908,
      "lngMax": 119.988,
      "rows": 12,
      "cols": 14
    },
    "seed": 3
  },
  "DAS_04": {
    "dasId": "DAS_04",
    "dasName": "DAS_04 \u2014 DAS Cisadane Hulu (Jawa Barat)",
    "siteId": "SITE_04",
    "siteName": "SITE_04 \u2014 Site 04 - Cianten Dramaga",
    "prov": "Jawa Barat",
    "center": [
      -6.642,
      106.685
    ],
    "zoom": 13,
    "dasAreaHa": 1640,
    "siteAreaHa": 350,
    "weeklyRain": [
      95,
      140,
      110,
      60,
      45,
      80,
      50
    ],
    "dasBoundary": [
      [
        -6.607,
        106.65
      ],
      [
        -6.605,
        106.715
      ],
      [
        -6.632,
        106.732
      ],
      [
        -6.675,
        106.72
      ],
      [
        -6.679,
        106.665
      ],
      [
        -6.647,
        106.642
      ]
    ],
    "siteBoundary": [
      [
        -6.625,
        106.67
      ],
      [
        -6.623,
        106.702
      ],
      [
        -6.655,
        106.706
      ],
      [
        -6.659,
        106.668
      ]
    ],
    "gridBounds": {
      "latMin": -6.675,
      "latMax": -6.609,
      "lngMin": 106.648,
      "lngMax": 106.728,
      "rows": 12,
      "cols": 14
    },
    "seed": 4
  },
  "DAS_05": {
    "dasId": "DAS_05",
    "dasName": "DAS_05 \u2014 DAS Citarum Hulu (Jawa Barat)",
    "siteId": "SITE_05",
    "siteName": "SITE_05 \u2014 Site 05 - Cisangkuy Pangalengan",
    "prov": "Jawa Barat",
    "center": [
      -7.165,
      107.562
    ],
    "zoom": 13,
    "dasAreaHa": 1950,
    "siteAreaHa": 440,
    "weeklyRain": [
      70,
      85,
      155,
      125,
      65,
      40,
      25
    ],
    "dasBoundary": [
      [
        -7.13,
        107.527
      ],
      [
        -7.128,
        107.592
      ],
      [
        -7.155,
        107.609
      ],
      [
        -7.198,
        107.597
      ],
      [
        -7.202,
        107.542
      ],
      [
        -7.17,
        107.519
      ]
    ],
    "siteBoundary": [
      [
        -7.148,
        107.547
      ],
      [
        -7.146,
        107.579
      ],
      [
        -7.178,
        107.583
      ],
      [
        -7.182,
        107.545
      ]
    ],
    "gridBounds": {
      "latMin": -7.198,
      "latMax": -7.132,
      "lngMin": 107.525,
      "lngMax": 107.605,
      "rows": 12,
      "cols": 14
    },
    "seed": 5
  },
  "DAS_06": {
    "dasId": "DAS_06",
    "dasName": "DAS_06 \u2014 DAS Serayu Hulu (Jawa Tengah)",
    "siteId": "SITE_06",
    "siteName": "SITE_06 \u2014 Site 06 - Merawu Banjarnegara",
    "prov": "Jawa Tengah",
    "center": [
      -7.285,
      109.715
    ],
    "zoom": 13,
    "dasAreaHa": 1730,
    "siteAreaHa": 390,
    "weeklyRain": [
      110,
      160,
      135,
      80,
      50,
      30,
      20
    ],
    "dasBoundary": [
      [
        -7.25,
        109.68
      ],
      [
        -7.248,
        109.745
      ],
      [
        -7.275,
        109.762
      ],
      [
        -7.318,
        109.75
      ],
      [
        -7.322,
        109.695
      ],
      [
        -7.29,
        109.672
      ]
    ],
    "siteBoundary": [
      [
        -7.268,
        109.7
      ],
      [
        -7.266,
        109.732
      ],
      [
        -7.298,
        109.736
      ],
      [
        -7.302,
        109.698
      ]
    ],
    "gridBounds": {
      "latMin": -7.318,
      "latMax": -7.252,
      "lngMin": 109.678,
      "lngMax": 109.758,
      "rows": 12,
      "cols": 14
    },
    "seed": 6
  },
  "DAS_07": {
    "dasId": "DAS_07",
    "dasName": "DAS_07 \u2014 DAS Brantas Hulu (Jawa Timur)",
    "siteId": "SITE_07",
    "siteName": "SITE_07 \u2014 Site 07 - Konto Pujon",
    "prov": "Jawa Timur",
    "center": [
      -7.845,
      112.465
    ],
    "zoom": 13,
    "dasAreaHa": 1580,
    "siteAreaHa": 340,
    "weeklyRain": [
      35,
      55,
      90,
      145,
      115,
      60,
      30
    ],
    "dasBoundary": [
      [
        -7.81,
        112.43
      ],
      [
        -7.808,
        112.495
      ],
      [
        -7.835,
        112.512
      ],
      [
        -7.878,
        112.5
      ],
      [
        -7.882,
        112.445
      ],
      [
        -7.85,
        112.422
      ]
    ],
    "siteBoundary": [
      [
        -7.828,
        112.45
      ],
      [
        -7.826,
        112.482
      ],
      [
        -7.858,
        112.486
      ],
      [
        -7.862,
        112.448
      ]
    ],
    "gridBounds": {
      "latMin": -7.878,
      "latMax": -7.812,
      "lngMin": 112.428,
      "lngMax": 112.508,
      "rows": 12,
      "cols": 14
    },
    "seed": 7
  },
  "DAS_08": {
    "dasId": "DAS_08",
    "dasName": "DAS_08 \u2014 DAS Batang Toru (Sumatera Utara)",
    "siteId": "SITE_08",
    "siteName": "SITE_08 \u2014 Site 08 - Pahae Tapanuli",
    "prov": "Sumatera Utara",
    "center": [
      1.835,
      99.045
    ],
    "zoom": 13,
    "dasAreaHa": 2250,
    "siteAreaHa": 520,
    "weeklyRain": [
      120,
      175,
      150,
      95,
      70,
      85,
      60
    ],
    "dasBoundary": [
      [
        1.87,
        99.01
      ],
      [
        1.872,
        99.075
      ],
      [
        1.845,
        99.092
      ],
      [
        1.802,
        99.08
      ],
      [
        1.798,
        99.025
      ],
      [
        1.83,
        99.002
      ]
    ],
    "siteBoundary": [
      [
        1.852,
        99.03
      ],
      [
        1.854,
        99.062
      ],
      [
        1.822,
        99.066
      ],
      [
        1.818,
        99.028
      ]
    ],
    "gridBounds": {
      "latMin": 1.802,
      "latMax": 1.868,
      "lngMin": 99.008,
      "lngMax": 99.088,
      "rows": 12,
      "cols": 14
    },
    "seed": 8
  },
  "DAS_09": {
    "dasId": "DAS_09",
    "dasName": "DAS_09 \u2014 DAS Asahan Hulu (Sumatera Utara)",
    "siteId": "SITE_09",
    "siteName": "SITE_09 \u2014 Site 09 - Tangga Parhitean",
    "prov": "Sumatera Utara",
    "center": [
      2.515,
      99.285
    ],
    "zoom": 13,
    "dasAreaHa": 2040,
    "siteAreaHa": 460,
    "weeklyRain": [
      80,
      105,
      130,
      110,
      75,
      50,
      40
    ],
    "dasBoundary": [
      [
        2.55,
        99.25
      ],
      [
        2.552,
        99.315
      ],
      [
        2.525,
        99.332
      ],
      [
        2.482,
        99.32
      ],
      [
        2.478,
        99.265
      ],
      [
        2.51,
        99.242
      ]
    ],
    "siteBoundary": [
      [
        2.532,
        99.27
      ],
      [
        2.534,
        99.302
      ],
      [
        2.502,
        99.306
      ],
      [
        2.498,
        99.268
      ]
    ],
    "gridBounds": {
      "latMin": 2.482,
      "latMax": 2.548,
      "lngMin": 99.248,
      "lngMax": 99.328,
      "rows": 12,
      "cols": 14
    },
    "seed": 9
  },
  "DAS_10": {
    "dasId": "DAS_10",
    "dasName": "DAS_10 \u2014 DAS Batanghari Hulu (Sumatera Barat)",
    "siteId": "SITE_10",
    "siteName": "SITE_10 \u2014 Site 10 - Sangir Solok Selatan",
    "prov": "Sumatera Barat",
    "center": [
      -1.485,
      101.245
    ],
    "zoom": 13,
    "dasAreaHa": 1890,
    "siteAreaHa": 430,
    "weeklyRain": [
      90,
      135,
      170,
      140,
      85,
      60,
      45
    ],
    "dasBoundary": [
      [
        -1.45,
        101.21
      ],
      [
        -1.448,
        101.275
      ],
      [
        -1.475,
        101.292
      ],
      [
        -1.518,
        101.28
      ],
      [
        -1.522,
        101.225
      ],
      [
        -1.49,
        101.202
      ]
    ],
    "siteBoundary": [
      [
        -1.468,
        101.23
      ],
      [
        -1.466,
        101.262
      ],
      [
        -1.498,
        101.266
      ],
      [
        -1.502,
        101.228
      ]
    ],
    "gridBounds": {
      "latMin": -1.518,
      "latMax": -1.452,
      "lngMin": 101.208,
      "lngMax": 101.288,
      "rows": 12,
      "cols": 14
    },
    "seed": 10
  },
  "DAS_11": {
    "dasId": "DAS_11",
    "dasName": "DAS_11 \u2014 DAS Musi Hulu (Bengkulu)",
    "siteId": "SITE_11",
    "siteName": "SITE_11 \u2014 Site 11 - Ketaun Lebong",
    "prov": "Bengkulu",
    "center": [
      -3.145,
      102.185
    ],
    "zoom": 13,
    "dasAreaHa": 1670,
    "siteAreaHa": 370,
    "weeklyRain": [
      65,
      90,
      120,
      155,
      105,
      70,
      35
    ],
    "dasBoundary": [
      [
        -3.11,
        102.15
      ],
      [
        -3.108,
        102.215
      ],
      [
        -3.135,
        102.232
      ],
      [
        -3.178,
        102.22
      ],
      [
        -3.182,
        102.165
      ],
      [
        -3.15,
        102.142
      ]
    ],
    "siteBoundary": [
      [
        -3.128,
        102.17
      ],
      [
        -3.126,
        102.202
      ],
      [
        -3.158,
        102.206
      ],
      [
        -3.162,
        102.168
      ]
    ],
    "gridBounds": {
      "latMin": -3.178,
      "latMax": -3.112,
      "lngMin": 102.148,
      "lngMax": 102.228,
      "rows": 12,
      "cols": 14
    },
    "seed": 11
  },
  "DAS_12": {
    "dasId": "DAS_12",
    "dasName": "DAS_12 \u2014 DAS Sekampung Hulu (Lampung)",
    "siteId": "SITE_12",
    "siteName": "SITE_12 \u2014 Site 12 - Way Besai Tanggamus",
    "prov": "Lampung",
    "center": [
      -5.125,
      104.585
    ],
    "zoom": 13,
    "dasAreaHa": 1520,
    "siteAreaHa": 310,
    "weeklyRain": [
      50,
      70,
      105,
      135,
      95,
      45,
      25
    ],
    "dasBoundary": [
      [
        -5.09,
        104.55
      ],
      [
        -5.088,
        104.615
      ],
      [
        -5.115,
        104.632
      ],
      [
        -5.158,
        104.62
      ],
      [
        -5.162,
        104.565
      ],
      [
        -5.13,
        104.542
      ]
    ],
    "siteBoundary": [
      [
        -5.108,
        104.57
      ],
      [
        -5.106,
        104.602
      ],
      [
        -5.138,
        104.606
      ],
      [
        -5.142,
        104.568
      ]
    ],
    "gridBounds": {
      "latMin": -5.158,
      "latMax": -5.092,
      "lngMin": 104.548,
      "lngMax": 104.628,
      "rows": 12,
      "cols": 14
    },
    "seed": 12
  },
  "DAS_13": {
    "dasId": "DAS_13",
    "dasName": "DAS_13 \u2014 DAS Kapuas Hulu (Kalimantan Barat)",
    "siteId": "SITE_13",
    "siteName": "SITE_13 \u2014 Site 13 - Melawi Sintang",
    "prov": "Kalimantan Barat",
    "center": [
      -0.385,
      111.845
    ],
    "zoom": 13,
    "dasAreaHa": 2400,
    "siteAreaHa": 550,
    "weeklyRain": [
      75,
      110,
      140,
      125,
      90,
      65,
      55
    ],
    "dasBoundary": [
      [
        -0.35,
        111.81
      ],
      [
        -0.348,
        111.875
      ],
      [
        -0.375,
        111.892
      ],
      [
        -0.418,
        111.88
      ],
      [
        -0.422,
        111.825
      ],
      [
        -0.39,
        111.802
      ]
    ],
    "siteBoundary": [
      [
        -0.368,
        111.83
      ],
      [
        -0.366,
        111.862
      ],
      [
        -0.398,
        111.866
      ],
      [
        -0.402,
        111.828
      ]
    ],
    "gridBounds": {
      "latMin": -0.418,
      "latMax": -0.352,
      "lngMin": 111.808,
      "lngMax": 111.888,
      "rows": 12,
      "cols": 14
    },
    "seed": 13
  },
  "DAS_14": {
    "dasId": "DAS_14",
    "dasName": "DAS_14 \u2014 DAS Mahakam Hulu (Kalimantan Utara)",
    "siteId": "SITE_14",
    "siteName": "SITE_14 \u2014 Site 14 - Kayan Malinau",
    "prov": "Kalimantan Utara",
    "center": [
      2.845,
      116.185
    ],
    "zoom": 13,
    "dasAreaHa": 2650,
    "siteAreaHa": 610,
    "weeklyRain": [
      85,
      125,
      165,
      145,
      100,
      80,
      60
    ],
    "dasBoundary": [
      [
        2.88,
        116.15
      ],
      [
        2.882,
        116.215
      ],
      [
        2.855,
        116.232
      ],
      [
        2.812,
        116.22
      ],
      [
        2.808,
        116.165
      ],
      [
        2.84,
        116.142
      ]
    ],
    "siteBoundary": [
      [
        2.862,
        116.17
      ],
      [
        2.864,
        116.202
      ],
      [
        2.832,
        116.206
      ],
      [
        2.828,
        116.168
      ]
    ],
    "gridBounds": {
      "latMin": 2.812,
      "latMax": 2.878,
      "lngMin": 116.148,
      "lngMax": 116.228,
      "rows": 12,
      "cols": 14
    },
    "seed": 14
  },
  "DAS_15": {
    "dasId": "DAS_15",
    "dasName": "DAS_15 \u2014 DAS Saddang Hulu (Sulawesi Selatan)",
    "siteId": "SITE_15",
    "siteName": "SITE_15 \u2014 Site 15 - Malea Tana Toraja",
    "prov": "Sulawesi Selatan",
    "center": [
      -3.165,
      119.865
    ],
    "zoom": 13,
    "dasAreaHa": 1980,
    "siteAreaHa": 450,
    "weeklyRain": [
      55,
      80,
      115,
      150,
      130,
      75,
      40
    ],
    "dasBoundary": [
      [
        -3.13,
        119.83
      ],
      [
        -3.128,
        119.895
      ],
      [
        -3.155,
        119.912
      ],
      [
        -3.198,
        119.9
      ],
      [
        -3.202,
        119.845
      ],
      [
        -3.17,
        119.822
      ]
    ],
    "siteBoundary": [
      [
        -3.148,
        119.85
      ],
      [
        -3.146,
        119.882
      ],
      [
        -3.178,
        119.886
      ],
      [
        -3.182,
        119.848
      ]
    ],
    "gridBounds": {
      "latMin": -3.198,
      "latMax": -3.132,
      "lngMin": 119.828,
      "lngMax": 119.908,
      "rows": 12,
      "cols": 14
    },
    "seed": 15
  }
}
FORECAST_DATES = [
  {
    "code": "H+1",
    "iso": "2026-10-17",
    "full": "Sabtu, 17 Okt 2026",
    "short": "17 Okt (Sab)"
  },
  {
    "code": "H+2",
    "iso": "2026-10-18",
    "full": "Minggu, 18 Okt 2026",
    "short": "18 Okt (Min)"
  },
  {
    "code": "H+3",
    "iso": "2026-10-19",
    "full": "Senin, 19 Okt 2026",
    "short": "19 Okt (Sen)"
  },
  {
    "code": "H+4",
    "iso": "2026-10-20",
    "full": "Selasa, 20 Okt 2026",
    "short": "20 Okt (Sel)"
  },
  {
    "code": "H+5",
    "iso": "2026-10-21",
    "full": "Rabu, 21 Okt 2026",
    "short": "21 Okt (Rab)"
  },
  {
    "code": "H+6",
    "iso": "2026-10-22",
    "full": "Kamis, 22 Okt 2026",
    "short": "22 Okt (Kam)"
  },
  {
    "code": "H+7",
    "iso": "2026-10-23",
    "full": "Jumat, 23 Okt 2026",
    "short": "23 Okt (Jum)"
  }
]

SITE_TO_DAS = {loc["siteId"]: loc["dasId"] for loc in LOCATIONS_DB.values()}

CLASSES_META = {
    1: {"name": "Sangat Rendah", "range": "1.00 - 1.80", "color": "#1a9641", "mitigasi": "Kondisi stabil. Pertahankan vegetasi alami."},
    2: {"name": "Rendah", "range": "1.81 - 2.60", "color": "#a6d96a", "mitigasi": "Inspeksi berkala saluran drainase lereng."},
    3: {"name": "Sedang", "range": "2.61 - 3.40", "color": "#ffffbf", "mitigasi": "Perkuat lereng dengan bio-engineering / tanaman berakar dalam."},
    4: {"name": "Tinggi", "range": "3.41 - 4.20", "color": "#fdae61", "mitigasi": "Pasang inclinometer/piezometer, buat sub-drainase & DPT."},
    5: {"name": "Sangat Tinggi", "range": "4.21 - 5.00", "color": "#d7191c", "mitigasi": "ZONA KRITIS! Batasi alat berat saat hujan lebat & aktifkan EWS."}
}

SLOPE_LABELS = {1: "0-8% (Datar)", 2: "8-15% (Landai)", 3: "15-25% (Agak Curam)", 4: "25-45% (Curam)", 5: ">45% (Sangat Curam)"}
GEO_LABELS = {1: "Aluvial Dataran", 2: "Sedimen Halus", 3: "Metamorf / Sedimen Miring", 4: "Vulkanik Tua Lapuk", 5: "Vulkanik Muda / Breksi / Sesar"}
SOIL_LABELS = {
    1: "DSMW: Je/Gh — Eutric Fluvisols / Gleysols (Aluvial - Skor 1)",
    2: "DSMW: Fo/Nd — Orthic Ferralsols / Nitosols (Latosol - Skor 2)",
    3: "DSMW: Bd/Lc — Dystric Cambisols / Luvisols (Mediteran - Skor 3)",
    4: "DSMW: Th/Ao — Humic Andosols / Orthic Acrisols (Andosol/Podsolik - Skor 4)",
    5: "DSMW: Re/I — Eutric Regosols / Lithosols (Regosol/Litosol - Skor 5)"
}
LC_LABELS = {
    1: "MapBiomas ID 3/5/76/33: Formasi Hutan / Mangrove / Tubuh Air (Skor 1)",
    2: "MapBiomas ID 9: 3.3. Kebun Kayu / Pulpwood Plantation (Skor 2)",
    3: "MapBiomas ID 13/35: 2.1. Tumbuhan Non-Hutan / 3.2. Sawit (Skor 3)",
    4: "MapBiomas ID 21/40/24: 3.4. Pertanian Lainnya / 3.1. Sawah / Permukiman (Skor 4)",
    5: "MapBiomas ID 25/30: 4.3. Non-Vegetasi Lainnya / 4.1. Lubang Tambang (Skor 5)"
}

# =====================================================================
# MODUL AUTO-CLIP & KONVERSI SKOR DSMW (.SHP SE-INDONESIA) & MAPBIOMAS (.TIF SE-INDONESIA)
# =====================================================================
DSMW_SOIL_SCORE_MAP = {
    # Skor 1 (Sangat Rendah): Fluvisols (J), Gleysols (G), Planosols (W), Water (WA)
    "J": 1, "JC": 1, "JD": 1, "JE": 1, "JT": 1,
    "G": 1, "GC": 1, "GD": 1, "GE": 1, "GH": 1, "GM": 1, "GP": 1, "GX": 1,
    "W": 1, "WD": 1, "WE": 1, "WH": 1, "WM": 1, "WS": 1, "WX": 1, "WA": 1, "GL": 1, "ST": 1,
    # Skor 2 (Rendah): Ferralsols (F - Latosol), Nitosols (N)
    "F": 2, "FA": 2, "FH": 2, "FO": 2, "FP": 2, "FR": 2, "FX": 2,
    "N": 2, "ND": 2, "NE": 2, "NH": 2,
    # Skor 3 (Sedang): Cambisols (B - Inceptisol), Luvisols (L - Mediteran), Phaeozems (H), Chernozems (C), Kastanozems (K), Greyzems (M)
    "B": 3, "BC": 3, "BD": 3, "BE": 3, "BF": 3, "BG": 3, "BH": 3, "BK": 3, "BV": 3, "BX": 3,
    "L": 3, "LA": 3, "LC": 3, "LF": 3, "LG": 3, "LK": 3, "LO": 3, "LP": 3, "LV": 3,
    "H": 3, "HC": 3, "HG": 3, "HH": 3, "HL": 3, "C": 3, "CG": 3, "CH": 3, "CK": 3, "CL": 3,
    "K": 3, "KH": 3, "KK": 3, "KL": 3, "M": 3, "MG": 3, "MO": 3,
    # Skor 4 (Tinggi): Acrisols (A - Podsolik), Andosols (T - Andosol), Podzols (P), Podzoluvisols (D), Vertisols (V - Grumosol), Solonetz (S), Solonchaks (Z)
    "A": 4, "AF": 4, "AG": 4, "AH": 4, "AO": 4, "AP": 4,
    "T": 4, "TH": 4, "TM": 4, "TO": 4, "TV": 4,
    "P": 4, "PF": 4, "PG": 4, "PH": 4, "PL": 4, "PO": 4, "PP": 4,
    "D": 4, "DD": 4, "DE": 4, "DG": 4,
    "V": 4, "VC": 4, "VP": 4, "S": 4, "SG": 4, "SM": 4, "SO": 4, "Z": 4, "ZG": 4, "ZM": 4, "ZO": 4, "ZT": 4,
    # Skor 5 (Sangat Tinggi): Regosols (R), Lithosols (I), Rendzinas (E), Histosols (O), Arenosols (Q), Rankers (U), Rock Debris (RK)
    "R": 5, "RC": 5, "RD": 5, "RE": 5, "RX": 5,
    "I": 5, "E": 5, "O": 5, "OD": 5, "OE": 5, "OX": 5,
    "Q": 5, "QA": 5, "QC": 5, "QF": 5, "QL": 5, "U": 5, "RK": 5, "DS": 5
}

MAPBIOMAS_CODE_SCORE_MAP = {
    1: 1,   # 1. Forest / Hutan
    3: 1,   # 1.1. Forest Formation / Formasi Hutan
    5: 1,   # 1.2. Mangrove
    76: 1,  # 1.3. Peat Swamp Forest / Hutan Rawa Gambut
    10: 3,  # 2. Non-Forest Natural Formation / Tumbuhan Non-Hutan
    13: 3,  # 2.1. Other Natural Vegetation / Tumbuhan Non-Hutan Lainnya
    18: 4,  # 3. Agriculture / Pertanian
    40: 4,  # 3.1. Rice Paddy / Sawah
    35: 3,  # 3.2. Oil Palm / Sawit
    9: 2,   # 3.3. Pulpwood Plantation / Kebun Kayu
    21: 4,  # 3.4. Other Agriculture / Pertanian Lainnya
    22: 5,  # 4. Non-Vegetated Area / Non Vegetasi
    30: 5,  # 4.1. Mining Pit / Lubang Tambang
    24: 4,  # 4.2. Urban Area / Permukiman
    25: 5,  # 4.3. Other Non-Vegetation / Non-Vegetasi Lainnya
    26: 1,  # 5. Water Body / Tubuh Air
    31: 1,  # 5.1. Aquaculture / Tambak
    33: 1,  # 5.2. River, Lake, Ocean / Sungai, Danau, Laut
    27: 3   # 6. Not Observed / Citra Tertutup Awan (Default Sedang)
}

def map_dsmw_code_to_score(code_str):
    """Mengubah kode DOMSOI / FAOSOIL pada DSMW .shp menjadi Skor Tanah (1-5)."""
    if not isinstance(code_str, str) or not code_str.strip():
        return 3
    clean = code_str.strip().split("-")[0].split()[0].upper()
    if clean in DSMW_SOIL_SCORE_MAP:
        return DSMW_SOIL_SCORE_MAP[clean]
    return DSMW_SOIL_SCORE_MAP.get(clean[:1], 3)

def reclassify_mapbiomas_array(pixel_array):
    """Mengubah array piksel Legend Code ID MapBiomas (.tif) menjadi Skor Tutupan Lahan (1-5) secara cepat."""
    lut = np.full(256, 3, dtype=np.uint8)
    for code_id, score_val in MAPBIOMAS_CODE_SCORE_MAP.items():
        if 0 <= code_id < 256:
            lut[code_id] = score_val
    clipped_idx = np.clip(pixel_array, 0, 255).astype(np.uint8)
    return lut[clipped_idx]


def point_in_poly(lat, lng, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        yi, xi = poly[i][0], poly[i][1]
        yj, xj = poly[j][0], poly[j][1]
        if ((yi > lat) != (yj > lat)) and (lng < (xj - xi) * (lat - yi) / (yj - yi + 1e-12) + xi):
            inside = not inside
        j = i
    return inside

def get_rainfall_score(rain_mm):
    if rain_mm <= 20: return 1, "Sangat Ringan (<=20 mm)"
    elif rain_mm <= 50: return 2, "Ringan (21-50 mm)"
    elif rain_mm <= 100: return 3, "Sedang (51-100 mm)"
    elif rain_mm <= 150: return 4, "Lebat (101-150 mm)"
    return 5, "Sangat Lebat (>150 mm)"

def get_class_id(score):
    if score <= 1.80: return 1
    elif score <= 2.60: return 2
    elif score <= 3.40: return 3
    elif score <= 4.20: return 4
    return 5

@st.cache_data
def generate_static_grid(das_key, site_key):
    das_obj = LOCATIONS_DB[das_key]
    site_parent = LOCATIONS_DB[SITE_TO_DAS[site_key]]
    b = das_obj["gridBounds"]
    rows, cols = b["rows"], b["cols"]
    lat_step = (b["latMax"] - b["latMin"]) / rows
    lng_step = (b["lngMax"] - b["lngMin"]) / cols
    seed = das_obj["seed"]
    cells = []

    for r in range(rows):
        for c in range(cols):
            lat1 = b["latMin"] + r * lat_step
            lat2 = lat1 + lat_step
            lng1 = b["lngMin"] + c * lng_step
            lng2 = lng1 + lng_step
            clat, clng = (lat1 + lat2) / 2.0, (lng1 + lng2) / 2.0

            if not point_in_poly(clat, clng, das_obj["dasBoundary"]):
                continue
            in_site = point_in_poly(clat, clng, site_parent["siteBoundary"])

            norm_r, norm_c = r / rows, c / cols
            wave = math.sin((r + seed) * 1.3) * math.cos((c + seed) * 1.1)

            slope_s = min(5, max(1, round(2.2 + norm_r * 2.5 + wave * 0.9)))
            geo_s = min(5, max(1, round(2.0 + norm_r * 2.3 + (0.6 if norm_c > 0.5 else -0.3))))
            soil_s = min(5, max(1, round(2.0 + norm_c * 2.2 + wave * 0.7)))
            base_lc_s = min(5, max(1, round((3.4 if in_site else 2.3) + wave * 1.1)))

            static_score = round(0.20 * slope_s + 0.20 * geo_s + 0.10 * soil_s, 2)
            cells.append({
                "lat1": lat1, "lat2": lat2, "lng1": lng1, "lng2": lng2,
                "center_lat": clat, "center_lng": clng,
                "in_site": in_site,
                "slope_score": slope_s, "geo_score": geo_s,
                "soil_score": soil_s, "base_lc_score": base_lc_s,
                "static_score": static_score
            })
    return pd.DataFrame(cells)

st.set_page_config(page_title="GeoSlide Cloud Monitor — 15 DAS & 15 Site", layout="wide")
st.title("⛰️ WebGIS Monitoring Potensi Longsor (15 DAS & 15 Lokasi Site)")
st.caption("Periode Prakiraan Hujan Mingguan: Sabtu, 17 Oktober 2026 s/d Jumat, 23 Oktober 2026 | Terhubung Cloud / Google Drive")

with st.sidebar:
    st.header("📍 1. Droplist Terpisah (15 DAS & 15 Site)")
    auto_sync = st.checkbox("Sinkronkan Otomatis DAS ↔ Site", value=True)

    das_key = st.selectbox(
        "Pilih Batas DAS / Catchment Area (15):",
        options=list(LOCATIONS_DB.keys()),
        format_func=lambda k: LOCATIONS_DB[k]["dasName"]
    )

    default_site_idx = list(LOCATIONS_DB.keys()).index(das_key) if auto_sync else 0
    site_options = [loc["siteId"] for loc in LOCATIONS_DB.values()]
    site_key = st.selectbox(
        "Pilih Lokasi Batas Site (15):",
        options=site_options,
        index=default_site_idx,
        format_func=lambda s: LOCATIONS_DB[SITE_TO_DAS[s]]["siteName"]
    )

    active_das = LOCATIONS_DB[das_key]
    active_site_parent = LOCATIONS_DB[SITE_TO_DAS[site_key]]

    st.divider()
    st.header("☁️ 2. Cloud / Google Drive Live Sync")
    gsheet_csv_url = st.text_input(
        "URL Google Sheets CSV (Publish to Web):",
        placeholder="https://docs.google.com/spreadsheets/d/.../pub?output=csv"
    )
    uploaded_excel = st.file_uploader("Atau Upload File Excel Lokal (.xlsx):", type=["xlsx"])

    weekly_rain = list(active_das["weeklyRain"])
    if gsheet_csv_url:
        try:
            df_cloud = pd.read_csv(gsheet_csv_url)
            sub = df_cloud[df_cloud["ID_DAS"] == das_key]["Curah_Hujan_mm"].dropna().tolist()
            if len(sub) >= 7:
                weekly_rain = [float(x) for x in sub[:7]]
                st.success("Tersinkronisasi real-time dari Google Sheets!")
        except Exception as e:
            st.warning(f"Gagal membaca URL Cloud: {e}")
    elif uploaded_excel is not None:
        df_up = pd.read_excel(uploaded_excel, sheet_name=0, skiprows=3)
        sub = df_up[df_up["ID_DAS"] == das_key]["Curah_Hujan_mm"].dropna().tolist()
        if len(sub) >= 7:
            weekly_rain = [float(x) for x in sub[:7]]
            st.success(f"Data 7 hari {das_key} berhasil dimuat!")

    st.divider()
    st.header("🗓️ 3. Pilih Tanggal Prakiraan (17–23 Okt 2026)")
    day_idx = st.selectbox(
        "Tanggal Prakiraan Hujan Harian:",
        options=list(range(7)),
        format_func=lambda i: f"{FORECAST_DATES[i]['code']} — {FORECAST_DATES[i]['full']} ({weekly_rain[i]} mm)"
    )
    rain_mm = st.slider("Curah Hujan Harian (mm/hari):", 0, 220, int(weekly_rain[day_idx]))
    rain_score, rain_label = get_rainfall_score(rain_mm)

    st.divider()
    st.header("🌳 4. Update Bulanan Tutupan Lahan")
    lc_delta = st.selectbox(
        "Kondisi Tutupan Lahan Bulanan/Triwulan:",
        options=[0, -1, 1, 2],
        format_func=lambda v: {
            0: "Baseline Eksisting Triwulan IV-2026",
            -1: "Rehabilitasi Vegetasi / Reboisasi (-1 Skor)",
            1: "Pembukaan Lahan Site Baru (+1 Skor)",
            2: "Lahan Terbuka Ekstrem (+2 Skor)"
        }[v]
    )

    st.divider()
    st.header("🔍 5. Cek Koordinat Titik Rawan")
    check_lat = st.number_input("Latitude:", value=float(active_das["center"][0]), format="%.4f", step=0.002)
    check_lng = st.number_input("Longitude:", value=float(active_das["center"][1]), format="%.4f", step=0.002)

df_grid = generate_static_grid(das_key, site_key).copy()
df_grid["eff_lc_score"] = df_grid["base_lc_score"].apply(lambda x: min(5, max(1, x + lc_delta)))
df_grid["total_score"] = (df_grid["static_score"] + 0.20 * df_grid["eff_lc_score"] + 0.30 * rain_score).round(2)
df_grid["class_id"] = df_grid["total_score"].apply(get_class_id)
df_grid["class_name"] = df_grid["class_id"].apply(lambda cid: CLASSES_META[cid]["name"])
df_grid["color"] = df_grid["class_id"].apply(lambda cid: CLASSES_META[cid]["color"])

cols_kpi = st.columns(5)
area_per_cell = active_das["dasAreaHa"] / len(df_grid)
for idx_c, cid in enumerate([1, 2, 3, 4, 5]):
    cnt = int((df_grid["class_id"] == cid).sum())
    pct = (cnt / len(df_grid)) * 100.0
    ha = round(cnt * area_per_cell)
    with cols_kpi[idx_c]:
        st.metric(f"Kelas {cid}: {CLASSES_META[cid]['name']}", f"{ha:,} Ha", f"{pct:.1f}% DAS")

col_map, col_info = st.columns([2.2, 1.0])
with col_map:
    st.subheader(f"🗺️ {active_das['dasName']} | {active_site_parent['siteName']}")
    st.caption(f"Tanggal Prakiraan Aktif: **{FORECAST_DATES[day_idx]['full']} ({FORECAST_DATES[day_idx]['code']})** — Curah Hujan: **{rain_mm} mm/hari** ({rain_label})")
    m = folium.Map(location=active_das["center"], zoom_start=13, tiles="Esri.WorldImagery")
    for _, row in df_grid.iterrows():
        folium.Rectangle(
            bounds=[[row["lat1"], row["lng1"]], [row["lat2"], row["lng2"]]],
            color="#ffffff" if row["in_site"] else "#1e293b",
            weight=0.8 if row["in_site"] else 0.3,
            fill=True, fill_color=row["color"], fill_opacity=0.70,
            tooltip=f"Kelas {row['class_id']}: {row['class_name']} (Skor: {row['total_score']:.2f})"
        ).add_to(m)
    folium.Polygon(active_das["dasBoundary"], color="#22d3ee", weight=2.5, dash_array="6, 6", fill=False, tooltip="Batas DAS").add_to(m)
    folium.Polygon(active_site_parent["siteBoundary"], color="#facc15", weight=3.2, fill=False, tooltip="Batas Lokasi Site").add_to(m)
    folium.Marker([check_lat, check_lng], tooltip="Titik Cek Koordinat").add_to(m)
    st_folium(m, width=850, height=520)

with col_info:
    st.subheader("🎯 Detail Titik Koordinat")
    df_grid["dist"] = ((df_grid["center_lat"] - check_lat)**2 + (df_grid["center_lng"] - check_lng)**2)**0.5
    nearest = df_grid.sort_values("dist").iloc[0]
    cid = int(nearest["class_id"])
    st.markdown(f"**Koordinat:** `{nearest['center_lat']:.4f}, {nearest['center_lng']:.4f}`")
    st.markdown(f"**Kelas:** **Kelas {cid} — {CLASSES_META[cid]['name']}** (`{nearest['total_score']:.2f} / 5.00`)")
    st.info(CLASSES_META[cid]["mitigasi"])
