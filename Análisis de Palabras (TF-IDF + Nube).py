
# vectorizer = TfidfVectorizer(stop_words='spanish', max_features=100)  esta vaina no funciona con español  -.- la conahsdhkasdkhakdj !"#!"#  xDDDDDDDDDDDDDDDDDDDD

import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
from wordcloud import WordCloud # type: ignore
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

# ----------------- Lista de stopwords en español -----------------
spanish_stopwords = [
    'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'se', 'del', 'las',
    'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como',
    'más', 'pero', 'sus', 'le', 'ya', 'o', 'este', 'sí', 'porque',
    'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre', 'también', 'me',
    'hasta', 'hay', 'donde', 'quien', 'desde', 'todo', 'nos', 'durante'
]

# ----------------- Selección de archivo -----------------
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    title="Selecciona el archivo de respuestas (.csv)",
    filetypes=[("CSV files", "*.csv")]
)

if not file_path:
    print("No se seleccionó ningún archivo. Saliendo...")
    exit()

# ----------------- Leer archivo -----------------
try:
    df = pd.read_csv(file_path)
except Exception as e:
    print(f"Error al leer el archivo: {e}")
    exit()

# ----------------- Combinar respuestas -----------------
textos = df.iloc[:, 2:].astype(str).apply(lambda x: ' '.join(x), axis=1)

# ----------------- Limpiar texto -----------------
def limpiar(texto):
    texto = texto.lower()
    texto = re.sub(r'[^a-záéíóúüñ ]', '', texto)
    return texto

textos_limpios = textos.apply(limpiar)

# ----------------- Calcular TF-IDF -----------------
vectorizer = TfidfVectorizer(stop_words=spanish_stopwords, max_features=100)
tfidf_matrix = vectorizer.fit_transform(textos_limpios)

# ----------------- Extraer palabras e importancias -----------------
palabras = vectorizer.get_feature_names_out()
importancias = tfidf_matrix.sum(axis=0).A1
df_importancia = pd.DataFrame({'Palabra': palabras, 'Importancia': importancias})
df_importancia = df_importancia.sort_values(by='Importancia', ascending=False)

# Guardar como CSV
df_importancia.to_csv('palabras_relevantes.csv', index=False)

# ----------------- Nube de palabras -----------------
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white'
).generate_from_frequencies(dict(zip(palabras, importancias)))

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Nube de Palabras Relevantes")
plt.savefig("nube_palabras.png")
plt.show()

