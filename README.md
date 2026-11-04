#  Sistema de Gestión Comercial

##  Descripción del proyecto

El **Sistema de Gestión Comercial** es una aplicación web desarrollada en Python utilizando Streamlit, diseñada para facilitar la administración de pequeños negocios mediante el control de productos, ventas e inventario.

El sistema permite organizar la información comercial, registrar operaciones y consultar reportes que ayudan a llevar un mejor control de las actividades del negocio.

## Objetivo

Desarrollar una herramienta sencilla y funcional que permita gestionar las principales operaciones de un pequeño negocio, facilitando el almacenamiento, consulta y análisis de la información.

##  Tecnologías utilizadas

- **Python:** lenguaje de programación principal.
- **Streamlit:** desarrollo de la interfaz web.
- **Pandas:** lectura, procesamiento y administración de datos.
- **Altair:** creación de gráficas estadísticas.
- **CSV:** almacenamiento de la información.

##  Funcionalidades principales

###  Gestión de productos
- Registrar nuevos productos.
- Consultar productos por código, nombre o categoría.
- Modificar información de los productos.
- Desactivar productos.
- Validar códigos duplicados y datos ingresados.

###  Registro de ventas
- Registrar ventas de productos.
- Verificar la disponibilidad de existencias.
- Calcular subtotal, IVA del 12 % y total.
- Actualizar automáticamente el inventario.

###  Control de inventarios
- Registrar entradas y salidas de productos.
- Consultar existencias disponibles.
- Identificar productos con stock bajo.
- Consultar el historial de movimientos.

###  Reportes y estadísticas
- Consultar ingresos y ventas registradas.
- Visualizar gráficas de ingresos por fecha.
- Identificar los productos más vendidos.
- Consultar información mediante filtros.

##  Estructura del proyecto

```text
Sistema_Gestion_Comercial/
│
├── App.py
│
├── datos/
│   ├── productos.csv
│   ├── ventas.csv
│   ├── detalle_ventas.csv
│   └── movimientos.csv
│
├── datos_prueba/
│   ├── productos.csv
│   ├── ventas.csv
│   ├── detalle_ventas.csv
│   └── movimientos.csv
│
├── Respaldo_datos/
│
└── README.md
```


Proyecto académico desarrollado como parte del aprendizaje y aplicación de conocimientos de programación en Python.
