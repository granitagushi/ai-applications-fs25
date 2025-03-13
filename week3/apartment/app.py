import gradio as gr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Dummy-Funktion zur Vorhersage des Apartmentpreises
def predict_apartment(rooms, area, town):
    # Basispreis und inkrementelle Berechnungen
    base_price = 1000
    price = base_price + rooms * 200 + area * 10
    # Standortfaktor (Beispielwerte, können angepasst werden)
    location_factor = {"Zürich": 1.5, "Kloten": 1.2, "Uster": 1.3, "Illnau-Effretikon": 1.1}
    factor = location_factor.get(town, 1.0)
    return price * factor

# Funktion zur Erstellung eines Plots, der den Einfluss eines Features zeigt
def visualize_influence(feature='area', fixed_rooms=3, fixed_town='Zürich'):
    if feature == 'area':
        x_values = np.linspace(30, 150, 50)  # Beispielbereich für Wohnfläche in qm
    elif feature == 'rooms':
        x_values = np.arange(1, 6)           # Beispielbereich für Zimmeranzahl
    else:
        return "Feature not supported"
    
    predictions = []
    for x in x_values:
        if feature == 'area':
            price = predict_apartment(fixed_rooms, x, fixed_town)
        elif feature == 'rooms':
            price = predict_apartment(x, 100, fixed_town)  # Feste Wohnfläche von 100 qm
        predictions.append(price)
    
    # Erstelle den Plot
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x_values, predictions, marker='o')
    ax.set_xlabel('Wohnfläche (qm)' if feature == 'area' else 'Zimmeranzahl')
    ax.set_ylabel('Vorhergesagter Preis')
    ax.set_title(f'Einfluss von {"Wohnfläche" if feature=="area" else "Zimmeranzahl"} auf den Preis')
    ax.grid(True)
    fig.tight_layout()
    return fig

# Wrapper-Funktion für Gradio, die die Visualisierung zurückgibt
def gradio_visualization(feature, fixed_rooms, fixed_town):
    return visualize_influence(feature, fixed_rooms, fixed_town)

# Gradio-Interface für die Apartment-Preisvorhersage
preis_interface = gr.Interface(
    fn=predict_apartment,
    inputs=[
        gr.Number(label="Zimmeranzahl", value=3),
        gr.Number(label="Wohnfläche (qm)", value=100),
        gr.Dropdown(choices=["Zürich", "Kloten", "Uster", "Illnau-Effretikon"], label="Ort", value="Zürich")
    ],
    outputs=gr.Number(label="Vorhergesagter Preis"),
    title="Apartment Preisvorhersage",
    description="Gib die Anzahl der Zimmer, die Wohnfläche und den Ort ein, um den Apartmentpreis vorherzusagen."
)

# Gradio-Interface für die Visualisierung der Einflussfaktoren
visual_interface = gr.Interface(
    fn=gradio_visualization,
    inputs=[
        gr.Dropdown(choices=["area", "rooms"], label="Feature auswählen", value="area"),
        gr.Number(label="Zimmeranzahl (fest)", value=3),
        gr.Dropdown(choices=["Zürich", "Kloten", "Uster", "Illnau-Effretikon"], label="Ort (fest)", value="Zürich")
    ],
    outputs=gr.Plot(label="Einflussfaktoren-Visualisierung"),
    title="Einflussfaktoren-Visualisierung",
    description="Visualisiere, wie sich Wohnfläche oder Zimmeranzahl auf den vorhergesagten Preis auswirken."
)

# Beide Interfaces in einem TabbedInterface zusammenführen
tabs = gr.TabbedInterface([preis_interface, visual_interface], ["Preisvorhersage", "Visualisierung"])

if __name__ == "__main__":
    tabs.launch()
