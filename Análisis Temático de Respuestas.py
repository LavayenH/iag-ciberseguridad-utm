import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import re

# ----------------- Selección de archivo -----------------
root = tk.Tk()
root.withdraw()  # Oculta la ventana principal
file_path = filedialog.askopenfilename(
    title="Selecciona el archivo de respuestas (.csv)",
    filetypes=[("CSV files", "*.csv")]
)

if not file_path:
    print("No se seleccionó ningún archivo. Saliendo...")
    exit()

# ----------------- Lectura del CSV -----------------
df = pd.read_csv(file_path)
textos = df.iloc[:, 2:].astype(str).apply(lambda x: ' '.join(x), axis=1)

# ----------------- Categorías definidas -----------------
categorias = {
    'Percepción de Inteligencia Artificial': ['ia', 'inteligencia artificial', 'generativa'],
    'Riesgos de Ciberseguridad': ['riesgo', 'ciberseguridad', 'amenaza', 'phishing'],
    'Desafíos Técnicos': ['deepfake', 'detección', 'automatización', 'técnico', 'algoritmo'],
    'Estrategias': ['estrategia', 'capacitación', 'mitigación', 'prevención', 'simulación']
}

conteo_categorias = {cat: 0 for cat in categorias}
citas_relevantes = {cat: [] for cat in categorias}

# ----------------- Clasificación -----------------
for respuesta in textos:
    for cat, keywords in categorias.items():
        if any(re.search(rf'\b{k}\b', respuesta.lower()) for k in keywords):
            conteo_categorias[cat] += 1
            if len(citas_relevantes[cat]) < 5:
                citas_relevantes[cat].append(respuesta[:300] + '...')

# ----------------- Mostrar resultados -----------------
print("Conteo por categoría:")
for cat, count in conteo_categorias.items():
    print(f"{cat}: {count}")

# ----------------- Guardar citas relevantes -----------------
with open('citas_relevantes.txt', 'w', encoding='utf-8') as f:
    for cat, citas in citas_relevantes.items():
        f.write(f"\n{cat.upper()}\n")
        for cita in citas:
            f.write(f"- {cita}\n")

# ----------------- Gráfico -----------------
plt.bar(conteo_categorias.keys(), conteo_categorias.values())
plt.title("Frecuencia de Categorías")
plt.ylabel("Número de menciones")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("grafico_categorias.png")
plt.show()
