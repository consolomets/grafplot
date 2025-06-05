import pandas as pd
import dash_cytoscape as cyto
from dash import Dash, html
import hashlib

cyto.load_extra_layouts()

# === Загрузка CSV ===
df = pd.read_csv("hierarchy.csv")

DEFAULT_BG = "#ffffff"
DEFAULT_FONT = "#000000"

def clean_color(val, default):
    if pd.isna(val):
        return default
    s = str(val).strip()
    if s.startswith('#') and len(s) in (4, 7):
        return s
    return default

# === Разделяем строки с рёбрами и "висячими" узлами ===
edge_df = df.dropna(subset=['Parent', 'Child'])
dangling_df = df[pd.isna(df['Parent']) & pd.notna(df['Child'])]

# === Собираем все уникальные узлы ===
all_nodes = pd.unique(edge_df[['Parent', 'Child']].values.ravel('K')).tolist()
all_nodes += list(dangling_df['Child'].unique())
all_nodes = pd.unique(all_nodes)

# === Стили узлов ===
node_styles = {n: {"font_color": DEFAULT_FONT, "background_color": DEFAULT_BG} for n in all_nodes}

# Назначаем цвета дочерним узлам
for _, row in df.iterrows():
    child = row.get('Child')
    if pd.notna(child):
        child = str(child)
        bg = clean_color(row.get('BackgroundColorChild'), DEFAULT_BG)
        font = clean_color(row.get('FontColorChild'), DEFAULT_FONT)
        node_styles[child] = {"font_color": font, "background_color": bg}

# === Генерация классов ===
def make_class_from_color(bg, font):
    return f"c-{hashlib.md5((bg+font).encode()).hexdigest()[:6]}"

nodes = []
classes_styles = {}

for node, style in node_styles.items():
    cls = make_class_from_color(style["background_color"], style["font_color"])
    classes_styles[cls] = {
        "background-color": style["background_color"],
        "color": style["font_color"]
    }
    nodes.append({
        "data": {"id": node, "label": node},
        "classes": cls
    })

edges = [{"data": {"source": row['Parent'], "target": row['Child']}} for _, row in edge_df.iterrows()]

# === Стили Cytoscape ===
stylesheet = [
    {
        "selector": "node",
        "style": {
            "shape": "rectangle",
            "border-color": "#000000",
            "border-width": 2,
            "label": "data(label)",
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

# Добавим стили для цветных классов
for cls, style in classes_styles.items():
    stylesheet.append({
        "selector": f".{cls}",
        "style": style
    })

# === Dash-приложение ===
app = Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape',
        elements=nodes + edges,
        layout={'name': 'dagre', 'rankDir': 'LR'},
        style={'height': '95vh', 'width': '100%'},
        stylesheet=stylesheet
    )
])

if __name__ == '__main__':
    app.run(debug=True)
