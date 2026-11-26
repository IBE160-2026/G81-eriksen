"""Forsiden og de norske feilsidene (NFR-1, AD-12 punkt 5)."""

from django.test import Client, SimpleTestCase, TestCase, override_settings

LENKE_TIL_SOK = '<a href="/">Gå til Søk</a>'


class ForsideTest(TestCase):
    # Søk leser startpunktene fra databasen (story 1.9), så testene trenger TestCase.
    def test_forsiden_viser_overskriften(self):  # NFR-1
        svar = self.client.get("/")
        self.assertEqual(svar.status_code, 200)
        self.assertContains(
            svar, '<h1 class="display" tabindex="-1">Hvor lang tid har du?</h1>', html=True
        )
        self.assertContains(svar, "<title>Finn tur – Your Next Adventure</title>", html=True)

    def test_grunnoppsett(self):  # AD-12 punkt 5
        svar = self.client.get("/")
        self.assertContains(svar, '<html lang="nb">')
        self.assertContains(svar, "<main>", count=1)
        self.assertContains(svar, "<h1", count=1)

    def test_head_gir_200(self):
        self.assertEqual(self.client.head("/").status_code, 200)

    def test_post_uten_data_gir_skjemaet_med_feil(self):  # FR-4 (story 1.9: Søk tar POST)
        svar = self.client.post("/")
        self.assertEqual(svar.status_code, 200)
        self.assertContains(svar, "Velg varighet")

    def test_andre_metoder_gir_405(self):
        self.assertEqual(self.client.put("/").status_code, 405)
        self.assertEqual(self.client.delete("/").status_code, 405)


class FeilsiderTest(SimpleTestCase):
    def test_404_er_norsk_med_lenke_til_sok(self):  # AD-12 punkt 5
        svar = self.client.get("/finnes-ikke/")
        self.assertEqual(svar.status_code, 404)
        self.assertContains(svar, "<h1>Jeg fant ikke siden</h1>", status_code=404, html=True)
        self.assertContains(svar, "Adressen finnes ikke, eller siden er flyttet.", status_code=404)
        self.assertContains(svar, LENKE_TIL_SOK, status_code=404, html=True)
        self.assertContains(svar, '<html lang="nb">', status_code=404)

    def test_csrf_feil_er_norsk_med_lenke_til_sok(self):  # AD-12 punkt 5
        klient = Client(enforce_csrf_checks=True)
        svar = klient.post("/", {"varighet": "2"})
        self.assertEqual(svar.status_code, 403)
        self.assertContains(svar, "<h1>Skjemaet kunne ikke sendes</h1>", status_code=403, html=True)
        self.assertContains(
            svar,
            "Skjemaet var for gammelt, eller nettleseren blokkerte en informasjonskapsel. "
            "Gå til Søk og prøv igjen.",
            status_code=403,
        )
        self.assertContains(svar, LENKE_TIL_SOK, status_code=403, html=True)

    @override_settings(ROOT_URLCONF="tests.web.urls_feil")
    def test_500_er_norsk_med_lenke_til_sok(self):  # AD-12 punkt 5
        klient = Client(raise_request_exception=False)
        with self.assertLogs("django.request", "ERROR"):
            svar = klient.get("/feil/")
        self.assertEqual(svar.status_code, 500)
        self.assertContains(svar, "<h1>Noe gikk galt</h1>", status_code=500, html=True)
        self.assertContains(svar, "Noe gikk galt hos meg. Prøv igjen om litt.", status_code=500)
        self.assertContains(svar, LENKE_TIL_SOK, status_code=500, html=True)
