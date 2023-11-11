from math import ceil

from django.core.paginator import Paginator
from django.shortcuts import render

from app.models import *

def handler404(request, exception):
    return render(request, 'admin/404.html', status=404)


def get_page_num(objects_lists, request, per_page=10):
    page_num = int(request.GET.get("page", 1))
    if page_num < 1 or page_num > ceil(objects_lists.count() / per_page):
        raise ValueError
    return page_num


def paginate(objects_list, request, page_num, per_page=10):
    paginator = Paginator(objects_list, per_page)
    return paginator.get_page(page_num), paginator.page_range


def index(request):
    questions = Question.objects.all()
    page_num = get_page_num(questions, request)
    try:
        page_num = get_page_num(questions, request)
    except ValueError:
        return handler404(request, ValueError())
    page, paginator_range = paginate(questions, request, page_num)
    return render(request, "index.html",
                  {'page': page,
                   'paginator_range': paginator_range,
                   'page_num': page_num
                   })


def hot_questions(request):
    hot_questions = Question.objects.filter_by_hot()
    try:
        page_num = get_page_num(hot_questions, request)
    except ValueError:
        return handler404(request, ValueError())
    page, paginator_range = paginate(hot_questions, request, page_num)
    return render(request, "index.html",
                  {'page': page,
                   'paginator_range': paginator_range,
                   'page_num': page_num
                   })


def tag_questions(request, tag_name):
    questions = Question.objects.filter_by_tag(tag_name)
    try:
        page_num = get_page_num(questions, request)
    except ValueError:
        return handler404(request, ValueError())
    page, paginator_range = paginate(questions, request, page_num)
    return render(request, "index.html",
                  {'page': page,
                   'paginator_range': paginator_range,
                   'page_num': page_num,
                   })


def question(request, question_id):
    question_id = int(question_id)
    question = Question.objects.filter_by_question(question_id)
    answers = Answer.objects.filter_by_question(question_id)
    per_page = 3
    if question_id < 0 or question_id > Question.objects.count():
        return handler404(request, ValueError())
    try:
        page_num = get_page_num(answers, request, per_page)
    except ValueError:
        return handler404(request, ValueError())
    page_num = int(request.GET.get("page", 1))
    page, paginator_range = paginate(answers, request, page_num, per_page)
    return render(request, "question.html",
                  {'question': question,
                   'page': page,
                   'paginator_range': paginator_range,
                   'page_num': page_num,
                   })


def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "signup.html")


def ask(request):
    return render(request, "ask.html")


def setting(request):
    return render(request, "setting.html")
