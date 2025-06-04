import pandas as pd
import dash
import dash_html_components as html
import dash_cytoscape as cyto
from ast import literal_eval

cyto.load_extra_layouts()

# === Загрузка CSV ===
df = pd.read_csv("hierarchy.csv")

# Use default colors if the CSV does not provide them
DEFAULT_BG = "#ffffff"
DEFAULT_FONT = "#000000"

# Ensure optional columns exist
if 'BackgroundColor' not in df.columns:
    df['BackgroundColor'] = DEFAULT_BG
if 'FontColor' not in df.columns:
    df['FontColor'] = DEFAULT_FONT

# === Построение графа ===
df['Node'] = df['Parent'].astype(str)
df['Target'] = df['Child'].astype(str)


# Уникальные узлы с учетом стилей
all_nodes = pd.unique(df[['Node', 'Target']].values.ravel('K'))
node_styles = {n: {"font_color": DEFAULT_FONT, "background_color": DEFAULT_BG}
               for n in all_nodes}

# Apply colors from CSV (assumed to describe the child node)
for _, row in df.iterrows():
    child = str(row['Child'])
    node_styles[child] = {
        "font_color": row.get('FontColor', DEFAULT_FONT),
        "background_color": row.get('BackgroundColor', DEFAULT_BG)
    }

# Создание узлов с учетом цветов
nodes = [
    {
        "data": {
            "id": n,
            "label": n,
            "font_color": style["font_color"],
            "background_color": style["background_color"],
        }
    }
    for n, style in node_styles.items()
]

# Создание рёбер
edges = [{"data": {"source": row['Parent'], "target": row['Child']}} for _, row in df.iterrows()]

# === Dash App ===
app = dash.Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape',
        elements=nodes + edges,
        layout={
            'name': 'dagre',
            'rankDir': 'LR'  # Right-to-left
        },
        style={'height': '95vh', 'width': '100%'},
            stylesheet = [
                {
                    "selector": "node",
                    "style": {
                        "shape": "rectangle",
                        "background-color": "data(background_color)",
                        "border-color": "#000000",
                        "border-width": 2,
                        "label": "data(label)",
                        "color": "data(font_color)",
                        "font-size": "12px",
                        "text-valign": "center",
                        "text-halign": "center",
                        "width": "label",
                        "height": "label",
                        "padding": "5px"
                    }
                },
                {
                    "selector": "edge",
                    "style": {
                        "width": 2,
                        "line-color": "#aaaaaa",
                        "target-arrow-shape": "triangle",
                        "target-arrow-color": "#aaaaaa",
                        "arrow-scale": 1
                    }
                }
            ]
    )
])

if __name__ == '__main__':
    app.run(debug=True)
