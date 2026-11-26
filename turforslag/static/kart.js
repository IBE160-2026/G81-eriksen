// Kart på Turforslag (FR-6, AR-10, UX-DR13, NFR-4). AD-1: den andre og siste egne JS-fila.
// Ren ES5 uten avhengigheter utover vendret Leaflet 1.9.4, lastet med defer etter leaflet.js.
// Leser ferdig GeoJSON fra json_script og tegner den. Filtrerer, beregner og henter
// ingenting annet enn fliser. Farger står bare i side.css (kart-tokenene).
// Feiler noe, vises Melding (info) med lenke til «Kartet i tekst», og resten av siden virker.
// window.YNAKart.start(element) starter kartet på nytt, for eksempel etter et fragmentbytte (1.11).
// «Kart lastes …» vises med aria-busy på kartflaten til første flisrunde er ferdig (1.11, 1A).
(function () {
  "use strict";

  var FLISER = "https://cache.kartverket.no/v1/wmts/1.0.0/topo/default/webmercator/{z}/{y}/{x}.png";
  var MAKS_ZOOM = 18;
  var HINT_MS = 1500;
  var HJUL_PAUSE_MS = 250; // Ett zoomsteg per hjulbevegelse, også med styreflate.
  // Luft rundt ruten, så knappene oppe og Kreditering nede ikke dekker den.
  var LUFT = { paddingTopLeft: [24, 72], paddingBottomRight: [24, 48] };

  function medier(sporring) {
    return !!(window.matchMedia && window.matchMedia(sporring).matches);
  }

  function stopp(element) {
    if (element.ynaRydd) {
      element.ynaRydd.forEach(function (rydd) {
        rydd();
      });
    }
    element.ynaRydd = [];
  }

  function lytt(element, mal, type, handler, valg) {
    mal.addEventListener(type, handler, valg);
    element.ynaRydd.push(function () {
      mal.removeEventListener(type, handler, valg);
    });
  }

  // «Kart lastes …» og aria-busy på kartflaten (beslutning 1A). Feiler aldri.
  function visLasting(flate, lastes, vis) {
    if (lastes) {
      if (vis) {
        lastes.removeAttribute("hidden");
      } else {
        lastes.setAttribute("hidden", "");
      }
    }
    if (flate) {
      if (vis) {
        flate.setAttribute("aria-busy", "true");
      } else {
        flate.removeAttribute("aria-busy");
      }
    }
  }

  function start(element) {
    try {
      stopp(element);
      // Kontrollene i malen. Klikklytteren kommer før alt som kan feile, så «Prøv igjen»
      // virker også når kartet ikke starter: da lastes siden på nytt. Når kartet er klart,
      // fylles handlingene inn under, og «Prøv igjen» laster bare flisene på nytt.
      var handlinger = {
        "prov-igjen": function () {
          window.location.reload();
        }
      };
      lytt(element, element, "click", function (hendelse) {
        var knapp = hendelse.target.closest("[data-kart-handling]");
        var handling = knapp && element.contains(knapp) && handlinger[knapp.getAttribute("data-kart-handling")];
        if (handling) {
          handling();
        }
      });
      element.classList.remove("no-js", "kart-feil", "kart-hint-vis");
      var flate = element.querySelector(".kart-flate");
      var lastes = element.querySelector(".kart-lastes");
      visLasting(flate, lastes, true);
      element.ynaRydd.push(function () {
        visLasting(flate, lastes, false);
      });
      var rute = JSON.parse(document.getElementById(element.getAttribute("data-kart-geojson")).textContent);
      var stille = medier("(prefers-reduced-motion: reduce)");
      var animer = { animate: !stille };

      // Hjulet ruller siden. På berøringsskjerm er flytting med én finger av (se under).
      var kart = L.map(flate, {
        attributionControl: false,
        zoomControl: false,
        maxZoom: MAKS_ZOOM,
        scrollWheelZoom: false,
        keyboard: true,
        dragging: !medier("(pointer: coarse)"),
        touchZoom: true,
        inertia: !stille,
        zoomAnimation: !stille,
        fadeAnimation: !stille,
        markerZoomAnimation: !stille
      });
      element.ynaRydd.push(function () {
        kart.remove();
      });
      if (stille) {
        // Piltastene flytter kartet med panBy, som ellers animerer.
        var panBy = kart.panBy;
        kart.panBy = function (avstand, valg) {
          return panBy.call(kart, avstand, L.extend({}, valg, { animate: false }));
        };
      }

      // Fliser. Feiler alle i en runde, vises meldingen. «Prøv igjen» laster dem på nytt.
      var lastet = 0;
      var feilet = 0;
      var fliser = L.tileLayer(FLISER, { maxZoom: MAKS_ZOOM });
      fliser.on("loading", function () {
        lastet = 0;
        feilet = 0;
      });
      fliser.on("tileload", function () {
        lastet += 1;
      });
      fliser.on("tileerror", function () {
        feilet += 1;
      });
      fliser.on("load", function () {
        visLasting(flate, lastes, false);
        element.classList.toggle("kart-feil", feilet > 0 && lastet === 0);
      });
      fliser.addTo(kart);

      // Rutelinjen: hvit kant under plommelilla linje. Markørene er pynt og kan ikke få fokus.
      var punkter = L.GeoJSON.coordsToLatLngs(rute.geometry.coordinates);
      L.polyline(punkter, { className: "kart-rute-kant", interactive: false }).addTo(kart);
      var linje = L.polyline(punkter, { className: "kart-rute", interactive: false }).addTo(kart);
      // Kartet får utsnitt før markøren legges til, ellers lages ikke markørens element ennå.
      kart.fitBounds(linje.getBounds(), L.extend({ animate: false }, LUFT));
      if (rute.properties && rute.properties.start) {
        var markor = L.marker(L.GeoJSON.coordsToLatLng(rute.properties.start), {
          icon: L.divIcon({ className: "kart-start", html: "S", iconSize: [24, 24] }),
          interactive: false,
          keyboard: false
        }).addTo(kart);
        if (markor.getElement()) {
          markor.getElement().setAttribute("aria-hidden", "true");
        }
      }
      L.control.scale({ imperial: false, position: "bottomleft" }).addTo(kart);

      // Kartet er klart: kontrollene kobles til kartet.
      handlinger.hele = function () {
        kart.fitBounds(linje.getBounds(), L.extend({}, animer, LUFT));
      };
      handlinger.inn = function () {
        kart.zoomIn(1, animer);
      };
      handlinger.ut = function () {
        kart.zoomOut(1, animer);
      };
      handlinger["prov-igjen"] = function () {
        element.classList.remove("kart-feil");
        fliser.redraw();
        flate.focus();
      };

      // Ctrl/Cmd + hjul zoomer, også over kontrollene og Kreditering. Uten tast ruller
      // hjulet siden som vanlig.
      var sistHjul = 0;
      lytt(element, element, "wheel", function (hendelse) {
        if (!hendelse.ctrlKey && !hendelse.metaKey) {
          return;
        }
        hendelse.preventDefault();
        if (!hendelse.deltaY || Date.now() - sistHjul < HJUL_PAUSE_MS) {
          return;
        }
        sistHjul = Date.now();
        handlinger[hendelse.deltaY < 0 ? "inn" : "ut"]();
      }, { passive: false });

      // Berøring (beslutning 2026-11-26, 1A): dragging er av for berøring, så én finger
      // ruller siden og viser hintet. To fingre flytter og kniper med Leaflets touchZoom
      // (knipingen flytter kartet med seg). Fanges før Leaflets lyttere.
      var hintTid = null;
      function skjulHint() {
        element.classList.remove("kart-hint-vis");
      }
      lytt(element, flate, "touchstart", function (hendelse) {
        window.clearTimeout(hintTid);
        kart.dragging.disable();
        if (hendelse.touches.length > 1) {
          skjulHint();
          return;
        }
        element.classList.add("kart-hint-vis");
        hintTid = window.setTimeout(skjulHint, HINT_MS);
      }, { capture: true, passive: true });
      // Mus på en maskin med berøringsskjerm kan alltid dra kartet.
      lytt(element, flate, "pointerdown", function (hendelse) {
        if (hendelse.pointerType === "mouse") {
          kart.dragging.enable();
        }
      }, true);
      element.ynaRydd.push(function () {
        window.clearTimeout(hintTid);
      });
      return kart;
    } catch (feil) {
      // Kartet kan ikke vises: meldingen og «Kartet i tekst» tar over.
      visLasting(element.querySelector(".kart-flate"), element.querySelector(".kart-lastes"), false);
      element.classList.remove("no-js");
      element.classList.add("kart-feil");
      return null;
    }
  }

  window.YNAKart = { start: start };

  Array.prototype.forEach.call(document.querySelectorAll("[data-kart]"), function (element) {
    start(element);
  });
})();
