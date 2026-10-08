#!/usr/bin/env python3
"""
Genera las páginas de cada servicio (una carpeta por servicio con su
index.html) a partir de la plantilla y los textos de abajo.

Uso (desde la raíz del sitio):
    python3 herramientas/generar_servicios.py

Si cambia el header, el menú, el footer o un texto de servicio, se edita
ACÁ y se vuelve a correr: pisa las 9 páginas. No editar los index.html de
las carpetas a mano porque se pierden los cambios en la próxima corrida.

Los textos legales deben ser revisados por el Dr. Crespo antes de publicar.
"""

import html
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DOMINIO = "https://drpablocrespo.com/"
VERSION = "20261008d"  # mismo ?v= que index.html
WHATSAPP = "5492804607019"

SERVICIOS = [
    {
        "slug": "derecho-penal",
        "nombre": "Derecho Penal",
        "title": "Abogado Penalista en San Isidro | Dr. Pablo Luis Crespo",
        "description": "Defensa penal en San Isidro, CABA y Trelew: asistencia en comisarías y fiscalías, excarcelaciones, audiencias, juicio oral y recursos.",
        "lead": "Defensa penal desde el primer momento: en la comisaría, en la fiscalía y durante todo el proceso.",
        "imagen": ("servicios_1.jpg", 900, 598, "Firma de un escrito judicial"),
        "intro": [
            "En una causa penal, las primeras horas y las primeras decisiones pueden definir el rumbo del proceso. Si fuiste detenido, citado a declarar o denunciado, es clave contar con un abogado defensor antes de dar cualquier paso.",
            "Analizamos el expediente, te explicamos con claridad cada etapa y diseñamos una estrategia de defensa a medida, con presencia en cada audiencia.",
        ],
        "incluye": [
            ("Defensa desde la investigación", "Intervención desde la etapa inicial, con acceso al expediente y control de cada medida."),
            ("Comisarías y fiscalías", "Asistencia en detenciones, citaciones y declaraciones."),
            ("Excarcelaciones y libertad", "Pedidos de excarcelación, eximición de prisión y morigeración de medidas."),
            ("Audiencias y juicio oral", "Preparación y litigio en cada audiencia y en el juicio."),
            ("Recursos y apelaciones", "Revisión de resoluciones desfavorables ante instancias superiores."),
        ],
        "faq": [
            ("¿Qué hago si me citan a declarar?", "No te presentes sin abogado. Antes de declarar tenés derecho a entrevistarte con tu defensor, y también a negarte a declarar sin que eso se use en tu contra. Consultanos apenas recibas la citación."),
            ("¿Qué pasa si detienen a un familiar?", "Comunicate cuanto antes. Podemos averiguar su situación procesal, presentarnos en la causa y, si corresponde, pedir la excarcelación."),
            ("¿Puedo consultar si todavía no hay una denuncia?", "Sí. Una consulta preventiva permite anticipar escenarios y evitar errores que después son difíciles de revertir."),
        ],
    },
    {
        "slug": "victimas-y-querellas",
        "nombre": "Víctimas y querellas",
        "title": "Querella Penal y Víctimas de Delitos | Dr. Pablo Luis Crespo",
        "description": "Representación de víctimas de delitos como querellantes en San Isidro, CABA y Trelew: denuncia, seguimiento de la causa, audiencias y juicio.",
        "lead": "Representación de víctimas para que su voz tenga peso real en el proceso penal.",
        "imagen": ("servicio_querellas.jpg", 880, 587, "Estatua de la justicia con su balanza"),
        "intro": [
            "La víctima de un delito tiene derecho a participar activamente del proceso: puede constituirse como parte querellante, proponer pruebas, intervenir en audiencias y cuestionar las decisiones que la afecten.",
            "Te acompañamos desde la denuncia, con un seguimiento activo de la investigación y comunicación clara sobre cada avance.",
        ],
        "incluye": [
            ("Denuncia penal", "Armado y presentación de una denuncia clara y completa."),
            ("Querella", "Constitución como parte querellante, con abogado propio en la causa."),
            ("Seguimiento de la investigación", "Propuesta de pruebas y control de cada paso de la fiscalía."),
            ("Audiencias y juicio oral", "Representación de la víctima hasta la sentencia."),
        ],
        "faq": [
            ("¿Qué es ser querellante?", "Es intervenir en la causa como parte, con abogado propio, para impulsar la investigación y participar de las decisiones, y no solo como testigo."),
            ("¿Puedo ser querellante si ya hice la denuncia?", "En general sí: la constitución como querellante puede pedirse con la causa en trámite. Conviene hacerlo cuanto antes para intervenir desde el comienzo."),
            ("¿Necesito abogado para denunciar?", "No es obligatorio para hacer la denuncia, pero sí para constituirse como querellante. Asesorarte desde el inicio ayuda a que la denuncia sea sólida."),
        ],
    },
    {
        "slug": "derecho-de-familia",
        "nombre": "Derecho de Familia",
        "title": "Abogado de Familia en San Isidro | Dr. Pablo Luis Crespo",
        "description": "Abogado de familia en San Isidro, CABA y Trelew: cuidado personal, régimen de comunicación, filiación y acuerdos, con foco en hijos e hijas.",
        "lead": "Conflictos familiares abordados con firmeza jurídica y cuidado de los vínculos, especialmente de hijos e hijas.",
        "imagen": ("servicios_2.jpg", 900, 600, "Balanza de la justicia"),
        "intro": [
            "Los conflictos familiares requieren una mirada que combine lo jurídico con lo humano. Priorizamos los acuerdos cuando son posibles y actuamos con firmeza judicial cuando hace falta.",
            "Trabajamos cada caso en detalle, explicando las alternativas, los tiempos y los costos reales de cada camino.",
        ],
        "incluye": [
            ("Cuidado personal", "Definición de con quién conviven los hijos y responsabilidad parental."),
            ("Régimen de comunicación", "Acuerdos o reclamos judiciales para sostener el vínculo con los hijos."),
            ("Filiación", "Reconocimiento e impugnación de filiación."),
            ("Acuerdos y mediación", "Convenios extrajudiciales y acompañamiento en la mediación."),
        ],
        "faq": [
            ("¿Qué es el cuidado personal?", "Es lo que antes se llamaba \"tenencia\": define con quién conviven los hijos. El Código Civil y Comercial prioriza el cuidado compartido."),
            ("¿Qué hago si no se cumple el régimen de comunicación?", "Se puede pedir judicialmente su cumplimiento y, según el caso, medidas para garantizarlo."),
            ("¿Es obligatorio pasar por mediación?", "En muchos casos sí: antes de iniciar el juicio hay una instancia de mediación. Te explicamos cómo aplica en tu caso y jurisdicción."),
        ],
    },
    {
        "slug": "divorcios",
        "nombre": "Divorcios",
        "title": "Abogado de Divorcios en San Isidro | Dr. Pablo Luis Crespo",
        "description": "Divorcios de común acuerdo o unilaterales en San Isidro, CABA y Trelew: propuesta reguladora, compensación económica, bienes y vivienda.",
        "lead": "Divorcios de común acuerdo o unilaterales, con una estrategia clara para los bienes, los hijos y la compensación económica.",
        "imagen": ("servicio_divorcios.jpg", 900, 600, "Firma de un convenio"),
        "intro": [
            "En Argentina el divorcio no requiere expresar causas: puede pedirlo uno solo de los cónyuges o ambos de común acuerdo. Lo importante es cómo se resuelven sus efectos: bienes, vivienda, hijos y compensación económica.",
            "Buscamos acuerdos sólidos que eviten conflictos futuros, y litigamos con firmeza cuando no hay acuerdo posible.",
        ],
        "incluye": [
            ("Divorcio de común acuerdo", "Presentación conjunta con propuesta reguladora."),
            ("Divorcio unilateral", "Cuando uno de los cónyuges decide avanzar solo."),
            ("Compensación económica", "Reclamo o defensa ante un desequilibrio económico causado por el divorcio."),
            ("División de bienes", "Liquidación de la comunidad y atribución de la vivienda familiar."),
        ],
        "faq": [
            ("¿Necesito el acuerdo de mi pareja para divorciarme?", "No. Cualquiera de los cónyuges puede pedir el divorcio sin expresar causa, acompañando una propuesta sobre sus efectos."),
            ("¿Qué es la compensación económica?", "Es una prestación para el cónyuge al que el divorcio le genera un desequilibrio económico manifiesto. Tiene un plazo para reclamarse, por eso conviene consultarlo a tiempo."),
            ("¿Cuánto tarda un divorcio?", "El divorcio en sí suele resolverse rápido. Lo que más tiempo lleva, si hay conflicto, es resolver los bienes y las cuestiones de los hijos."),
        ],
    },
    {
        "slug": "alimentos",
        "nombre": "Alimentos",
        "title": "Abogado de Alimentos y Cuota Alimentaria | Dr. Pablo Luis Crespo",
        "description": "Fijación, aumento y cobro de cuota alimentaria en San Isidro, CABA y Trelew. Alimentos provisorios y ejecución de cuotas adeudadas.",
        "lead": "Fijación, actualización y cobro de la cuota alimentaria para hijos e hijas.",
        "imagen": ("servicio_alimentos.jpg", 900, 646, "Acuerdo cerrado con un apretón de manos"),
        "intro": [
            "La cuota alimentaria cubre las necesidades de hijos e hijas: manutención, educación, salud, vivienda, vestimenta y esparcimiento. Ambos progenitores tienen la obligación de aportar según sus posibilidades.",
            "Te ayudamos a fijarla, a actualizarla cuando cambian las circunstancias y a ejecutarla si no se paga.",
        ],
        "incluye": [
            ("Fijación de cuota", "Por acuerdo o por vía judicial."),
            ("Aumento o reducción", "Actualización cuando cambian los ingresos o las necesidades."),
            ("Alimentos provisorios", "Cuota durante el juicio para cubrir necesidades urgentes."),
            ("Ejecución de cuotas adeudadas", "Reclamo de lo que no se pagó, con embargos si corresponde."),
        ],
        "faq": [
            ("¿Hasta qué edad corresponden los alimentos?", "En general hasta los 21 años, y hasta los 25 si el hijo o la hija estudia o se capacita y eso le impide mantenerse."),
            ("¿Qué hago si no pagan la cuota?", "Se puede iniciar la ejecución de lo adeudado y pedir medidas como embargos. Cuanto antes se reclame, mejor."),
            ("¿Se puede pedir una cuota mientras dura el juicio?", "Sí: pueden pedirse alimentos provisorios para cubrir las necesidades urgentes durante el proceso."),
        ],
    },
    {
        "slug": "sucesiones",
        "nombre": "Sucesiones",
        "title": "Abogado de Sucesiones en San Isidro | Dr. Pablo Luis Crespo",
        "description": "Trámite sucesorio completo en San Isidro, CABA y Trelew: declaratoria de herederos, testamentos, inscripción de bienes y partición.",
        "lead": "Trámite sucesorio completo, desde el inicio hasta la inscripción de los bienes a nombre de los herederos.",
        "imagen": ("servicio_sucesiones.jpg", 900, 600, "Biblioteca jurídica con bustos"),
        "intro": [
            "Cuando fallece un familiar, la sucesión es el trámite judicial que permite determinar quiénes son los herederos y transmitirles los bienes. Nos ocupamos de todo el proceso para que no tengas que lidiar con cada paso.",
            "Desde el principio te explicamos la documentación necesaria, los costos y los tiempos estimados.",
        ],
        "incluye": [
            ("Inicio de la sucesión", "Armado y presentación del expediente."),
            ("Declaratoria de herederos", "Determinación judicial de quiénes heredan."),
            ("Sucesiones testamentarias", "Cuando la persona dejó testamento."),
            ("Inscripción y partición", "Inscripción de inmuebles, vehículos y otros bienes, y división entre herederos."),
        ],
        "faq": [
            ("¿Qué documentación necesito para iniciar una sucesión?", "Principalmente el acta de defunción, las partidas que acrediten el vínculo con la persona fallecida y la información sobre sus bienes. En la primera consulta te damos la lista completa para tu caso."),
            ("¿Cuánto tarda una sucesión?", "Depende del juzgado, de la cantidad de herederos y de los bienes. Si hay acuerdo y la documentación está completa, el trámite es mucho más ágil."),
            ("¿Qué pasa si los herederos no se ponen de acuerdo?", "Se puede avanzar igual con la declaratoria de herederos y, si no hay acuerdo, resolver la partición por vía judicial."),
        ],
    },
    {
        "slug": "violencia-de-genero",
        "nombre": "Violencia de género y familiar",
        "title": "Abogado en Violencia de Género y Familiar | Dr. Pablo Luis Crespo",
        "description": "Medidas urgentes de protección, prohibición de acercamiento y exclusión del hogar en San Isidro, CABA y Trelew. Acompañamiento civil y penal.",
        "lead": "Medidas urgentes de protección y acompañamiento integral en las causas civiles y penales.",
        "imagen": ("servicios_3.jpg", 900, 600, "Libros de derecho"),
        "aviso": "Si estás en peligro ahora, llamá al 911. La Línea 144 brinda contención y asesoramiento gratuito las 24 horas, todos los días.",
        "intro": [
            "Frente a una situación de violencia, lo primero es la protección. Solicitamos medidas urgentes y te acompañamos en la denuncia y en todo el proceso, con reserva y cuidado.",
            "Coordinamos las actuaciones civiles y penales para que las medidas sean efectivas y se sostengan en el tiempo.",
        ],
        "incluye": [
            ("Medidas urgentes de protección", "Pedidos al juzgado para frenar la situación de violencia."),
            ("Prohibición de acercamiento", "Y prohibición de contacto por cualquier medio."),
            ("Exclusión del hogar", "Para que la persona agresora deje la vivienda."),
            ("Protección de hijos e hijas", "Medidas específicas para resguardar a los niños."),
            ("Actuaciones civiles y penales", "Seguimiento coordinado de ambas causas."),
        ],
        "faq": [
            ("¿Qué medidas de protección se pueden pedir?", "Entre otras, prohibición de acercamiento y de contacto, exclusión de la persona agresora del hogar y medidas para proteger a hijos e hijas. El juzgado puede dictarlas con urgencia."),
            ("¿Tengo que hacer una denuncia penal para pedir medidas?", "No necesariamente: las medidas de protección también pueden pedirse ante la justicia de familia. Evaluamos en cada caso qué vía conviene."),
            ("¿La consulta es confidencial?", "Sí. Todo lo que nos cuentes está amparado por el secreto profesional."),
        ],
    },
    {
        "slug": "amparos-de-salud",
        "nombre": "Amparos de salud",
        "title": "Abogado de Amparos de Salud | Dr. Pablo Luis Crespo",
        "description": "Amparos de salud contra obras sociales y prepagas: medicamentos, tratamientos, cirugías, internaciones y discapacidad. San Isidro, CABA y Trelew.",
        "lead": "Reclamos judiciales urgentes cuando la obra social o la prepaga no cubre a tiempo lo que tu salud necesita.",
        "imagen": ("servicio_amparos.jpg", 900, 600, "Estetoscopio sobre una mesa"),
        "intro": [
            "Asesoramiento y representación en amparos de salud para obtener la cobertura de medicamentos, tratamientos, cirugías, internaciones, estudios, rehabilitación, diálisis, prestaciones por discapacidad y demás servicios indispensables para proteger la salud y la vida.",
            "Analizamos cada caso con rapidez, reunimos la documentación necesaria y promovemos las medidas judiciales urgentes que correspondan para reclamar el acceso efectivo a la prestación indicada.",
        ],
        "incluye": [
            ("Medicamentos", "Cobertura de medicación indicada por tu médico."),
            ("Tratamientos y cirugías", "Incluidas internaciones y estudios."),
            ("Rehabilitación y diálisis", "Continuidad de tratamientos prolongados."),
            ("Prestaciones por discapacidad", "Terapias, transporte, educación y apoyos."),
            ("Medidas cautelares urgentes", "Para obtener la cobertura mientras sigue el juicio."),
        ],
        "faq": [
            ("¿Qué es un amparo de salud?", "Es una acción judicial rápida para exigir que la obra social, la prepaga o el Estado cubra una prestación indicada por tu médico cuando la niegan o la demoran."),
            ("¿Qué necesito para iniciarlo?", "La indicación médica, la documentación de tu cobertura y, si existe, la negativa. Si la obra social o la prepaga no responde, también se puede avanzar."),
            ("¿Cuánto tarda?", "Junto con el amparo suele pedirse una medida cautelar para que la cobertura se otorgue de inmediato, mientras sigue el juicio."),
        ],
    },
    {
        "slug": "ciudadania-italiana",
        "nombre": "Ciudadanía italiana",
        "title": "Ciudadanía Italiana: Asesoramiento Legal | Dr. Pablo Luis Crespo",
        "description": "Ciudadanía italiana con acompañamiento legal: Ley 74/2025, hijos menores, armado de carpeta, traducciones, actas y asesoría online.",
        "lead": "Tu ciudadanía italiana, con respaldo legal de punta a punta: armado de carpeta, traducciones, actas y asesoría online, desde cualquier lugar.",
        "imagen": ("ciudadania_vittoriano.jpg", 900, 1100, "Bandera italiana sobre el monumento a Víctor Manuel II en Roma"),
        "logo": True,
        "plazo": ("Plazo prorrogado · Hijos menores", "Hasta el 31 de mayo de 2029", "Para quienes eran menores al 24/05/2025. Es perentorio: una vez vencido, no se reciben más solicitudes."),
        "casos": [
            ("Tus hijos eran menores", "Menores de 18 al 24/05/2025, hijos de un ciudadano italiano por nacimiento reconocido por vía administrativa, judicial o con turno otorgado antes del 27/03/2025."),
            ("Eras menor y ahora sos mayor", "Si ya cumpliste 18, la declaración la tenés que hacer vos personalmente, dentro del mismo plazo."),
            ("Naturalización del ascendiente", "Si ocurrió cuando su hijo era menor, tu línea de ciudadanía podría continuar. Lo evaluamos con tu documentación."),
        ],
        "intro": [
            "La reforma de la Ley 74/2025 cambió las reglas de la ciudadanía italiana por descendencia. Hoy es clave revisar cada caso en detalle: cómo obtuvo la ciudadanía tu ascendiente, en qué fecha y qué documentación existe.",
            "Nos ocupamos del análisis, del armado completo de la carpeta y de acompañarte hasta la declaración ante el consulado.",
        ],
        "incluye": [
            ("Armado de carpeta", "Reunimos y ordenamos toda la documentación de tu caso."),
            ("Traducciones", "Traducciones de la documentación necesaria para el trámite."),
            ("Actas de Italia y España", "Gestión de actas para ambas ciudadanías."),
            ("Asesoría online", "Consultas y seguimiento a distancia, sin importar dónde vivas."),
        ],
        "pasos": [
            ("Consulta inicial", "Nos escribís y vemos si tu caso reúne los requisitos."),
            ("Análisis del caso", "Revisamos cómo obtuvo la ciudadanía tu ascendiente y qué documentación hay."),
            ("Armado de carpeta", "Preparamos actas, traducciones y toda la documentación."),
            ("Declaración en el consulado", "El trámite requiere documentación y una declaración presencial."),
        ],
        "faq": [
            ("¿La prórroga significa ciudadanía automática?", "No. Hay que verificar cómo obtuvo la ciudadanía el progenitor italiano y si el caso reúne los requisitos de la ley."),
            ("¿Y si ya cumplí 18 años?", "Si eras menor al 24/05/2025, la declaración la hacés vos personalmente, dentro del mismo plazo."),
            ("¿Qué pasa si se vence el plazo?", "El plazo del 31/05/2029 es perentorio: una vez vencido, no se reciben más solicitudes. Conviene revisarlo con tiempo."),
        ],
    },
]


def e(texto):
    return html.escape(texto, quote=True)


def json_ld(s):
    url = f"{DOMINIO}{s['slug']}/"
    grafo = [
        {
            "@type": "Service",
            "@id": f"{url}#servicio",
            "name": s["nombre"],
            "serviceType": s["nombre"],
            "description": s["description"],
            "url": url,
            "areaServed": ["San Isidro", "Zona Norte del Gran Buenos Aires", "Capital Federal", "Trelew"],
            "provider": {
                "@type": "Attorney",
                "@id": f"{DOMINIO}#attorney",
                "name": "Pablo Luis Crespo",
                "url": DOMINIO,
                "telephone": f"+{WHATSAPP}",
            },
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Inicio", "item": DOMINIO},
                {"@type": "ListItem", "position": 2, "name": "Servicios", "item": f"{DOMINIO}#servicios"},
                {"@type": "ListItem", "position": 3, "name": s["nombre"], "item": url},
            ],
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in s["faq"]
            ],
        },
    ]
    datos = json.dumps({"@context": "https://schema.org", "@graph": grafo}, ensure_ascii=False, indent=2)
    return "\n".join("      " + linea for linea in datos.splitlines())


def prosa(items):
    """Ítems como párrafos que arrancan con el tema en negrita."""
    return "\n\n".join(
        f"            <p><strong>{e(t)}.</strong> {e(d)}</p>" for t, d in items
    )


def bloque(titulo, cuerpo, clase=""):
    """Sección de texto: título a la izquierda, texto a la derecha."""
    return f"""
      <section class="section page-article{(' ' + clase) if clase else ''}">
        <div class="container article-layout">
          <div class="article-aside">
            <h2>{e(titulo)}</h2>
          </div>

          <div class="article-body">
{cuerpo}
          </div>
        </div>
      </section>
"""


def envoltorio(titulo, descripcion, url, cuerpo, robots="index, follow", json="", clase_body="service-page", scripts_extra=""):
    """Head, header, menú, footer y WhatsApp flotante: compartidos por todas
    las páginas generadas (servicios y /agendar/)."""
    bloque_json = f"""
    <script type="application/ld+json">
{json}
    </script>
""" if json else ""

    return f"""<!doctype html>
<html lang="es-AR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <!-- Página generada por herramientas/generar_servicios.py: no editar a mano -->

    <title>{e(titulo)}</title>

    <meta name="description" content="{e(descripcion)}" />
    <meta name="robots" content="{robots}" />
    <meta name="theme-color" content="#dbe8f3" />

    <link rel="canonical" href="{url}" />

    <meta property="og:type" content="website" />
    <meta property="og:locale" content="es_AR" />
    <meta property="og:title" content="{e(titulo)}" />
    <meta property="og:description" content="{e(descripcion)}" />
    <meta property="og:image" content="{DOMINIO}img/og-image.jpg" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:url" content="{url}" />
    <meta property="og:site_name" content="Pablo Luis Crespo - Abogado" />
    <meta name="twitter:card" content="summary_large_image" />

    <link rel="icon" href="../img/favicon-32x32.png" type="image/png" sizes="32x32" />
    <link rel="icon" href="../img/favicon-16x16.png" type="image/png" sizes="16x16" />
    <link rel="apple-touch-icon" href="../img/apple-touch-icon.png" sizes="180x180" />

    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Forum&display=swap"
      rel="stylesheet"
    />

    <link rel="stylesheet" href="../style-juridico.css?v={VERSION}" />
{bloque_json}
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js" defer></script>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/ScrollTrigger.min.js" defer></script>
  </head>

  <body class="{clase_body}">
    <!-- HEADER -->
    <header class="header" data-header>
      <div class="header-inner">
        <a href="../" class="header-logo" aria-label="MCDV & Asociados - Inicio">
          <img src="../img/logo-mcdv.png" alt="MCDV & Asociados" width="272" height="284" />
        </a>

        <a href="../" class="header-name" aria-label="Dr. Pablo Luis Crespo - Inicio">
          <span class="header-name-dr">Dr.</span>
          Pablo Luis Crespo
        </a>

        <button class="menu-toggle" type="button" aria-label="Abrir menú" aria-expanded="false" data-menu-toggle>
          <span class="menu-label">Menu</span>
          <span class="menu-icon" aria-hidden="true">
            <span></span>
            <span></span>
          </span>
        </button>
      </div>
    </header>

    <!-- MENU -->
    <div class="menu-overlay" data-menu>
      <div class="menu-overlay-bg"></div>

      <div class="menu-panel">
        <div class="menu-panel-top">
          <span>Índice</span>
          <button class="menu-close" type="button" aria-label="Cerrar menú" data-menu-close>
            <span></span>
            <span></span>
          </button>
        </div>

        <nav class="menu-navigation" aria-label="Navegación principal">
          <a href="../" data-menu-link><span class="menu-link-text">Inicio</span></a>
          <a href="../#profesional" data-menu-link><span class="menu-link-text">Sobre mí</span></a>
          <a href="../#servicios" data-menu-link><span class="menu-link-text">Servicios</span></a>
          <a href="../ciudadania-italiana/" data-menu-link><span class="menu-link-text">Ciudadanía Italiana</span></a>
          <a href="../amparos-de-salud/" data-menu-link><span class="menu-link-text">Amparos de Salud</span></a>
          <a href="../#about" data-menu-link><span class="menu-link-text">Método de trabajo</span></a>
          <a href="../#contact" data-menu-link><span class="menu-link-text">Contacto</span></a>
        </nav>

        <div class="menu-panel-bottom">
          <div>
            <span class="menu-small-label">Atención</span>
            <span>Lunes a Viernes · 09 — 18 hs</span>
          </div>
        </div>
      </div>
    </div>

{cuerpo}
    <!-- FOOTER -->
    <footer class="footer">
      <div class="container footer-main">
        <div class="footer-brand">
          <span class="footer-name"> Dr. Pablo Luis Crespo </span>
          <span class="footer-role">Abogado · Derecho Penal y de Familia</span>
          <span class="footer-phone">
            <a href="tel:+{WHATSAPP}">Llamar al estudio</a>
            · Lunes a Viernes, 9 a 18 hs
          </span>
        </div>
      </div>

      <div class="container footer-contact">
        <div class="footer-address">
          <span class="footer-address-city">San Isidro</span>
          <a href="https://maps.google.com/?q=Ituzaing%C3%B3+522+San+Isidro+Buenos+Aires" target="_blank" rel="noopener" class="footer-map-link">Ituzaingó 522</a>
        </div>

        <div class="footer-address">
          <span class="footer-address-city">CABA</span>
          <a href="https://maps.google.com/?q=Av.+Corrientes+1464+Of.+302+Buenos+Aires" target="_blank" rel="noopener" class="footer-map-link">Av. Corrientes 1464, Of. 302</a>
        </div>

        <div class="footer-address">
          <span class="footer-address-city">Trelew, Chubut</span>
          <a href="https://maps.google.com/?q=La+Madrid+1190+Trelew+Chubut" target="_blank" rel="noopener" class="footer-map-link">La Madrid 1190</a>
        </div>
      </div>

      <div class="container footer-bottom">
        <span class="footer-studio">
          Desarrollo y Diseño Web por
          <a href="https://wa.me/5492804713889?text=Hola%20Juli%C3%A1n%2C%20me%20interesa%20discutir%20un%20proyecto%20web." target="_blank" rel="noopener" class="footer-studio-link">Julián Luchelli Fassa</a>
        </span>
      </div>
    </footer>

    <!-- WHATSAPP FLOTANTE -->
    <a href="#" id="waFloat" class="wa-float" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">
      <img src="../img/wsp.png" alt="WhatsApp" class="wa-icon" width="52" height="52" />
    </a>

    <script src="../script.js?v={VERSION}" defer></script>
{scripts_extra}  </body>
</html>
"""


def pagina(s):
    url = f"{DOMINIO}{s['slug']}/"
    img, w, h, alt = s["imagen"]
    otros = [o for o in SERVICIOS if o["slug"] != s["slug"]]

    # Con logo (ciudadanía): la foto queda a la izquierda, detrás del
    # texto, y se funde en azul hacia la derecha, donde va el logo en PNG.
    con_logo = bool(s.get("logo"))
    clase_hero = "page-hero page-hero--logo" if con_logo else "page-hero"
    abre_copy = (
        '<div class="container page-hero-inner">\n          <div class="page-hero-copy">'
        if con_logo else '<div class="container page-hero-copy">'
    )
    marca = ""
    if con_logo:
        marca = """
          <div class="page-hero-brand">
            <img
              src="../img/logo-ciudadania.png"
              alt="Cittadinanza Ital — Estudio de Ciudadanías Italianas"
              width="560"
              height="419"
            />
          </div>
"""
    cierra_copy = "</div>" + marca + "        </div>" if con_logo else "</div>"

    aviso = ""
    if s.get("aviso"):
        aviso = f"""
      <div class="page-alert" role="note">
        <div class="container">
          <p>{e(s['aviso'])}</p>
        </div>
      </div>
"""

    plazo = ""
    if s.get("plazo"):
        etiqueta, fecha, texto = s["plazo"]
        plazo = f"""
      <section class="page-deadline">
        <div class="container page-deadline-inner">
          <div>
            <span class="eyebrow">{e(etiqueta)}</span>
            <p class="page-deadline-date">{e(fecha)}</p>
          </div>
          <p>{e(texto)}</p>
        </div>
      </section>
"""

    casos = ""
    if s.get("casos"):
        casos = bloque("¿En qué casos podemos ayudarte?", f"""          <div class="article-points">
{prosa(s['casos'])}
          </div>""", "page-article--alt")

    parrafos = "\n\n".join(f"            <p>{e(p)}</p>" for p in s["intro"])

    pasos = ""
    if s.get("pasos"):
        pasos = bloque("Cómo trabajamos", f"""          <div class="article-points">
{prosa(s['pasos'])}
          </div>""")

    faqs = "\n\n".join(
        f"""            <details class="faq-item">
              <summary>{e(q)}</summary>
              <p>{e(a)}</p>
            </details>"""
        for q, a in s["faq"]
    )
    relacionados = "\n".join(
        f'            <li><a href="../{o["slug"]}/">{e(o["nombre"])}</a></li>' for o in otros
    )

    cuerpo = f"""    <main>
      <!-- ENCABEZADO: foto de fondo que aparece en degradé hacia la derecha -->
      <section class="{clase_hero}">
        <img
          class="page-hero-bg"
          src="../img/{img}"
          alt="{e(alt)}"
          width="{w}"
          height="{h}"
          fetchpriority="high"
        />

        {abre_copy}
          <nav class="breadcrumb" aria-label="Ruta de navegación">
            <a href="../">Inicio</a>
            <span aria-hidden="true">/</span>
            <a href="../#servicios">Servicios</a>
            <span aria-hidden="true">/</span>
            <span aria-current="page">{e(s['nombre'])}</span>
          </nav>

          <h1>{e(s['nombre'])}</h1>

          <p class="page-lead">{e(s['lead'])}</p>

          <a href="../agendar/" class="dark-button">
            <span>Agendar consulta</span>
            <span>↗</span>
          </a>
        {cierra_copy}
      </section>
{aviso}{plazo}
      <!-- TEXTO PRINCIPAL -->{bloque("Cómo te acompañamos", f"""{parrafos}

            <h3>Qué incluye</h3>

          <div class="article-points">
{prosa(s['incluye'])}
          </div>""")}{casos}
{pasos}
      <!-- PREGUNTAS FRECUENTES -->
      <section class="section page-faq">
        <div class="container faq-layout">
          <div class="faq-aside">
            <h2>Preguntas frecuentes</h2>
            <p>¿Tenés otra duda? La resolvemos en la primera consulta.</p>
          </div>

          <div class="faq-list">
{faqs}
          </div>
        </div>
      </section>

      <!-- LLAMADO A LA ACCIÓN -->
      <section class="page-cta">
        <div class="container page-cta-inner">
          <h2>¿Querés que analicemos tu caso?</h2>

          <p>
            Elegí día y horario y reservá tu consulta: presencial en CABA o
            virtual desde cualquier lugar.
          </p>

          <a href="../agendar/" class="dark-button">
            <span>Agendar consulta</span>
            <span>↗</span>
          </a>
        </div>
      </section>

      <!-- OTRAS ÁREAS -->
      <section class="section page-related">
        <div class="container">
          <h2>Otras áreas de práctica</h2>

          <ul class="page-related-list">
{relacionados}
          </ul>
        </div>
      </section>
    </main>

"""

    return envoltorio(s["title"], s["description"], url, cuerpo, json=json_ld(s))


def pagina_agendar():
    """Página /agendar/: fuera del menú y de Google (noindex). Solo se llega
    desde los botones "Agendar consulta". La lógica vive en agenda.js: sin
    backend, el cliente paga con el link de Mercado Pago del Dr. y le avisa
    el turno por WhatsApp."""
    cuerpo = """    <main>
      <!-- ENCABEZADO -->
      <section class="page-hero page-hero--compact">
        <div class="container page-hero-copy">
          <nav class="breadcrumb" aria-label="Ruta de navegación">
            <a href="../">Inicio</a>
            <span aria-hidden="true">/</span>
            <span aria-current="page">Agendar consulta</span>
          </nav>

          <h1>Agendar consulta</h1>

          <p class="page-lead">
            Elegí día y horario, pagá con Mercado Pago y mandá el comprobante
            por WhatsApp. Lunes a viernes, de 9 a 16 hs.
          </p>
        </div>
      </section>

      <!-- AGENDA -->
      <section class="section agenda">
        <div class="container agenda-layout">
          <form class="agenda-form" data-agenda novalidate>
            <p class="agenda-demo" data-agenda-demo hidden>
              Vista previa: todavía no está cargado el link de pago.
            </p>

            <fieldset class="agenda-step">
              <legend>Modalidad</legend>

              <div class="agenda-options">
                <label class="agenda-option">
                  <input type="radio" name="modalidad" value="virtual" required />
                  <span class="agenda-option-title">Virtual</span>
                  <span class="agenda-option-text">Videollamada, desde cualquier lugar.</span>
                </label>

                <label class="agenda-option">
                  <input type="radio" name="modalidad" value="presencial" />
                  <span class="agenda-option-title">Presencial</span>
                  <span class="agenda-option-text">Av. Corrientes 1464, Of. 302, CABA.</span>
                </label>
              </div>
            </fieldset>

            <fieldset class="agenda-step">
              <legend>Día y horario</legend>

              <p class="agenda-hint">Hora de Argentina (GMT−3).</p>

              <div class="agenda-calendar">
                <div class="agenda-calendar-head">
                  <button type="button" class="agenda-nav" data-agenda-prev aria-label="Mes anterior">‹</button>
                  <span class="agenda-month" data-agenda-month aria-live="polite"></span>
                  <button type="button" class="agenda-nav" data-agenda-next aria-label="Mes siguiente">›</button>
                </div>

                <div class="agenda-weekdays" aria-hidden="true">
                  <span>Lu</span><span>Ma</span><span>Mi</span><span>Ju</span><span>Vi</span><span>Sá</span><span>Do</span>
                </div>

                <div class="agenda-days" data-agenda-days></div>
              </div>

              <div class="agenda-times" data-agenda-times aria-live="polite"></div>
            </fieldset>

            <fieldset class="agenda-step">
              <legend>Tus datos</legend>

              <div class="agenda-fields">
                <label class="agenda-field-wide">
                  <span>Nombre y apellido</span>
                  <input type="text" name="nombre" autocomplete="name" required maxlength="120" />
                </label>

                <label class="agenda-field-wide">
                  <span>Contanos brevemente tu consulta</span>
                  <textarea name="consulta" rows="4" required maxlength="1000"></textarea>
                </label>
              </div>
            </fieldset>

            <p class="agenda-error" data-agenda-error role="alert" hidden></p>

            <button type="submit" class="dark-button agenda-submit">
              <span>Continuar</span>
              <span>→</span>
            </button>
          </form>

          <aside class="agenda-summary" aria-label="Resumen del turno">
            <h2>Tu turno</h2>

            <dl>
              <div><dt>Modalidad</dt><dd data-resumen="modalidad">—</dd></div>
              <div><dt>Día</dt><dd data-resumen="dia">—</dd></div>
              <div><dt>Horario</dt><dd data-resumen="hora">—</dd></div>
              <div><dt>Consulta</dt><dd data-resumen="precio">—</dd></div>
            </dl>
          </aside>

          <!-- CONFIRMAR: primero se lee, después se abre Mercado Pago -->
          <div class="agenda-done" data-agenda-done hidden tabindex="-1">
            <h2>Confirmá tu turno</h2>
            <p class="agenda-done-turno" data-agenda-done-text></p>

            <ol class="agenda-pasos">
              <li class="agenda-paso is-active" data-paso="pago">
                <span class="agenda-paso-num" aria-hidden="true">1</span>
                <div>
                  <h3>Pagá la consulta</h3>
                  <p class="agenda-pestana">
                    <strong>Atención:</strong> Mercado Pago se abre en otra
                    pestaña. Cuando termines de pagar, volvé a esta.
                  </p>
                  <a href="#" class="mp-button" data-agenda-pago target="_blank" rel="noopener">
                    Pagar con
                    <img src="../img/logo-mercadopago.png" alt="Mercado Pago" width="142" height="37" />
                  </a>
                </div>
              </li>

              <li class="agenda-paso" data-paso="whatsapp">
                <span class="agenda-paso-num" aria-hidden="true">2</span>
                <div>
                  <h3>Mandá el comprobante</h3>
                  <p>Tocá el botón y adjuntá la captura del pago en el chat.</p>
                  <a href="#" class="wa-button" data-agenda-whatsapp target="_blank" rel="noopener" aria-disabled="true">
                    <img src="../img/wsp.png" alt="" width="22" height="22" />
                    Enviar por WhatsApp
                  </a>
                  <p class="agenda-error" data-agenda-wa-error role="alert" hidden>Primero pagá la consulta (paso 1).</p>
                </div>
              </li>
            </ol>

            <p class="agenda-done-small">
              El Dr. verifica cada pago antes de confirmar el turno.
              <button type="button" class="agenda-volver" data-agenda-volver>Cambiar día u horario</button>
            </p>
          </div>
        </div>
      </section>
    </main>
"""
    return envoltorio(
        "Agendar consulta | Dr. Pablo Luis Crespo",
        "Reservá tu consulta con el Dr. Pablo Luis Crespo: elegí día y horario, virtual o presencial en CABA.",
        f"{DOMINIO}agendar/",
        cuerpo,
        robots="noindex, follow",
        clase_body="service-page agenda-page",
        scripts_extra=f'    <script src="../agenda.js?v={VERSION}" defer></script>\n',
    )


def main():
    for s in SERVICIOS:
        carpeta = RAIZ / s["slug"]
        carpeta.mkdir(exist_ok=True)
        (carpeta / "index.html").write_text(pagina(s), encoding="utf-8")
        print("ok", s["slug"])

    carpeta = RAIZ / "agendar"
    carpeta.mkdir(exist_ok=True)
    (carpeta / "index.html").write_text(pagina_agendar(), encoding="utf-8")
    print("ok agendar")


if __name__ == "__main__":
    main()
