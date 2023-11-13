from math import ceil

from django.core.paginator import Paginator
from django.shortcuts import render

from app.models import *


def handler404(request, exception):
    return render(request, 'admin/404.html', status=404)


def get_page_num(size, request, per_page):
    page_num = int(request.GET.get("page", 1))
    if page_num < 1 or page_num > ceil(size / per_page):
        raise ValueError
    return page_num


def paginate(objects_list, request, page_num=1, per_page=12):
    size = len(objects_list)
    page_num = get_page_num(size, request, per_page)
    paginator = Paginator(objects_list, per_page)
    res_page_range = page_range = paginator.page_range
    if (len(page_range) >= 10):
        res_page_range = []
        res_page_range.append(page_range[0])
        if (page_num < 4):
            res_page_range.extend(page_range[1:5])
        elif page_num > page_range[-1] - 3:
            res_page_range.extend(page_range[-5:-1:1])
        else:
            res_page_range.extend(page_range[page_num - 3:page_num + 2])
        res_page_range.append(page_range[-1])
    return paginator.get_page(page_num), res_page_range, page_num


def validate_question_id(question_id):
    question_id = int(question_id)
    if question_id < 0 or question_id > Question.objects.count():
        raise ValueError


def index(request):
    questions = Question.objects.all()
    try:
        page, paginator_range, page_num = paginate(questions, request)
    except:
        return handler404(request, ValueError())
    return render(request, "index.html",
                  {'page': page,
                   'paginator_range': paginator_range,
                   'page_num': page_num
                   })


def hot_questions(request):
    logging.info('before filter')
    hot_questions = Question.objects.filter_by_hot()
    logging.info('after filter')
    try:
        logging.info('before paginator')
        page, paginator_range, page_num = paginate(hot_questions, request)
        logging.info('after paginator')
    except:
        return handler404(request, ValueError())
    return render(request, "index.html",
                  {'page': page,
                   'paginator_range': paginator_range,
                   'page_num': page_num
                   })


def tag_questions(request, tag_name):
    tag_questions = Question.objects.filter_by_tag(tag_name)
    try:
        page, paginator_range, page_num = paginate(tag_questions, request)
    except:
        return handler404(request, ValueError())
    return render(request, "index.html",
                  {'page': page,
                   'paginator_range': paginator_range,
                   'page_num': page_num,
                   })


def question(request, question_id):
    try:
        validate_question_id(question_id)
        question = Question.objects.get(pk=question_id)
        page, paginator_range, page_num = paginate(question.answers.all(), request, per_page=5)
    except:
        return handler404(request, ValueError())
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
