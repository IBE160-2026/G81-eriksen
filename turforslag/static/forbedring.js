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
      // «Vis passord»: nettleseren kan gjenopprette avkrysningen, så feltets type følger den.
      document.querySelectorAll(".vis-passord input").forEach(function (boks) {
        var felt = boks.parentNode.parentNode.querySelector("input[id]");
        if (felt) {
          felt.type = boks.checked ? "text" : "password";
        }
      });
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

  // «Vis passord» (FR-14, 2.1): en avkrysningsboks under hvert passordfelt bytter mellom
  // type="password" og type="text". Uten JS står feltet som vanlig passordfelt.
  function visPassord() {
    try {
      document.querySelectorAll('input[type="password"]').forEach(function (felt) {
        var etikett = document.createElement("label");
        etikett.className = "vis-passord";
        var boks = document.createElement("input");
        boks.type = "checkbox";
        boks.addEventListener("change", function () {
          felt.type = boks.checked ? "text" : "password";
        });
        etikett.appendChild(boks);
        etikett.appendChild(document.createTextNode("Vis passord"));
        felt.parentNode.appendChild(etikett);
      });
    } catch (feil) {
      // Feiler stille.
    }
  }

  document.addEventListener("submit", vedInnsending);
  window.addEventListener("pageshow", vedVisning);
  giFokus();
  visPassord();
})();
