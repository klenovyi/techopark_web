def info(request):
    context ={'tags' :  ["World Cup","Champion Cup", "Europe League","Russian Premier League","La Liga","Bundesliga","FNL","blablabla"],
              'members': ['Andrey Pakhomov', 'Vasya Pupkin', 'Leonid Messi', 'Pupa & Lupa', 'Ivanov Ivan']}
    return context