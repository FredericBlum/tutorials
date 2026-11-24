import sqlite3
import csv
from tabulate import tabulate
from pyconcepticon import Concepticon
from collections import defaultdict
from lingpy import rc, tokens2class
import umap
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

conc = Concepticon('../data/concepticon/')
clist = conc.conceptlists['Bowern-2021-342b'].concepts
concept_list = [clist[item].concepticon_gloss for item in clist]

concepts = defaultdict(list)
for idx, gloss in enumerate(concept_list):
    concepts[gloss] = idx

# empty vector for 342 concepts (Bowern list)
sc_model = rc('dolgo')
sound_classes = [c for c in
                    sorted(set(sc_model.converter.values())) if c not
                    in "+_" + sc_model.vowels + sc_model.tones] + ["?"]
cls2idx = {c: i for i, c in enumerate(sound_classes)}

data = defaultdict(list)
with open('huntergatherer_sa.tsv', encoding='utf8') as f:
    tsv_reader = csv.reader(f, delimiter='\t')
    next(tsv_reader)
    for row in tsv_reader:
        lang = row[1]
        if lang not in data:
            nested_vector = [[len(sound_classes) * [0] for _ in range(2)] for c in range(342)]

            data[lang] = [row[2], nested_vector]
        class_string = tokens2class(row[4].split(' '), sc_model)
        reduced_string = [t for t in class_string if t in sound_classes][:2]
        # print(reduced_string)
        vector = [len(sound_classes) * [0] for _ in range(2)]

        idx = concepts[row[3]]
        for pos in range(2):
            cls = reduced_string[pos] if pos < len(reduced_string) else 'H'
            vector[pos][cls2idx[cls]] = 1

        data[lang][1][idx] = vector

# for lang in data:
#     print(lang, data[lang][0], data[lang][1])
#     print('---')

# Flatten vector for all languages
new_data = defaultdict(list)
for lang, (family, concept_vectors) in data.items():
    flat_vector = []
    for concept_vector in concept_vectors:
        for position_vector in concept_vector:
            flat_vector.extend(position_vector)
    new_data[lang] = [family, flat_vector]

reduced = defaultdict(list)
for lang in new_data:
    if new_data[lang][0] not in ['Quechuan', 'Aymaran', 'Chonan', 'Lengua-Mascoy', 'Guaicuruan', 'Mataguayan', 'Zamucoan', 'Uru-Chipaya', 'Barbacoan', 'Indo-European', 'Nambiquaran', 'Huarpean', 'Bororoan']:
        reduced[lang] = new_data[lang]


data = reduced
gcodes = list(data.keys())
families = ['Isolates' if v[0] == '' else v[0] for v in data.values()]

fam_order = sorted(set(families), key=lambda f: (f != 'Isolates', f))
feature_vectors = [v[1] for v in data.values()]

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

# # Boxed labels for highlighted languages
# for i, (gcode, fam) in enumerate(zip(gcodes, families)):
#     if gcode in highlight:
#         fig.add_annotation(
#             x=coords[i, 0],
#             y=coords[i, 1],
#             text=gcode,
#             showarrow=False,
#             xshift=10,
#             yshift=10,
#             bgcolor='white',
#             bordercolor='black',
#             borderwidth=1,
#             borderpad=3,
#             font=dict(size=12)
#         )

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
file_path = "huntergatherer_simarility.html"
fig.write_html(file_path)
