"use strict";


/* =========================================================
   ELEMENTOS PRINCIPALES
========================================================= */

const hasGsap = typeof window.gsap !== "undefined";
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

const header = document.querySelector("[data-header]");

const menu = document.querySelector("[data-menu]");
const menuPanel = document.querySelector(".menu-panel");
const menuOverlayBg = document.querySelector(".menu-overlay-bg");
const menuToggle = document.querySelector("[data-menu-toggle]");
const menuClose = document.querySelector("[data-menu-close]");
const menuLinks = document.querySelectorAll("[data-menu-link]");

/* =========================================================
   FALLBACK DE ANIMACIONES
   Si GSAP no carga por red/CDN, la página sigue teniendo
   transiciones y reveals funcionales con CSS + IntersectionObserver.

   IMPORTANTE: esto debe correr SOLO cuando GSAP no está
   disponible. Antes corría siempre, en paralelo con el
   reveal de ScrollTrigger, y la clase "js-reveal" (con su
   propio "transition") terminaba pisando la transición propia
   de .area-card y .service-panel al tener la misma
   especificidad y estar declarada después en el CSS — por eso
   el hover se sentía instantáneo/roto en tarjetas y acordeón.
========================================================= */
if (!hasGsap) {
  const revealTargets = document.querySelectorAll(
    ".professional-content, .section-heading, .about-title, .about-content, .contact-intro, .statement h2, .statement p, .area-card, .service-panel"
  );

  revealTargets.forEach(element => element.classList.add("js-reveal"));

  if ("IntersectionObserver" in window) {
    const revealObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        revealObserver.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });

    revealTargets.forEach(element => revealObserver.observe(element));
  } else {
    revealTargets.forEach(element => element.classList.add("is-visible"));
  }
}



/* =========================================================
   PRELOADER
========================================================= */

window.addEventListener("load", () => {
  const preloader = document.querySelector("[data-preloader]");

  if (!preloader) return;

  /* Se sostiene un poco más para que el logo alcance a leerse
     bien antes de empezar el fade (antes eran 400ms). */
  setTimeout(() => {
    preloader.classList.add("loaded");
  }, 1600);
});


/* =========================================================
   HEADER AL HACER SCROLL
========================================================= */

function updateHeader() {
  if (!header) return;

  header.classList.toggle("scrolled", window.scrollY > 40);
}

window.addEventListener("scroll", updateHeader, {
  passive: true
});

updateHeader();


/* =========================================================
   MENU
========================================================= */

let menuOpen = false;
let menuTimeline = null;


function resetMenuStyles() {
  if (!hasGsap) return;

  gsap.set(menuPanel, {
    clearProps: "transform"
  });

  gsap.set(menuOverlayBg, {
    clearProps: "opacity"
  });

  gsap.set(".menu-navigation a", {
    clearProps: "all"
  });
}


function openMenu() {
  if (!menu || !menuPanel || !menuOverlayBg) return;
  if (menuOpen) return;

  menuOpen = true;

  menu.classList.add("active");
  document.body.classList.add("menu-open");

  menuToggle?.setAttribute("aria-expanded", "true");
  menuToggle?.setAttribute("aria-label", "Cerrar menú");

  if (!hasGsap || reducedMotion.matches) {
    return;
  }

  if (menuTimeline) {
    menuTimeline.kill();
  }

  resetMenuStyles();

  menuTimeline = gsap.timeline();

  menuTimeline
    .fromTo(
      menuOverlayBg,
      {
        opacity: 0
      },
      {
        opacity: 1,
        duration: 0.45,
        ease: "power2.out"
      }
    )
    .fromTo(
      menuPanel,
      {
        x: "100%"
      },
      {
        x: "0%",
        duration: 0.7,
        ease: "power4.out"
      },
      "-=0.25"
    )
    .fromTo(
      ".menu-navigation a",
      {
        x: 40,
        opacity: 0
      },
      {
        x: 0,
        opacity: 1,
        duration: 0.45,
        stagger: 0.06,
        ease: "power3.out"
      },
      "-=0.35"
    );
}


function closeMenu() {
  if (!menu || !menuPanel || !menuOverlayBg) return;
  if (!menuOpen) return;

  menuOpen = false;

  if (!hasGsap || reducedMotion.matches) {
    menu.classList.remove("active");
    document.body.classList.remove("menu-open");

    menuToggle?.setAttribute("aria-expanded", "false");
    menuToggle?.setAttribute("aria-label", "Abrir menú");

    resetMenuStyles();

    return;
  }

  if (menuTimeline) {
    menuTimeline.kill();
  }

  menuTimeline = gsap.timeline({
    onComplete: () => {
      menu.classList.remove("active");
      document.body.classList.remove("menu-open");

      menuToggle?.setAttribute("aria-expanded", "false");
      menuToggle?.setAttribute("aria-label", "Abrir menú");

      resetMenuStyles();

      menuTimeline = null;
    }
  });

  menuTimeline
    .to(
      ".menu-navigation a",
      {
        x: 20,
        opacity: 0,
        duration: 0.25,
        stagger: 0.025,
        ease: "power2.in"
      }
    )
    .to(
      menuPanel,
      {
        x: "100%",
        duration: 0.55,
        ease: "power3.inOut"
      },
      "-=0.1"
    )
    .to(
      menuOverlayBg,
      {
        opacity: 0,
        duration: 0.4,
        ease: "power2.out"
      },
      "-=0.3"
    );
}


menuToggle?.addEventListener("click", () => {
  if (menuOpen) {
    closeMenu();
  } else {
    openMenu();
  }
});


menuClose?.addEventListener("click", closeMenu);


menuOverlayBg?.addEventListener("click", closeMenu);


menuLinks.forEach(link => {
  link.addEventListener("click", event => {
    const targetId = link.getAttribute("href");

    if (targetId && targetId.startsWith("#")) {
      event.preventDefault();
      const targetElement = document.querySelector(targetId);

      closeMenu();

      if (targetElement) {
        // En mobile se espera un breve instante a que el panel se retire
        const delay = window.innerWidth <= 768 ? 200 : 80;
        setTimeout(() => {
          targetElement.scrollIntoView({ behavior: "smooth", block: "start" });
        }, delay);
      }
    } else {
      closeMenu();
    }
  });
});


document.addEventListener("keydown", event => {
  if (event.key === "Escape" && menuOpen) {
    closeMenu();
  }
});


/* =========================================================
   HERO SLIDER
========================================================= */

const heroSlides = document.querySelectorAll("[data-hero-slide]");

let currentSlide = 0;
let heroTimer = null;
let isAnimatingSlide = false;

/* Duración del zoom Ken Burns por imagen: debe ser MENOR al
   intervalo del carrusel para que siempre termine de zoomear
   antes de cambiar de slide. Antes el timer (7000ms) cortaba
   la transición (8500ms) a mitad de camino, y la imagen
   retomaba desde una escala random la próxima vez — eso se
   veía "desfigurado". */
const HERO_ZOOM_MS = 7200;
const HERO_INTERVAL_MS = 7800;

function resetZoom(image) {
  if (!image) return;

  image.classList.remove("is-zooming");

  // Fuerza el reflow para poder reiniciar la transición limpia
  void image.offsetWidth;
}

function startZoom(image) {
  if (!image) return;

  requestAnimationFrame(() => {
    image.classList.add("is-zooming");
  });
}


function animateSlideIn(slide) {
  if (!hasGsap || reducedMotion.matches || !slide) return;

  const title = slide.querySelector(".hero-title");
  const description = slide.querySelector(".hero-description");
  const button = slide.querySelector(".hero-button");

  gsap.timeline()
    .fromTo(
      title,
      {
        y: 45,
        opacity: 0
      },
      {
        y: 0,
        opacity: 1,
        duration: 0.9,
        ease: "power4.out"
      }
    )
    .fromTo(
      description,
      {
        y: 25,
        opacity: 0
      },
      {
        y: 0,
        opacity: 1,
        duration: 0.7,
        ease: "power3.out"
      },
      "-=0.55"
    )
    .fromTo(
      button,
      {
        y: 20,
        opacity: 0
      },
      {
        y: 0,
        opacity: 1,
        duration: 0.6,
        ease: "power3.out"
      },
      "-=0.4"
    );
}


function changeSlide(nextIndex) {
  if (
    isAnimatingSlide ||
    !heroSlides.length ||
    nextIndex === currentSlide
  ) {
    return;
  }

  const oldSlideFallback = heroSlides[currentSlide];
  const newSlideFallback = heroSlides[nextIndex];

  if (!hasGsap || reducedMotion.matches) {
    oldSlideFallback.classList.remove("is-active");
    resetZoom(oldSlideFallback.querySelector(".hero-image"));

    newSlideFallback.classList.add("is-active");

    const newImageFallback = newSlideFallback.querySelector(".hero-image");
    resetZoom(newImageFallback);
    startZoom(newImageFallback);

    currentSlide = nextIndex;

    return;
  }

  isAnimatingSlide = true;

  const oldSlide = heroSlides[currentSlide];
  const newSlide = heroSlides[nextIndex];

  const oldContent = oldSlide.querySelector(".hero-copy");
  const newContent = newSlide.querySelector(".hero-copy");

  newSlide.classList.add("is-active");

  const newImage = newSlide.querySelector(".hero-image");
  resetZoom(newImage);
  startZoom(newImage);

  gsap.timeline({
    onComplete: () => {
      oldSlide.classList.remove("is-active");
      resetZoom(oldSlide.querySelector(".hero-image"));

      currentSlide = nextIndex;
      isAnimatingSlide = false;
    }
  })
    .to(
      oldContent,
      {
        y: -30,
        opacity: 0,
        duration: 0.45,
        ease: "power2.in"
      }
    )
    .fromTo(
      newContent,
      {
        y: 45,
        opacity: 0
      },
      {
        y: 0,
        opacity: 1,
        duration: 0.8,
        ease: "power4.out"
      },
      "-=0.25"
    );
}


function nextSlide() {
  if (!heroSlides.length) return;

  changeSlide(
    (currentSlide + 1) % heroSlides.length
  );
}


function startHeroTimer() {
  stopHeroTimer();

  if (reducedMotion.matches) return;

  heroTimer = setInterval(nextSlide, HERO_INTERVAL_MS);
}


function stopHeroTimer() {
  if (!heroTimer) return;

  clearInterval(heroTimer);
  heroTimer = null;
}


if (heroSlides.length) {
  const firstSlide = heroSlides[0];
  const firstImage = firstSlide.querySelector(".hero-image");

  // Antes, al venir "is-active" ya puesto en el HTML, el
  // navegador no tenía un "estado anterior" desde el cual
  // animar y la primera imagen quedaba estática (sin zoom).
  resetZoom(firstImage);
  startZoom(firstImage);

  if (!hasGsap) {
    firstSlide.querySelector(".hero-copy")?.classList.add("is-fallback-visible");
  }

  if (!reducedMotion.matches) {
    animateSlideIn(firstSlide);
    startHeroTimer();
  }
}


/* =========================================================
   PAUSAR HERO CUANDO LA PESTAÑA NO ESTÁ VISIBLE
========================================================= */

document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    stopHeroTimer();
    return;
  }

  if (!reducedMotion.matches) {
    startHeroTimer();
  }
});


/* =========================================================
   GSAP + SCROLLTRIGGER
========================================================= */

if (
  hasGsap &&
  typeof ScrollTrigger !== "undefined" &&
  !reducedMotion.matches
) {

  gsap.registerPlugin(ScrollTrigger);


  /* -------------------------------------------------------
     TRAZO DORADO
  ------------------------------------------------------- */

  const heroLinePath = document.querySelector(".hero-line-path");

  if (heroLinePath) {
    const pathLength = heroLinePath.getTotalLength();

    gsap.set(heroLinePath, {
      strokeDasharray: pathLength,
      strokeDashoffset: pathLength
    });

    gsap.to(
      heroLinePath,
      {
        strokeDashoffset: 0,
        duration: 1.8,
        ease: "power3.inOut"
      }
    );
  }


  /* -------------------------------------------------------
     HERO SCROLL

     IMPORTANTE:
     No tocamos el scale de las imágenes acá.
     El zoom cinematográfico pertenece al CSS del slider.
  ------------------------------------------------------- */

  const hero = document.querySelector(".hero");
  const heroImageWraps = document.querySelectorAll(".hero-image-wrap");
  const heroTitles = document.querySelectorAll(".hero-title");
  const heroLineWrap = document.querySelector(".hero-line-wrap");

  if (hero) {

    gsap.timeline({
      scrollTrigger: {
        trigger: hero,
        start: "top top",
        end: "bottom top",
        scrub: 1
      }
    })
      .to(
        heroImageWraps,
        {
          yPercent: 8,
          ease: "none"
        },
        0
      )
      .to(
        heroTitles,
        {
          yPercent: -8,
          ease: "none"
        },
        0
      )
      .to(
        heroLineWrap,
        {
          y: 25,
          opacity: 0.75,
          ease: "none"
        },
        0
      );
  }


  /* -------------------------------------------------------
     REVEAL DE SECCIONES
  ------------------------------------------------------- */

  gsap.utils
    .toArray(
      ".professional-content, .section-heading, .about-title, .about-content, .contact-intro, .statement h2, .statement p"
    )
    .forEach(element => {

      gsap.fromTo(
        element,
        {
          y: 45,
          opacity: 0
        },
        {
          y: 0,
          opacity: 1,
          duration: 1.1,
          ease: "power3.out",

          scrollTrigger: {
            trigger: element,
            start: "top 82%",
            toggleActions: "play none none reverse"
          }
        }
      );

    });


  /* -------------------------------------------------------
     AREA CARDS
  ------------------------------------------------------- */

  gsap.utils
    .toArray(".area-card")
    .forEach((card, index) => {

      gsap.fromTo(
        card,
        {
          y: 50,
          opacity: 0
        },
        {
          y: 0,
          opacity: 1,
          duration: 0.8,
          delay: index * 0.08,
          ease: "power3.out",

          scrollTrigger: {
            trigger: card,
            start: "top 88%",
            toggleActions: "play none none reverse"
          }
        }
      );

    });


  /* -------------------------------------------------------
     SERVICE PANELS
  ------------------------------------------------------- */

  gsap.utils
    .toArray(".service-panel")
    .forEach(panel => {

      gsap.fromTo(
        panel,
        {
          y: 35,
          opacity: 0
        },
        {
          y: 0,
          opacity: 1,
          duration: 0.8,
          ease: "power3.out",

          clearProps: "opacity,transform",

          scrollTrigger: {
            trigger: panel,
            start: "top 88%",
            toggleActions: "play none none reverse"
          }
        }
      );

    });


  window.addEventListener("load", () => {
    ScrollTrigger.refresh();
  });
}


/* =========================================================
   SERVICIOS — ACORDEÓN
========================================================= */

const servicePanels = document.querySelectorAll(
  "[data-service-trigger]"
);

servicePanels.forEach(button => {

  button.addEventListener("click", () => {

    const panel = button.closest(".service-panel");

    if (!panel) return;

    const isOpen = panel.classList.contains("is-active");


    servicePanels.forEach(otherButton => {

      const otherPanel =
        otherButton.closest(".service-panel");

      if (!otherPanel) return;

      otherPanel.classList.remove("is-active");

      otherButton.setAttribute(
        "aria-expanded",
        "false"
      );

    });


    if (!isOpen) {

      panel.classList.add("is-active");

      button.setAttribute(
        "aria-expanded",
        "true"
      );

    }

  });

});


/* Todas las tarjetas cerradas desde el primer acceso.
   Asegura el estado inicial sin depender del HTML. */
document.addEventListener("DOMContentLoaded", () => {

  servicePanels.forEach(button => {

    const panel = button.closest(".service-panel");

    if (!panel) return;

    panel.classList.remove("is-active");

    button.setAttribute(
      "aria-expanded",
      "false"
    );

  });

});


/* =========================================================
   WHATSAPP
========================================================= */

const WA_NUMBER = "5492804607019";

const defaultMessage =
  "Hola Dr. Crespo, quisiera hacer una consulta.";


function waLink(message) {

  return (
    "https://wa.me/" +
    WA_NUMBER +
    "?text=" +
    encodeURIComponent(message)
  );

}


["waMenu", "waContact", "waFloat"].forEach(id => {

  const element = document.getElementById(id);

  if (!element) return;

  element.href = waLink(defaultMessage);

});


/* =========================================================
   FORMULARIO
========================================================= */

const contactForm =
  document.getElementById("contactForm");

const formConfirm =
  document.getElementById("formConfirm");


if (contactForm) {

  contactForm.addEventListener("submit", event => {

    event.preventDefault();


    const nombreInput =
      document.getElementById("nombre");

    const emailInput =
      document.getElementById("email");

    const mensajeInput =
      document.getElementById("mensaje");


    const nombre =
      nombreInput?.value.trim() || "";

    const email =
      emailInput?.value.trim() || "";

    const telefono =
      document.getElementById("telefono")
        ?.value.trim() ||
      "No brindó teléfono";

    const mensaje =
      mensajeInput?.value.trim() || "";


    /* -----------------------------------------------------
       VALIDACIÓN
    ----------------------------------------------------- */

    let valid = true;


    [
      [nombreInput, nombre],
      [mensajeInput, mensaje]
    ].forEach(([input, value]) => {

      if (!input) return;

      const invalid = !value;

      input.classList.toggle(
        "is-invalid",
        invalid
      );

      if (invalid) {
        valid = false;
      }

    });


    if (emailInput) {

      const emailOk =
        !email ||
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

      emailInput.classList.toggle(
        "is-invalid",
        !emailOk
      );

      if (!emailOk) {
        valid = false;
      }

    }


    if (!valid) return;


    /* -----------------------------------------------------
       MENSAJE WHATSAPP
    ----------------------------------------------------- */

    const text =
      "Hola Dr. Crespo, soy " +
      nombre +
      ". Mi email es " +
      (email || "no brindó email") +
      ". Teléfono: " +
      telefono +
      ". Consulta: " +
      mensaje;


    formConfirm?.classList.add("show");


    window.open(
      waLink(text),
      "_blank",
      "noopener"
    );


    contactForm.reset();

  });


  /* -------------------------------------------------------
     QUITAR ERROR AL ESCRIBIR
  ------------------------------------------------------- */

  contactForm
    .querySelectorAll("input, textarea")
    .forEach(field => {

      field.addEventListener("input", () => {

        field.classList.remove(
          "is-invalid"
        );

      });

    });

}


/* =========================================================
   REDUCED MOTION
========================================================= */

if (reducedMotion.matches) {

  if (hasGsap) {
    gsap.globalTimeline.pause(0);
  }

  stopHeroTimer();

  document.documentElement.style.scrollBehavior =
    "auto";
}