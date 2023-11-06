from random import randint
from math import ceil
from django.core.paginator import Paginator
from django.shortcuts import render

titles = ['Kylian Mbappe is a best forward of all time !',
          'Lionel Messi is a best forward of all time !',
          'CR7 is a best forward of all time !']

content = [
    """ 
    At international level, Mbappé made his senior debut for France in 2017, at age of 18. At the
    2018 FIFA World Cup, Mbappé became the youngest French player to score at a World Cup, as well
    as the second teenager, after Pelé, to score in a World Cup Final. He finished as the joint
    second-highest goalscorer as France won the tournament; he went on to win the FIFA World Cup
    Best Young Player and French Player of the Year awards for his performances. At the 2022 FIFA
    World Cup, France reached the final again; Mbappé won the Golden Boot and Silver Ball and set
    the record for most goals scored in World Cup finals by scoring a hat-trick.
    """,
    """
     Ankara messi ankara messi Ankara messi ankara messi 
     Ankara messi ankara messi goal goal goal goal goal goal !!!!
    """,
    """
     After a successful season with Sporting that brought the young player to the attention of
     Europe’s biggest football clubs, Ronaldo signed with English powerhouse Manchester United in
     2003. He was an instant sensation and soon came to be regarded as one of the best forwards in
     the game. His finest season with United came in 2007–08, when he scored 42 League and Cup goals
     and earned the Golden Shoe award as Europe’s leading scorer, with 31 League goals. After helping
     United to a Champions League title in May 2008, Ronaldo captured Fédération Internationale de
     Football Association (FIFA) World Player of the Year honours for his stellar 2007–08 season. He
     also led United to an appearance in the 2009 Champions League final, which they lost to FC Barcelona.
    """,
]

tags = ["World Cup", "Champion Cup", "Europe League", "Russian Premier League", "La Liga", "Bundesliga", "FNL",
        "blablabla"]

questions = [
    {
        'id': i,
        'title': titles[i % 3],
        'content': content[i % 3],
        'like': randint(0, 300),
        'tags': [t for t in tags if randint(0, 1)]
    } for i in range(88)
]

answers = [
    {
        'id': i,
        'title': titles[i % 3],
        'content': content[i % 3],
        'like': randint(0, 10)
    } for i in range(10)
]


def handler404(request,exception):
    return render(request, 'admin/404.html', status=404)


def get_page_num(objects_lists, request, per_page=10):
    page_num = int(request.GET.get("page", 1))
    if page_num < 1 or page_num > ceil(len(objects_lists) / per_page):
        raise ValueError
    return page_num


def paginate(objects_list, request, page_num, per_page=10):
    paginator = Paginator(objects_list, per_page)
    return paginator.get_page(page_num), paginator.page_range


def index(request):
    try:
        page_num = get_page_num(questions, request)
    except ValueError:
        return handler404(request,ValueError())
    page, paginator_range = paginate(questions, request, page_num)
    return render(request, "index.html",
                  {'page': page,
                   'paginator_range': paginator_range,
                   'page_num': page_num
                   })


def hot_questions(request):
    hot_questions = [q for q in questions if q['like'] > 100]
    hot_questions.sort(key=lambda x: x["like"], reverse=True)
    try:
        page_num = get_page_num(hot_questions, request)
    except ValueError:
        return handler404(request,ValueError())
    page, paginator_range = paginate(hot_questions, request, page_num)
    return render(request, "index.html",
                  {'page': page,
                   'paginator_range': paginator_range,
                   'page_num': page_num
                   })


def tag_questions(request, tag_name):
    tag_questions = list(filter(lambda it: tag_name in it["tags"], questions))
    try:
        page_num = get_page_num(questions, request)
    except ValueError:
        return handler404(request,ValueError())
    page, paginator_range = paginate(tag_questions, request, page_num)
    return render(request, "index.html",
                  {'page': page,
                   'paginator_range': paginator_range,
                   'page_num': page_num,
                   })


def question(request, question_id):
    per_page = 3
    if question_id < 0 or question_id > len(questions):
        return handler404(request,ValueError())
    try:
        page_num = get_page_num(answers, request, per_page)
    except ValueError:
        return handler404(request,ValueError())
    page_num = int(request.GET.get("page", 1))
    page, paginator_range = paginate(answers, request, page_num, per_page)
    return render(request, "question.html",
                  {'question': questions[question_id],
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
