from django.shortcuts import render

def schedule_week(request, year, week):
    return render(request, 'schedule/schedule-week.html')
