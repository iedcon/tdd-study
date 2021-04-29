from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from .models import Item, List
import re

# Create your tests here.
class HomePageTest(TestCase):

    # csrf로 인한 테스트 문제를 해결하기 위한 메소드
    @staticmethod
    def remove_csrf(html_code):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', html_code)

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(self.remove_csrf(response.content.decode()), self.remove_csrf(expected_html))


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        new_list = List()
        new_list.save()

        first_item = Item()
        first_item.text = '첫 번째 아이템'
        first_item.list = new_list
        first_item.save()

        second_item = Item()
        second_item.text = '두 번째 아이템'
        second_item.list = new_list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, new_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, '첫 번째 아이템')
        self.assertEqual(first_saved_item.list, new_list)
        self.assertEqual(second_saved_item.text, '두 번째 아이템')
        self.assertEqual(second_saved_item.list, new_list)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        new_list = List.objects.create()
        response = self.client.get(f'/lists/{new_list.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='다른 목록 아이템 1', list=other_list)
        Item.objects.create(text='다른 목록 아이템 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, '다른 목록 아이템 1')
        self.assertNotContains(response, '다른 목록 아이템 2')

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        response = self.client.post(
            '/lists/new/', 
            data={'item_text': '신규 작업 아이템'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '신규 작업 아이템')

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new/', 
            data={'item_text': '신규 작업 아이템'}
        )

        new_item = Item.objects.first()
        self.assertRedirects(response, f'/lists/{new_item.list.id}/')


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item/',
            data={'item_text': '기존 목록에 신규 아이템'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '기존 목록에 신규 아이템')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item/',
            data={'item_text': '기존 목록에 신규 아이템'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

