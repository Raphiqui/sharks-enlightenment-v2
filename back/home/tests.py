import json
import re

from django.template.loader import render_to_string
from django.test import RequestFactory
from django.utils import translation
from django.views.defaults import server_error
from wagtail.images import get_image_model
from wagtail.images.tests.utils import get_test_image_file
from wagtail.models import Locale, Page, Site
from wagtail.test.utils import WagtailPageTestCase
from wagtail_localize.models import TranslationSource
from wagtail_localize.operations import translate_object, translate_page_subtree

from home.models import HomePage, QuizPage, SharkPage, SharksPage


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

    def body(self, response):
        return response.content.decode().split("</head>", 1)[1]

    def test_switcher_hidden_without_translations(self):
        response = self.client.get(self.homepage.url)
        self.assertNotContains(response, 'hreflang="')

    def test_switcher_lists_current_page_and_translations(self):
        self.translate_homepage("fr")
        body = self.body(self.client.get(self.homepage.url))
        # Rendered twice: desktop and mobile switchers.
        self.assertEqual(body.count('hreflang="en"'), 2)
        self.assertEqual(body.count('hreflang="fr"'), 2)

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
        content = self.body(self.client.get(self.homepage.url))
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

    def quiz_with_question(self, question):
        quiz_data = [
            {
                "type": "question_list",
                "value": [
                    {
                        "question": question,
                        "options": [
                            {"type": "option", "value": {"option": "A", "is_correct": True}},
                        ],
                        "answer": "",
                    }
                ],
            }
        ]
        quiz_page = QuizPage(title="Quiz", quiz=quiz_data)
        self.homepage.add_child(instance=quiz_page)
        return quiz_page

    def test_quiz_endpoint_serves_requested_language(self):
        quiz_page = self.quiz_with_question("Are sharks mammals?")
        locale = Locale.objects.get_or_create(language_code="fr")[0]
        translation = quiz_page.copy_for_translation(locale, copy_parents=True)
        translation.quiz[0].value[0]["question"] = "Les requins sont-ils des mammifères ?"
        translation.save_revision().publish()

        fr = self.client.get("/api/quiz?lang=fr").json()
        en = self.client.get("/api/quiz?lang=en").json()

        self.assertEqual(fr["questions"][0]["question"], "Les requins sont-ils des mammifères ?")
        self.assertEqual(en["questions"][0]["question"], "Are sharks mammals?")

    def test_quiz_endpoint_falls_back_to_default_language(self):
        self.quiz_with_question("Are sharks mammals?")

        payload = self.client.get("/api/quiz?lang=fr").json()

        self.assertEqual(payload["questions"][0]["question"], "Are sharks mammals?")


class SeoTests(WagtailPageTestCase):
    """
    Tests for what search engines see: robots.txt, sitemap and <head> metadata.
    """

    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.all().delete()
        Site.objects.create(
            hostname="testserver",
            root_page=root_page,
            is_default_site=True,
            site_name="Sharks Enlightenment",
        )
        self.homepage = HomePage(title="Home", hero_subtitle="Dive into the world of sharks.")
        root_page.add_child(instance=self.homepage)
        # The site root must be the home page for sitemap and canonical URLs.
        Site.objects.update(root_page=self.homepage)

    def translate(self, page, language_code):
        locale = Locale.objects.get_or_create(language_code=language_code)[0]
        translation = page.copy_for_translation(locale, copy_parents=True)
        translation.save_revision().publish()
        translation.refresh_from_db()
        return translation

    def head(self, page):
        return self.client.get(page.url).content.decode().split("</head>")[0]

    def test_robots_txt_points_to_sitemap(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertIn("Disallow: /admin/", response.content.decode())
        self.assertIn("Sitemap: http://testserver/sitemap.xml", response.content.decode())

    def test_sitemap_lists_every_locale(self):
        self.translate(self.homepage, "fr")
        content = self.client.get("/sitemap.xml").content.decode()
        self.assertIn("<loc>http://testserver/en/</loc>", content)
        self.assertIn("<loc>http://testserver/fr/</loc>", content)

    def test_html_lang_matches_page_language(self):
        french = self.translate(self.homepage, "fr")
        self.assertIn('<html lang="en"', self.head(self.homepage))
        self.assertIn('<html lang="fr"', self.head(french))

    def test_title_includes_site_name(self):
        self.assertRegex(
            self.head(self.homepage), r"<title>\s*Home\s*- Sharks Enlightenment\s*</title>"
        )

    def test_meta_description_falls_back_on_hero_subtitle(self):
        self.assertIn(
            '<meta name="description" content="Dive into the world of sharks." />',
            self.head(self.homepage),
        )

    def test_meta_description_prefers_search_description(self):
        self.homepage.search_description = "Learn to love sharks."
        self.homepage.save_revision().publish()
        self.assertIn(
            '<meta name="description" content="Learn to love sharks." />', self.head(self.homepage)
        )

    def test_canonical_url(self):
        self.assertIn(
            '<link rel="canonical" href="http://testserver/en/" />', self.head(self.homepage)
        )

    def test_hreflang_alternates_with_x_default(self):
        self.translate(self.homepage, "fr")
        head = self.head(self.homepage)
        self.assertIn('<link rel="alternate" hreflang="en" href="http://testserver/en/" />', head)
        self.assertIn('<link rel="alternate" hreflang="fr" href="http://testserver/fr/" />', head)
        self.assertIn(
            '<link rel="alternate" hreflang="x-default" href="http://testserver/en/" />', head
        )

    def test_no_hreflang_without_translations(self):
        self.assertNotIn('<link rel="alternate"', self.head(self.homepage))

    def test_open_graph_tags(self):
        head = self.head(self.homepage)
        self.assertIn('<meta property="og:type" content="website" />', head)
        self.assertIn('<meta property="og:title" content="Home" />', head)
        self.assertIn('<meta property="og:site_name" content="Sharks Enlightenment" />', head)

    def test_home_page_structured_data_is_website(self):
        head = self.head(self.homepage)
        data = json.loads(
            re.search(r'<script type="application/ld\+json">(.*?)</script>', head).group(1)
        )
        self.assertEqual(data["@type"], "WebSite")
        self.assertEqual(data["name"], "Sharks Enlightenment")
        self.assertEqual(data["inLanguage"], "en")

    def test_shark_page_structured_data_is_article(self):
        sharks = SharksPage(title="Sharks")
        self.homepage.add_child(instance=sharks)
        shark = SharkPage(
            title="Whale shark",
            name="Whale shark",
            latin_name="Rhincodon typus",
            size="14 m",
            conservation_status="endangered",
            image=get_image_model().objects.create(title="Whale shark", file=get_test_image_file()),
            description="<p>The <b>largest</b> fish in the world.</p>",
        )
        sharks.add_child(instance=shark)

        head = self.head(shark)
        data = json.loads(
            re.search(r'<script type="application/ld\+json">(.*?)</script>', head).group(1)
        )
        self.assertEqual(data["@type"], "Article")
        self.assertEqual(data["headline"], "Whale shark")
        self.assertEqual(data["alternativeHeadline"], "Rhincodon typus")
        self.assertEqual(data["description"], "The largest fish in the world.")
        self.assertIn("fill-1200x630", data["image"])
        self.assertIn('<meta property="og:type" content="article" />', head)
        self.assertIn('<meta name="twitter:card" content="summary_large_image" />', head)

    def test_search_results_are_not_indexed(self):
        response = self.client.get("/en/search/?query=shark")
        self.assertContains(response, '<meta name="robots" content="noindex, follow" />')


class ErrorPageTests(WagtailPageTestCase):
    """
    Tests for the custom 404 and 500 pages.
    """

    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(hostname="testserver", root_page=root_page, is_default_site=True)
        self.homepage = HomePage(title="Home")
        root_page.add_child(instance=self.homepage)
        Site.objects.update(root_page=self.homepage)

    def test_missing_page_uses_custom_404(self):
        response = self.client.get("/en/this-page-does-not-exist/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        self.assertContains(response, "This page swam away", status_code=404)
        self.assertContains(response, 'href="/en/"', status_code=404)

    def test_404_is_translated(self):
        self.translate_homepage("fr")
        response = self.client.get("/fr/cette-page-n-existe-pas/")
        self.assertContains(response, "Cette page s'est échappée", status_code=404)

    def test_404_is_not_indexed(self):
        response = self.client.get("/en/this-page-does-not-exist/")
        self.assertContains(response, '<meta name="robots" content="noindex" />', status_code=404)

    def test_500_renders_without_a_request(self):
        # Django renders 500.html with no context: it must not need a page,
        # a request or the database.
        with translation.override("en"):
            html = render_to_string("500.html")
        self.assertIn("Something went wrong", html)
        self.assertIn('<meta name="robots" content="noindex" />', html)

    def test_server_error_view_uses_custom_500(self):
        with translation.override("en"):
            response = server_error(RequestFactory().get("/"))
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Something went wrong", response.content)

    def test_preview_routes_only_exist_in_debug(self):
        # Tests run with DEBUG=False, like production.
        self.assertEqual(self.client.get("/en/500/").status_code, 404)

    def test_sitemap_never_lists_error_pages(self):
        content = self.client.get("/sitemap.xml").content.decode()
        self.assertNotIn("/404/", content)
        self.assertNotIn("/500/", content)

    def translate_homepage(self, language_code):
        locale = Locale.objects.get_or_create(language_code=language_code)[0]
        translation = self.homepage.copy_for_translation(locale, copy_parents=True)
        translation.save_revision().publish()
        return translation


class SharkFactsBlockTests(WagtailPageTestCase):
    """
    Tests for the shark facts block rendered on the homepage.
    """

    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(hostname="testsite", root_page=root_page, is_default_site=True)
        image = get_image_model().objects.create(title="Mako", file=get_test_image_file())
        self.homepage = HomePage(
            title="Home",
            body=[
                (
                    "shark_facts",
                    {
                        "facts": [
                            {
                                "highlight": "45 mph",
                                "caption": "Top speed of the shortfin mako",
                                "description": "The fastest shark in the ocean.",
                                "image": image,
                                "source": "https://example.com/mako",
                                "wide": True,
                            },
                            {"highlight": "400+", "caption": "Known shark species"},
                        ]
                    },
                )
            ],
        )
        root_page.add_child(instance=self.homepage)

    def test_facts_are_rendered(self):
        response = self.client.get(self.homepage.url)
        self.assertContains(response, "45 mph")
        self.assertContains(response, "Top speed of the shortfin mako")
        self.assertContains(response, "The fastest shark in the ocean.")
        self.assertContains(response, 'href="https://example.com/mako"')
        self.assertContains(response, "Known shark species")
        self.assertContains(response, 'class="shark-fact ', count=2)

    def test_wide_fact_spans_two_columns(self):
        html = self.client.get(self.homepage.url).content.decode()
        cards = re.findall(r'<article\s+class="shark-fact [^"]*"', html)
        self.assertIn("sm:col-span-2", cards[0])
        self.assertNotIn("sm:col-span-2", cards[1])


class TranslationConfigTests(WagtailPageTestCase):
    """
    Tests that every page type can be submitted for translation with wagtail-localize.
    """

    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(hostname="testsite", root_page=root_page, is_default_site=True)
        self.homepage = HomePage(
            title="Home", body=[("heading", {"title": "Welcome", "subtitle": "", "eyebrow": ""})]
        )
        root_page.add_child(instance=self.homepage)
        self.sharks = SharksPage(title="Sharks")
        self.homepage.add_child(instance=self.sharks)
        self.shark = SharkPage(
            title="Blue shark",
            name="Blue shark",
            latin_name="Prionace glauca",
            image=get_image_model().objects.create(title="Blue", file=get_test_image_file()),
            size="3.8 m",
            conservation_status="near threatened",
        )
        self.sharks.add_child(instance=self.shark)
        self.fr = Locale.objects.create(language_code="fr")

    def segment_paths(self, page):
        source, _ = TranslationSource.get_or_create_from_instance(page)
        return set(source.stringsegment_set.values_list("context__path", flat=True))

    def test_subtree_translation_creates_french_pages(self):
        # Same sequence as the "Translate" admin action with "Include subtree" ticked
        translate_object(self.homepage, [self.fr])
        translate_page_subtree(self.homepage.id, [self.fr], None, None)
        self.assertTrue(
            SharkPage.objects.filter(locale=self.fr, latin_name="Prionace glauca").exists()
        )

    def test_page_titles_are_translatable(self):
        for page in (self.homepage, self.sharks, self.shark):
            self.assertIn("title", self.segment_paths(page))

    def test_homepage_body_is_translatable(self):
        self.assertTrue(any(p.startswith("body.") for p in self.segment_paths(self.homepage)))

    def test_shark_latin_name_is_not_translatable(self):
        paths = self.segment_paths(self.shark)
        self.assertIn("name", paths)
        self.assertNotIn("latin_name", paths)


class SharkThumbnailTests(WagtailPageTestCase):
    """
    Tests for the shark cards on the sharks listing page.
    """

    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(hostname="testsite", root_page=root_page, is_default_site=True)
        homepage = HomePage(title="Home")
        root_page.add_child(instance=homepage)
        image = get_image_model().objects.create(title="Blue", file=get_test_image_file())
        self.sharks = SharksPage(title="Sharks")
        homepage.add_child(instance=self.sharks)
        shark = SharkPage(
            title="Blue shark",
            name="Blue shark",
            latin_name="Prionace glauca",
            image=image,
            size="3.8 m",
            conservation_status="near threatened",
        )
        self.sharks.add_child(instance=shark)
        card = {"name": "Blue shark", "image": image, "shark_page": shark}
        self.sharks.sharks = [
            ("shark_thumbnails", {**card, "scientific_name": "Prionace glauca"}),
            ("shark_thumbnails", {**card, "scientific_name": ""}),
        ]
        self.sharks.save_revision().publish()

    def test_scientific_name_badge_only_when_filled(self):
        response = self.client.get(self.sharks.url)
        self.assertContains(response, "Prionace glauca", count=1)

    def test_image_is_cropped_to_a_square(self):
        html = self.client.get(self.sharks.url).content.decode()
        images = re.findall(r'<img[^>]*alt="Blue shark"[^>]*>', html)
        self.assertEqual(len(images), 2)
        for img in images:
            self.assertIn(".fill-800x800.", img)
            width = re.search(r'width="(\d+)"', img).group(1)
            height = re.search(r'height="(\d+)"', img).group(1)
            self.assertEqual(width, height)


class AnatomyBlockTests(WagtailPageTestCase):
    """
    Tests for the interactive anatomy block.
    """

    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(hostname="testsite", root_page=root_page, is_default_site=True)
        image = get_image_model().objects.create(title="Shark", file=get_test_image_file())
        self.homepage = HomePage(
            title="Home",
            body=[("anatomy", {"title": "Shark anatomy", "image": image})],
        )
        root_page.add_child(instance=self.homepage)

    def test_labels_are_translated(self):
        block = self.homepage.body[0]
        with translation.override("fr"):
            html = block.render()
        self.assertIn("Nageoire dorsale", html)
        self.assertNotIn("Dorsal Fin", html)
