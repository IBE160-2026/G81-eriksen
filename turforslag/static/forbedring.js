// Progressiv forbedring for alle sider (AR-18, UX-DR21, NFR-2).
// Ren ES uten avhengigheter. Lastes med defer. Alt virker uten denne fila,
// og feil her stopper aldri siden.
(function () {
  "use strict";

  // Sperre mot dobbeltinnsending: første submit merker skjemaet og setter
  // aria-disabled på knappen. Senere submit på samme skjema stoppes.
  // Knappen er ikke disabled, så den beholder fokus.
  function vedInnsending(hendelse) {
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
    } catch (feil) {
      // Feiler stille: skjemaet sendes som vanlig.
    }
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
