import csv
import sqlite3
import json
import numpy as np
import umap
from ala.data import convert_data, load_data, concept2vec, get_db
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from collections import defaultdict

query = """
SELECT
    l.cldf_glottocode,
    l.cldf_name,
    l.family,
    l.cldf_latitude,
    l.cldf_longitude
FROM
    languagetable AS l
WHERE
    l.cldf_macroarea = 'South America'
;
"""

# Load coordinates
db = sqlite3.connect('data/lexibank.sqlite3').cursor()
db.execute(query)
table = db.fetchall()
languages = defaultdict(list)

for item in table:
    languages[item[0]] = [item[3], item[4]]


# Load data
DATA = "Lexibank"
conceptlist = 'Starostin-1991-110'
wl, families = load_data('lexibank', 1, False, conceptlist)
lb_conv = concept2vec(get_db('data/lexibank.sqlite3'), conceptlist)
data = convert_data(wl, families, lb_conv, load='lexical')



# Structure of loaded data:
# 'hwan1238': ['Koreanic', 89, [vector] }
reduced = defaultdict(list)
for lang in data:
    if data[lang][0] not in ['Quechuan', 'Aymaran', 'Chonan', 'Lengua-Mascoy', 'Guaicuruan', 'Mataguayan', 'Zamucoan', 'Uru-Chipaya', 'Barbacoan', 'Indo-European', 'Nambiquaran', 'Huarpean', 'Bororoan']:
        reduced[lang] = data[lang]

highlight = ['paez1247', 'amar1274', 'cand1248', 'urar1246', 'puin1248']

data = reduced
gcodes = list(data.keys())
families = ['Isolates' if v[0] == 'Unclassified' else v[0] for v in data.values()]
fam_order = sorted(set(families), key=lambda f: (f != 'Isolates', f))

feature_vectors = [v[2] for v in data.values()]

# Convert to numpy array
X = np.array(feature_vectors)

coords = umap.UMAP(
    n_components=2,
    metric='jaccard',
    random_state=42,
    n_neighbors=50, #50 for LB, 80 for GB
    min_dist=0.2,
    compatibility_layout=False, 
    init="recursive",
    optimizer="adam"
).fit_transform(X)

######################################################
# Build consistent family -> color mapping (shared by both subplots)
palette = px.colors.qualitative.Plotly
fam_colors = {fam: palette[i % len(palette)] for i, fam in enumerate(fam_order)}

# Map gcode -> umap coords (for JS lookups later)
gcode_to_umap = {g: [float(coords[i, 0]), float(coords[i, 1])] for i, g in enumerate(gcodes)}

print("Creating visualization...")
fig = make_subplots(
    rows=1, cols=2,
    column_widths=[0.5, 0.5],
    specs=[[{'type': 'scatter'}, {'type': 'map'}]],
    subplot_titles=('UMAP (Jaccard distance)', 'South America Map')
)

# ---------------- UMAP traces (one per family) ----------------
for fam in fam_order:
    mask = np.array([f == fam for f in families])
    fam_gcodes = [g for g, m in zip(gcodes, mask) if m]
    is_hl = [g in highlight for g in fam_gcodes]

    fig.add_trace(
        go.Scatter(
            x=coords[mask, 0],
            y=coords[mask, 1],
            mode='markers',
            name=fam,
            legendgroup=fam,
            marker=dict(
                size=14,
                color=fam_colors[fam],
                line=dict(width=1, color='black'),
                opacity=0.8
            ),
            text=fam_gcodes,
            customdata=[fam] * len(fam_gcodes),
            hovertemplate=(
                '<b>%{text}</b><br>'
                'Family: %{customdata}<br>'
                '<extra></extra>'
            ),
            showlegend=True
        ),
        row=1, col=1
    )

# ---------------- Map traces (one per family) ----------------
for fam in fam_order:
    fam_gcodes, lats, lons, is_hl = [], [], [], []
    for g, f in zip(gcodes, families):
        if f == fam and g in languages:
            lat, lon = languages[g]
            fam_gcodes.append(g)
            lats.append(lat)
            lons.append(lon)
            is_hl.append(g in highlight)

    if not fam_gcodes:
        continue

    fig.add_trace(
        go.Scattermap(
            lat=lats,
            lon=lons,
            mode='markers',
            marker=dict(
                size=12,
                color=fam_colors[fam]
            ),
            text=fam_gcodes,
            customdata=[fam] * len(fam_gcodes),
            hovertemplate=(
                '<b>%{text}</b><br>'
                'Family: %{customdata}<br>'
                '<extra></extra>'
            ),
            legendgroup=fam,
            name=fam,
            showlegend=False
        ),
        row=1, col=2
    )

# ---------------- Hidden "highlight" traces (shared across subplots) ----------------
highlight_umap_idx = len(fig.data)
fig.add_trace(
    go.Scatter(
        x=[], y=[],
        mode='markers',
        marker=dict(size=22, color='rgba(0,0,0,0)', line=dict(width=4, color='crimson')),
        hoverinfo='skip',
        showlegend=False,
        name='highlight'
    ),
    row=1, col=1
)

highlight_map_idx = len(fig.data)
fig.add_trace(
    go.Scattermap(
        lat=[], lon=[],
        mode='markers',
        marker=dict(size=20, color='crimson', opacity=0.6),
        hoverinfo='skip',
        showlegend=False,
        name='highlight'
    ),
    row=1, col=2
)

# ---------------- Layout ----------------
esri_physical_style = {
    "version": 8,
    "sources": {
        "esri-physical": {
            "type": "raster",
            "tiles": [
                "https://server.arcgisonline.com/ArcGIS/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}"
            ],
            "tileSize": 256,
            "attribution": "Tiles © Esri — Source: US National Park Service"
        }
    },
    "layers": [
        {
            "id": "esri-physical-layer",
            "type": "raster",
            "source": "esri-physical",
            "minzoom": 0,
            "maxzoom": 19
        }
    ]
}


fig.update_layout(
    map=dict(
        style=esri_physical_style,#"open-street-map",
        center=dict(lat=-15, lon=-60),
        zoom=2.5,
        bearing=0,
        pitch=0
    ),
    title=dict(
        text='Language Distribution and UMAP Projection',
        font=dict(size=18)
    ),
    legend=dict(
        title='Family',
        font=dict(size=12),
        itemsizing='constant'
    ),
    width=1600,
    height=800,
    hoverlabel=dict(font_size=13)
)
fig.update_xaxes(visible=False, row=1, col=1)
fig.update_yaxes(visible=False, row=1, col=1)

# ---------------- JS for cross-subplot hover highlighting ----------------
# build gcode -> [umap_x, umap_y, lat, lon] lookup for JS
gcode_lookup = {}
for g in gcodes:
    ux, uy = gcode_to_umap.get(g, [None, None])
    if g in languages:
        lat, lon = languages[g]
    else:
        lat, lon = None, None
    gcode_lookup[g] = [ux, uy, lat, lon]

div_id = "lang-dist-plot"
post_js = f"""
var gd = document.getElementById('{div_id}');
var gcodeData = {json.dumps(gcode_lookup)};
var HL_UMAP = {highlight_umap_idx};
var HL_MAP = {highlight_map_idx};

gd.on('plotly_hover', function(ev) {{
    var pt = ev.points && ev.points[0];
    if (!pt || !pt.text) return;
    var d = gcodeData[pt.text];
    if (!d) return;

    if (d[0] !== null && d[1] !== null) {{
        Plotly.restyle(gd, {{x: [[d[0]]], y: [[d[1]]]}}, [HL_UMAP]);
    }}
    if (d[2] !== null && d[3] !== null) {{
        Plotly.restyle(gd, {{lat: [[d[2]]], lon: [[d[3]]]}}, [HL_MAP]);
    }}
}});

gd.on('plotly_unhover', function(ev) {{
    Plotly.restyle(gd, {{x: [[]], y: [[]]}}, [HL_UMAP]);
    Plotly.restyle(gd, {{lat: [[]], lon: [[]]}}, [HL_MAP]);
}});
"""

fig.write_html('new_map.html', div_id=div_id, post_script=post_js)
print("Done!")
