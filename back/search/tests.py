from wagtail.models import Page
from wagtail.search.backends import get_search_backend
from wagtail.test.utils import WagtailPageTestCase

from home.models import HomePage


class SearchViewTests(WagtailPageTestCase):
    """
    Tests for the site search view.
    """

    def setUp(self):
        root_page = Page.get_first_root_node()
        self.homepage = HomePage(title="Home about sharks")
        root_page.add_child(instance=self.homepage)
        # The search backend normally indexes on transaction commit, which
        # never happens inside TestCase's wrapping transaction — index
        # synchronously so search() can actually find the page.
        get_search_backend().add(self.homepage)

    def test_search_without_query_returns_no_results(self):
        response = self.client.get("/en/search/")

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["search_query"])
        self.assertEqual(len(response.context["search_results"]), 0)

    def test_search_with_matching_query_returns_results(self):
        response = self.client.get("/en/search/", {"query": "sharks"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["search_query"], "sharks")
        result_pks = [page.pk for page in response.context["search_results"]]
        self.assertIn(self.homepage.pk, result_pks)

    def test_search_with_non_matching_query_returns_no_results(self):
        response = self.client.get("/en/search/", {"query": "nonexistentxyz"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["search_results"]), 0)

    def test_search_with_invalid_page_falls_back_to_first_page(self):
        response = self.client.get("/en/search/", {"query": "sharks", "page": "not-a-number"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["search_results"].number, 1)

    def test_search_with_out_of_range_page_falls_back_to_last_page(self):
        response = self.client.get("/en/search/", {"query": "sharks", "page": "999"})

        self.assertEqual(response.status_code, 200)
        results = response.context["search_results"]
        self.assertEqual(results.number, results.paginator.num_pages)
