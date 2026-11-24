import sqlite3
from tabulate import tabulate
from pyconcepticon import Concepticon
from ala.data import convert_data, load_data, concept2vec, feature2vec, get_db
from ala.utils import write_table, main
from collections import defaultdict
import umap
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


DATA = "Lexibank"
# DATA = "Grambank"

if DATA == "Lexibank":
    conceptlist = 'Starostin-1991-110'
    wl, families = load_data('lexibank', 1, False, conceptlist)
    lb_conv = concept2vec(get_db('data/lexibank.sqlite3'), conceptlist)
    data = convert_data(wl, families, lb_conv, load='lexical')

elif DATA == "Grambank":
    gb, families = load_data('grambank', 1, False)
    gb_conv = feature2vec(get_db('data/grambank.sqlite3'))
    data = convert_data(gb, families, gb_conv, load='grambank')


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

# Interactive plotly
import plotly.graph_objects as go

fig = go.Figure()

# One trace per family (so the legend works like seaborn's hue)
for fam in fam_order:
    mask = np.array([f == fam for f in families])
    fig.add_trace(go.Scatter(
        x=coords[mask, 0],
        y=coords[mask, 1],
        mode='markers',
        name=fam,
        marker=dict(
            size=14,
            line=dict(width=1, color='black'),
            opacity=0.8
        ),
        text=[g for g, m in zip(gcodes, mask) if m],
        customdata=[fam] * mask.sum(),
        hovertemplate=(
            '<b>%{text}</b><br>'
            'Family: %{customdata}<br>'
            '<extra></extra>'
        )
    ))

# Boxed labels for highlighted languages
for i, (gcode, fam) in enumerate(zip(gcodes, families)):
    if gcode in highlight:
        fig.add_annotation(
            x=coords[i, 0],
            y=coords[i, 1],
            text=gcode,
            showarrow=False,
            xshift=10,
            yshift=10,
            bgcolor='white',
            bordercolor='black',
            borderwidth=1,
            borderpad=3,
            font=dict(size=12)
        )

fig.update_layout(
    title=dict(
        text='UMAP (Jaccard distance) of Vectors',
        font=dict(size=18)
    ),
    xaxis=dict(visible=False),   # hides ticks, labels, grid, spines
    yaxis=dict(visible=False),
    legend=dict(
        title='Family',
        font=dict(size=12),
        itemsizing='constant'
    ),
    width=1200,
    height=800,
    hoverlabel=dict(font_size=13)
)

# Save as interactive HTML
file_path = DATA + ".html"
fig.write_html(file_path)
