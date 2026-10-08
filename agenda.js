/* =========================================================
   AGENDA DE TURNOS — página /agendar/
   ---------------------------------------------------------
   Versión simple, sin backend:
   1. El cliente elige modalidad, día y horario (lunes a viernes,
      en hora de Argentina sin importar desde qué país entre).
   2. "Continuar" lleva a "Confirmá tu turno", que avisa ANTES de
      abrir Mercado Pago (el navegador siempre salta a la pestaña
      nueva, así que primero se lee y después se paga).
   3. Paga con el link del Dr. (otra pestaña), vuelve y le manda
      el turno por WhatsApp (mensaje ya escrito) con la captura
      del comprobante. El Dr. busca el N° de operación de la
      captura en su app de Mercado Pago y recién ahí confirma el
      turno (las capturas se falsifican).

   LINK_MERCADOPAGO: el Dr. lo crea en la app de Mercado Pago
   (Cobrar → Link de pago, monto fijo, que se pueda usar varias
   veces) y se pega acá. Mientras esté vacío, la página funciona
   en MODO DEMO (sirve para la preview).
========================================================= */

const LINK_MERCADOPAGO = "https://mpago.li/1bM3MA2";
const WHATSAPP = "5492804607019";
const PRECIO = "$ 50.000";

(() => {
  const form = document.querySelector("[data-agenda]");

  if (!form) return;

  const DEMO = !LINK_MERCADOPAGO;
  const ZONA = "America/Argentina/Buenos_Aires";
  const HORA_INICIO = 9;
  const HORA_FIN = 16;
  const DURACION_MIN = 60;
  const DIAS_ADELANTE = 30;
  const HORAS_ANTICIPACION = 24;

  const DIAS = ["domingo", "lunes", "martes", "miércoles", "jueves", "viernes", "sábado"];
  const MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"];

  const raiz = form.closest(".agenda-layout");
  const $ = selector => raiz.querySelector(selector);

  const el = {
    demo: $("[data-agenda-demo]"),
    month: $("[data-agenda-month]"),
    prev: $("[data-agenda-prev]"),
    next: $("[data-agenda-next]"),
    days: $("[data-agenda-days]"),
    times: $("[data-agenda-times]"),
    error: $("[data-agenda-error]"),
    summary: $(".agenda-summary"),
    done: $("[data-agenda-done]"),
    doneText: $("[data-agenda-done-text]"),
    whatsapp: $("[data-agenda-whatsapp]"),
    pago: $("[data-agenda-pago]"),
    pasos: [...raiz.querySelectorAll("[data-paso]")],
    volver: $("[data-agenda-volver]"),
    waError: $("[data-agenda-wa-error]"),
  };

  const estado = {
    modalidad: "",
    dia: "",   // "2026-10-05"
    hora: "",  // "09:00"
    mes: null, // { y, m } (m: 1-12)
  };

  /* -------------------------------------------------------
     FECHAS EN HORA DE ARGENTINA
     Todo se maneja como "minutos de reloj argentino", así el
     calendario es el mismo aunque el cliente esté en Italia.
  ------------------------------------------------------- */

  function ahoraArgentina() {
    const partes = Object.fromEntries(
      new Intl.DateTimeFormat("en-CA", {
        timeZone: ZONA,
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        hourCycle: "h23",
      })
        .formatToParts(new Date())
        .map(p => [p.type, p.value])
    );

    return {
      y: Number(partes.year),
      m: Number(partes.month),
      d: Number(partes.day),
      h: Number(partes.hour),
      min: Number(partes.minute),
    };
  }

  const pad = n => String(n).padStart(2, "0");
  const claveDia = (y, m, d) => `${y}-${pad(m)}-${pad(d)}`;
  const minutosDe = (y, m, d, h = 0, min = 0) => Date.UTC(y, m - 1, d, h, min) / 60000;
  const diaSemana = (y, m, d) => new Date(Date.UTC(y, m - 1, d)).getUTCDay(); // 0 = domingo

  function horarios() {
    const lista = [];

    for (let t = HORA_INICIO * 60; t + DURACION_MIN <= HORA_FIN * 60; t += DURACION_MIN) {
      lista.push(`${pad(Math.floor(t / 60))}:${pad(t % 60)}`);
    }

    return lista;
  }

  function turnoDisponible(dia, hora) {
    const [y, m, d] = dia.split("-").map(Number);
    const [h, min] = hora.split(":").map(Number);
    const ahora = ahoraArgentina();
    const limite = minutosDe(ahora.y, ahora.m, ahora.d, ahora.h, ahora.min) + HORAS_ANTICIPACION * 60;

    return minutosDe(y, m, d, h, min) >= limite;
  }

  function diaHabilitado(y, m, d) {
    const semana = diaSemana(y, m, d);
    const ahora = ahoraArgentina();
    const hoy = minutosDe(ahora.y, ahora.m, ahora.d);
    const este = minutosDe(y, m, d);

    if (semana === 0 || semana === 6) return false;
    if (este < hoy || este > hoy + DIAS_ADELANTE * 1440) return false;

    return horarios().some(hora => turnoDisponible(claveDia(y, m, d), hora));
  }

  function fechaLarga(dia) {
    const [y, m, d] = dia.split("-").map(Number);
    return `${DIAS[diaSemana(y, m, d)]} ${d} de ${MESES[m - 1]}`;
  }

  /* -------------------------------------------------------
     CALENDARIO
  ------------------------------------------------------- */

  function dibujarMes() {
    const { y, m } = estado.mes;
    const ahora = ahoraArgentina();
    const primerDia = (diaSemana(y, m, 1) + 6) % 7; // lunes = 0
    const diasDelMes = new Date(Date.UTC(y, m, 0)).getUTCDate();

    el.month.textContent = `${MESES[m - 1]} ${y}`;

    // No se puede ir antes del mes actual ni después del último día habilitado
    const limite = new Date(Date.UTC(ahora.y, ahora.m - 1, ahora.d + DIAS_ADELANTE));
    el.prev.disabled = y === ahora.y && m === ahora.m;
    el.next.disabled = y > limite.getUTCFullYear() || (y === limite.getUTCFullYear() && m >= limite.getUTCMonth() + 1);

    const fragmento = document.createDocumentFragment();

    for (let i = 0; i < primerDia; i++) {
      fragmento.appendChild(document.createElement("span"));
    }

    for (let d = 1; d <= diasDelMes; d++) {
      const clave = claveDia(y, m, d);
      const boton = document.createElement("button");

      boton.type = "button";
      boton.className = "agenda-day";
      boton.textContent = d;
      boton.dataset.dia = clave;
      boton.setAttribute("aria-label", fechaLarga(clave));
      boton.disabled = !diaHabilitado(y, m, d);

      if (clave === estado.dia) {
        boton.classList.add("is-selected");
        boton.setAttribute("aria-pressed", "true");
      }

      fragmento.appendChild(boton);
    }

    el.days.replaceChildren(fragmento);
  }

  function dibujarHorarios() {
    el.times.replaceChildren();

    if (!estado.dia) return;

    const titulo = document.createElement("p");
    titulo.className = "agenda-times-title";
    titulo.textContent = `Horarios del ${fechaLarga(estado.dia)}`;
    el.times.appendChild(titulo);

    const grilla = document.createElement("div");
    grilla.className = "agenda-times-grid";

    horarios().forEach(hora => {
      const boton = document.createElement("button");

      boton.type = "button";
      boton.className = "agenda-time";
      boton.textContent = `${hora} hs`;
      boton.dataset.hora = hora;
      boton.disabled = !turnoDisponible(estado.dia, hora);

      if (hora === estado.hora) {
        boton.classList.add("is-selected");
        boton.setAttribute("aria-pressed", "true");
      }

      grilla.appendChild(boton);
    });

    el.times.appendChild(grilla);

    // Los turnos no se bloquean solos: dos personas pueden pedir el mismo
    if (estado.hora) {
      const aviso = document.createElement("p");
      aviso.className = "agenda-aviso";
      aviso.innerHTML =
        "<strong>Horario a confirmar.</strong> El Dr. te lo confirma por WhatsApp; " +
        "si ya está tomado, te ofrece otro.";
      el.times.appendChild(aviso);
    }
  }

  function actualizarResumen() {
    const resumen = campo => el.summary.querySelector(`[data-resumen="${campo}"]`);

    resumen("modalidad").textContent =
      estado.modalidad === "presencial" ? "Presencial (CABA)" : estado.modalidad === "virtual" ? "Virtual" : "—";
    resumen("dia").textContent = estado.dia ? fechaLarga(estado.dia) : "—";
    resumen("hora").textContent = estado.hora ? `${estado.hora} hs (a confirmar)` : "—";
    resumen("precio").textContent = PRECIO;
  }

  el.days.addEventListener("click", event => {
    const boton = event.target.closest("[data-dia]");
    if (!boton || boton.disabled) return;

    estado.dia = boton.dataset.dia;
    estado.hora = "";

    dibujarMes();
    dibujarHorarios();
    actualizarResumen();
  });

  el.times.addEventListener("click", event => {
    const boton = event.target.closest("[data-hora]");
    if (!boton || boton.disabled) return;

    estado.hora = boton.dataset.hora;

    dibujarHorarios();
    actualizarResumen();
  });

  function moverMes(delta) {
    let { y, m } = estado.mes;
    m += delta;
    if (m === 0) { m = 12; y--; }
    if (m === 13) { m = 1; y++; }
    estado.mes = { y, m };
    dibujarMes();
  }

  el.prev.addEventListener("click", () => moverMes(-1));
  el.next.addEventListener("click", () => moverMes(1));

  form.addEventListener("change", event => {
    if (event.target.name === "modalidad") {
      estado.modalidad = event.target.value;
      actualizarResumen();
    }
  });

  // Apenas la persona corrige algo, el aviso de error se va
  ["input", "change", "click"].forEach(tipo =>
    form.addEventListener(tipo, event => {
      if (event.target.closest(".agenda-submit")) return;
      if (!el.error.hidden) mostrarError("");
    })
  );

  /* -------------------------------------------------------
     ENVÍO: arma el WhatsApp y pasa a "Confirmá tu turno"
  ------------------------------------------------------- */

  function mostrarError(mensaje) {
    el.error.textContent = mensaje;
    el.error.hidden = !mensaje;
    if (mensaje) el.error.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  function validar(datos) {
    if (!estado.modalidad) return "Elegí si la consulta es virtual o presencial.";
    if (!estado.dia || !estado.hora) return "Elegí el día y el horario del turno.";
    if (!datos.nombre) return "Completá tu nombre.";
    if (!datos.consulta) return "Contanos brevemente tu consulta.";
    return "";
  }

  form.addEventListener("submit", event => {
    event.preventDefault();

    const campos = new FormData(form);
    const datos = {
      nombre: String(campos.get("nombre") || "").trim(),
      consulta: String(campos.get("consulta") || "").trim(),
    };

    const problema = validar(datos);
    if (problema) return mostrarError(problema);

    const mensaje = [
      "Hola, pagué la consulta por Mercado Pago y quiero confirmar mi turno.",
      `Nombre: ${datos.nombre}`,
      `Modalidad: ${estado.modalidad === "presencial" ? "presencial" : "virtual"}`,
      `Turno: ${fechaLarga(estado.dia)}, ${estado.hora} hs (hora de Argentina)`,
      `Consulta: ${datos.consulta}`,
      "",
      "Te adjunto la captura del comprobante.",
    ].join("\n");

    // En el celular wa.me abre la app. En la compu abre WhatsApp Web
    // directo: wa.me ahí dispara el cartel "¿Abrir la aplicación?"
    const celular = /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent);
    const texto = encodeURIComponent(mensaje);
    el.whatsapp.href = celular
      ? `https://wa.me/${WHATSAPP}?text=${texto}`
      : `https://web.whatsapp.com/send?phone=${WHATSAPP}&text=${texto}`;

    const modalidad = estado.modalidad === "presencial" ? "Presencial" : "Virtual";
    const dia = fechaLarga(estado.dia);
    el.doneText.textContent =
      `${dia.charAt(0).toUpperCase()}${dia.slice(1)}, ${estado.hora} hs · ${modalidad} · ${PRECIO}`;

    el.pago.href = DEMO ? "#" : LINK_MERCADOPAGO;
    marcarPaso("pago");

    form.hidden = true;
    el.summary.hidden = true;
    el.done.hidden = false;
    el.done.focus();
    el.done.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  /* -------------------------------------------------------
     PASOS: el WhatsApp queda bloqueado hasta que se toca
     "Pagar". Al tocarlo, el paso 1 queda hecho y se habilita
     el 2. (La web no sabe si el pago se completó: eso lo
     verifica el Dr. en su app de Mercado Pago.)
  ------------------------------------------------------- */

  function marcarPaso(activo) {
    el.pasos.forEach(paso => {
      paso.classList.toggle("is-active", paso.dataset.paso === activo);
      paso.classList.toggle("is-done", activo === "whatsapp" && paso.dataset.paso === "pago");
    });

    el.whatsapp.setAttribute("aria-disabled", String(activo !== "whatsapp"));
    el.waError.hidden = true;
  }

  el.whatsapp.addEventListener("click", event => {
    if (el.whatsapp.getAttribute("aria-disabled") !== "true") return;

    event.preventDefault();
    el.waError.hidden = false;
  });

  el.pago.addEventListener("click", event => {
    if (DEMO) {
      event.preventDefault();
      alert("Vista previa: acá se abriría Mercado Pago.");
    }
    marcarPaso("whatsapp");
  });

  el.volver.addEventListener("click", () => {
    el.done.hidden = true;
    form.hidden = false;
    el.summary.hidden = false;
    form.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  /* -------------------------------------------------------
     INICIO
  ------------------------------------------------------- */

  const ahora = ahoraArgentina();
  estado.mes = { y: ahora.y, m: ahora.m };

  if (DEMO) el.demo.hidden = false;

  // Si en el mes actual ya no quedan días, arranca en el siguiente
  const total = new Date(Date.UTC(ahora.y, ahora.m, 0)).getUTCDate();
  let quedanDias = false;
  for (let d = 1; d <= total; d++) if (diaHabilitado(ahora.y, ahora.m, d)) quedanDias = true;
  if (!quedanDias) moverMes(1);

  dibujarMes();
  actualizarResumen();
})();
