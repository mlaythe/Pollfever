import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question

def create_question(question_text, days):
  time = timezone.now() + datetime.timedelta(days=days)
  return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionViewTests(TestCase):
  def test_index_view_with_no_questions(self):
    response = self.client.get(reverse('pollfever:index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No polls are available.")
    self.assertQuerysetEqual(response.context['latest_question_list'], [])

  def test_index_view_with_a_past_question(self):
    create_question(question_text="Past question.", days=-30)
    response = self.client.get(reverse('pollfever:index'))
    self.assertQuerysetEqual(
        response.context['latest_question_list'],
        ['<Question: Past question.>']
    )

  def test_index_view_with_a_future_question(self):
    create_question(question_text="Future question.", days=30)
    response = self.client.get(reverse('pollfever:index'))
    self.assertContains(response, "No polls are available.")
    self.assertQuerysetEqual(response.context['latest_question_list'], [])

  def test_index_view_with_future_question_and_past_question(self):
    create_question(question_text="Past question.", days=-30)
    create_question(question_text="Future question.", days=30)
    response = self.client.get(reverse('pollfever:index'))
    self.assertQuerysetEqual(
        response.context['latest_question_list'],
        ['<Question: Past question.>']
    )

  def test_index_view_with_two_past_questions(self):
    create_question(question_text="Past question 1.", days=-30)
    create_question(question_text="Past question 2.", days=-5)
    response = self.client.get(reverse('pollfever:index'))
    self.assertQuerysetEqual(
        response.context['latest_question_list'],
        ['<Question: Past question 2.>', '<Question: Past question 1.>']
    )

class QuestionIndexDetailTests(TestCase):
  def test_detail_view_with_a_future_question(self):
    future_question = create_question(question_text='Future question.', days=5)
    url = reverse('pollfever:detail', args=(future_question.id,))
    response = self.client.get(url)
    self.assertEqual(response.status_code, 404)

  def test_detail_view_with_a_past_question(self):
    past_question = create_question(question_text='Past Question.', days=-5)
    url = reverse('pollfever:detail', args=(past_question.id,))
    response = self.client.get(url)
    self.assertContains(response, past_question.question_text)
