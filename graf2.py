import pandas as pd
import dash
import dash_html_components as html
import dash_cytoscape as cyto
from ast import literal_eval

cyto.load_extra_layouts()

# === Загрузка CSV ===
df = pd.read_csv("hierarchy.csv")

# === Построение графа ===
df['Node'] = df['Parent'].astype(str)
df['Target'] = df['Child'].astype(str)

# Уникальные узлы
all_nodes = pd.unique(df[['Node', 'Target']].values.ravel('K'))

# Создание узлов
nodes = [{"data": {"id": n, "label": n}} for n in all_nodes]

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
                        "background-color": "#ffffff",
                        "border-color": "#000000",
                        "border-width": 2,
                        "label": "data(label)",
                        "color": "#000000",
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
