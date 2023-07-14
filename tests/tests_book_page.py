from datetime import date, timedelta
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from books import models
from tests.webdriver_test_case import WebdriverTestCase
from selenium.webdriver.common.by import By


class BookPageTests(WebdriverTestCase):
    '''Selenium tests for book page.'''

    # TODO: #90 - remove once all tests switch to using fake data.
    fixtures = []

    def setUp(self):
        super().setUp()
        self.book = models.Book.objects.create(
            title='Першая кніга',
            title_ru='Первая книга',
            slug='pershaya-kniga',
            date=date.today(),
        )
        self.book.authors.set([self.fake_data.person_ales])
        self.book.translators.set([self.fake_data.person_bela])

        narration = models.Narration.objects.create(
            book=self.book,
            language=models.Language.BELARUSIAN,
            duration=timedelta(hours=14, minutes=15),
        )
        narration.links.set([
            self.fake_data.create_link(self.fake_data.link_type_knizhny_voz,
                                       self.book),
            self.fake_data.create_link(self.fake_data.link_type_kobo,
                                       self.book),
        ])
        narration.narrators.set([self.fake_data.person_viktar])

        publisher = models.Publisher.objects.create(
            name="audiobooks.by",
            slug="audiobooksby",
            url="https://audiobooks.by/about",
            description="Мы - каманда энтузіястаў, якія любяць " +
            "беларускую літаратуру і аўдыякнігі.")
        narration.publishers.set([publisher])
        self.book.tag.set(
            [self.fake_data.tag_poetry, self.fake_data.tag_fiction])

    def _get_book_url(self) -> str:
        return f'{self.live_server_url}/books/{self.book.slug}'

    def _check_person_present_and_clickable(self,
                                            person: models.Person) -> None:
        self.driver.get(self._get_book_url())
        elem = self.driver.find_element(By.LINK_TEXT, person.name)
        self.scroll_and_click(elem)
        self.assertIn(f'/person/{person.slug}', self.driver.current_url)

    def test_click_authors(self):
        self.assertGreaterEqual(self.book.authors.count(), 1)
        for author in self.book.authors.all():
            self._check_person_present_and_clickable(author)

    def test_click_translators(self):
        self.assertGreaterEqual(self.book.translators.count(), 1)
        for translator in self.book.translators.all():
            self._check_person_present_and_clickable(translator)

    def test_click_narrators(self):
        self.assertGreaterEqual(self.book.narrations.count(), 1)
        for narration in self.book.narrations.all():
            for narrator in narration.narrators.all():
                self._check_person_present_and_clickable(narrator)

    def test_has_narration_links(self):
        self.assertGreaterEqual(self.book.narrations.count(), 1)
        self.driver.get(self._get_book_url())
        for narration in self.book.narrations.all():
            for link in narration.links.all():
                caption = link.url_type.caption
                elem = self.driver.find_elements(By.LINK_TEXT, caption)
                found_link = False
                for e in elem:
                    if e.get_dom_attribute('href') == link.url:
                        found_link = True
                        break
                self.assertTrue(found_link)

    def test_click_tags(self):
        self.assertGreaterEqual(self.book.tag.count(), 1)
        for tag in self.book.tag.all():
            self.driver.get(self._get_book_url())
            elem = self.driver.find_element(By.LINK_TEXT, tag.name)
            self.scroll_and_click(elem)
            self.assertIn(f'/catalog/{tag.slug}', self.driver.current_url)
            tag_header = self.driver.find_element(By.CSS_SELECTOR, '#books h1')
            self.assertEqual(tag.name, tag_header.text)

    def test_renders_text_elements(self):
        self.driver.get(self._get_book_url())
        book_elem = self.driver.find_element(By.CSS_SELECTOR, '#books')
        self.assertIn('14 гадзін 15 хвілін', book_elem.text)
        self.assertEqual(f'Першая Кніга аўдыякніга', self.driver.title)
        description = self.driver.find_element(
            By.CSS_SELECTOR,
            'meta[name="description"]').get_dom_attribute('content')
        self.assertIn(self.book.title, description)
        self.assertIn(self.book.authors.first().name, description)

    def test_free_books_have_listen_free_text(self):
        self.driver.get(self._get_book_url())
        header = self.driver.find_element(By.CSS_SELECTOR, '.links-header')
        self.assertIn('Дзе паслухаць бясплатна', header.text)

    def test_paid_books_have_where_to_buy_text(self):
        narration = self.book.narrations.first()
        narration.paid = True
        narration.save()
        self.driver.get(self._get_book_url())
        header = self.driver.find_element(By.CSS_SELECTOR, '.links-header')
        self.assertIn('Дзе купіць', header.text)

    def test_russian_only_books_show_both_titles(self):
        belarusian_title = 'Першая кніга'
        russian_title = 'Первая книга'
        narration = self.book.narrations.first()
        narration.language = models.Language.RUSSIAN
        narration.save()
        self.driver.get(self._get_book_url())
        body_text = self.driver.find_element(By.CSS_SELECTOR, '#books').text
        self.assertIn(belarusian_title, body_text)
        self.assertIn(russian_title, body_text)

    def test_has_publisher_clickable_link(self):
        self.driver.get(self._get_book_url())
        publisher = models.Publisher.objects.filter(
            name="audiobooks.by").first()
        elem = self.driver.find_element(By.LINK_TEXT, f"{publisher.name}")
        self.scroll_and_click(elem)
        self.assertIn(f'/publisher/{publisher.slug}', self.driver.current_url)