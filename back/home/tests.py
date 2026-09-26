from wagtail.models import Locale, Page, Site
from wagtail.test.utils import WagtailPageTestCase

from home.models import HomePage, QuizPage


class HomeSetUpTests(WagtailPageTestCase):
    """
    Tests for basic page structure setup and HomePage creation.
    """

    def test_root_create(self):
        root_page = Page.objects.get(pk=1)
        self.assertIsNotNone(root_page)

    def test_homepage_create(self):
        root_page = Page.objects.get(pk=1)
        homepage = HomePage(title="Home")
        root_page.add_child(instance=homepage)
        self.assertTrue(HomePage.objects.filter(title="Home").exists())


class HomeTests(WagtailPageTestCase):
    """
    Tests for homepage functionality and rendering.
    """

    def setUp(self):
        """
        Create a homepage instance for testing.
        """
        root_page = Page.get_first_root_node()
        Site.objects.create(hostname="testsite", root_page=root_page, is_default_site=True)
        self.homepage = HomePage(title="Home")
        root_page.add_child(instance=self.homepage)

    def test_homepage_is_renderable(self):
        self.assertPageIsRenderable(self.homepage)

    def test_homepage_template_used(self):
        response = self.client.get(self.homepage.url)
        self.assertTemplateUsed(response, "home/home_page.html")


class MobileMenuTests(WagtailPageTestCase):
    """
    Tests for the mobile navigation menu markup rendered in the header.
    """

    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(hostname="testsite", root_page=root_page, is_default_site=True)
        self.homepage = HomePage(title="Home")
        root_page.add_child(instance=self.homepage)
        self.response = self.client.get(self.homepage.url)

    def test_menu_button_is_accessible(self):
        self.assertContains(self.response, 'aria-controls="mobile-menu"')
        self.assertContains(self.response, 'aria-expanded="false"')
        self.assertContains(self.response, 'aria-label="Toggle menu"')

    def test_menu_button_has_no_inline_handler(self):
        # Toggle behaviour lives in front/src/header.js
        self.assertNotContains(self.response, "onclick=")

    def test_mobile_menu_starts_collapsed(self):
        self.assertContains(self.response, 'id="mobile-menu"')
        self.assertContains(self.response, "max-h-0 py-0")

    def test_mobile_menu_items_are_delimited(self):
        self.assertContains(self.response, "border-t border-border/50 divide-y divide-border/50")


class LanguageSwitcherTests(WagtailPageTestCase):
    """
    Tests for the segmented language switcher rendered in the header.
    """

    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(hostname="testsite", root_page=root_page, is_default_site=True)
        self.homepage = HomePage(title="Home")
        root_page.add_child(instance=self.homepage)

    def translate_homepage(self, language_code):
        locale = Locale.objects.get_or_create(language_code=language_code)[0]
        translation = self.homepage.copy_for_translation(locale, copy_parents=True)
        translation.save_revision().publish()
        translation.refresh_from_db()
        return translation

    def test_switcher_hidden_without_translations(self):
        response = self.client.get(self.homepage.url)
        self.assertNotContains(response, 'hreflang="')

    def test_switcher_lists_current_page_and_translations(self):
        self.translate_homepage("fr")
        response = self.client.get(self.homepage.url)
        # Rendered twice: desktop and mobile switchers.
        self.assertContains(response, 'hreflang="en"', count=2)
        self.assertContains(response, 'hreflang="fr"', count=2)

    def test_switcher_marks_current_language(self):
        self.translate_homepage("fr")
        response = self.client.get(self.homepage.url)
        self.assertContains(response, 'aria-current="true"', count=2)
        self.assertRegex(
            response.content.decode(),
            r'hreflang="en"[^>]*aria-current="true"',
        )

    def test_switcher_follows_settings_language_order(self):
        self.translate_homepage("fr")
        self.translate_homepage("es")
        content = self.client.get(self.homepage.url).content.decode()
        self.assertLess(content.index('hreflang="en"'), content.index('hreflang="es"'))
        self.assertLess(content.index('hreflang="es"'), content.index('hreflang="fr"'))

    def test_switcher_skips_unpublished_translations(self):
        translation = self.translate_homepage("fr")
        translation.unpublish()
        response = self.client.get(self.homepage.url)
        self.assertNotContains(response, 'hreflang="fr"')


class QuizApiTests(WagtailPageTestCase):
    """
    Tests for the /api/quiz endpoint, which reshapes a QuizPage's StreamField
    data into the JSON structure consumed by the frontend quiz component.
    """

    def setUp(self):
        root_page = Page.get_first_root_node()
        self.homepage = HomePage(title="Home")
        root_page.add_child(instance=self.homepage)

    def test_quiz_endpoint_404_when_no_quiz_page(self):
        # LocaleMiddleware 302s a 404 on an unprefixed URL to its `/en/`-prefixed
        # form before Wagtail's catch-all page-serving pattern 404s for real, so
        # follow the redirect to check the response the client actually ends up with.
        response = self.client.get("/api/quiz", follow=True)
        self.assertEqual(response.status_code, 404)

    def test_quiz_endpoint_returns_transformed_questions(self):
        quiz_data = [
            {
                "type": "question_list",
                "value": [
                    {
                        "question": "What is the largest fish species?",
                        "options": [
                            {
                                "type": "option",
                                "value": {"option": "Whale shark", "is_correct": True},
                            },
                            {
                                "type": "option",
                                "value": {"option": "Great white shark", "is_correct": False},
                            },
                        ],
                        "answer": "The whale shark is the largest fish species.",
                    },
                    {
                        "question": "Are sharks mammals?",
                        "options": [
                            {"type": "option", "value": {"option": "Yes", "is_correct": False}},
                            {"type": "option", "value": {"option": "No", "is_correct": True}},
                        ],
                        "answer": "Sharks are fish, not mammals.",
                    },
                ],
            }
        ]
        quiz_page = QuizPage(title="Quiz", quiz=quiz_data)
        self.homepage.add_child(instance=quiz_page)

        response = self.client.get("/api/quiz")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload["questions"]), 2)

        first, second = payload["questions"]
        self.assertEqual(first["question"], "What is the largest fish species?")
        self.assertEqual(first["explanation"], "The whale shark is the largest fish species.")
        self.assertEqual(
            first["options"],
            [
                {"option": "Whale shark", "is_correct": True},
                {"option": "Great white shark", "is_correct": False},
            ],
        )
        self.assertEqual(second["question"], "Are sharks mammals?")
        self.assertEqual(second["options"][1], {"option": "No", "is_correct": True})
