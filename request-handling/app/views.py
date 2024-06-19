from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    from_landing = request.GET.get('from-landing')
    counter_click.update([str(from_landing)])
    print(dict(counter_click))
    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    ab_test_arg = request.GET.get('ab-test-arg')
    if ab_test_arg == 'test':
        counter_show.update(['test'])
        return render(request, 'landing_alternate.html')
    else:
        counter_show.update(['original'])
        return render(request, 'landing.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:

    if dict(counter_click).get('test') is None or dict(counter_show).get('test'):
        test_conversion = 0
    else:
        test_conversion = dict(counter_click).get('test') / dict(counter_show).get('test')

    if dict(counter_click).get('original') is None or dict(counter_show).get('original') is None:
        original_conversion = 0
    else:
        original_conversion = dict(counter_click).get('original') / dict(counter_show).get('original')

    return render(request, 'stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })
