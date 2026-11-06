import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date
import html
import re
import unicodedata
# ==========================================
# CONFIGURACIÓN
# ==========================================
st.set_page_config(
   page_title="K Cine | Tu mundo de películas",
   page_icon="🎬",
   layout="wide",
   initial_sidebar_state="collapsed"
)
# ==========================================
# DIRECCIÓN EXACTA DE LA CARPETA MEDIA
# ==========================================
HOME = Path.home()
POSIBLES_RUTAS = [
   HOME / "Desktop" / "Peliculas" / "media",
   HOME / "Escritorio" / "Peliculas" / "media",
   HOME / "OneDrive" / "Desktop" / "Peliculas" / "media",
   HOME / "OneDrive" / "Escritorio" / "Peliculas" / "media",
]
MEDIA_DIR = next(
   (ruta for ruta in POSIBLES_RUTAS if ruta.exists()),
   HOME / "Desktop" / "Peliculas" / "media"
)
# Archivo CSV junto a app.py
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "peliculas.csv"
# ==========================================
# NORMALIZAR NOMBRES
# ==========================================
def normalizar(texto):
   texto = str(texto).strip().lower()
   texto = unicodedata.normalize("NFKD", texto)
   texto = "".join(
       c for c in texto
       if not unicodedata.combining(c)
   )
   return re.sub(r"[^a-z0-9]", "", texto)

# ==========================================
# NOMBRES DE LOS CARTELES
# ==========================================
IMAGENES_PELICULAS = {
   "clayface": "Clayface",
   "elpoderdelared": "ElPoderDeLaRed",
   "elshowdeterrorderocky": "ElShowDeTerrorDeRocky",
   "elsilenciodeloscorderos": "ElSilencioDeLosCorderos",
   "lavenganzadelcharronegro": "LaVenganzaDelCharroNegro",
   "laleyendadelcharro": "LaVenganzaDelCharroNegro",
   "streetfighter": "StreetFighter"
}
# ==========================================
# BUSCAR IMÁGENES
# ==========================================
def buscar_imagen_local(titulo):
   if not MEDIA_DIR.exists():
       return None
   nombre = normalizar(titulo)
   nombre_archivo = IMAGENES_PELICULAS.get(
       nombre,
       str(titulo)
   )
   nombre_archivo = normalizar(nombre_archivo)
   extensiones = [".jpg", ".jpeg", ".png", ".webp"]
   for archivo in MEDIA_DIR.iterdir():
       if (
           archivo.is_file()
           and normalizar(archivo.stem) == nombre_archivo
           and archivo.suffix.lower() in extensiones
       ):
           return str(archivo)
   return None

# ==========================================
# ESTILOS CSS
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');
:root {
   --gold: #d9a928;
   --gold-light: #f2cc55;
   --bg: #101012;
   --card: #202023;
   --text: #f5f5f5;
}
html, body, [class*="css"],
[data-testid="stAppViewContainer"] {
   font-family: 'Montserrat', sans-serif;
}
.stApp {
   background: var(--bg);
   color: var(--text);
}
[data-testid="stHeader"] {
   background: transparent;
}
.block-container {
   max-width: 1250px;
   padding-top: 1rem;
   padding-bottom: 2rem;
}
h1, h2, h3, p, label {
   color: var(--text);
}
.eyebrow {
   color: var(--gold);
   text-transform: uppercase;
   font-size: 11px;
   letter-spacing: 2px;
   font-weight: 700;
}
.hero {
   background:
       linear-gradient(100deg, rgba(21,21,23,.92), rgba(41,35,38,.88)),
       url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=1200&q=80');
   background-size: cover;
   background-position: center;
   padding: 50px 35px;
   border-left: 4px solid var(--gold);
   min-height: 320px;
   display: flex;
   flex-direction: column;
   justify-content: center;
   border-radius: 4px;
   box-shadow: 0 10px 30px rgba(0,0,0,.5);
}
.hero h1 {
   font-size: clamp(28px, 4vw, 45px);
   font-weight: 800;
   line-height: 1.2;
   margin: 15px 0;
}
.hero p {
   color: #e0dcdf;
   max-width: 520px;
   line-height: 1.8;
}
.movie-card {
   background: var(--card);
   border-bottom: 2px solid var(--gold);
   padding: 14px;
   margin-bottom: 12px;
   min-height: 160px;
   border-radius: 4px;
   box-shadow: 0 4px 15px rgba(0,0,0,.3);
}
.movie-card h3 {
   font-size: 16px;
   margin: 12px 0 8px;
   font-weight: 700;
}
.movie-card p {
   color: #bdbbc0;
   font-size: 12px;
   line-height: 1.6;
}
.movie-meta {
   color: var(--gold-light);
   font-size: 10px;
   font-weight: 700;
   text-transform: uppercase;
   letter-spacing: .5px;
}
.legal-box {
   max-width: 800px;
   margin: 10px auto;
   background: #202023;
   border-top: 2px solid var(--gold);
   padding: 30px;
   border-radius: 4px;
}
.footer {
   text-align: center;
   color: #aaa;
   background: #151517;
   padding: 22px;
   margin-top: 30px;
   font-size: 11px;
}
div[data-testid="stButton"] button,
div[data-testid="stLinkButton"] a {
   background: var(--gold);
   color: #111;
   border: 1px solid var(--gold);
   border-radius: 2px;
   font-weight: 700;
}
div[data-testid="stButton"] button:hover,
div[data-testid="stLinkButton"] a:hover {
   background: var(--gold-light);
   color: #111;
}
div[data-testid="stRadio"] label {
   color: var(--gold-light);
}
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
   background: #222225;
}
hr {
   border-color: #333;
}
@media (max-width: 700px) {
   .hero {
       padding: 25px 20px;
   }
   .legal-box {
       padding: 20px;
   }
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# BASE DE DATOS DE EJEMPLO
# ==========================================
ejemplo = pd.DataFrame([
   {
       "titulo": "Clayface",
       "sinopsis": "Una historia oscura de misterio, sombras y transformación.",
       "genero": "Terror",
       "anio": 2026,
       "fecha_estreno": "2026-10-23",
       "imagen": "",
       "trailer": "https://www.youtube.com/results?search_query=Clayface+trailer"
   },
   {
       "titulo": "El poder de la red",
       "sinopsis": "Un thriller cibernético sobre secretos y conexiones digitales.",
       "genero": "Suspenso",
       "anio": 2026,
       "fecha_estreno": "2026-12-10",
       "imagen": "",
       "trailer": "https://www.youtube.com/results?search_query=El+poder+de+la+red"
   },
   {
       "titulo": "El show de terror de Rocky",
       "sinopsis": "Una película musical de culto llena de humor y fantasía.",
       "genero": "Musical",
       "anio": 1975,
       "fecha_estreno": "",
       "imagen": "",
       "trailer": "https://www.youtube.com/results?search_query=Rocky+Horror+Picture+Show"
   },
   {
       "titulo": "El silencio de los corderos",
       "sinopsis": "Una agente del FBI investiga un caso de misterio y suspenso.",
       "genero": "Suspenso",
       "anio": 1991,
       "fecha_estreno": "",
       "imagen": "",
       "trailer": "https://www.youtube.com/results?search_query=Silence+of+the+Lambs"
   },
   {
       "titulo": "La venganza del Charro Negro",
       "sinopsis": "Una aventura animada inspirada en las leyendas mexicanas.",
       "genero": "Animación",
       "anio": 2026,
       "fecha_estreno": "",
       "imagen": "",
       "trailer": "https://www.youtube.com/results?search_query=Charro+Negro"
   },
   {
       "titulo": "Street Fighter",
       "sinopsis": "Una historia de acción inspirada en el famoso universo de videojuegos.",
       "genero": "Acción",
       "anio": 2026,
       "fecha_estreno": "2026-10-16",
       "imagen": "",
       "trailer": "https://www.youtube.com/results?search_query=Street+Fighter+trailer"
   }
])

# ==========================================
# COLUMNAS DEL CSV
# ==========================================
ALIASES = {
   "titulo": ["titulo", "title", "pelicula", "nombre", "movie"],
   "sinopsis": ["sinopsis", "descripcion", "description", "resumen"],
   "genero": ["genero", "genre", "categoria", "category"],
   "anio": ["anio", "ano", "year", "año", "estreno"],
   "fecha_estreno": ["fechaestreno", "fecha", "releasedate"],
   "imagen": ["imagen", "image", "poster", "urlimagen", "portada"],
   "trailer": ["trailer", "urltrailer", "enlace", "link"]
}

# ==========================================
# CARGAR DATOS
# ==========================================
def cargar_datos():
   if not CSV_PATH.exists():
       return ejemplo.copy(), True
   try:
       df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
       columnas = {}
       for columna in df.columns:
           clave = normalizar(columna)
           for destino, opciones in ALIASES.items():
               if clave in [normalizar(x) for x in opciones]:
                   columnas[columna] = destino
                   break
       df = df.rename(columns=columnas)
       if "titulo" not in df.columns:
           st.error("El CSV necesita una columna de título.")
           return ejemplo.copy(), True
       defaults = {
           "sinopsis": "Sinopsis no disponible.",
           "genero": "Sin clasificar",
           "anio": 0,
           "fecha_estreno": "",
           "imagen": "",
           "trailer": ""
       }
       for columna, valor in defaults.items():
           if columna not in df.columns:
               df[columna] = valor
       df = df.fillna("")
       for columna in [
           "titulo", "sinopsis", "genero",
           "imagen", "trailer", "fecha_estreno"
       ]:
           df[columna] = df[columna].astype(str)
       return df, False
   except Exception as error:
       st.error(f"Error al leer peliculas.csv: {error}")
       return ejemplo.copy(), True

df, usando_ejemplo = cargar_datos()

# ==========================================
# AVISOS DE CARPETAS
# ==========================================
if not MEDIA_DIR.exists():
   st.error(
       f"No se encontró la carpeta de imágenes: {MEDIA_DIR}"
   )
else:
   st.caption(
       f"📁 Carteles cargados desde: {MEDIA_DIR}"
   )
if usando_ejemplo:
   st.caption("🎬 Estás viendo el catálogo de ejemplo.")

# ==========================================
# FUNCIONES GENERALES
# ==========================================
def texto_seguro(valor):
   return html.escape(str(valor))

def imagen_valida(titulo, url=""):
   local = buscar_imagen_local(titulo)
   if local:
       return local
   url = str(url).strip()
   if url.startswith(("https://", "http://")):
       return url
   return (
       "https://images.unsplash.com/"
       "photo-1485846234645-a62644f84728"
       "?auto=format&fit=crop&w=600&q=80"
   )

# ==========================================
# MOSTRAR TARJETAS
# ==========================================
def mostrar_tarjeta(pelicula):
   titulo = texto_seguro(pelicula["titulo"])
   sinopsis = texto_seguro(pelicula["sinopsis"])
   genero = texto_seguro(pelicula["genero"])
   anio = texto_seguro(pelicula["anio"])
   trailer = str(pelicula["trailer"]).strip()
   imagen = imagen_valida(
       pelicula["titulo"],
       pelicula["imagen"]
   )
   st.image(
       imagen,
       use_container_width=True
   )
   st.markdown(f"""
<div class="movie-card">
<div class="movie-meta">{genero} · {anio}</div>
<h3>{titulo}</h3>
<p>{sinopsis}</p>
</div>
   """, unsafe_allow_html=True)
   if trailer.startswith(("https://", "http://")):
       st.link_button(
           "Ver tráiler ↗",
           trailer,
           use_container_width=True
       )
   else:
       st.caption("Tráiler próximamente")

# ==========================================
# MOSTRAR PELÍCULAS
# ==========================================
def mostrar_peliculas(datos, columnas=3):
   if datos.empty:
st.info("No se encontraron películas.")
       return
   for inicio in range(0, len(datos), columnas):
       grupo = datos.iloc[inicio:inicio + columnas]
       cols = st.columns(columnas)
       for col, (_, pelicula) in zip(cols, grupo.iterrows()):
           with col:
               mostrar_tarjeta(pelicula)

# ==========================================
# PIE DE PÁGINA
# ==========================================
def pie_pagina():
   st.markdown("""
<div class="footer">
       Una conversación para después de la función.
<br><br>
       K CINE · Proyecto escolar
<br>
       Las fechas, imágenes y descripciones deben verificarse antes de publicar.
</div>
   """, unsafe_allow_html=True)

# ==========================================
# NAVEGACIÓN
# ==========================================
st.markdown("""
<div style="
   display:flex;
   align-items:center;
   gap:12px;
   padding:10px 0 20px;
   border-bottom:1px solid #333;
">
<div style="
       background:#080808;
       border:1px solid #d9a928;
       padding:8px 15px;
       color:#d9a928;
       font-size:23px;
       font-weight:800;
   ">
       K
</div>
<div>
<div style="font-weight:800;letter-spacing:2px;">
           K CINE
</div>
<div style="color:#aaa;font-size:10px;">
           TU MUNDO DE PELÍCULAS
</div>
</div>
</div>
""", unsafe_allow_html=True)

if "pagina" not in st.session_state:
   st.session_state["pagina"] = "Inicio"

pagina = st.radio(
   "Navegación principal",
   ["Inicio", "Películas", "Próximos estrenos"],
   horizontal=True,
   label_visibility="collapsed",
   key="navegacion"
)
st.markdown("---")

# ==========================================
# INICIO
# ==========================================
if pagina == "Inicio":
   izquierda, derecha = st.columns(
       [1.1, 0.9],
       gap="large"
   )
   with izquierda:
       st.markdown("""
<div class="hero">
<div class="eyebrow">
               Tu próxima película empieza aquí
</div>
<h1>
               El cine se disfruta.<br>
               Las opiniones se comparten.
</h1>
<p>
               Explora películas de ayer y de hoy,
               descubre lo que viene y encuentra
               tu próxima historia favorita.
</p>
</div>
       """, unsafe_allow_html=True)
       if st.button("Explorar películas →"):
           st.session_state["navegacion"] = "Películas"
           st.rerun()
   with derecha:
       if not df.empty:
           destacada = df.iloc[0]
           st.markdown(
               '<div class="eyebrow">En foco · Cartelera</div>',
               unsafe_allow_html=True
           )
           st.image(
               imagen_valida(
                   destacada["titulo"],
                   destacada["imagen"]
               ),
               use_container_width=True
           )
           st.markdown(
               f"### {texto_seguro(destacada['titulo'])}"
           )
           st.caption(destacada["sinopsis"])
           enlace = str(destacada["trailer"]).strip()
           if enlace.startswith(("https://", "http://")):
               st.link_button("Ver tráiler ↗", enlace)
   st.markdown("---")
   st.markdown("### Lo que viene")
   st.write("Descubre algunas de las películas de nuestro catálogo.")
   mostrar_peliculas(df.head(3), columnas=3)

# ==========================================
# CATÁLOGO DE PELÍCULAS
# ==========================================
elif pagina == "Películas":
   st.markdown(
       '<div class="eyebrow">Descubre qué ver</div>',
       unsafe_allow_html=True
   )
   st.title("Películas")
   st.write("Encuentra tu próxima historia favorita.")
   busqueda = st.text_input(
       "Buscar película",
       placeholder="Título, descripción o palabra clave..."
   )
   c1, c2, c3 = st.columns([1, 1, 0.65])
   anios = sorted(
       {
           str(x) for x in df["anio"]
           if str(x).strip() not in ("", "0", "0.0")
       },
       reverse=True
   )
   generos = sorted(
       {
           str(x) for x in df["genero"]
           if str(x).strip()
       }
   )
   with c1:
       anio_seleccionado = st.selectbox(
           "Año de la película",
           ["Todos"] + anios
       )
   with c2:
       genero_seleccionado = st.selectbox(
           "Género",
           ["Todos"] + generos
       )
   with c3:
       st.write("")
       st.write("")
       limpiar = st.button("Limpiar filtros")
   if limpiar:
       st.rerun()
   filtradas = df.copy()
   if busqueda.strip():
       patron = re.escape(busqueda.strip())
       mascara = (
           filtradas["titulo"].str.contains(
               patron, case=False, na=False
           )
           |
           filtradas["sinopsis"].str.contains(
               patron, case=False, na=False
           )
       )
       filtradas = filtradas[mascara]
   if anio_seleccionado != "Todos":
       filtradas = filtradas[
           filtradas["anio"].astype(str) == anio_seleccionado
       ]
   if genero_seleccionado != "Todos":
       filtradas = filtradas[
           filtradas["genero"] == genero_seleccionado
       ]
   st.caption(
       f"{len(filtradas)} película(s) encontrada(s)"
   )
   mostrar_peliculas(filtradas, columnas=3)
   with st.expander("Consultar datos en tabla"):
       st.dataframe(
           filtradas[
               ["titulo", "genero", "anio", "sinopsis"]
           ],
           use_container_width=True,
           hide_index=True
       )

# ==========================================
# PRÓXIMOS ESTRENOS
# ==========================================
elif pagina == "Próximos estrenos":
   st.markdown(
       '<div class="eyebrow">Lo que viene</div>',
       unsafe_allow_html=True
   )
   st.title("Próximos estrenos")
   st.write(
       "Consulta las fechas registradas en la base de datos."
   )
   fechas = pd.to_datetime(
       df["fecha_estreno"],
       errors="coerce"
   ).dt.date
   proximos = df[
       fechas.notna() & (fechas >= date.today())
   ].copy()
   proximos["fecha_orden"] = pd.to_datetime(
       proximos["fecha_estreno"],
       errors="coerce"
   )
   proximos = proximos.sort_values("fecha_orden")
   if proximos.empty:
st.info(
           "No hay próximos estrenos con fechas futuras registradas."
       )
   else:
       for inicio in range(0, len(proximos), 3):
           grupo = proximos.iloc[inicio:inicio + 3]
           cols = st.columns(3)
           for col, (_, pelicula) in zip(cols, grupo.iterrows()):
               with col:
                   mostrar_tarjeta(pelicula)
                   fecha = pd.to_datetime(
                       pelicula["fecha_estreno"],
                       errors="coerce"
                   )
                   if pd.notna(fecha):
                       st.markdown(
                           f"**Estreno:** {fecha.strftime('%d/%m/%Y')}"
                       )

# ==========================================
# INFORMACIÓN LEGAL
# ==========================================
st.markdown("---")
st.markdown("### Información")
legal = st.selectbox(
   "Consulta las secciones legales",
   [
       "Selecciona una sección",
       "Derechos de autor",
       "Aviso de privacidad",
       "Términos y condiciones"
   ]
)
if legal == "Derechos de autor":
   st.markdown("""
<div class="legal-box">
<h3>Derechos de autor</h3>
<p>
       Este sitio es un proyecto escolar con fines educativos.
       Los nombres, imágenes, carteles y materiales audiovisuales
       pertenecen a sus respectivos titulares. Se deben respetar
       sus derechos de autor y las condiciones de uso de cada recurso.
</p>
</div>
   """, unsafe_allow_html=True)
elif legal == "Aviso de privacidad":
   st.markdown("""
<div class="legal-box">
<h3>Aviso de privacidad</h3>
<p>
       Esta aplicación muestra información sobre películas.
       No solicita datos personales ni necesita una cuenta
       para consultar el catálogo. Si en el futuro se recopila
       información, se deberá informar qué datos se obtienen
       y cómo se utilizan.
</p>
</div>
   """, unsafe_allow_html=True)
elif legal == "Términos y condiciones":
   st.markdown("""
<div class="legal-box">
<h3>Términos y condiciones</h3>
<p>
       La información del catálogo se ofrece con fines informativos.
       Las fechas, sinopsis y enlaces deben comprobarse antes de su
       publicación. Los enlaces externos llevan a sitios de terceros,
       que tienen sus propias condiciones de uso.
</p>
</div>
   """, unsafe_allow_html=True)

# ==========================================
# FINAL
# ==========================================
pie_pagina()