"""
Evaluador de Riesgo de Deserción Estudiantil
Sistema Semáforo con Perspectiva Interseccional
----------------------------------------------------
Instalar dependencias:
    pip install streamlit plotly pandas

Ejecutar:
    streamlit run evaluador_riesgo_desercion.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Evaluador de Riesgo de Deserción",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# ESTILOS CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
}

/* Header principal */
.main-header {
    background: linear-gradient(135deg, #FDD969 0%, #FCBF1E 60%, #f5a800 100%);
    padding: 32px 36px;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 32px;
    box-shadow: 0 8px 32px rgba(252,191,30,0.3);
}
.main-header h1 {
    color: #1a1a1a;
    font-size: 2rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.5px;
}
.main-header p {
    color: #333;
    margin: 8px 0 0 0;
    font-size: 0.95rem;
    font-weight: 400;
}

/* Tarjeta de dimensión */
.dim-card {
    background: #fafafa;
    border-left: 5px solid #FCBF1E;
    border-radius: 0 12px 12px 0;
    padding: 18px 20px;
    margin-bottom: 6px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.dim-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 4px;
}
.dim-subtitle {
    font-size: 0.78rem;
    color: #888;
    margin-bottom: 10px;
    font-style: italic;
}

/* Semáforo */
.semaforo-verde {
    background: linear-gradient(135deg, #27ae60, #2ecc71);
    color: white;
    padding: 20px 28px;
    border-radius: 14px;
    text-align: center;
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    box-shadow: 0 6px 20px rgba(46,204,113,0.4);
    letter-spacing: -0.5px;
}
.semaforo-amarillo {
    background: linear-gradient(135deg, #e67e22, #f39c12);
    color: white;
    padding: 20px 28px;
    border-radius: 14px;
    text-align: center;
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    box-shadow: 0 6px 20px rgba(243,156,18,0.4);
    letter-spacing: -0.5px;
}
.semaforo-rojo {
    background: linear-gradient(135deg, #c0392b, #e74c3c);
    color: white;
    padding: 20px 28px;
    border-radius: 14px;
    text-align: center;
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    box-shadow: 0 6px 20px rgba(231,76,60,0.4);
    letter-spacing: -0.5px;
}

/* Interseccionalidad */
.intersec-card {
    background: #fffbf0;
    border: 1.5px solid #FDD969;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 10px;
}
.intersec-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.9rem;
    color: #333;
    margin-bottom: 6px;
}
.intersec-body {
    font-size: 0.85rem;
    color: #555;
    line-height: 1.5;
}
.intersec-badge {
    display: inline-block;
    background: #FCBF1E;
    color: #1a1a1a;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    margin: 2px 4px 2px 0;
}

/* Rutas */
.ruta-card {
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 12px;
    border: 2px solid;
}
.ruta-verde { background: #f0fdf6; border-color: #2ecc71; }
.ruta-amarilla { background: #fffbf0; border-color: #FCBF1E; }
.ruta-roja { background: #fff5f5; border-color: #e74c3c; }
.ruta-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.05rem;
    margin-bottom: 10px;
}
.ruta-item {
    font-size: 0.88rem;
    color: #444;
    padding: 5px 0;
    border-bottom: 1px solid rgba(0,0,0,0.05);
    line-height: 1.5;
}

/* Acción específica por dimensión */
.accion-dim {
    background: #f7f7f7;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 8px;
    font-size: 0.85rem;
    color: #444;
    border-left: 4px solid #FDD969;
}
.accion-dim strong {
    color: #1a1a1a;
    font-family: 'Syne', sans-serif;
}

/* Sidebar */
.sidebar-note {
    background: #fffbf0;
    border-radius: 10px;
    padding: 12px;
    font-size: 0.82rem;
    color: #555;
    line-height: 1.5;
    border: 1px solid #FDD969;
}

/* Score badge */
.score-badge {
    display: inline-block;
    background: #1a1a1a;
    color: #FDD969;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    padding: 8px 18px;
    border-radius: 30px;
    margin-top: 10px;
}

/* Divider */
.yellow-divider {
    height: 4px;
    background: linear-gradient(90deg, #FDD969, #FCBF1E, #FDD969);
    border-radius: 4px;
    margin: 28px 0;
}

/* Voz del estudiante */
.quote-card {
    background: #f9f5e7;
    border-left: 4px solid #FCBF1E;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    font-size: 0.83rem;
    color: #555;
    font-style: italic;
    line-height: 1.6;
    margin-top: 6px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATOS: DIMENSIONES, ÍTEMS Y PESOS
# Cada ítem: (texto, peso, voz_del_estudiante_opcional)
# Peso: 1 = leve, 2 = moderado, 3 = crítico
# ─────────────────────────────────────────────
DIMENSIONES = {
    "💰 Económica": {
        "color": "#E67E22",
        "descripcion": "Presión financiera, trabajo simultáneo, falta de apoyo económico",
        "items": [
            ("Trabaja para sostenerse económicamente mientras estudia", 2,
             "la presión económica y la necesidad de trabajar para sostenerse pueden llevar a la deserción"),
            ("No cuenta con apoyo financiero familiar o institucional", 2, None),
            ("Ha considerado pausar o dejar sus estudios por razones económicas", 3, None),
            ("Tiene dificultades para cubrir gastos básicos (alimentación, transporte, materiales)", 2, None),
        ]
    },
    "👨‍👩‍👧 Social y Familiar": {
        "color": "#8E44AD",
        "descripcion": "Red de apoyo, aislamiento, origen geográfico, choque cultural",
        "items": [
            ("Se trasladó de otra ciudad o región para estudiar", 1,
             "estudiantes que se trasladan de áreas rurales a urbanas pueden experimentar un choque cultural"),
            ("No tiene red de apoyo cercana (familia, amigos) en la ciudad donde estudia", 2, None),
            ("Experimenta sensación de soledad o aislamiento en la institución", 2, None),
            ("Proviene de colegio con menor nivel académico o contexto rural", 1, None),
        ]
    },
    "📚 Académica": {
        "color": "#2980B9",
        "descripcion": "Rendimiento, carga curricular, acceso a tutorías, nivelación",
        "items": [
            ("La carga académica supera su capacidad de gestión del tiempo", 2,
             "para graduarse en cinco años tienes que ver en promedio ocho materias... tú ya estás que no puedes con tu tiempo"),
            ("Tiene bajo rendimiento o ha reprobado asignaturas", 2, None),
            ("Está cursando materias nivelatorias que retrasan su avance curricular", 2,
             "cuando uno está en primera matrícula tiene materias nivelatorias que atrasan demasiado el proceso"),
            ("No accede fácilmente a tutorías o monitorías de apoyo académico", 1,
             "si no tienes suerte te explican por fuera del horario, pero por lo general a veces no"),
            ("Percibe que los apoyos académicos disponibles son insuficientes o desactualizados", 1, None),
        ]
    },
    "🧠 Salud Mental": {
        "color": "#E74C3C",
        "descripcion": "Estrés, ansiedad, agotamiento emocional, uso de servicios de bienestar",
        "items": [
            ("Reporta síntomas de estrés, ansiedad o agotamiento emocional frecuente", 2,
             "la carga emocional y el estrés pueden ser factores significativos que afectan el rendimiento y la motivación"),
            ("Ha presentado episodios de depresión o crisis emocional durante su carrera", 3, None),
            ("Siente que la presión académica afecta su bienestar general", 2, None),
            ("Desconoce o no utiliza los servicios de psicología y bienestar universitario", 1, None),
        ]
    },
    "🧭 Vocacional": {
        "color": "#27AE60",
        "descripcion": "Claridad sobre la elección de carrera, identidad profesional, sentido de pertenencia",
        "items": [
            ("Ingresó al programa sin tener certeza sobre su vocación", 2,
             "muchos estudiantes ingresan a programas sin una verdadera vocación, lo que puede llevar a la desilusión"),
            ("Siente que la carrera no corresponde realmente a sus intereses o expectativas", 2, None),
            ("Ha pensado seriamente en cambiar de programa o de institución", 2, None),
            ("Experimenta baja identidad o débil sentido de pertenencia con su disciplina", 2,
             "la baja densidad de contenidos específicos al inicio debilita los lazos simbólicos con la carrera"),
        ]
    },
    "🏛️ Institucional": {
        "color": "#16A085",
        "descripcion": "Acceso a servicios, rutas de atención, orientación académica, cultura institucional",
        "items": [
            ("Desconoce los servicios y rutas de apoyo que ofrece la institución", 1, None),
            ("Las rutas de atención le parecen informales, azarosas o poco accesibles", 2,
             "la respuesta del sistema ante la dificultad no es sistémica sino contingente"),
            ("No recibe orientación académica sistemática sobre su trayectoria curricular", 2, None),
            ("Percibe falta de empatía o comprensión de docentes y personal administrativo", 1, None),
        ]
    },
}

# ─────────────────────────────────────────────
# INTERSECCIONALIDADES
# Pares de dimensiones que se amplifican mutuamente
# ─────────────────────────────────────────────
INTERSECCIONES = [
    {
        "dims": ("💰 Económica", "📚 Académica"),
        "titulo": "Doble jornada: trabajo + estudio",
        "descripcion": "Equilibrar trabajo remunerado y exigencias académicas genera fatiga crónica. "
                       "El agotamiento reduce la capacidad de atención, participación y resiliencia ante dificultades académicas.",
        "nivel_alerta": "alto"
    },
    {
        "dims": ("👨‍👩‍👧 Social y Familiar", "🧠 Salud Mental"),
        "titulo": "Aislamiento que amplifica el malestar emocional",
        "descripcion": "Sin red de apoyo, los episodios de ansiedad o depresión no tienen contención. "
                       "La soledad actúa como multiplicador del impacto de otras dificultades.",
        "nivel_alerta": "alto"
    },
    {
        "dims": ("🧭 Vocacional", "📚 Académica"),
        "titulo": "Desmotivación que profundiza la percepción de fracaso",
        "descripcion": "La falta de identificación con la carrera hace que los errores académicos se "
                       "interpreten como confirmación de que 'este no es mi lugar', acelerando el abandono.",
        "nivel_alerta": "alto"
    },
    {
        "dims": ("💰 Económica", "👨‍👩‍👧 Social y Familiar"),
        "titulo": "Vulnerabilidad material y social simultánea",
        "descripcion": "El desplazamiento geográfico sin red de apoyo combinado con presión económica "
                       "representa uno de los perfiles de riesgo más críticos: el estudiante enfrenta "
                       "soledad, precariedad y exigencia académica al mismo tiempo.",
        "nivel_alerta": "crítico"
    },
    {
        "dims": ("🏛️ Institucional", "🧠 Salud Mental"),
        "titulo": "Invisibilidad institucional que agrava la crisis",
        "descripcion": "No saber a quién acudir en un momento de crisis emocional es un detonante directo "
                       "de abandono. La informalidad en las rutas de atención tiene consecuencias graves "
                       "cuando el malestar es urgente.",
        "nivel_alerta": "alto"
    },
    {
        "dims": ("🧭 Vocacional", "🏛️ Institucional"),
        "titulo": "Desorientación sin andamiaje institucional",
        "descripcion": "Un estudiante sin vocación clara que además no recibe orientación institucional "
                       "queda en un vacío: no sabe qué quiere y no tiene a quién preguntarle. "
                       "La institución falla en proveer el soporte que sostendría la permanencia.",
        "nivel_alerta": "moderado"
    },
    {
        "dims": ("📚 Académica", "🏛️ Institucional"),
        "titulo": "Carga curricular sin soporte formal",
        "descripcion": "La saturación académica sin tutorías accesibles y rutas claras obliga al estudiante "
                       "a resolver por sus propios medios o rendirse. El apoyo contingente e informal "
                       "no es una red de seguridad real.",
        "nivel_alerta": "moderado"
    },
    {
        "dims": ("👨‍👩‍👧 Social y Familiar", "🧭 Vocacional"),
        "titulo": "Sin pertenencia social ni vocacional",
        "descripcion": "El sentido de pertenencia se construye tanto desde los vínculos con pares como "
                       "desde la identidad disciplinar. Si ambos fallan, el estudiante no encuentra "
                       "razón para continuar en la institución.",
        "nivel_alerta": "alto"
    },
]

# ─────────────────────────────────────────────
# RUTAS DE INTERVENCIÓN
# ─────────────────────────────────────────────
RUTAS = {
    "BAJO": {
        "titulo": "✅ Ruta Preventiva",
        "clase": "ruta-verde",
        "descripcion": "El estudiante presenta señales de bajo riesgo. Se recomienda un acompañamiento de seguimiento liviano para sostener su trayectoria.",
        "acciones": [
            "📅 Entrevista de bienestar al inicio del siguiente semestre",
            "📢 Socializar servicios de apoyo disponibles (psicología, tutorías, orientación vocacional)",
            "👥 Invitar a redes estudiantiles, grupos de estudio y actividades de integración",
            "📋 Verificar que el plan de materias sea coherente con sus capacidades actuales",
        ]
    },
    "MODERADO": {
        "titulo": "⚠️ Ruta de Acompañamiento Activo",
        "clase": "ruta-amarilla",
        "descripcion": "El estudiante presenta señales de alerta en varias dimensiones. Se requiere intervención estructurada antes de que el riesgo escale.",
        "acciones": [
            "🧑‍🏫 Asignación de tutor o consejero de acompañamiento personalizado",
            "🧠 Referencia a servicios de psicología y bienestar universitario",
            "📋 Revisión conjunta de la carga académica y posible ajuste de créditos",
            "🧭 Sesión de orientación vocacional si se identifica desajuste con el programa",
            "💬 Canal de comunicación directa y regular con coordinación académica",
            "👥 Vinculación a grupos de apoyo entre pares o mentorías con estudiantes avanzados",
        ]
    },
    "ALTO": {
        "titulo": "🚨 Ruta de Intervención Urgente",
        "clase": "ruta-roja",
        "descripcion": "El estudiante presenta riesgo alto de deserción. Se activa un protocolo de retención inmediata con intervención en múltiples frentes.",
        "acciones": [
            "🚨 Contacto inmediato por parte de coordinación académica o bienestar (no esperar que el estudiante llegue)",
            "🧠 Atención psicológica prioritaria: primera cita en menos de una semana",
            "💰 Revisión urgente de elegibilidad para becas, subsidios o apoyos económicos de emergencia",
            "📅 Ajuste del plan de estudios: reducción de créditos o aplazamiento temporal de materias exigentes",
            "🤝 Vinculación inmediata a grupos de apoyo entre pares y mentoría uno a uno",
            "🏛️ Apertura de caso especial ante decanatura o dirección de programa",
            "🔄 Seguimiento quincenal hasta verificar estabilización del caso",
            "📞 Comunicación con familia u red de apoyo (con consentimiento del estudiante)",
        ]
    }
}

# ─────────────────────────────────────────────
# ACCIONES ESPECÍFICAS POR DIMENSIÓN
# ─────────────────────────────────────────────
ACCIONES_DIM = {
    "💰 Económica": {
        "umbral": 3,
        "icono": "💰",
        "accion": "Revisar acceso a becas socioeconómicas, subsidios de alimentación y transporte, y opciones de trabajo estudiantil institucional. Considerar ajuste de carga académica para quienes trabajan."
    },
    "👨‍👩‍👧 Social y Familiar": {
        "umbral": 2,
        "icono": "👨‍👩‍👧",
        "accion": "Activar programas de integración para estudiantes foráneos o de primera generación. Conectar con residencias estudiantiles, redes de acogida o grupos de interés compartido."
    },
    "📚 Académica": {
        "umbral": 3,
        "icono": "📚",
        "accion": "Vincular a programa de nivelación reforzado y tutorías actualizadas. Revisar el plan de materias con consejero académico para construir una ruta realista de avance curricular."
    },
    "🧠 Salud Mental": {
        "umbral": 2,
        "icono": "🧠",
        "accion": "Referencia proactiva a psicología — no esperar que el estudiante solicite el servicio. Capacitar docentes para identificar señales de alerta. Mapear y comunicar rutas de atención en salud mental."
    },
    "🧭 Vocacional": {
        "umbral": 2,
        "icono": "🧭",
        "accion": "Aplicar instrumento de orientación vocacional. Explorar posibilidad de transferencia interna, doble programa o ajustes curriculares que generen mayor identificación con la disciplina."
    },
    "🏛️ Institucional": {
        "umbral": 2,
        "icono": "🏛️",
        "accion": "Mapear y comunicar rutas de atención de forma clara y accesible. Designar un referente institucional como punto de contacto único. Formalizar el acompañamiento para que no dependa del azar."
    },
}

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎓 Guía de uso")
    st.markdown("""
    <div class='sidebar-note'>
    <strong>Cómo usar esta herramienta:</strong><br><br>
    1. Complete el checklist por cada dimensión de riesgo.<br><br>
    2. Haga clic en <strong>Evaluar Riesgo</strong>.<br><br>
    3. Revise el semáforo, el perfil interseccional y la ruta de intervención sugerida.
    <br><br>
    <strong>Escala de pesos:</strong><br>
    • Peso 1 = Factor leve<br>
    • Peso 2 = Factor moderado<br>
    • Peso 3 = Factor crítico<br><br>
    <strong>Niveles de riesgo:</strong><br>
    🟢 <strong>Bajo:</strong> 0–6 pts<br>
    🟡 <strong>Moderado:</strong> 7–14 pts<br>
    🔴 <strong>Alto:</strong> 15+ pts
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔗 Sobre la interseccionalidad")
    st.markdown("""
    <div class='sidebar-note'>
    Los factores de riesgo no operan de forma aislada. Esta herramienta identifica
    <strong>intersecciones críticas</strong> entre dimensiones, donde la combinación
    de factores genera un riesgo mayor que la suma de sus partes.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class='main-header'>
    <h1>🎓 Evaluador de Riesgo de Deserción Estudiantil</h1>
    <p>Sistema semáforo con perspectiva interseccional · Detección temprana · Rutas de intervención</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FORMULARIO DE EVALUACIÓN
# ─────────────────────────────────────────────
st.markdown("## 📋 Evaluación por Dimensiones")
st.caption("Marque todas las situaciones que aplican al estudiante evaluado. Cada ítem tiene un peso diferencial según su impacto en el riesgo de deserción.")

scores = {}
items_activos_por_dim = {}

for dim_name, dim_data in DIMENSIONES.items():
    st.markdown(f"""
    <div class='dim-card'>
        <div class='dim-title'>{dim_name}</div>
        <div class='dim-subtitle'>{dim_data['descripcion']}</div>
    </div>
    """, unsafe_allow_html=True)

    dim_score = 0
    items_activos = []

    for idx, item_data in enumerate(dim_data["items"]):
        item_text, peso, voz = item_data
        col_check, col_peso = st.columns([10, 1])
        with col_check:
            checked = st.checkbox(
                f"{item_text}",
                key=f"{dim_name}_{idx}",
                help=f"Peso de este factor: {peso}"
            )
        with col_peso:
            color_peso = "#FCBF1E" if peso == 1 else ("#E67E22" if peso == 2 else "#E74C3C")
            st.markdown(
                f"<span style='background:{color_peso};color:white;padding:2px 8px;border-radius:12px;font-size:0.75rem;font-weight:700;'>P{peso}</span>",
                unsafe_allow_html=True
            )
        if checked:
            dim_score += peso
            items_activos.append(item_text)
            if voz:
                st.markdown(f"<div class='quote-card'>💬 «{voz}»</div>", unsafe_allow_html=True)

    scores[dim_name] = dim_score
    items_activos_por_dim[dim_name] = items_activos
    st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# BOTÓN DE EVALUACIÓN
# ─────────────────────────────────────────────
st.markdown("<div class='yellow-divider'></div>", unsafe_allow_html=True)

evaluar = st.button("🔍 Evaluar Riesgo del Estudiante", use_container_width=True, type="primary")

if evaluar:
    total_score = sum(scores.values())
    max_score = sum(w for dim in DIMENSIONES.values() for _, w, _ in dim["items"])
    pct = round((total_score / max_score) * 100, 1)
    dims_activas = [d for d, s in scores.items() if s > 0]

    # Nivel de riesgo
    if total_score <= 6:
        risk_level = "BAJO"
        risk_class = "semaforo-verde"
        risk_emoji = "🟢"
    elif total_score <= 14:
        risk_level = "MODERADO"
        risk_class = "semaforo-amarillo"
        risk_emoji = "🟡"
    else:
        risk_level = "ALTO"
        risk_class = "semaforo-rojo"
        risk_emoji = "🔴"

    # ── RESULTADO SEMÁFORO ──────────────────
    st.markdown("## 🚦 Resultado de la Evaluación")

    col_a, col_b, col_c = st.columns([2, 3, 2])
    with col_b:
        st.markdown(
            f"<div class='{risk_class}'>Riesgo {risk_level} {risk_emoji}"
            f"<br><span style='font-size:0.85rem;font-weight:400;opacity:0.9;'>"
            f"Puntaje: {total_score} / {max_score} pts &nbsp;|&nbsp; {pct}%</span></div>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── GRÁFICA RADAR ───────────────────────
    col_radar, col_barras = st.columns(2)

    dim_names = list(scores.keys())
    max_per_dim = [sum(w for _, w, _ in DIMENSIONES[d]["items"]) for d in dim_names]
    normalized = [round(s / m * 10, 2) for s, m in zip(scores.values(), max_per_dim)]
    colores_dims = [DIMENSIONES[d]["color"] for d in dim_names]

    with col_radar:
        st.markdown("### 📡 Perfil Interseccional")
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=normalized + [normalized[0]],
            theta=dim_names + [dim_names[0]],
            fill="toself",
            fillcolor="rgba(252,191,30,0.25)",
            line=dict(color="#FCBF1E", width=2.5),
            name="Riesgo"
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 10], tickfont=dict(size=10)),
                angularaxis=dict(tickfont=dict(size=11)),
            ),
            showlegend=False,
            margin=dict(l=30, r=30, t=30, b=30),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=350,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_barras:
        st.markdown("### 📊 Puntaje por Dimensión")
        df_scores = pd.DataFrame({
            "Dimensión": dim_names,
            "Puntaje": list(scores.values()),
            "Máximo": max_per_dim,
        })
        df_scores["Porcentaje"] = (df_scores["Puntaje"] / df_scores["Máximo"] * 100).round(1)

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=df_scores["Porcentaje"],
            y=df_scores["Dimensión"],
            orientation="h",
            marker=dict(
                color=colores_dims,
                line=dict(width=0)
            ),
            text=[f"{p}%" for p in df_scores["Porcentaje"]],
            textposition="outside",
        ))
        fig_bar.add_vline(x=50, line_dash="dot", line_color="#FCBF1E", line_width=1.5,
                          annotation_text="50%", annotation_font_size=10)
        fig_bar.update_layout(
            xaxis=dict(range=[0, 115], showgrid=False, ticksuffix="%"),
            yaxis=dict(automargin=True),
            margin=dict(l=10, r=40, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=350,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── INTERSECCIONALIDADES ──────────────────
    st.markdown("<div class='yellow-divider'></div>", unsafe_allow_html=True)
    st.markdown("## 🔗 Intersecciones de Riesgo Identificadas")
    st.caption("Las dimensiones activas se cruzan entre sí, generando riesgos compuestos mayores que cada factor por separado.")

    intersecs_encontradas = []
    for intersec in INTERSECCIONES:
        d1, d2 = intersec["dims"]
        if scores.get(d1, 0) > 0 and scores.get(d2, 0) > 0:
            intersecs_encontradas.append(intersec)

    if intersecs_encontradas:
        col_i1, col_i2 = st.columns(2)
        for i, intersec in enumerate(intersecs_encontradas):
            col = col_i1 if i % 2 == 0 else col_i2
            badge_color = {"crítico": "#E74C3C", "alto": "#E67E22", "moderado": "#F39C12"}.get(intersec["nivel_alerta"], "#888")
            with col:
                st.markdown(f"""
                <div class='intersec-card'>
                    <div class='intersec-title'>
                        <span class='intersec-badge'>{intersec['dims'][0]}</span>
                        <span style='color:#bbb;font-size:0.8rem;'>✕</span>
                        <span class='intersec-badge'>{intersec['dims'][1]}</span>
                        <span style='float:right;background:{badge_color};color:white;font-size:0.72rem;padding:2px 8px;border-radius:12px;font-weight:600;'>{intersec['nivel_alerta'].upper()}</span>
                    </div>
                    <div style='font-family:Syne,sans-serif;font-weight:700;font-size:0.88rem;color:#333;margin:6px 0 4px;'>{intersec['titulo']}</div>
                    <div class='intersec-body'>{intersec['descripcion']}</div>
                </div>
                """, unsafe_allow_html=True)
        if any(i["nivel_alerta"] == "crítico" for i in intersecs_encontradas):
            st.error("⚠️ Se detectó al menos una intersección CRÍTICA. El riesgo real puede ser superior al puntaje individual.")
    else:
        st.info("No se identificaron intersecciones significativas entre dimensiones activas. El riesgo parece concentrarse en una sola dimensión.")

    # ── RUTA DE INTERVENCIÓN ──────────────────
    st.markdown("<div class='yellow-divider'></div>", unsafe_allow_html=True)
    st.markdown("## 🗺️ Ruta de Intervención Sugerida")

    ruta = RUTAS[risk_level]
    st.markdown(f"""
    <div class='ruta-card {ruta["clase"]}'>
        <div class='ruta-title'>{ruta['titulo']}</div>
        <p style='font-size:0.88rem;color:#555;margin-bottom:12px;'>{ruta['descripcion']}</p>
        {''.join(f"<div class='ruta-item'>• {a}</div>" for a in ruta['acciones'])}
    </div>
    """, unsafe_allow_html=True)

    # Acciones específicas por dimensión activa
    acciones_especificas = []
    for dim, datos in ACCIONES_DIM.items():
        if scores.get(dim, 0) >= datos["umbral"]:
            acciones_especificas.append((dim, datos))

    if acciones_especificas:
        st.markdown("### 🎯 Acciones Específicas por Dimensión Prioritaria")
        for dim, datos in acciones_especificas:
            color = DIMENSIONES[dim]["color"]
            st.markdown(f"""
            <div class='accion-dim' style='border-left:4px solid {color};'>
                <strong>{datos['icono']} {dim}</strong><br>
                {datos['accion']}
            </div>
            """, unsafe_allow_html=True)

    # ── RESUMEN EXPORTABLE ────────────────────
    st.markdown("<div class='yellow-divider'></div>", unsafe_allow_html=True)
    st.markdown("### 📄 Resumen del Caso")

    resumen_lineas = [
        f"NIVEL DE RIESGO: {risk_level} ({total_score}/{max_score} pts)",
        "",
        "DIMENSIONES AFECTADAS:",
    ]
    for dim in dims_activas:
        resumen_lineas.append(f"  • {dim}: {scores[dim]} pts")
        for item in items_activos_por_dim[dim]:
            resumen_lineas.append(f"      - {item}")

    if intersecs_encontradas:
        resumen_lineas.append("")
        resumen_lineas.append("INTERSECCIONES IDENTIFICADAS:")
        for i in intersecs_encontradas:
            resumen_lineas.append(f"  • {i['titulo']} [{i['nivel_alerta'].upper()}]")

    resumen_lineas.append("")
    resumen_lineas.append(f"RUTA SUGERIDA: {ruta['titulo']}")
    for a in ruta["acciones"]:
        resumen_lineas.append(f"  • {a}")

    resumen_texto = "\n".join(resumen_lineas)
    st.text_area("Copie este resumen para incluir en el expediente del estudiante:", resumen_texto, height=220)
    st.download_button(
        label="⬇️ Descargar resumen (.txt)",
        data=resumen_texto,
        file_name="evaluacion_riesgo_estudiante.txt",
        mime="text/plain"
    )
