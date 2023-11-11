def info(request):
    context ={'tags' :  ["tags 1","tags 2", "tags 3","tags 4","tags 5","tags 6","tags 7","tags 8", "tags 9"],
              'members': ['Andrey Pakhomov', 'Vasya Pupkin', 'Leonid Messi', 'Pupa & Lupa', 'Ivanov Ivan']}
    return context