"""Egen brukermodell fra første migrering (AR-9, AD-7)."""

import importlib
from io import StringIO

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import migrations
from django.test import TestCase

from turforslag.admin import BrukerOpprettSkjema
from turforslag.models import Bruker


class BrukermodellTest(TestCase):
    def test_auth_user_model_er_bruker(self):  # AR-9
        self.assertIs(get_user_model(), Bruker)

    def test_e_post_er_brukernavn(self):  # AR-9
        self.assertEqual(Bruker.USERNAME_FIELD, "email")
        self.assertEqual(Bruker.REQUIRED_FIELDS, [])
        self.assertTrue(Bruker._meta.get_field("email").unique)

    def test_ingen_brukernavn_fornavn_eller_etternavn(self):  # AR-9
        feltnavn = {felt.name for felt in Bruker._meta.get_fields()}
        self.assertNotIn("username", feltnavn)
        self.assertNotIn("first_name", feltnavn)
        self.assertNotIn("last_name", feltnavn)

    def test_brukt_heving_har_standard_0(self):  # AR-9, AD-11
        bruker = Bruker.objects.create_user("ola@eksempel.no", "passord123")
        bruker.refresh_from_db()
        self.assertEqual(bruker.brukt_heving, 0)

    def test_create_user_lagrer_e_post_med_sma_bokstaver(self):  # AD-7
        bruker = Bruker.objects.create_user("Ola@Eksempel.NO", "passord123")
        bruker.refresh_from_db()
        self.assertEqual(bruker.email, "ola@eksempel.no")
        self.assertTrue(bruker.check_password("passord123"))
        self.assertFalse(bruker.is_staff)
        self.assertFalse(bruker.is_superuser)

    def test_save_lagrer_e_post_med_sma_bokstaver(self):  # AD-7
        bruker = Bruker(email="Kari@Eksempel.NO")
        bruker.set_password("passord123")
        bruker.save()
        bruker.refresh_from_db()
        self.assertEqual(bruker.email, "kari@eksempel.no")

    def test_create_superuser(self):  # AR-9
        bruker = Bruker.objects.create_superuser("Admin@Eksempel.NO", "passord123")
        self.assertEqual(bruker.email, "admin@eksempel.no")
        self.assertTrue(bruker.is_staff)
        self.assertTrue(bruker.is_superuser)

    def test_create_user_krever_e_post(self):  # AR-9
        with self.assertRaises(ValueError):
            Bruker.objects.create_user("", "passord123")

    def test_innlogging_uansett_store_og_sma_bokstaver(self):  # AD-7
        bruker = Bruker.objects.create_user("admin@eksempel.no", "passord123")
        self.assertEqual(authenticate(username="Admin@Eksempel.NO", password="passord123"), bruker)

    def test_admin_skjema_avviser_e_post_som_finnes_med_andre_bokstaver(self):  # AD-7
        Bruker.objects.create_user("ola@eksempel.no", "passord123")
        skjema = BrukerOpprettSkjema(
            data={
                "email": "Ola@Eksempel.NO",
                "usable_password": "true",
                "password1": "passord123",
                "password2": "passord123",
            }
        )
        self.assertFalse(skjema.is_valid())
        self.assertIn("email", skjema.errors)
        self.assertEqual(Bruker.objects.count(), 1)

    def test_admin_viser_brukerne(self):  # AR-9
        admin = Bruker.objects.create_superuser("admin@eksempel.no", "passord123")
        self.client.force_login(admin)
        self.assertEqual(self.client.get("/admin/turforslag/bruker/").status_code, 200)
        self.assertEqual(self.client.get("/admin/turforslag/bruker/add/").status_code, 200)
        endre = f"/admin/turforslag/bruker/{admin.pk}/change/"
        self.assertEqual(self.client.get(endre).status_code, 200)


class PassordTest(TestCase):
    def test_kort_passord_avvises(self):  # AD-7
        with self.assertRaises(ValidationError):
            validate_password("1234567")

    def test_passord_med_8_tegn_godtas(self):  # AD-7
        self.assertIsNone(validate_password("12345678"))

    def test_enkelt_passord_godtas_fordi_bare_lengden_sjekkes(self):  # AD-7
        bruker = Bruker(email="ola@eksempel.no")
        self.assertIsNone(validate_password("password", user=bruker))
        self.assertIsNone(validate_password("ola@eksempel.no", user=bruker))


class MigreringTest(TestCase):
    def test_forste_migrering_lager_bruker(self):  # AR-9
        forste = importlib.import_module("turforslag.migrations.0001_initial").Migration
        lag = [op for op in forste.operations if isinstance(op, migrations.CreateModel)]
        bruker = next(op for op in lag if op.name == "Bruker")
        felt = dict(bruker.fields)
        self.assertNotIn("username", felt)
        self.assertNotIn("first_name", felt)
        self.assertNotIn("last_name", felt)
        self.assertTrue(felt["email"].unique)
        self.assertEqual(felt["brukt_heving"].default, 0)

    def test_ingen_manglende_migreringer(self):  # AR-15
        utdata = StringIO()
        call_command("makemigrations", "--check", "--dry-run", stdout=utdata, stderr=utdata)
        self.assertIn("No changes detected", utdata.getvalue())
