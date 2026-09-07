# Contexto — Sitio Dr. Pablo Luis Crespo (abogado penal y de familia)

## Qué es
Landing page (HTML/CSS/JS puro, sin frameworks) para el estudio del Dr. Pablo
Luis Crespo. Encargo de un amigo del usuario. Archivos: `index.html`,
`style-juridico.css`, `script.js`, `robots.txt`, `sitemap.xml`.

## Convenciones del proyecto (respetar)
- Sin frameworks. Preferir CSS por sobre JS cuando se pueda.
- No agregar código innecesario ni reestructurar sin que se pida.
- Al modificar un archivo, entregarlo siempre completo (no fragmentos).
- Paleta: fondo cálido, títulos navy, texto gris carbón, **botones dorados**
  (decisión final del cliente, no cambiar a azul institucional aunque una
  auditoría previa lo haya sugerido), verde para WhatsApp/confirmaciones.
- Extensión real de cada imagen en `img/` (verificada por contenido, no
  asumir — ya hubo bugs de rutas rotas por esto): `hero_1.png`, `hero_2.png`,
  `hero_3.png`, `pablo.jpeg`, `parallax1.png`, `parallax2.jpg`,
  `servicios_1.jpg`, `servicios_2.jpg`, `servicios_3.jpg`, `wsp.png`,
  `favicon-16x16.png`, `favicon-32x32.png`. `img/derecho_penal.png` existe
  en la carpeta pero no se referencia en ningún lado (pesa ~3.2MB) — queda
  pendiente confirmar con el usuario si se puede borrar.
- GSAP + ScrollTrigger vía CDN para animaciones; hay un fallback sin GSAP
  con `IntersectionObserver` y la clase `.js-reveal` — ese fallback debe
  correr **solo si GSAP no está disponible** (`if (!hasGsap)`), nunca en
  paralelo, porque pisa las transiciones propias de `.area-card` y
  `.service-panel`.

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

## Pendiente / a confirmar
- Confirmar que el dominio real es `pablocrespoabogado.com.ar` (aparece
  en canonical, Open Graph, JSON-LD, `robots.txt` y `sitemap.xml`) — si
  cambia, hay que actualizarlo en todos esos lugares.
- `img/derecho_penal.png` (~3.2MB, sin usar en ningún lado) — confirmar si
  se puede borrar o si está reservado para algo que falta maquetar.
- Confirmar en el sitio en vivo (no solo local) que las imágenes cargan
  bien tras subir los archivos corregidos, y que el hover y el zoom del
  hero se sienten suaves — si seguía habiendo cache vieja del CSS/JS,
  puede necesitar más de un hard refresh o purgar cache del hosting/CDN.
- Experimento acordado pero **no aplicado**: reemplazar el acordeón
  vertical de Servicios por 4 tarjetas horizontales con hover (la
  seleccionada se expande e ilumina con imagen de fondo, las demás se
  achican/opacan; en mobile, layout vertical sin hover; ninguna abierta
  por defecto; resolver con CSS puro en lo posible para no engordar el JS).
- Datos de contacto (email) siguen pendientes de definir.
