# Contexto — Sitio Dr. Pablo Luis Crespo (abogado penal y de familia)

## Qué es
Sitio (HTML/CSS/JS puro, sin frameworks) del estudio del Dr. Pablo Luis
Crespo. Encargo de un amigo del usuario. Archivos: `index.html` (inicio),
9 carpetas de servicio con su `index.html` (generadas por
`herramientas/generar_servicios.py`), `style-juridico.css`, `script.js`,
`robots.txt`, `sitemap.xml`.

## Cómo retomar (estado al 2026-10-07)
- **Nada commiteado ni pusheado.** Todo lo de las rondas 4 a 16 está solo
  en el working tree. **El sitio en vivo sigue siendo el del commit
  `2490af8`** (anterior a todo esto): el primer push lleva todo junto. El repo despliega solo (GitHub → Hostinger; el `CNAME`
  es de GitHub Pages, así que hay que confirmar cuál sirve el dominio):
  **commitear/pushear SOLO cuando el usuario lo pida**, después del "ok"
  del cliente.
- **Desde la ronda 22 la agenda NO usa Google ni backend** (ver abajo).
  Lo de Google Calendar / Apps Script / MP Checkout Pro quedó respaldado
  en `~/Downloads/crespo-respaldo-2026-10-07-con-google-calendar/` (copia
  completa del sitio al 2026-10-07, antes del cambio). Las rondas 15 a 21
  son historia: describen esa versión.
- Copia para mostrar: carpeta `~/Downloads/preview-crespo/` y
  `~/Downloads/preview-crespo.zip` (sin `.git`, sin este md y sin
  `herramientas/`). El cliente revisa en **Netlify Drop** (subirlo solo
  si el usuario lo pide). Se actualiza en Netlify → sitio → Deploys →
  arrastrar la carpeta descomprimida (no el zip, por las subcarpetas).
- Para regenerar ese zip: copiar `index.html`, `style-juridico.css`,
  `script.js`, `robots.txt`, `sitemap.xml`, las 9 carpetas de servicio y
  solo las imágenes referenciadas en el HTML/CSS.
- Al commitear, entran también los archivos nuevos sin seguimiento: las 9
  carpetas, `herramientas/` y las imágenes nuevas de `img/`
  (`servicio_*.jpg`, `og-image.jpg`, `apple-touch-icon.png`,
  `bg_ciudadania.jpg`, `ciudadania_vittoriano.jpg`). NO van los PNG y JPG
  viejos sin usar (ver la lista en Pendiente).
- Para verificar visualmente se usó Chrome headless por CDP (script de
  Node en el scratchpad). Chrome headless se declara táctil: para probar
  el hover hay que lanzarlo con `--blink-settings=primaryPointerType=4,
  primaryHoverType=2,availablePointerTypes=4,availableHoverTypes=2`.

## Convenciones del proyecto (respetar)
- Sin frameworks. Preferir CSS por sobre JS cuando se pueda.
- No agregar código innecesario ni reestructurar sin que se pida.
- Al modificar un archivo, entregarlo siempre completo (no fragmentos).
- Paleta (actual): **celeste** como color del sitio (fondos claros
  `--sky-*`; acentos `--celeste*` en etiquetas, bullets y hovers), navy
  azulado para los bloques oscuros y los títulos, y **botones dorados**
  (decisión del cliente: el dorado se reserva para botones y líneas
  principales). Verde solo para WhatsApp. Celeste plano en bloques
  grandes se ve "infantil": usarlo apagado y como sistema.
- Estilo pedido por el cliente: **simple y conciso**. Nada de tarjetas
  genéricas numeradas, frases de relleno ("te atiende personalmente…"),
  títulos duplicados (etiqueta + H2 que dicen lo mismo) ni botones
  repetidos (un solo CTA por bloque). El número de teléfono NO se muestra
  (va en el JSON-LD y en `href="tel:"` con el texto "Llamar al estudio").
- Extensión real de cada imagen en `img/` (verificada por contenido, no
  asumir — ya hubo bugs de rutas rotas por esto): `hero_1.png`, `hero_2.png`,
  `hero_3.png`, `pablo.jpeg`, `parallax1.png`, `parallax2.jpg`,
  `servicios_1.jpg`, `servicios_2.jpg`, `servicios_3.jpg`, `wsp.png`,
  `favicon-16x16.png`, `favicon-32x32.png` (lista histórica: ver las
  rondas siguientes para las imágenes nuevas).
- GSAP + ScrollTrigger vía CDN para animaciones; hay un fallback sin GSAP
  con `IntersectionObserver` y la clase `.js-reveal` — ese fallback debe
  correr **solo si GSAP no está disponible** (`if (!hasGsap)`), nunca en
  paralelo, porque pisa las transiciones propias de las tarjetas
  (hoy `.service-card`).

## Arreglado en la última sesión
- Bug de hover/transiciones "rotas": el fallback de reveal corría siempre
  (no solo sin GSAP) y su `.js-reveal` pisaba la transición de las tarjetas.
- Zoom del hero: el timer del carrusel (7000ms) cortaba la transición de
  zoom (8500ms) a mitad de camino. Ahora usa reset limpio por slide
  (`resetZoom`/`startZoom`, clase `.is-zooming`) con timing sincronizado
  (`HERO_ZOOM_MS`/`HERO_INTERVAL_MS`).
- Se eliminó un bloque "PATCH FINAL" al final del CSS con reglas de menú
  y divisores duplicadas que se peleaban con las originales.
- Antialiasing global, min-height fijo removido en tarjetas de Áreas,
  ajuste de header en mobile chico.
- Fondo parallax: Statement → `img/parallax1.jpg`, Contacto →
  `img/parallax2.jpg` (con overlay oscuro + panel translúcido detrás del
  formulario para que no reste legibilidad).
- Botón flotante de WhatsApp: ícono circular con `img/wsp.png`.

## Arreglado en esta sesión (revisión pre-entrega)
- Rutas de imagen rotas por extensión incorrecta (404 en vivo aunque el
  código "se veía bien"): `img/pablo.png`→`pablo.jpeg`, `servicios_1/2/3.png`
  →`.jpg` (tanto en el `<img>` de cada area-card como en el fondo de
  `.services::before` en el CSS), y `img/parallax1.jpg`→`.png` en el fondo
  de `.statement::before`. Antes de este fix, la foto de perfil, las 3
  imágenes de Áreas de práctica y los fondos de Statement/Servicios no
  cargaban.
- JSON-LD (`Attorney.image`) apuntaba también a `pablo.png` — corregido a
  `pablo.jpeg`.
- SEO: meta description recortada a ~150 caracteres (la anterior se
  truncaba en el SERP), agregado `og:image:width/height/alt`, agregado
  `<link rel="icon" sizes="16x16">` (existía el archivo pero no estaba
  enlazado) y `apple-touch-icon` (usando el 32x32 como mínimo viable —
  ideal reemplazar por un 180x180 real más adelante), `preload` +
  `fetchpriority="high"` en la imagen del primer slide del hero (LCP), y
  `<lastmod>` en `sitemap.xml`.

## Arreglado en esta sesión (ronda 2 — hover + nueva sección + dirección)
- El hover de botones/tarjetas "no andaba": **no era un bug de código**. Se
  probó en un Edge headless real (vía CDP) contra el sitio y se confirmó que
  este equipo Windows tiene la opción de accesibilidad "Mostrar animaciones
  en Windows" desactivada (`SystemParameters.ClientAreaAnimation = False`),
  lo que hace que Edge/Chrome reporten `prefers-reduced-motion: reduce` en
  TODOS los sitios, no solo este. La regla `@media (prefers-reduced-motion:
  reduce)` del CSS forzaba `transition-duration: 0.01ms !important` de
  forma global — correcto para el zoom del hero / parallax / reveals de
  scroll, pero mataba también el feedback de hover de botones y tarjetas
  (que es corto y lo dispara el usuario, no el tipo de movimiento que esa
  preferencia busca evitar). Se agregó una excepción dentro del mismo media
  query que restaura `transition-duration: 0.2s` solo para botones,
  `.area-card`, `.service-panel`, links de footer y el flotante de
  WhatsApp — verificado con el mismo test automatizado (antes: `color
  1e-05s...`, después: `color 0.2s...`, con 0 errores de consola y 0
  requests fallidos).
- Nueva sección **"Amparos de salud"** agregada entre Servicios y Contacto
  (`id="amparos-salud"`, link correspondiente en el menú). Reutiliza el
  layout/CSS de la sección `.about` (Método de trabajo) — mismo patrón
  título + lead + párrafos + botón — sin agregar CSS nuevo. También hereda
  el reveal-on-scroll de GSAP/fallback porque usa las mismas clases
  genéricas (`.about-title`, `.about-content`). Se sumó "Amparos de salud"
  al `knowsAbout` del JSON-LD.
- Dirección actualizada a **Ituzaingó 522, San Isidro** en el footer
  (se quitó "Lex Tower", nombre del edificio de la dirección anterior en
  Corrientes — no aplica más) y en el JSON-LD (`PostalAddress`,
  `areaServed`). Por decisión del usuario, se actualizó **todo** el resto
  del copy que decía "CABA"/"Capital Federal" (title, meta description,
  Open Graph, Twitter Card, alts de imágenes, JSON-LD) a "San Isidro" /
  "Zona Norte del Gran Buenos Aires" para mantener consistencia de NAP
  (Name-Address-Phone) de cara al SEO local.
- Se bump-eó `?v=` de `style-juridico.css` y `script.js` en `index.html`
  para evitar que quede cache vieja servida tras estos cambios.

## Arreglado en esta sesión (ronda 3 — reorden, imagen, optimización, deploy)
- Orden de secciones cambiado a pedido: **Amparos de salud** ahora va justo
  después de Áreas de práctica (antes ahí estaba Statement), y **Statement**
  ("En una causa penal, actuar a tiempo...") pasó a estar justo encima de
  Contacto ("Hablemos sobre tu situación"). Link del menú reordenado igual.
- Se buscó y sumó una foto libre de derechos (Unsplash License, uso
  comercial permitido sin atribución) para el fondo de "Amparos de salud":
  `img/amparos_salud.jpg` (foto de un estetoscopio en blanco y negro).
  La sección pasó de fondo blanco a fondo oscuro con overlay + imagen fija,
  misma técnica que Statement/Servicios (`::before` + gradient), sin CSS
  nuevo salvo ese bloque puntual.
- Optimización de imágenes (mismo nombre de archivo, cero cambios de
  referencia):
  - `servicios_1/2/3.jpg` se mostraban a ~1600px de ancho cuando se
    renderizan en tarjetas de ~400px → redimensionadas a 900px de ancho
    (retina-ready) y recomprimidas: 104KB→47KB, **364KB→118KB**, 177KB→70KB.
  - `parallax1.png` (1.9MB, un PNG sin transparencia real — alpha 100%
    opaco en toda la imagen, o sea una foto guardada sin necesidad como
    PNG) se convirtió a `parallax1.jpg` (200KB, misma calidad visible).
  - `hero_1/2/3.png` en realidad eran archivos JPEG con la extensión
    cambiada a mano (confirmado por contenido, no por nombre) → renombrados
    a `hero_1/2/3.jpg` (mismos bytes, sin recompresión, extensión correcta
    ahora sí coincide con el contenido real y con el Content-Type que va a
    servir el hosting).
  - Bump de `?v=` en `index.html` a `20260907c` tras estos cambios de CSS.
- **Archivos viejos que quedaron huérfanos y hay que borrar a mano** (no
  hay permiso de `rm` en este entorno): `img/hero_1.png`, `img/hero_2.png`,
  `img/hero_3.png`, `img/parallax1.png`, `img/derecho_penal.png` — ninguno
  se referencia ya en el código, suman ~5.5MB de peso muerto.
- Auditoría completa con un Edge headless real (CDP): 0 errores de consola,
  0 requests fallidos, sin IDs duplicados, jerarquía de encabezados
  correcta, sin imágenes rotas. Se probó el menú mobile, el acordeón de
  Servicios y las tarjetas de Áreas en 375px/390px/320px de ancho — todo
  responsive. Un falso positivo detectado y descartado: el menú mobile
  "parecía" mostrarse vacío en una captura, pero era solo la animación de
  entrada (~1.4s) atrapada a mitad de camino — con tiempo completo se ve
  perfecto.
- Nota de diseño (no aplicada, solo observación): en viewports muy angostos
  (~320-390px) el botón flotante de WhatsApp puede superponerse levemente
  al botón "Solicitar consulta" al final de algunas secciones — es un
  trade-off común de los FAB flotantes, no bloquea el tap, no se tocó nada
  para no reestructurar sin que se pida.

## Arreglado en esta sesión (ronda 4 — celeste + sección Ciudadanía italiana, 2026-09-30)
- **NO commitear ni pushear sin pedido explícito**: el repo publica con
  GitHub Pages, cualquier push actualiza el sitio en vivo.
- Pedido del cliente (según referencias de su Instagram): fondo del sitio
  **celeste**, manteniendo el dorado y el navy. Se usó un celeste frío y
  apagado (tokens `--sky-50/100/200`, `--sky-line`) porque uno saturado con
  el dorado quedaba feo. Cambian solo los fondos claros: `body`, preloader,
  `.professional` (Sobre mí) y `.about` (Método). `--cream`/`--white` NO se
  tocaron porque se usan como color de texto sobre fondos oscuros.
- Nueva sección **Ciudadanía italiana** (`#ciudadania-italiana`, segundo
  negocio del Dr. Crespo: Cittadinanza Ital), justo debajo de Áreas de
  práctica, con link en el menú. La base es el diseño "Sección en landing —
  A" del canvas de Claude (https://claude.ai/artifact/726AKn4kchLDwcyku7ireq),
  adaptado al sitio: fondo `--sky-200`, tricolor italiano, título navy,
  botón dorado que abre WhatsApp con un mensaje sobre ciudadanía, y 4
  tarjetas numeradas. El logo `img/logo-ciudadania.png` se pasó del footer
  a esta sección. Se sumó a los reveals de GSAP y del fallback.
- Footer sin logo: vuelve al layout de 2 columnas (nombre a la izquierda,
  sedes a la derecha; en mobile queda todo centrado).
- `style-juridico.css` tenía finales de línea CRLF (sin cambios reales):
  se normalizó a LF. `?v=` pasó a `20260930a`.

## Arreglado en esta sesión (ronda 5 — sistema celeste + auditoría, 2026-09-30)
- El celeste plano en toda una sección se veía "infantil". Se reencaró
  como sistema de color: navy más azul (`--navy-*` y todos los overlays
  `rgba(7, 26, 46, …)`), el celeste como acento (`--celeste`,
  `--celeste-light`, `--celeste-deep`) para etiquetas, bullets, hovers,
  el énfasis del Statement, los labels del formulario y las ciudades del
  footer. El **dorado queda solo para botones y líneas principales**.
  Fondos claros: Sobre mí y Método en `--sky-100`, Ciudadanía en `#f6f9fc`.
- Se agregaron etiquetas (`.eyebrow`) a todas las secciones para darles
  estructura: Sobre mí, Especialidades, Ciudadanía italiana, Derecho a la
  salud, Método de trabajo, Qué hacemos, Contacto.
- Ciudadanía italiana rediseñada, **todo centrado**: logo → etiqueta →
  título → bajada → 4 ítems como índice editorial (columnas con filetes
  celestes, sin cajas, números en celeste que pasan a dorado en hover) →
  botón. En tablet y mobile queda en 2x2 para que la sección sea corta.
- Logo `img/logo-ciudadania.png` regenerado desde `logo_cita.jpeg`
  (480×360, transparente, 23KB, nítido en retina).
- Servicios: se sumaron los paneles **Amparos de salud** y **Ciudadanía
  italiana** (antes faltaban, aunque ambas tienen su sección).
- SEO: la meta description, OG y WebPage mencionan amparos y ciudadanía;
  se sumó "Ciudadanía italiana" a `knowsAbout`; `theme-color` actualizado;
  `width`/`height` reales en las imágenes de hero y áreas; `lastmod` del
  sitemap al 2026-09-30.
- Mobile: `#amparos-salud::before` también usa `background-attachment:
  scroll` (faltaba, en iOS se veía mal) y el footer deja lugar al botón
  flotante de WhatsApp.
- `?v=` en `20260930b`.

## Arreglado en esta sesión (ronda 6 — menos navy, footer centrado, 2026-09-30)
- Se **eliminó la sección Statement** ("En una causa penal, actuar a
  tiempo…"): repetía el slide 2 del hero y sumaba otro bloque oscuro.
  Se quitaron también su CSS y sus selectores en el JS.
- **Servicios** pasó de foto con velo navy a foto con **velo celeste**
  (`img/parallax1.jpg`, las columnas del tribunal, que quedó libre al
  sacar el Statement), con parallax `fixed`. Títulos en navy y paneles
  blancos translúcidos; el panel abierto sigue en navy.
- Parallax GSAP (scrub) en la foto de "Sobre mí": la imagen se desplaza
  dentro del marco. Su hover pasó de zoom a saturación para no pelearse
  con el transform de GSAP.
- Contraste: `--gray` de `#72777c` a `#5b6570`.
- Áreas conecta con el resto: al pie dice "También te acompañamos en
  amparos de salud y ciudadanía italiana", con links a las dos secciones.
- Footer apilado y centrado: nombre → filete → 3 sedes en fila (en
  mobile, en columna) → filete → crédito.
- `?v=` en `20260930c`.

## Arreglado en esta sesión (ronda 7 — fusión Áreas + Servicios, 2026-09-30)
- Áreas de práctica y Servicios repetían contenido: se fusionaron en una
  sola sección **Servicios** (`#servicios`, en el lugar de Áreas), con 6
  tarjetas con foto: Penal, Familia, Violencia de género, Amparos,
  Ciudadanía y Asesoramiento integral. Cada una tiene título, bajada,
  lista de servicios y link: "Consultar" lleva a #contact, y en Amparos y
  Ciudadanía "Ver más" lleva a su sección.
- Desktop con mouse: la tarjeta con hover o foco se ensancha dentro de su
  fila (flex-grow, base 26%) y despliega la lista (grid 0fr → 1fr).
  Táctil o ≤1000px (`(hover: none)`): el detalle se ve siempre, en 2
  columnas. ≤760px: **carrusel horizontal con scroll-snap** (antes eran
  ~3400px de tarjetas apiladas).
- Fotos nuevas de 900px para las tarjetas: `img/servicio_amparos.jpg`,
  `servicio_ciudadania.jpg` y `servicio_asesoramiento.jpg` (salen de
  amparos_salud, parallax2 y hero_3).
- Se eliminaron el acordeón de Servicios (HTML, CSS y JS) y todo el CSS
  de `.areas`, `.area-card` y `.card-link`. El menú ya no tiene "Áreas de
  Práctica" y el botón del slide 3 del hero ahora dice "Ver
  especialidades" (#servicios).
- "Sobre mí" pasa a `--sky-25` (#f6f9fc) para no fundirse con el celeste
  de Servicios.
- `?v=` en `20260930d`.

## Arreglado en esta sesión (ronda 8 — header invertido + SEO, 2026-09-30)
- Header invertido: fondo celeste translúcido con blur, texto e ícono de
  menú en navy, logo oscuro (`img/logo-mcdv.png`). "Dr. Pablo Luis Crespo"
  va **todo de un solo color** (antes "Dr." iba en dorado). Se mantiene
  el filete dorado inferior. `theme-color` → `#dbe8f3`.
  `img/logo-mcdv-light.png` quedó sin uso.
- SEO: el H1 incluye "Abogado penal y de familia en San Isidro" (como
  `.hero-kicker`, en letra chica arriba del slogan). Los slides 2 y 3
  tienen su propia bajada chica, para que se vean consistentes.
- Footer: teléfono visible con link `tel:` y horario (NAP para SEO local).
- Se eliminó la tarjeta "Asesoramiento integral": era genérica, se
  superponía con Método de trabajo y repetía la foto del slide 3 del
  hero. Quedan 5 servicios.
- `?v=` en `20260930e`.

## Arreglado en esta sesión (ronda 9 — hero, 9 áreas, auditoría, 2026-09-30)
- Hero: la foto arranca debajo del header (`--header-h`: 104px, 86px en
  mobile), cada slide tiene su encuadre (`--hero-pos`) y el zoom crece
  hacia el sujeto (`--hero-origin`), con escala 1.07 en vez de 1.14.
  Antes la cabeza de la estatua quedaba cortada.
- Indicadores del carrusel (3 barras abajo a la derecha): la activa se
  llena durante el slide, se puede hacer clic para saltar y el timer se
  reinicia (`setActiveDot`, `[data-hero-dot]`).
- Se sacaron los títulos duplicados: "Especialidades" arriba de
  Servicios, "Ciudadanía italiana" arriba de su H2 y "Derecho a la salud"
  arriba de "Amparos de salud".
- Servicios pasa a **9 áreas**: Penal, Víctimas y querellas, Familia,
  Divorcios, Alimentos, Sucesiones, Violencia de género, Amparos y
  Ciudadanía. Las nuevas salen de sub-servicios que ya figuraban en el
  sitio (**validar con el Dr.**). Fotos nuevas de 900px en
  `img/servicio_*.jpg`: la de Sucesiones sale de `derecho_penal.png`, que
  ahora puede borrarse; las demás son recortes de las fotos del hero.
  `servicios_2.jpg` se recortó a 900×600.
- Auditoría: todas las zonas táctiles llegan a 44px (menú, indicadores,
  links de tarjetas, sedes, teléfono y crédito; el subrayado pasó a
  text-decoration). `og-image.jpg` de 1200×630 con nombre y rubro para
  redes. `apple-touch-icon.png` real de 180×180. El botón del formulario
  dice "Enviar por WhatsApp", que es lo que hace. JSON-LD `knowsAbout`
  ampliado.
- Probado y descartado: `srcset` en el hero. Con `object-fit: cover` en
  mobile hace falta una foto de ~1250px de ancho igual.
- `?v=` en `20260930g`.

## Arreglado en esta sesión (ronda 10 — páginas por servicio, 2026-09-30)
- **Una página por servicio** (9 carpetas con `index.html`, URLs
  limpias tipo `/derecho-penal/`): derecho-penal, victimas-y-querellas,
  derecho-de-familia, divorcios, alimentos, sucesiones,
  violencia-de-genero, amparos-de-salud, ciudadania-italiana. Cada una
  tiene breadcrumb, H1 con palabra clave + ciudad, "Cómo te
  acompañamos", "Qué incluye", pasos, preguntas frecuentes (con
  `<details>` nativo), CTA a WhatsApp con mensaje según el área y links
  a las otras áreas. JSON-LD por página: Service + BreadcrumbList +
  FAQPage. Todas están en `sitemap.xml`.
- **Se generan con `herramientas/generar_servicios.py`**: plantilla y
  textos viven ahí. NO editar a mano los `index.html` de las carpetas:
  editar el script y correr `python3 herramientas/generar_servicios.py`.
  Si cambia el header, el menú o el footer del inicio, hay que replicarlo
  en la plantilla. El `VERSION` del script tiene que coincidir con el
  `?v=` del index.
- La página de Ciudadanía usa los textos del canvas de Claude (plazo
  31/05/2029, casos, pasos, preguntas). Violencia de género tiene un
  aviso con el 911 y la Línea 144. **Todos los textos legales tiene que
  validarlos el Dr.**
- Tarjetas del inicio: todas dicen **"Ver más"** (antes algunas decían
  "Consultar"), con botón de contorno dorado visible siempre, y llevan a
  su página. El texto accesible completa "Ver más sobre X" (`.sr-only`).
- Ciudadanía en el inicio: fondo con foto de Roma (Piazza Venezia) y velo
  claro con parallax (`img/bg_ciudadania.jpg`); **logo grande a la
  izquierda** sobre un panel blanco; botones "Evaluar mi caso" y "Ver
  más". En mobile queda apilado y centrado.
- Fotos nuevas (Unsplash, licencia libre sin atribución):
  `bg_ciudadania.jpg`, `ciudadania_vittoriano.jpg` (encabezado de la
  página de Ciudadanía) y `servicio_ciudadania.jpg` (pasaporte italiano,
  reemplaza la foto genérica de firma).
- Amparos en el inicio: se suma un botón "Ver más" a su página.
- Nuevos estilos reutilizables: `.ghost-button` (y `--light`),
  `.section-actions`, `.sr-only`.
- Validado: 0 links internos rotos en las 10 páginas, JSON-LD válido,
  sin desborde horizontal y zonas táctiles de 44px.
- `?v=` en `20260930h`.
- Pendiente de decisión del cliente: qué hacer con el logo de MCDV en el
  navbar (convive con Cittadinanza y con el nombre del Dr.).

## Arreglado en esta sesión (ronda 11 — refinado de páginas, 2026-09-30)
- Páginas de servicio: el **H1 es solo el nombre del servicio**
  ("Sucesiones"). La palabra clave + ciudad sigue en el `<title>` y en la
  meta description, que no se ven en la página.
- Encabezado: la foto del servicio es **fondo del banner** y aparece en
  degradé desde el azul de la izquierda (en mobile, el degradé va de
  arriba hacia abajo). Ya no hay foto enmarcada a la derecha.
- **Un solo botón** en el encabezado (WhatsApp). Se sacó el botón
  duplicado con el número.
- "Cómo te acompañamos" queda centrado en una columna de lectura y "Qué
  incluye" pasa a una grilla pareja abajo (4 ítems: una fila de 4; 5
  ítems: 3 + 2).
- Se sacaron los 4 pasos genéricos repetidos en cada página (eran relleno
  copiado). Solo Ciudadanía conserva los suyos.
- **El número de teléfono no se ve en ningún lado.** Los links dicen
  "Llamar al estudio" (`href="tel:..."`) y el número queda en el JSON-LD
  (`telephone`), que es de donde Google toma el dato para el SEO local.
  Esconderlo con CSS sería texto oculto y Google lo penaliza.
- Inicio: Amparos y Ciudadanía tienen un solo botón ("Ver más" a su
  página). Se borraron `.ghost-button` y `.section-actions`, que quedaron
  sin uso.
- `?v=` en `20260930i`.

## Arreglado en esta sesión (ronda 12 — mosaico en páginas de servicio, 2026-09-30)
- El contenido todo centrado en una columna se veía básico. Se pasó a un
  **mosaico** (`.mosaic`, grilla de 3 columnas): "Cómo te acompañamos"
  en una tarjeta ancha y alineada a la izquierda, al lado una tarjeta
  azul "Qué incluye", debajo los ítems numerados (`.tile-item`) y una
  tarjeta con la foto del Dr. ("Te atiende personalmente…") que completa
  la última fila. Con 4 ítems, la foto ocupa 2 columnas
  (`.tile-photo--wide`: foto a la derecha y texto sobre azul); con 5,
  ocupa 1. En tablet y mobile el mosaico queda en 2 columnas.
- Preguntas frecuentes en 2 columnas: título fijo (sticky) a la izquierda
  y acordeón a la derecha (`.faq-layout`).
- `?v=` en `20260930j`.

## Arreglado en esta sesión (ronda 13 — páginas de servicio como texto, 2026-09-30)
- A pedido del cliente se sacó el mosaico: la tarjeta azul "Qué
  incluye", la foto con "Te atiende personalmente…" y las tarjetas
  numeradas 01, 02… (se veían genéricas). **Cada página ahora es texto
  explicativo**: título de la sección a la izquierda (fijo al bajar) y
  texto a la derecha (`.page-article`, `.article-layout`). "Qué incluye"
  va como subtítulo dentro del texto, con párrafos que arrancan con el
  tema en negrita (`.article-points`).
- Ciudadanía: "¿En qué casos podemos ayudarte?" y "Cómo trabajamos"
  usan el mismo formato de texto. El plazo del 31/05/2029 sigue como
  franja destacada.
- Preguntas frecuentes con el mismo esquema (`.faq-layout` comparte
  estilos con `.article-layout`).
- Se borró del CSS todo lo del mosaico y de las grillas de pasos
  (`.mosaic`, `.tile*`, `.steps-grid`, `.step*`).
- `?v=` en `20260930k`.

## Arreglado en esta sesión (ronda 14 — logo de Cittadinanza sin recuadro, 2026-09-30)
- `img/logo-ciudadania.png` regenerado desde `logo_cita.jpeg` con un
  recorte más ajustado y el alfa encogido 1px: sin el borde claro que
  se le veía sobre fondos oscuros (560×419, 17KB). Se ve bien tanto sobre
  azul como sobre fondos claros.
- Página de Ciudadanía: banner invertido (`.page-hero--logo`). La foto va
  a la izquierda, oscurecida detrás del título, y se funde en azul liso
  hacia la derecha, donde va **el logo en PNG, grande y sin recuadro**, a
  la altura del título. En mobile el logo queda arriba del texto, más
  chico.
- Inicio: el logo de la sección Ciudadanía también va directo sobre el
  fondo, sin el panel blanco.
- **Bug corregido:** `.sr-only` dentro de `.dark-button` se hacía visible
  porque `.dark-button span { position: relative }` le ganaba, y el botón
  decía "Ver más sobre ciudadanía italiana". Ahora `.sr-only` usa
  `!important`.
- `?v=` en `20260930l`.

## Arreglado en esta sesión (ronda 15 — agenda de turnos con pago, 2026-10-02)
- **Página `/agendar/`** (la genera el script): noindex, fuera del menú y
  del sitemap. Solo se llega desde los botones "Agendar consulta".
  Modalidad (virtual o presencial en CABA), calendario de lunes a viernes
  y horarios de 9 a 16 hs en **hora de Argentina** (se calcula con
  `Intl` en `America/Argentina/Buenos_Aires`, así funciona igual desde el
  exterior), datos (nombre, email, teléfono, consulta), pago
  (precio + alias/CBU/titular con botón "Copiar" + link de MP opcional) y
  comprobante adjunto (imagen o PDF, hasta 5 MB). Resumen del turno fijo a
  la derecha (en mobile se oculta y la aclaración del pago pasa arriba del
  botón). Pantalla final de "Turno reservado".
- Lógica en **`agenda.js`** (raíz). `const AGENDA_URL = ""` → **MODO DEMO**:
  horarios ocupados de ejemplo, reserva simulada y aviso de "Vista previa".
  Sirve para la preview de Netlify.
- Backend en **`herramientas/agenda-apps-script.gs`** (Google Apps Script,
  gratis, en la cuenta de Google del Dr.):
  - GET: horarios ocupados (CUALQUIER evento de su calendario bloquea),
    feriados de Argentina y datos de pago.
  - POST: valida todo de nuevo, `LockService` + rechequeo del horario
    (**los turnos no se pisan**), guarda el comprobante en Drive, crea el
    evento en Calendar (recordatorio 60 min), le manda al Dr. un mail con
    el comprobante adjunto (aviso inmediato en el celular vía Gmail) y le
    manda la confirmación al cliente.
  - Precio, alias, CBU y horarios se configuran en el `CONFIG` del script,
    no en la web.
  - Instalación paso a paso: **`herramientas/AGENDA-INSTALACION.md`**.
- Probado: flujo completo en modo demo (validaciones, selección, reserva)
  y la ruta real contra un servidor de prueba que imita Apps Script
  (POST `text/plain` sin preflight, archivo intacto en base64, feriado
  bloqueado y caso "turno recién tomado" → recarga la disponibilidad).
  **El backend real no se pudo probar desde acá** (requiere la cuenta del
  Dr.): probarlo después de instalarlo (paso 9 de la guía).
- CTAs: "Solicitar consulta" del inicio y "Consultar por WhatsApp" /
  "Escribir por WhatsApp" de las páginas de servicio → **"Agendar
  consulta"**. WhatsApp queda solo en el botón flotante.
- Contacto (inicio): el formulario que mandaba a WhatsApp se reemplazó
  por un panel "Agendá tu consulta" (horario, modalidad, pago y botón). Se
  borraron su JS (bloque FORMULARIO) y su CSS (`.contact-form`,
  `.field-row`, `.form-confirm`).
- Regla global `[hidden] { display: none !important; }` (el botón de MP
  aparecía aunque no hubiera link).
- Generador reorganizado: `envoltorio()` arma head, header, menú y footer
  compartidos; `pagina()` arma las páginas de servicio y
  `pagina_agendar()`, la agenda. Se sacaron `wa_link` y los campos `wa`.
- `?v=` en `20261002a` (index, generador y páginas).

## Arreglado en esta sesión (ronda 16 — Mercado Pago integrado, 2026-10-03)
- **Pago con Mercado Pago Checkout Pro**, sin comprobantes. Es el modo por
  defecto (`CONFIG.MODO_PAGO = "mercadopago"`); el de transferencia con
  comprobante queda como alternativa configurable.
  1. `crear_pago`: valida, retiene el horario 30 min (reserva "pendiente" en
     las Propiedades del script, con `LockService`) y crea la preferencia en
     MP (monto `PRECIO_NUMERO`, ARS, `external_reference` = id de la
     reserva, `notification_url` = el propio script `?accion=webhook`,
     `back_urls` → `/agendar/?ref=…`, `expires` a los 30 min, sin efectivo
     ni cajero). Devuelve el `init_point` y la web redirige.
  2. Webhook de MP o vuelta del cliente (`?accion=estado`): el script
     **consulta el pago en `/v1/payments/{id}`** (no confía en el aviso:
     Apps Script no puede leer headers, así que no se puede validar la
     firma) y confirma solo si está `approved`, en ARS, por el monto
     correcto y con la referencia de esa reserva. Es idempotente (el aviso
     repetido no duplica nada). Recién ahí crea el evento en Calendar y
     manda los 2 mails.
  3. El cliente vuelve sin pagar → `?accion=liberar` libera el horario en el
     momento. Las reservas sin pagar vencen solas a los 30 min.
- **El Access Token de MP va en las Propiedades del script
  (`MP_ACCESS_TOKEN`)**, nunca en el código ni en la web.
- Frontend (`agenda.js`): según `config.modoPago` muestra el bloque de MP
  (precio + "reservamos tu horario 30 minutos") o el de transferencia
  (alias/CBU + comprobante). Botón "Pagar y reservar". Al volver de MP
  (`?ref=…&payment_id=…&status=…`) consulta el estado (hasta 10 intentos,
  cada 3 s) y muestra "Turno confirmado", "El pago no se completó", "La
  reserva venció" o "Estamos esperando la confirmación". En modo demo
  simula todo el recorrido.
- **Pruebas:** `node herramientas/pruebas-agenda.mjs` corre **25 pruebas**
  del script real simulando Google y MP (superposición, retención,
  monto menor, pago pendiente, webhook repetido, pago de otra reserva,
  vencimiento, liberar, credencial inválida, bot). 25/25 OK. El recorrido
  del navegador se probó en modo demo y contra un servidor de prueba
  (crear pago → "MP" falso → vuelta aprobada o cancelada). **Falta la
  prueba real** con la cuenta del Dr. (pago real de $10 y devolución:
  ver la guía).
- `herramientas/AGENDA-INSTALACION.md` reescrita: A) credencial de MP,
  B) script + propiedad `MP_ACCESS_TOKEN` + permisos (`probarPermisos`
  verifica la credencial), C) conectar la web y probar.

## Arreglado en esta sesión (ronda 17 — blindaje del cobro, 2026-10-03)
- Precio cargado: **$ 50.000** (`PRECIO` / `PRECIO_NUMERO` en el script y
  en la demo de `agenda.js`).
- Revisión de riesgos de plata; se cerraron 4 huecos:
  1. **Red de seguridad:** `revisarPendientes()` corre cada 15 min (se
     programa una vez con `instalarRevisionAutomatica()`). Busca en MP
     (`/v1/payments/search?external_reference=`) los pagos aprobados de
     las reservas de los últimos 3 días y los confirma. Cubre el caso en
     que el webhook no llega y el cliente no vuelve.
  2. **Pago sin reserva** (pagado muy tarde) → mail "⚠ Revisar" al Dr. Las
     reservas ahora se guardan 7 días (antes 2 h / 2 días).
  3. **Pago duplicado** sobre una reserva confirmada → mail "⚠ Revisar" para
     devolverlo. Monto distinto → también avisa. Las alertas salen una sola
     vez por pago (`alerta_<id>` en las Propiedades).
  4. **Acaparamiento:** un solo pago en curso por email (reintentar libera
     el anterior) y tope `MAX_RESERVAS_EN_CURSO` = 8.
- `liberar` ya no borra la reserva: la marca "liberada". Si el pago llega
  igual después, se confirma (si el horario sigue libre).
- Pruebas: **33/33 OK** (`node herramientas/pruebas-agenda.mjs`).
- Guía: tabla "Qué pasa si algo sale mal con un pago", paso de
  `instalarRevisionAutomatica` y fase previa de prueba con **credenciales y
  usuarios de prueba de MP** (plata ficticia), antes de tocar plata real.

## Arreglado en esta sesión (ronda 18 — ajustes según el asistente de MP, 2026-10-03)
- Consulta al asistente de IA de Mercado Pago Developers. Confirmó el diseño
  (el aviso es solo un disparador y se decide consultando
  `/v1/payments/{id}` con el token) y marcó estos ajustes, ya aplicados:
  - Siempre `init_point` (nunca `sandbox_init_point`). Para probar se usa
    la credencial de producción (`APP_USR-…`) de la **cuenta de prueba
    vendedora**.
  - Los webhooks esperan 200/201 y Apps Script responde siempre 302 (no se
    puede cambiar): Mercado Pago puede reintentar. El script es idempotente
    y la confirmación ya no depende del webhook: **la reconciliación pasó de
    15 a 5 minutos** (sin confirmar: últimos 3 días; confirmadas: último
    día). Con credenciales de prueba MP no manda webhooks.
  - Se sacó `statement_descriptor` (no confirmado como campo válido).
- Guía: fase de prueba detallada (crear la app Checkout Pro, cuentas
  vendedor y comprador AR, comprador en incógnito, tarjetas de prueba con
  titular APRO/OTHE/CONT, vto 11/30, qué verificar en cada caso, "Simular"
  webhook en el panel).
- El Dr. puede compartir sus credenciales de producción con el desarrollador
  desde el panel de MP (alternativa a pegarlas en la visita).
- Pruebas: 35/35 OK.

## Arreglado en esta sesión (ronda 19 — plugin de MP + revisión de seguridad, 2026-10-03)
- Plugin oficial `mercadopago` instalado en Claude Code (skills
  `mp-test-setup`, `mp-review`, `mp-webhooks`, `mp-test-cards`,
  `mp-connect`). Su MCP **requiere autorizar la cuenta del usuario** desde
  `/mcp` (OAuth). Sin eso no se pueden crear las cuentas de prueba.
- Revisión de seguridad local (credenciales, HTTPS, HMAC, verificación en el
  servidor, idempotencia):
  - Sin credenciales en ningún archivo; todo HTTPS; el token solo se lee de
    las Propiedades del script. OK.
  - Verificación en el servidor: status, ARS, monto y external_reference,
    consultando con el token del Dr. (un pago de otra cuenta devuelve 404).
    OK.
  - Idempotencia: probada. OK.
  - HMAC: no se puede (Apps Script no expone headers). Riesgo aceptado y
    mitigado: el aviso es solo un disparador. **Nuevo:** guarda contra
    avisos falsos masivos: ids no numéricos se descartan, y un pago ya
    resuelto o inválido se ignora 10 min (`CacheService`, clave
    `aviso_<id>`). Los pendientes no se memorizan, para que su "aprobado"
    pase.
- El `.gs` creció a ~780 líneas por un reformateo al guardar (sin cambios
  de lógica; 32 funciones, sin duplicados).
- Pruebas: 37/37 OK.

## Arreglado en esta sesión (ronda 20 — entorno de prueba de MP, 2026-10-03)
- Con el plugin conectado (OAuth, cuenta de desarrollador **del usuario**):
  - App creada: **"Turnos Dr Pablo Crespo"** (Checkout Pro, MLA), App ID
    `7304854327005527`. Las credenciales de producción no están activadas
    (no hacen falta para probar).
  - Cuentas de prueba (las creó la automatización de MP): vendedor
    `TESTUSER4813893044627817969` (id 3735929984) y comprador
    `TESTUSER4523892745797791342` (id 3735929986). Las contraseñas están en
    el panel: Tus integraciones → la app → Cuentas de prueba.
  - La app tiene credencial de prueba `TEST-…` (panel → Credenciales de
    prueba). **No se guarda en ningún archivo**: el hook del plugin bloquea
    credenciales escritas en comandos o archivos. Se pasa como variable de
    entorno.
- **`herramientas/servidor-prueba-local.mjs`**: sirve el sitio en
  `http://localhost:8787` y corre el `.gs` REAL contra la API de prueba de
  MP (Google simulado: eventos y mails salen en la terminal). Lee
  `MP_ACCESS_TOKEN` del entorno. En la copia que manda al navegador,
  reescribe `AGENDA_URL` (los archivos del sitio no se tocan), saca
  `notification_url` (MP no llega a localhost), usa `sandbox_init_point`
  si la credencial es `TEST-`, reconcilia cada 1 min y no sirve
  `herramientas/`. Probado con una credencial inventada: sitio 200, agenda
  conectada, disponibilidad OK y rechazo de MP (403) manejado sin dejar el
  horario retenido.
- Uso: `export MP_ACCESS_TOKEN="TEST-…"` y después
  `node herramientas/servidor-prueba-local.mjs`. Abrir
  `http://localhost:8787/agendar/` en incógnito y pagar como el comprador de
  prueba (APRO, OTHE, CONT). Live Server no sirve para esto (sin backend se
  queda en modo demo).
- Plan B si el checkout de prueba no acepta la credencial `TEST-`: entrar
  con la **cuenta vendedora de prueba**, crear una app ahí y usar SU
  credencial de producción `APP_USR-…` (lo que recomendó el asistente de
  MP).

## Arreglado en esta sesión (ronda 21 — ✅ PRUEBA REAL CON MERCADO PAGO OK, 2026-10-03)
- **El recorrido completo funcionó contra la API real de MP (modo prueba)**:
  preferencia creada → la compradora de prueba pagó $ 50.000 (dinero en
  cuenta) → pago N° 182201871260 `approved` → el script lo verificó en
  `/v1/payments/{id}` (monto, estado y referencia) → creó el turno
  (Calendar simulado) y mandó los 2 mails (simulados). Falta solo la parte
  real de Google (Calendar y Gmail), que se valida en la instalación.
- **La combinación que funciona para probar (no cambiarla):**
  - Clave: la que muestra el panel de la app en **Credenciales de
    prueba** → Access Token `APP_USR-…`. Pertenece a la **cuenta vendedora
    de prueba** (`TESTUSER4813893044627817969`, id 3735929984); la
    preferencia sale con id `3735929984-…`.
  - Pago: ventana de incógnito → iniciar sesión en mercadopago.com.ar con
    la **compradora de prueba** (`TESTUSER4523892745797791342`, id
    3735929986; contraseña y código en el panel → Cuentas de prueba; el
    código es igual a los últimos 6 dígitos del User ID) → en ESA ventana
    abrir la agenda y pagar con **dinero en cuenta** (se le cargaron
    $ 100.000 ficticios con `add_money_test_user`).
  - Lo que NO funcionó: la clave `TEST-…` de la app (la devuelve el MCP;
    da "una de las partes es de prueba" o el botón "Pagar" en gris) y
    pagar sin iniciar sesión como compradora.
- Servidor de prueba local: ahora también escribe todo en
  `herramientas/.prueba-local/servidor.log` (ignorado por Git) y expone
  `http://localhost:8787/estado-prueba` (reservas, eventos, último error
  de MP), así se puede diagnosticar sin copiar la terminal. En local saca
  `auto_return` (MP lo rechaza con localhost), `notification_url` y
  `payer`. Se probó y se quitó un modo de "pago automático por API": con
  la clave de la vendedora de prueba, MP exige que el pagador sea la
  compradora de prueba ("Unauthorized use of live credentials").
- La app "Turnos Dr Pablo Crespo" (7304854327005527) es del usuario y solo
  sirve para pruebas. En producción va todo con la cuenta del Dr.

## Arreglado en esta sesión (ronda 22 — agenda simple: link de MP + WhatsApp, 2026-10-07)
- El Dr. solo quiere cobrar con Mercado Pago cuando le piden turno: se
  **eliminó todo lo de Google** (Apps Script, Calendar, Gmail, Drive) y el
  Checkout Pro con webhooks. Se borraron de `herramientas/`:
  `agenda-apps-script.gs`, `AGENDA-INSTALACION.md`, `pruebas-agenda.mjs`,
  `servidor-prueba-local.mjs`, `.prueba-local/` y el `.gitignore` (solo
  ignoraba eso). Respaldo completo en
  `~/Downloads/crespo-respaldo-2026-10-07-con-google-calendar/`.
- **Recorrido nuevo de `/agendar/`** (sin backend, `agenda.js` ~300 líneas):
  modalidad → día y horario (mismo calendario, lun a vie 9–16 hs, hora
  argentina, 24 hs de anticipación; ya no hay horarios ocupados ni
  feriados) → nombre y consulta (sin email, teléfono ni comprobante) →
  "Pagar con Mercado Pago" abre el **link de pago del Dr.** en otra
  pestaña → pantalla "Avisanos por WhatsApp" con el mensaje ya escrito
  (nombre, modalidad, turno, consulta). El Dr. ve el pago en su app de MP
  y confirma el turno por WhatsApp, a mano.
- Configuración arriba de `agenda.js`: `LINK_MERCADOPAGO` (vacío → **modo
  demo**: no abre MP y lo avisa), `WHATSAPP`, `PRECIO` ($ 50.000).
- Para activarlo: el Dr. crea en la app de MP **Cobrar → Link de pago**,
  monto fijo $ 50.000, reutilizable; se pega el link en
  `LINK_MERCADOPAGO`. Nada más.
- Inicio (Contacto): texto nuevo y "Pago: Mercado Pago" (antes
  "Transferencia o Mercado Pago").
- CSS: se borraron los estilos de alias/CBU, copiar, comprobante, campo
  trampa y estado de carga; se sumaron `.agenda-done-small` y el
  `scroll-margin-top` de `.agenda-done`.
- Probado en Chrome headless (desktop 1366 y mobile 390), en modo demo y
  con un link de MP de prueba: validaciones, resumen, apertura de MP,
  link de WhatsApp, sin errores de consola ni scroll horizontal. Las 9
  páginas de servicio solo cambian en el `?v=`.
- `?v=` en `20261007a`.

## Arreglado en esta sesión (ronda 23 — comprobante, avisos y medios de pago, 2026-10-08)
- Link de pago real en `agenda.js`: `https://mpago.li/1bM3MA2`.
- **Comprobante: solo la captura, por WhatsApp.** El cliente no escribe
  ningún número (decisión final del usuario, después de probar un campo
  obligatorio "Número de comprobante": era muy técnico). El mensaje ya
  escrito termina en "Te adjunto la captura del comprobante" y la
  pantalla final le pide adjuntarla con el clip: WhatsApp no deja
  adjuntar archivos desde un link y la web no tiene servidor. La captura
  de MP trae el N° de operación, que es lo que el Dr. busca.
- Al elegir horario aparece un aviso dorado: "Horario a confirmar con el
  Dr." (los turnos se pueden pisar; si se ocupó, ofrece otro o devuelve).
  En el resumen el horario dice "(a confirmar)".
- Paso de pago: chips con íconos (Tarjeta de crédito, Tarjeta de débito,
  Dinero en cuenta de Mercado Pago; `.agenda-medios`) y nota de
  seguridad (página oficial de MP a nombre del Dr., el sitio no ve la
  tarjeta, MP manda el comprobante por mail). Efectivo/transferencia no
  se muestran: dependen de la configuración del link, no verificada.
- Pantalla final "Confirmá tu turno" con 3 pasos (pagar, capturar,
  adjuntar en el chat), botón "Enviar por WhatsApp" y
  "Cada comprobante se verifica en la cuenta de Mercado Pago del Dr.
  antes de confirmar el turno" (disuade a los truchos).
- **Regla para el Dr.:** confirmar solo si el N° de operación de la
  captura figura en su app de MP (Actividad → buscar) como aprobado, por
  $ 50.000. Nunca confiar en la
  captura sola (se falsifican). Si el número no existe: es trucho, y queda
  el WhatsApp del que lo mandó como prueba.
- `?v=` en `20261008a`.

## Arreglado en esta sesión (ronda 24 — confirmar antes de pagar, logo de MP, 2026-10-08)
- El navegador siempre salta a la pestaña nueva y el cliente perdía las
  instrucciones. Ahora **"Continuar" NO abre Mercado Pago**: lleva a
  "Confirmá tu turno" (turno · modalidad · precio) con 2 pasos en fila:
  1. "Pagá la consulta": aviso dorado "Atención: Mercado Pago se abre en
     otra pestaña. Cuando termines de pagar, volvé a esta." + botón
     **"Pagar con [logo oficial de MP]"** (`.mp-button`,
     `img/logo-mercadopago.png`, 284×74, bajado del CDN de MP
     http2.mlstatic.com). Al tocarlo, el paso 1 queda ✓ y se resalta el 2.
  2. "Mandá el comprobante": botón verde de WhatsApp (`.wa-button`, con
     `img/wsp.png`). Se puede tocar siempre (no hay bloqueo).
  Abajo: "El Dr. verifica cada pago antes de confirmar el turno." y
  "Cambiar día u horario" (vuelve al formulario).
- Se sacó el bloque "Pago de la consulta" (chips de tarjetas y la nota de
  seguridad: no se veían creíbles) y los textos de relleno. El precio va
  en el resumen ("Consulta") y en la pantalla de confirmar.
- Aviso del horario más corto: "Horario a confirmar. El Dr. te lo
  confirma por WhatsApp; si ya está tomado, te ofrece otro."
- WhatsApp en la compu: `wa.me` dispara el cartel "¿Abrir la
  aplicación?" (xdg-open en Linux, y también en Windows/Mac). Ahora en la
  compu los links van a `web.whatsapp.com/send?phone=…&text=…` y en el
  celular siguen con `wa.me` (detecta por userAgent). Aplica al botón de
  la agenda (`agenda.js`) y al flotante/menú (`waLink` en `script.js`).
- **El WhatsApp del paso 2 está bloqueado** (`aria-disabled`, gris, sin
  abrir nada; muestra "Primero pagá la consulta (paso 1).") hasta que se
  toca "Pagar con Mercado Pago". La web solo sabe que se tocó el botón,
  no si se pagó: eso lo verifica el Dr. Probado con clics reales.
- Preview para el Dr.: Netlify Drop con la cuenta del usuario (sin cuenta
  los sitios de Drop se borran al rato), arrastrando la carpeta
  `~/Downloads/preview-crespo`. GitHub recién con el ok del Dr.
- `?v=` en `20261008d`.

## Pendiente / a confirmar
- ✅ **Link de pago real cargado (2026-10-07):** `LINK_MERCADOPAGO =
  "https://mpago.li/1bM3MA2"` en `agenda.js` (lo pasó el Dr. por WhatsApp,
  contacto "Aspyr"; confirmado: monto, cuenta del Dr. y reutilizable). La
  agenda ya no está en modo demo: **el cobro es real**. Falta: push a
  GitHub cuando el usuario lo pida. La app de prueba "Turnos Dr Pablo
  Crespo" (7304854327005527) del panel de MP del usuario ya no se usa.
- **Esperando el "ok" del cliente** sobre la preview de Netlify. Después:
  commit y push (con su autorización).
- Agenda: falta confirmar con el Dr. la duración del turno (se asumió
  60 min, de 9 a 16 hs), la anticipación (24 hs), la política de
  cancelación y si las urgencias penales siguen solo por WhatsApp. Como el
  Dr. confirma a mano, dos clientes pueden pedir el mismo horario: él
  reacomoda por WhatsApp.
- **Logo de MCDV en el navbar**: el cliente no sabe qué hacer, porque
  convive con el nombre del Dr. y con Cittadinanza. Opciones propuestas:
  (1) sacarlo, (2) moverlo al footer como "Miembro de MCDV & Asociados"
  (recomendada), (3) reemplazarlo por un monograma propio.
- **Validar con el Dr. todos los textos legales** de las 9 páginas de
  servicio y del inicio (sobre todo Ciudadanía, Ley 74/2025 y plazo al
  31/05/2029, y los plazos que se mencionan en Alimentos y Divorcios). Las
  áreas Víctimas y querellas, Divorcios, Alimentos y Sucesiones salieron
  de sub-servicios que ya estaban en el sitio: confirmar que las ofrece.
- No es de código: definir la marca principal (MCDV, Dr. Crespo,
  Cittadinanza); cargar el perfil de Google Business de las 3 sedes; pasar
  el email de contacto; política de privacidad (el formulario junta
  datos); página 404; dar de alta Search Console y enviar el sitemap.
- Dominio real: `drpablocrespo.com` (CNAME, canonical, OG, JSON-LD,
  robots y sitemap coinciden).
- Archivos sin usar para borrar a mano: `img/hero_1/2/3.png`,
  `img/parallax1.png`, `img/derecho_penal.png` (ya convertido en
  `servicio_sucesiones.jpg`), `img/logo-mcdv-light.png`,
  `img/logo_cita.jpeg` (fuente del PNG del logo: conviene guardarla fuera
  del repo) y `img/WhatsApp Image 2026-09-07 at 21.53.54.jpeg`.
- Después del deploy, confirmar en el sitio en vivo que no quedó CSS/JS
  viejo en caché (el `?v=` actual es `20261008d`).
