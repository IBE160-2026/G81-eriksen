// Progressiv forbedring for alle sider (AR-18, UX-DR21, UX-DR22–25, NFR-2).
// Ren ES5 uten avhengigheter. Lastes med defer. Alt virker uten denne fila,
// og feil her stopper aldri siden.
// «Nytt forslag» (FR-7, 1.11): skjemaet sendes med fetch og headeren X-Fragment: 1, og
// fetch følger PRG-redirecten til fragmentet (HTML, aldri JSON). Rotelementet ([data-tittel])
// byttes, document.title settes, fokus går til ny h1, og kartet startes med YNAKart.start.
// Feiler hentingen, sendes skjemaet som vanlig.
(function () {
  "use strict";

  // Sperre mot dobbeltinnsending: første submit merker skjemaet og setter
  // aria-disabled på knappen. Senere submit på samme skjema stoppes.
  // Knappen er ikke disabled, så den beholder fokus.
  function vedInnsending(hendelse) {
    var stoppet = false;
    try {
      var skjema = hendelse.target;
      if (!(skjema instanceof HTMLFormElement) || hendelse.defaultPrevented) {
        return;
      }
      if (skjema.hasAttribute("data-sendes")) {
        hendelse.preventDefault();
        return;
      }
      skjema.setAttribute("data-sendes", "");
      var knapp =
        hendelse.submitter ||
        skjema.querySelector('button:not([type]), button[type="submit"], input[type="submit"]');
      if (knapp) {
        knapp.setAttribute("aria-disabled", "true");
      }
      if (skjema.hasAttribute("data-nytt-forslag") && window.fetch && window.DOMParser && window.FormData) {
        hendelse.preventDefault();
        stoppet = true;
        hentForslag(skjema);
      }
    } catch (feil) {
      // Feiler stille: skjemaet sendes som vanlig. Er innsendingen alt stoppet for
      // fragmentbyttet, sendes det her uten submit-hendelse.
      if (stoppet) {
        hendelse.target.submit();
      }
    }
  }

  // Henter nytt forslag som HTML-fragment og bytter det inn (FR-7, UX-DR22–25).
  // Det gamle forslaget dempes (aria-busy, side.css), knappen beholder fokus, og
  // lasteteksten leses opp i live-regionen utenfor beholderen. Selve byttet meldes ikke.
  function hentForslag(skjema) {
    var gammel = skjema.closest("[data-tittel]");
    var status = document.querySelector("[data-lastestatus]");
    var byttet = false;
    if (!gammel) {
      skjema.submit();
      return;
    }
    gammel.setAttribute("aria-busy", "true");
    if (status) {
      status.textContent = skjema.getAttribute("data-lastetekst") || "";
    }
    fetch(skjema.action, {
      method: "POST",
      body: new FormData(skjema),
      headers: { "X-Fragment": "1" },
      credentials: "same-origin"
    })
      .then(function (svar) {
        if (!svar.ok) {
          throw svar;
        }
        return svar.text();
      })
      .then(function (html) {
        var dokument = new DOMParser().parseFromString(html, "text/html");
        var ny = dokument.querySelector("[data-tittel]");
        if (!ny || !gammel.parentNode) {
          throw new Error("Svaret har ikke noe forslag.");
        }
        ny = document.importNode(ny, true);
        gammel.parentNode.replaceChild(ny, gammel);
        byttet = true;
        if (status) {
          status.textContent = "";
        }
        document.title = ny.getAttribute("data-tittel");
        var kart = ny.querySelector("[data-kart]");
        if (kart && window.YNAKart) {
          window.YNAKart.start(kart);
        }
        var overskrift = ny.querySelector("h1");
        if (overskrift) {
          overskrift.focus();
        }
      })
      .catch(function () {
        if (!byttet) {
          // Vanlig innsending uten submit-hendelse, så sperren ikke stopper den.
          skjema.submit();
        }
      });
  }

  // Siden kan komme tilbake fra nettleserens hurtigbuffer (Tilbake-knappen).
  // Da slippes sperren, så skjemaet kan sendes igjen.
  function vedVisning(hendelse) {
    try {
      if (!hendelse.persisted) {
        return;
      }
      document.querySelectorAll("form[data-sendes]").forEach(function (skjema) {
        skjema.removeAttribute("data-sendes");
        skjema.querySelectorAll('[aria-disabled="true"]').forEach(function (knapp) {
          knapp.removeAttribute("aria-disabled");
        });
      });
    } catch (feil) {
      // Feiler stille.
    }
  }

  // Melding etter navigering (tabindex="-1" og data-fokus) får fokus ved innlasting.
  function giFokus() {
    try {
      var element = document.querySelector("[data-fokus]");
      if (element) {
        element.focus();
      }
    } catch (feil) {
      // Feiler stille.
    }
  }

  document.addEventListener("submit", vedInnsending);
  window.addEventListener("pageshow", vedVisning);
  giFokus();
})();
