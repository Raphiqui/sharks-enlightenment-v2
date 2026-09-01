from wagtail.models import Page, Site
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
