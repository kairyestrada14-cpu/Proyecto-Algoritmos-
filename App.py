import streamlit as st
import pandas as pd
from pathlib import Path
import altair as alt

# ==========================================
# 1. CONFIGURACIÓN GENERAL
# ==========================================

st.set_page_config(
    page_title="Gestión Comercial",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. DISEÑO Y COLORES
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --azul-fondo:     #0D1270;
        --azul-medio:     #1C238F;
        --azul-acento:    #3B49E0;
        --azul-hover:     #2A32B5;
        --azul-claro:     #5C6BFF;
        --turquesa:       #0FB5A6;
        --fondo-app:      #F4F6FB;
        --blanco:         #FFFFFF;
        --borde-suave:    #E2E6F5;
        --texto:          #2B2F45;
        --texto-suave:    #5A6078;
        --menu-texto:     #AEB4E8;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont,
                     'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        color: var(--texto);
    }

    /* ===== BASE ===== */
    .stApp { background-color: var(--fondo-app); }
    .block-container {
        padding-top: 2.5rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    /* ===== BARRA SUPERIOR: ocultar Deploy/menú ===== */
    header[data-testid="stHeader"] { background: transparent; }
    [data-testid="stAppDeployButton"] { display: none !important; }
    [data-testid="stDeployButton"]    { display: none !important; }
    .stDeployButton                   { display: none !important; }
    [data-testid="stToolbarActions"]  { display: none !important; }
    #MainMenu                         { visibility: hidden !important; }
    footer                            { visibility: hidden !important; }

    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: var(--fondo-app); }
    ::-webkit-scrollbar-thumb { background: #C2C8E8; border-radius: 8px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--azul-acento); }

    /* ======================================================
       SIDEBAR (menú estilo dashboard, SIN iconos)
    ====================================================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A0E52 0%, #141A86 100%);
        min-width: 280px !important;
        width: 280px !important;
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    [data-testid="stSidebar"] * { color: #FFFFFF; }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1.6rem; }

    /* Cabecera de marca */
    .menu-brand {
        padding: 0 0.3rem 1.1rem 0.3rem;
        margin-bottom: 0.4rem;
        border-bottom: 1px solid rgba(255,255,255,0.12);
    }
    .menu-brand .brand-title {
        font-size: 21px;
        font-weight: 800;
        letter-spacing: -0.4px;
        color: #FFFFFF;
        line-height: 1.2;
    }
    .menu-brand .brand-sub {
        font-size: 12px;
        color: var(--menu-texto);
        margin-top: 3px;
    }

    /* Etiqueta de sección */
    .menu-label {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.6px;
        color: rgba(255,255,255,0.40);
        margin: 1rem 0.4rem 0.5rem 0.4rem;
    }

    /* Separación entre items */
    [data-testid="stSidebar"] div.stButton { margin-bottom: 5px; }

    /* Items del menú */
    [data-testid="stSidebar"] div.stButton > button {
        background-color: transparent;
        color: var(--menu-texto);
        border: none;
        border-radius: 10px;
        font-weight: 600;
        font-size: 15px;
        text-align: left;
        justify-content: flex-start;
        padding: 0.7rem 1rem;
        width: 100%;
        transition: all 0.18s ease-in-out;
    }
    [data-testid="stSidebar"] div.stButton > button p {
        text-align: left;
        width: 100%;
        margin: 0;
    }
    [data-testid="stSidebar"] div.stButton > button:hover {
        background-color: rgba(255,255,255,0.08);
        color: #FFFFFF;
        transform: translateX(2px);
    }
    /* Item activo */
    [data-testid="stSidebar"] div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, rgba(92,107,255,0.32) 0%, rgba(92,107,255,0.10) 100%);
        color: #FFFFFF;
        box-shadow: inset 3px 0 0 0 #7A84FF;
    }

    /* Pie del menú */
    .menu-footer {
        margin-top: 1.3rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255,255,255,0.12);
        font-size: 12px;
        color: rgba(255,255,255,0.55);
        text-align: center;
    }

    /* Ocultar aviso "Press Enter" */
    [data-testid="InputInstructions"]      { display: none !important; }
    [data-testid="stWidgetInstructions"]   { display: none !important; }

    /* ======================================================
       TÍTULOS Y TEXTO
    ====================================================== */
    .main-title {
        color: var(--azul-fondo);
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 0;
        letter-spacing: -0.5px;
    }
    .subtitle {
        color: var(--texto-suave);
        font-size: 15px;
        margin-top: 5px;
        margin-bottom: 25px;
    }
    h1 { color: var(--azul-fondo); font-weight: 800; }
    h2, h3 { color: var(--azul-medio); font-weight: 700; }
    p, span, label, li { color: var(--texto); }
    a { color: var(--azul-acento); }

    /* ===== TARJETAS DE MÉTRICAS ===== */
    [data-testid="stMetric"] {
        background-color: var(--blanco);
        border: 1px solid var(--borde-suave);
        border-left: 4px solid var(--azul-acento);
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 4px 14px rgba(13, 18, 112, 0.07);
        transition: all 0.2s ease-in-out;
    }
    [data-testid="stMetric"]:hover {
        box-shadow: 0 6px 20px rgba(13, 18, 112, 0.12);
        transform: translateY(-2px);
    }
    [data-testid="stMetricLabel"] { color: var(--texto-suave); font-weight: 600; }
    [data-testid="stMetricValue"] { color: var(--azul-fondo); font-weight: 700; }
    [data-testid="stMetricDelta"] svg { stroke: var(--turquesa); }

    /* ===== BOTONES (área principal) ===== */
    .block-container div.stButton > button {
        background-color: var(--azul-acento);
        color: #FFFFFF;
        border-radius: 10px;
        border: 1px solid var(--azul-acento);
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease-in-out;
    }
    .block-container div.stButton > button:hover {
        background-color: var(--azul-hover);
        border-color: var(--azul-hover);
    }

    /* ===== FORMULARIOS Y CAMPOS ===== */
    div[data-testid="stForm"] {
        background-color: var(--blanco);
        border: 1px solid var(--borde-suave);
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 14px rgba(13, 18, 112, 0.05);
    }
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stDateInput"] input,
    [data-testid="stTextArea"] textarea {
        background-color: #FFFFFF !important;
        color: var(--texto) !important;
        border: 1px solid var(--borde-suave) !important;
        border-radius: 8px !important;
    }
    [data-baseweb="input"],
    [data-baseweb="base-input"] { background-color: #FFFFFF !important; }
    [data-testid="stNumberInput"] button {
        background-color: #F0F2FA !important;
        color: var(--azul-fondo) !important;
    }
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: var(--texto) !important;
        border: 1px solid var(--borde-suave) !important;
        border-radius: 8px !important;
    }
    input::placeholder, textarea::placeholder { color: #9AA0B5 !important; }
    [data-testid="stTextInput"] input:focus,
    [data-testid="stNumberInput"] input:focus,
    [data-testid="stDateInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {
        border-color: var(--azul-acento) !important;
        box-shadow: 0 0 0 2px rgba(59, 73, 224, 0.15) !important;
    }

    /* ===== BOTÓN DEL FORMULARIO ===== */
    div[data-testid="stFormSubmitButton"] > button {
        background-color: var(--azul-acento) !important;
        color: #FFFFFF !important;
        border: 1px solid var(--azul-acento) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease-in-out !important;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: var(--azul-hover) !important;
        border-color: var(--azul-hover) !important;
    }

    /* ===== PESTAÑAS / EXPANDER / TABLAS / ALERTAS ===== */
    [data-testid="stTabs"] button { font-weight: 600; color: var(--texto-suave); }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: var(--azul-acento);
        border-bottom-color: var(--azul-acento);
    }
    [data-testid="stExpander"] {
        border: 1px solid var(--borde-suave);
        border-radius: 12px;
        background-color: var(--blanco);
    }
    [data-testid="stDataFrame"] {
        border: 1px solid var(--borde-suave);
        border-radius: 12px;
    }
    [data-testid="stNotification"], .stAlert { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. CARPETA, ARCHIVOS CSV Y UTILIDADES
# ==========================================

CARPETA_DATOS = Path("datos")
CARPETA_DATOS.mkdir(exist_ok=True)

# Valores que se consideran "producto activo"
VALORES_ACTIVOS = {"true", "1", "si", "sí", "activo"}

# Formato de fecha para mostrar en pantalla: 27 / 10 / 2026
FORMATO_FECHA = "%d / %m / %Y"

COLUMNAS = {
    "productos": [
        "codigo", "nombre", "categoria", "precio",
        "cantidad", "stock_minimo", "activo"
    ],
    "ventas": [
        "numero_venta", "fecha", "subtotal", "iva", "total"
    ],
    "detalle_ventas": [
        "numero_venta", "codigo_producto", "nombre_producto",
        "cantidad", "precio_unitario", "subtotal"
    ],
    "movimientos": [
        "fecha", "codigo_producto", "tipo_movimiento",
        "cantidad", "descripcion"
    ]
}

ARCHIVOS = {
    nombre: CARPETA_DATOS / f"{nombre}.csv"
    for nombre in COLUMNAS
}


def inicializar_archivos():
    for nombre, ruta in ARCHIVOS.items():
        if not ruta.exists():
            pd.DataFrame(columns=COLUMNAS[nombre]).to_csv(
                ruta, index=False, encoding="utf-8-sig"
            )


def leer_datos(nombre):
    return pd.read_csv(
        ARCHIVOS[nombre],
        dtype={"codigo": str, "codigo_producto": str},
        keep_default_na=False
    )


def guardar_datos(nombre, datos):
    datos.to_csv(ARCHIVOS[nombre], index=False, encoding="utf-8-sig")


def es_activo(serie):
    """Máscara booleana de los productos marcados como activos."""
    return serie.astype(str).str.lower().isin(VALORES_ACTIVOS)


def formatear_fechas(serie):
    """Convierte una columna de fechas a texto '27 / 10 / 2026'."""
    return pd.to_datetime(serie, errors="coerce").dt.strftime(FORMATO_FECHA)


def ahora_texto():
    """Marca de tiempo actual para guardar en los CSV."""
    return pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")


inicializar_archivos()

# ==========================================
# 4. LEER INFORMACIÓN PARA EL INICIO
# ==========================================

productos = leer_datos("productos")
ventas = leer_datos("ventas")
detalles = leer_datos("detalle_ventas")
movimientos = leer_datos("movimientos")

for columna in ["precio", "cantidad", "stock_minimo"]:
    if columna in productos.columns:
        productos[columna] = pd.to_numeric(
            productos[columna], errors="coerce"
        ).fillna(0)

for columna in ["subtotal", "iva", "total"]:
    if columna in ventas.columns:
        ventas[columna] = pd.to_numeric(
            ventas[columna], errors="coerce"
        ).fillna(0)

activos = productos[es_activo(productos["activo"])]

stock_bajo = activos[activos["cantidad"] <= activos["stock_minimo"]]

ingresos = ventas["total"].sum()

# ==========================================
# 5. MENÚ LATERAL
# ==========================================

with st.sidebar:
    st.markdown(
        '<div class="menu-brand">'
        '<div class="brand-title">Gestión Comercial</div>'
        '<div class="brand-sub">Panel administrativo </div>'
        '</div>',
        unsafe_allow_html=True
    )

    if "modulo_actual" not in st.session_state:
        st.session_state.modulo_actual = "Inicio"

    st.markdown('<div class="menu-label">MENÚ</div>', unsafe_allow_html=True)

    opciones = [
        "Inicio",
        "Gestión de productos",
        "Registro de ventas",
        "Control de inventarios",
        "Reportes y estadísticas",
    ]

    for nombre in opciones:
        seleccionado = st.session_state.modulo_actual == nombre
        if st.button(
            nombre,
            key=f"menu_{nombre}",
            use_container_width=True,
            type="primary" if seleccionado else "secondary"
        ):
            st.session_state.modulo_actual = nombre
            st.rerun()

    modulo = st.session_state.modulo_actual

    st.markdown(
        '<div class="menu-footer">Sistema de Gestión Comercial </div>',
        unsafe_allow_html=True
    )


# ==========================================
# 6. PÁGINA DE INICIO
# ==========================================

if modulo == "Inicio":

    st.markdown(
        '<p class="main-title">¡Bienvenido!</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="subtitle">'
        'Aquí tienes el resumen general de tu gestión comercial.'
        '</p>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label="📦 Productos activos", value=len(activos))
    with c2:
        st.metric(label="🛋 Ventas registradas", value=len(ventas))
    with c3:
        st.metric(label="💰 Ingresos totales", value=f"Q{ingresos:,.2f}")
    with c4:
        st.metric(label="⚠️ Productos con stock bajo", value=len(stock_bajo))

    st.write("")

    izquierda, derecha = st.columns([2, 1])

    with izquierda:
        st.subheader("📈 Ingresos por fecha")

        if not ventas.empty and "fecha" in ventas.columns:
            grafica = ventas.copy()
            grafica["fecha"] = pd.to_datetime(grafica["fecha"], errors="coerce")
            grafica = grafica.dropna(subset=["fecha"])

            if not grafica.empty:
                resumen_inicio = (
                    grafica.assign(
                        dia=grafica["fecha"].dt.strftime(FORMATO_FECHA)
                    )
                    .groupby("dia", as_index=False)["total"]
                    .sum()
                    .rename(columns={"total": "Ingresos"})
                )

                base_inicio = alt.Chart(resumen_inicio).encode(
                    x=alt.X(
                        "dia:N", title="Fecha",
                        axis=alt.Axis(labelAngle=0, labelColor="#5A6078",
                                      titleColor="#1C238F")
                    ),
                    y=alt.Y(
                        "Ingresos:Q", title="Ingresos (Q)",
                        axis=alt.Axis(labelColor="#5A6078", titleColor="#1C238F")
                    ),
                    tooltip=[
                        alt.Tooltip("dia:N", title="Fecha"),
                        alt.Tooltip("Ingresos:Q", title="Ingresos", format=",.2f")
                    ]
                )
                barras_inicio = base_inicio.mark_bar(
                    cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=52,
                    color=alt.Gradient(
                        gradient="linear",
                        stops=[
                            alt.GradientStop(color="#6B78F0", offset=0),
                            alt.GradientStop(color="#3B49E0", offset=1),
                        ],
                        x1=1, x2=1, y1=0, y2=1,
                    ),
                )
                etiquetas_inicio = base_inicio.mark_text(
                    dy=-8, color="#1C238F", fontWeight="bold", fontSize=12
                ).encode(text=alt.Text("Ingresos:Q", format=",.0f"))

                st.altair_chart(
                    (barras_inicio + etiquetas_inicio).properties(height=320),
                    use_container_width=True
                )
            else:
                st.info("Todavía no hay fechas válidas para graficar.")
        else:
            st.info("La gráfica aparecerá cuando registres tus primeras ventas.")

    with derecha:
        st.subheader("🔔 Alertas de inventario")

        if stock_bajo.empty:
            st.success("No hay productos con stock bajo.")
        else:
            st.warning(f"Hay {len(stock_bajo)} productos que necesitan revisión.")
            st.dataframe(
                stock_bajo[["codigo", "nombre", "cantidad", "stock_minimo"]],
                hide_index=True,
                use_container_width=True
            )

    st.write("")
    st.subheader("📋 Últimos productos registrados")

    if productos.empty:
        st.info(
            "Todavía no hay productos registrados. "
            "Ingresa a Gestión de productos para comenzar."
        )
    else:
        st.dataframe(
            productos.tail(5).iloc[::-1],
            hide_index=True,
            use_container_width=True
        )

# ==========================================
# 7. MÓDULO: GESTIÓN DE PRODUCTOS
# ==========================================

elif modulo == "Gestión de productos":
    st.markdown(
        '<p class="main-title">📦 Gestión de productos</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="subtitle">'
        'Administra el catálogo de productos de tu empresa.'
        '</p>',
        unsafe_allow_html=True
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "➕ Registrar",
        "🔎 Consultar",
        "✏️ Modificar",
        "🚫 Desactivar"
    ])

    # ----- PESTAÑA 1: REGISTRAR -----
    with tab1:
        st.subheader("Registrar nuevo producto")
        st.caption("Completa los datos del producto. Los campos marcados son obligatorios.")

        with st.form("form_registrar_producto"):
            col_a, col_b = st.columns(2)

            with col_a:
                codigo = st.text_input(
                    "Código del producto *", placeholder="Ej: P-001"
                ).strip()
                nombre = st.text_input(
                    "Nombre del producto *", placeholder="Ej: Camiseta algodón"
                )
                categoria = st.text_input(
                    "Categoría *", placeholder="Ej: Ropa"
                )

            with col_b:
                precio = st.number_input(
                    "Precio de venta (Q)",
                    min_value=0.01, value=1.00, step=0.50
                )
                cantidad = st.number_input(
                    "Cantidad de productos",
                    min_value=0, value=0, step=1
                )
                stock_minimo = st.number_input(
                    "Stock mínimo",
                    min_value=0, value=5, step=1,
                    help="Cantidad a partir de la cual se mostrará una alerta de stock bajo."
                )

            st.write("")
            guardar = st.form_submit_button(
                "Guardar producto", use_container_width=True
            )

        if guardar:
            if not codigo or not nombre.strip() or not categoria.strip():
                st.error("Completa el código, nombre y categoría.")
            elif productos["codigo"].astype(str).str.strip().str.lower().eq(
                codigo.lower()
            ).any():
                st.error("Ya existe un producto con ese código.")
            else:
                nuevo_producto = pd.DataFrame([{
                    "codigo": codigo,
                    "nombre": nombre.strip(),
                    "categoria": categoria.strip(),
                    "precio": precio,
                    "cantidad": int(cantidad),
                    "stock_minimo": int(stock_minimo),
                    "activo": True
                }])
                productos = pd.concat([productos, nuevo_producto], ignore_index=True)
                guardar_datos("productos", productos)

                if cantidad > 0:
                    nuevo_movimiento = pd.DataFrame([{
                        "fecha": ahora_texto(),
                        "codigo_producto": codigo,
                        "tipo_movimiento": "Entrada inicial",
                        "cantidad": int(cantidad),
                        "descripcion": "Registro inicial del producto"
                    }])
                    movimientos = pd.concat(
                        [movimientos, nuevo_movimiento], ignore_index=True
                    )
                    guardar_datos("movimientos", movimientos)

                st.success("¡Producto registrado correctamente!")
                st.rerun()

    # ----- PESTAÑA 2: CONSULTAR -----
    with tab2:
        st.subheader("Catálogo de productos")

        filtro = st.text_input(
            "Buscar por código, nombre o categoría",
            key="buscar_producto",
            placeholder="Escribe para filtrar..."
        )

        productos_mostrar = productos.copy()

        if filtro.strip():
            coincidencias = (
                productos_mostrar["codigo"].astype(str).str.contains(
                    filtro, case=False, na=False)
                | productos_mostrar["nombre"].astype(str).str.contains(
                    filtro, case=False, na=False)
                | productos_mostrar["categoria"].astype(str).str.contains(
                    filtro, case=False, na=False)
            )
            productos_mostrar = productos_mostrar[coincidencias]

        if not productos_mostrar.empty:
            st.caption(f"Mostrando {len(productos_mostrar)} de {len(productos)} productos.")
            st.dataframe(
                productos_mostrar,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "codigo": "Código",
                    "nombre": "Nombre",
                    "categoria": "Categoría",
                    "precio": st.column_config.NumberColumn("Precio", format="Q%.2f"),
                    "cantidad": "Cantidad",
                    "stock_minimo": "Stock mínimo",
                    "activo": "Activo",
                }
            )
        else:
            st.info("No se encontraron productos.")

    # ----- PESTAÑA 3: MODIFICAR -----
    with tab3:
        st.subheader("Modificar producto existente")

        if productos.empty:
            st.info("Primero debes registrar un producto.")
        else:
            codigos = productos["codigo"].astype(str).tolist()

            codigo_editar = st.selectbox(
                "Selecciona el código del producto",
                options=codigos, key="codigo_editar"
            )
            producto_actual = productos[
                productos["codigo"].astype(str) == codigo_editar
            ].iloc[0]

            with st.form("form_modificar_producto"):
                col_a, col_b = st.columns(2)
                with col_a:
                    nombre_nuevo = st.text_input(
                        "Nombre", value=str(producto_actual["nombre"])
                    )
                    categoria_nueva = st.text_input(
                        "Categoría", value=str(producto_actual["categoria"])
                    )
                    precio_nuevo = st.number_input(
                        "Precio de venta (Q)",
                        min_value=0.01,
                        value=max(float(producto_actual["precio"]), 0.01),
                        step=0.50
                    )
                with col_b:
                    cantidad_nueva = st.number_input(
                        "Cantidad de productos en existencia",
                        min_value=0,
                        value=max(int(producto_actual["cantidad"]), 0),
                        step=1
                    )
                    stock_minimo_nuevo = st.number_input(
                        "Stock mínimo",
                        min_value=0,
                        value=max(int(producto_actual["stock_minimo"]), 0),
                        step=1
                    )

                st.write("")
                modificar = st.form_submit_button(
                    "💾 Guardar cambios", use_container_width=True
                )

            if modificar:
                if not nombre_nuevo.strip() or not categoria_nueva.strip():
                    st.error("El nombre y la categoría son obligatorios.")
                else:
                    indice = productos.index[
                        productos["codigo"].astype(str) == codigo_editar
                    ][0]
                    cantidad_anterior = int(productos.at[indice, "cantidad"])

                    productos.at[indice, "nombre"] = nombre_nuevo.strip()
                    productos.at[indice, "categoria"] = categoria_nueva.strip()
                    productos.at[indice, "precio"] = precio_nuevo
                    productos.at[indice, "cantidad"] = int(cantidad_nueva)
                    productos.at[indice, "stock_minimo"] = int(stock_minimo_nuevo)
                    guardar_datos("productos", productos)

                    diferencia = int(cantidad_nueva) - cantidad_anterior
                    if diferencia != 0:
                        nuevo_movimiento = pd.DataFrame([{
                            "fecha": ahora_texto(),
                            "codigo_producto": codigo_editar,
                            "tipo_movimiento": (
                                "Entrada por ajuste" if diferencia > 0
                                else "Salida por ajuste"
                            ),
                            "cantidad": abs(diferencia),
                            "descripcion": "Ajuste desde Gestión de productos"
                        }])
                        movimientos = pd.concat(
                            [movimientos, nuevo_movimiento], ignore_index=True
                        )
                        guardar_datos("movimientos", movimientos)

                    st.success("Producto actualizado correctamente.")
                    st.rerun()

    # ----- PESTAÑA 4: DESACTIVAR -----
    with tab4:
        st.subheader("Desactivar producto")

        if productos.empty:
            st.info("No hay productos registrados.")
        else:
            codigos = productos["codigo"].astype(str).tolist()

            codigo_desactivar = st.selectbox(
                "Selecciona el producto",
                options=codigos, key="codigo_desactivar"
            )
            producto_desactivar = productos[
                productos["codigo"].astype(str) == codigo_desactivar
            ].iloc[0]

            with st.container(border=True):
                col_1, col_2, col_3 = st.columns(3)
                col_1.metric("Nombre", str(producto_desactivar["nombre"]))
                col_2.metric("Categoría", str(producto_desactivar["categoria"]))
                esta_activo = str(producto_desactivar["activo"]).lower() in VALORES_ACTIVOS
                col_3.metric("Estado actual", "Activo" if esta_activo else "Inactivo")

            st.warning(
                "Al desactivar el producto, dejará de contarse como activo "
                "y no aparecerá en las alertas de inventario."
            )

            confirmar = st.checkbox(
                "Confirmo que deseo desactivar este producto.",
                key="confirmar_desactivar"
            )

            if st.button(
                "🚫 Desactivar producto",
                disabled=not confirmar,
                use_container_width=True
            ):
                indice = productos.index[
                    productos["codigo"].astype(str) == codigo_desactivar
                ][0]
                productos.at[indice, "activo"] = False
                guardar_datos("productos", productos)
                st.success("Producto desactivado correctamente.")
                st.rerun()


# ==========================================
# 8. MÓDULO: REGISTRO DE VENTAS
# ==========================================

elif modulo == "Registro de ventas":
    st.markdown(
        '<p class="main-title">🛋 Registro de ventas</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="subtitle">'
        'Registra ventas, calcula el IVA y actualiza el inventario.'
        '</p>',
        unsafe_allow_html=True
    )

    IVA = 0.12

    productos_activos = productos[es_activo(productos["activo"])].copy()

    if productos_activos.empty:
        st.warning(
            "No hay productos activos para vender. "
            "Primero registra un producto en Gestión de productos."
        )
    else:
        st.subheader("Seleccionar productos")

        opciones = {
            f"{fila['codigo']} - {fila['nombre']}": str(fila["codigo"])
            for _, fila in productos_activos.iterrows()
        }

        seleccionados = st.multiselect(
            "Selecciona uno o varios productos",
            options=list(opciones.keys()),
            key="productos_seleccionados_venta",
            placeholder="Elige uno o varios productos"
        )

        detalles_venta = []
        subtotal_venta = 0.0

        for opcion in seleccionados:
            codigo_producto = opciones[opcion]
            producto = productos_activos[
                productos_activos["codigo"].astype(str) == codigo_producto
            ].iloc[0]

            existencia = int(float(producto["cantidad"]))
            precio_unitario = float(producto["precio"])

            st.markdown(f"### {producto['nombre']}")
            st.caption(
                f"Código: {codigo_producto} | "
                f"Precio: Q{precio_unitario:.2f} | "
                f"Existencias: {existencia}"
            )

            cantidad_vendida = st.number_input(
                f"Cantidad de productos a vender: {producto['nombre']}",
                min_value=0,
                max_value=max(existencia, 0),
                value=1 if existencia > 0 else 0,
                step=1,
                key=f"cantidad_venta_{codigo_producto}"
            )

            if cantidad_vendida > 0:
                importe = cantidad_vendida * precio_unitario
                subtotal_venta += importe
                detalles_venta.append({
                    "codigo_producto": codigo_producto,
                    "nombre_producto": producto["nombre"],
                    "cantidad": int(cantidad_vendida),
                    "precio_unitario": precio_unitario,
                    "subtotal": importe
                })

        if seleccionados:
            st.divider()
            st.subheader("Resumen de la venta")
            st.write("**Productos seleccionados:**")

            for detalle in detalles_venta:
                st.write(
                    f"- {detalle['nombre_producto']}: "
                    f"{detalle['cantidad']} unidades × "
                    f"Q{detalle['precio_unitario']:.2f} = "
                    f"Q{detalle['subtotal']:.2f}"
                )

            iva_venta = round(subtotal_venta * IVA, 2)
            total_venta = round(subtotal_venta + iva_venta, 2)

            col1, col2, col3 = st.columns(3)
            col1.metric("Subtotal", f"Q{subtotal_venta:.2f}")
            col2.metric("IVA (12 %)", f"Q{iva_venta:.2f}")
            col3.metric("Total", f"Q{total_venta:.2f}")

            st.divider()

            if not detalles_venta:
                st.info("Indica una cantidad mayor que cero para vender.")

            confirmar_venta = st.checkbox(
                "Confirmo que deseo registrar esta venta.",
                key="confirmar_venta"
            )

            if st.button(
                "Guardar venta",
                use_container_width=True,
                disabled=not confirmar_venta or not detalles_venta
            ):
                error_stock = None
                for detalle in detalles_venta:
                    fila_actual = productos[
                        productos["codigo"].astype(str) == detalle["codigo_producto"]
                    ]
                    if fila_actual.empty:
                        error_stock = (
                            f"No se encontró el producto {detalle['nombre_producto']}."
                        )
                        break

                    existencia_actual = int(float(fila_actual.iloc[0]["cantidad"]))
                    if detalle["cantidad"] > existencia_actual:
                        error_stock = (
                            f"No hay suficientes unidades de "
                            f"{detalle['nombre_producto']}. "
                            f"Disponibles: {existencia_actual}."
                        )
                        break

                    if str(fila_actual.iloc[0]["activo"]).lower() not in VALORES_ACTIVOS:
                        error_stock = (
                            f"El producto {detalle['nombre_producto']} "
                            "ya no está activo."
                        )
                        break

                if error_stock:
                    st.error(error_stock)
                else:
                    numeros_existentes = pd.to_numeric(
                        ventas["numero_venta"], errors="coerce"
                    )
                    numero_venta = (
                        int(numeros_existentes.max()) + 1
                        if numeros_existentes.notna().any() else 1
                    )
                    fecha_venta = ahora_texto()

                    nueva_venta = pd.DataFrame([{
                        "numero_venta": numero_venta,
                        "fecha": fecha_venta,
                        "subtotal": round(subtotal_venta, 2),
                        "iva": iva_venta,
                        "total": total_venta
                    }])
                    ventas = pd.concat([ventas, nueva_venta], ignore_index=True)
                    guardar_datos("ventas", ventas)

                    nuevos_detalles = []
                    for detalle in detalles_venta:
                        nuevos_detalles.append({
                            "numero_venta": numero_venta,
                            "codigo_producto": detalle["codigo_producto"],
                            "nombre_producto": detalle["nombre_producto"],
                            "cantidad": detalle["cantidad"],
                            "precio_unitario": detalle["precio_unitario"],
                            "subtotal": detalle["subtotal"]
                        })
                        indice = productos.index[
                            productos["codigo"].astype(str) == detalle["codigo_producto"]
                        ][0]
                        productos.at[indice, "cantidad"] = (
                            int(float(productos.at[indice, "cantidad"]))
                            - detalle["cantidad"]
                        )

                    detalles = pd.concat(
                        [detalles, pd.DataFrame(nuevos_detalles)], ignore_index=True
                    )
                    guardar_datos("productos", productos)
                    guardar_datos("detalle_ventas", detalles)

                    nuevos_movimientos = [{
                        "fecha": fecha_venta,
                        "codigo_producto": detalle["codigo_producto"],
                        "tipo_movimiento": "Venta",
                        "cantidad": detalle["cantidad"],
                        "descripcion": f"Venta número {numero_venta}"
                    } for detalle in detalles_venta]

                    movimientos = pd.concat(
                        [movimientos, pd.DataFrame(nuevos_movimientos)],
                        ignore_index=True
                    )
                    guardar_datos("movimientos", movimientos)

                    st.success(
                        f"¡Venta número {numero_venta} registrada correctamente!"
                    )
                    st.rerun()
        else:
            st.info("Selecciona los productos que deseas vender.")


# ==========================================
# 9. MÓDULO: CONTROL DE INVENTARIOS
# ==========================================

elif modulo == "Control de inventarios":
    st.markdown(
        '<p class="main-title">📊 Control de inventarios</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="subtitle">'
        'Administra las existencias y los movimientos de productos.'
        '</p>',
        unsafe_allow_html=True
    )

    tab1, tab2, tab3 = st.tabs([
        "📋 Existencias",
        "📥 Entrada de productos",
        "📤 Salida de productos"
    ])

    # ----- PESTAÑA 1: EXISTENCIAS -----
    with tab1:
        st.subheader("Existencias actuales")

        inventario = productos.copy()

        if not inventario.empty:
            inventario["cantidad"] = pd.to_numeric(
                inventario["cantidad"], errors="coerce"
            ).fillna(0)
            inventario["stock_minimo"] = pd.to_numeric(
                inventario["stock_minimo"], errors="coerce"
            ).fillna(0)
            inventario["activo"] = es_activo(inventario["activo"])

            inventario_activo = inventario[inventario["activo"]].copy()

            col1, col2, col3 = st.columns(3)
            col1.metric("Productos activos", len(inventario_activo))
            col2.metric(
                "Unidades disponibles",
                int(inventario_activo["cantidad"].sum())
            )
            stock_bajo_inv = inventario_activo[
                inventario_activo["cantidad"] <= inventario_activo["stock_minimo"]
            ]
            col3.metric("Productos con stock bajo", len(stock_bajo_inv))

            if not inventario_activo.empty:
                st.dataframe(
                    inventario_activo[
                        ["codigo", "nombre", "categoria",
                         "cantidad", "stock_minimo", "precio"]
                    ],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No hay productos activos registrados.")

            if not stock_bajo_inv.empty:
                st.warning(
                    "Hay productos que alcanzaron o están por debajo "
                    "de su stock mínimo."
                )
                st.dataframe(
                    stock_bajo_inv[
                        ["codigo", "nombre", "cantidad", "stock_minimo"]
                    ],
                    use_container_width=True,
                    hide_index=True
                )
        else:
            st.info("Todavía no hay productos registrados.")

    # ----- PESTAÑA 2: ENTRADA -----
    with tab2:
        st.subheader("Registrar entrada de inventario")
        st.write("Utiliza esta opción cuando recibas nuevas unidades de un producto.")

        productos_activos_inv = productos[es_activo(productos["activo"])].copy()

        if productos_activos_inv.empty:
            st.info("No hay productos activos para seleccionar.")
        else:
            opciones_inv = {
                f"{fila['codigo']} - {fila['nombre']}": str(fila["codigo"])
                for _, fila in productos_activos_inv.iterrows()
            }

            with st.form("form_entrada_inventario"):
                producto_entrada = st.selectbox(
                    "Producto", options=list(opciones_inv.keys())
                )
                cantidad_entrada = st.number_input(
                    "Cantidad de productos que ingresan",
                    min_value=1, value=1, step=1
                )
                descripcion_entrada = st.text_input(
                    "Descripción", placeholder="Ej. Compra a proveedor"
                )
                guardar_entrada = st.form_submit_button(
                    "Registrar entrada", use_container_width=True
                )

            if guardar_entrada:
                codigo_entrada = opciones_inv[producto_entrada]
                indice_entrada = productos.index[
                    productos["codigo"].astype(str) == codigo_entrada
                ][0]
                cantidad_actual = int(float(productos.at[indice_entrada, "cantidad"]))
                productos.at[indice_entrada, "cantidad"] = (
                    cantidad_actual + int(cantidad_entrada)
                )
                guardar_datos("productos", productos)

                nuevo_movimiento = pd.DataFrame([{
                    "fecha": ahora_texto(),
                    "codigo_producto": codigo_entrada,
                    "tipo_movimiento": "Entrada",
                    "cantidad": int(cantidad_entrada),
                    "descripcion": descripcion_entrada.strip() or "Entrada de inventario"
                }])
                movimientos = pd.concat(
                    [movimientos, nuevo_movimiento], ignore_index=True
                )
                guardar_datos("movimientos", movimientos)

                st.success(
                    f"Entrada registrada. Existencias actualizadas: "
                    f"{cantidad_actual + int(cantidad_entrada)} unidades."
                )
                st.rerun()

    # ----- PESTAÑA 3: SALIDA -----
    with tab3:
        st.subheader("Registrar salida de inventario")
        st.write(
            "Utiliza esta opción para registrar pérdidas, daños "
            "u otras salidas que no correspondan a una venta."
        )

        productos_activos_salida = productos[es_activo(productos["activo"])].copy()

        if productos_activos_salida.empty:
            st.info("No hay productos activos para seleccionar.")
        else:
            opciones_salida = {
                f"{fila['codigo']} - {fila['nombre']}": str(fila["codigo"])
                for _, fila in productos_activos_salida.iterrows()
            }

            with st.form("form_salida_inventario"):
                producto_salida = st.selectbox(
                    "Producto", options=list(opciones_salida.keys())
                )
                codigo_salida = opciones_salida[producto_salida]
                fila_salida = productos_activos_salida[
                    productos_activos_salida["codigo"].astype(str) == codigo_salida
                ].iloc[0]
                existencia_salida = max(int(float(fila_salida["cantidad"])), 0)

                st.caption(f"Existencias disponibles: {existencia_salida}")

                cantidad_salida = st.number_input(
                    "Cantidad de productos que salen",
                    min_value=1,
                    max_value=max(existencia_salida, 1),
                    value=1, step=1,
                    disabled=existencia_salida == 0
                )
                descripcion_salida = st.text_input(
                    "Motivo de la salida", placeholder="Ej. Producto dañado"
                )
                guardar_salida = st.form_submit_button(
                    "Registrar salida",
                    use_container_width=True,
                    disabled=existencia_salida == 0
                )

            if guardar_salida:
                indice_salida = productos.index[
                    productos["codigo"].astype(str) == codigo_salida
                ][0]
                existencia_actual = int(float(productos.at[indice_salida, "cantidad"]))

                if int(cantidad_salida) > existencia_actual:
                    st.error("No hay suficientes unidades disponibles.")
                elif not descripcion_salida.strip():
                    st.error("Escribe el motivo de la salida.")
                else:
                    productos.at[indice_salida, "cantidad"] = (
                        existencia_actual - int(cantidad_salida)
                    )
                    guardar_datos("productos", productos)

                    nuevo_movimiento = pd.DataFrame([{
                        "fecha": ahora_texto(),
                        "codigo_producto": codigo_salida,
                        "tipo_movimiento": "Salida",
                        "cantidad": int(cantidad_salida),
                        "descripcion": descripcion_salida.strip()
                    }])
                    movimientos = pd.concat(
                        [movimientos, nuevo_movimiento], ignore_index=True
                    )
                    guardar_datos("movimientos", movimientos)

                    st.success(
                        f"Salida registrada. Quedan "
                        f"{existencia_actual - int(cantidad_salida)} unidades."
                    )
                    st.rerun()

    # ----- HISTORIAL DE MOVIMIENTOS -----
    st.divider()
    st.subheader("📑 Historial de movimientos")

    if not movimientos.empty:
        movimientos_mostrar = movimientos.sort_values(
            "fecha", ascending=False
        ).copy()
        movimientos_mostrar["fecha"] = formatear_fechas(movimientos_mostrar["fecha"])
        st.dataframe(
            movimientos_mostrar,
            use_container_width=True,
            hide_index=True,
            column_config={
                "fecha": "Fecha",
                "codigo_producto": "Código",
                "tipo_movimiento": "Tipo de movimiento",
                "cantidad": "Cantidad",
                "descripcion": "Descripción",
            }
        )
    else:
        st.info("Todavía no hay movimientos de inventario.")


# ==========================================
# 10. MÓDULO: REPORTES Y ESTADÍSTICAS
# ==========================================

elif modulo == "Reportes y estadísticas":
    st.markdown(
        '<p class="main-title">📈 Reportes y estadísticas</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="subtitle">'
        'Analiza las ventas y el rendimiento de tu negocio.'
        '</p>',
        unsafe_allow_html=True
    )

    ventas_reporte = ventas.copy()
    detalles_reporte = detalles.copy()

    if not ventas_reporte.empty:
        for columna in ["total", "subtotal", "iva"]:
            ventas_reporte[columna] = pd.to_numeric(
                ventas_reporte[columna], errors="coerce"
            ).fillna(0)

    if not detalles_reporte.empty:
        for columna in ["cantidad", "subtotal"]:
            detalles_reporte[columna] = pd.to_numeric(
                detalles_reporte[columna], errors="coerce"
            ).fillna(0)

    # ----- INDICADORES GENERALES -----
    st.subheader("Resumen general")

    numero_ventas = len(ventas_reporte)
    ingresos_totales = (
        ventas_reporte["total"].sum() if not ventas_reporte.empty else 0
    )
    promedio_venta = (
        ingresos_totales / numero_ventas if numero_ventas > 0 else 0
    )
    unidades_vendidas = (
        int(detalles_reporte["cantidad"].sum())
        if not detalles_reporte.empty else 0
    )

    col1, col2 = st.columns(2)
    col1.metric("Ventas registradas", numero_ventas)
    col2.metric("Ingresos totales", f"Q{ingresos_totales:,.2f}")

    col3, col4 = st.columns(2)
    col3.metric("Promedio por venta", f"Q{promedio_venta:,.2f}")
    col4.metric("Unidades vendidas", unidades_vendidas)

    st.divider()

    # ----- FILTRAR VENTAS POR FECHA -----
    st.subheader("Consultar ventas por período")

    if not ventas_reporte.empty:
        ventas_reporte["fecha_dt"] = pd.to_datetime(
            ventas_reporte["fecha"], errors="coerce"
        )
        fechas_validas = ventas_reporte["fecha_dt"].dropna()

        if not fechas_validas.empty:
            fecha_minima = fechas_validas.min().date()
            fecha_maxima = fechas_validas.max().date()

            col_inicio, col_fin = st.columns(2)
            with col_inicio:
                fecha_inicio = st.date_input(
                    "Fecha inicial",
                    value=fecha_minima,
                    min_value=fecha_minima,
                    max_value=fecha_maxima,
                    format="DD/MM/YYYY",
                    key="fecha_inicio_reporte"
                )
            with col_fin:
                fecha_fin = st.date_input(
                    "Fecha final",
                    value=fecha_maxima,
                    min_value=fecha_minima,
                    max_value=fecha_maxima,
                    format="DD/MM/YYYY",
                    key="fecha_fin_reporte"
                )

            if fecha_inicio <= fecha_fin:
                ventas_filtradas = ventas_reporte[
                    ventas_reporte["fecha_dt"].dt.date.between(
                        fecha_inicio, fecha_fin
                    )
                ].copy()
            else:
                ventas_filtradas = ventas_reporte.iloc[0:0].copy()
                st.error(
                    "La fecha inicial no puede ser posterior a la fecha final."
                )

            total_periodo = ventas_filtradas["total"].sum()
            st.metric(
                "Ingresos del período seleccionado",
                f"Q{total_periodo:,.2f}"
            )

            if not ventas_filtradas.empty:
                resumen_diario = (
                    ventas_filtradas.assign(
                        dia=ventas_filtradas["fecha_dt"].dt.strftime(FORMATO_FECHA)
                    )
                    .groupby("dia", as_index=False)["total"]
                    .sum()
                    .rename(columns={"total": "Ingresos"})
                )

                st.subheader("Ingresos por día")

                base_dia = alt.Chart(resumen_diario).encode(
                    x=alt.X(
                        "dia:N", title="Fecha",
                        axis=alt.Axis(labelAngle=0, labelColor="#5A6078",
                                      titleColor="#1C238F")
                    ),
                    y=alt.Y(
                        "Ingresos:Q", title="Ingresos (Q)",
                        axis=alt.Axis(labelColor="#5A6078", titleColor="#1C238F")
                    ),
                    tooltip=[
                        alt.Tooltip("dia:N", title="Fecha"),
                        alt.Tooltip("Ingresos:Q", title="Ingresos", format=",.2f")
                    ]
                )
                barras_dia = base_dia.mark_bar(
                    cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=52,
                    color=alt.Gradient(
                        gradient="linear",
                        stops=[
                            alt.GradientStop(color="#6B78F0", offset=0),
                            alt.GradientStop(color="#3B49E0", offset=1),
                        ],
                        x1=1, x2=1, y1=0, y2=1,
                    ),
                )
                etiquetas_dia = base_dia.mark_text(
                    dy=-8, color="#1C238F", fontWeight="bold", fontSize=12
                ).encode(text=alt.Text("Ingresos:Q", format=",.0f"))

                st.altair_chart(
                    (barras_dia + etiquetas_dia).properties(height=340),
                    use_container_width=True
                )
            else:
                st.info("No hay ventas en el período seleccionado.")

            st.subheader("Detalle de ventas del período")

            columnas_ventas = [
                "numero_venta", "fecha", "subtotal", "iva", "total"
            ]
            ventas_mostrar = ventas_filtradas[columnas_ventas].copy()
            ventas_mostrar["fecha"] = formatear_fechas(ventas_mostrar["fecha"])

            st.dataframe(
                ventas_mostrar,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "numero_venta": "N.º venta",
                    "fecha": "Fecha",
                    "subtotal": st.column_config.NumberColumn("Subtotal", format="Q%.2f"),
                    "iva": st.column_config.NumberColumn("IVA", format="Q%.2f"),
                    "total": st.column_config.NumberColumn("Total", format="Q%.2f"),
                }
            )

            csv_ventas = ventas_mostrar.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "⬇️ Descargar ventas del período (CSV)",
                data=csv_ventas,
                file_name="reporte_ventas.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("Las fechas de las ventas no son válidas.")
    else:
        st.info("Todavía no hay ventas registradas para generar reportes.")

    st.divider()

    # ----- PRODUCTOS MÁS VENDIDOS -----
    st.subheader("🏆 Productos más vendidos")

    if not detalles_reporte.empty:
        resumen_productos = (
            detalles_reporte.groupby(
                ["codigo_producto", "nombre_producto"], as_index=False
            )
            .agg(
                Unidades_vendidas=("cantidad", "sum"),
                Ingresos=("subtotal", "sum")
            )
            .sort_values("Unidades_vendidas", ascending=False)
        )

        st.dataframe(
            resumen_productos,
            use_container_width=True,
            hide_index=True,
            column_config={
                "codigo_producto": "Código",
                "nombre_producto": "Producto",
                "Unidades_vendidas": "Unidades vendidas",
                "Ingresos": st.column_config.NumberColumn("Ingresos", format="Q%.2f"),
            }
        )

        base_prod = alt.Chart(resumen_productos).encode(
            y=alt.Y(
                "nombre_producto:N", sort="-x", title="Producto",
                axis=alt.Axis(labelColor="#5A6078", titleColor="#1C238F")
            ),
            x=alt.X(
                "Unidades_vendidas:Q", title="Unidades vendidas",
                axis=alt.Axis(labelColor="#5A6078", titleColor="#1C238F")
            ),
            tooltip=[
                alt.Tooltip("nombre_producto:N", title="Producto"),
                alt.Tooltip("Unidades_vendidas:Q", title="Unidades"),
                alt.Tooltip("Ingresos:Q", title="Ingresos", format=",.2f"),
            ],
        )
        barras_prod = base_prod.mark_bar(
            cornerRadiusTopRight=6, cornerRadiusBottomRight=6, size=34
        ).encode(
            color=alt.Color(
                "Unidades_vendidas:Q",
                scale=alt.Scale(range=["#A9B2F5", "#3B49E0", "#1C238F"]),
                legend=None,
            )
        )
        etiquetas_prod = base_prod.mark_text(
            dx=10, color="#1C238F", fontWeight="bold", fontSize=12
        ).encode(text=alt.Text("Unidades_vendidas:Q", format=",.0f"))

        altura_prod = max(180, len(resumen_productos) * 70)

        st.altair_chart(
            (barras_prod + etiquetas_prod).properties(height=altura_prod),
            use_container_width=True
        )

        csv_productos = resumen_productos.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "⬇️ Descargar reporte de productos (CSV)",
            data=csv_productos,
            file_name="reporte_productos_mas_vendidos.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("Todavía no hay detalles de ventas para analizar productos.")
