from django.shortcuts import render
from .models import *
from django.http import JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

import json
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def weatherInfo(request):
    r = requests.get('https://get.geojs.io/')
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    ipAdd = ip_request.json()['ip']    
    url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
    geo_request = requests.get(url)
    geo_data = geo_request.json()
    url = 'https://api.openweathermap.org/data/2.5/weather?lat='+geo_data['latitude']+'&lon='+geo_data['longitude']+'&units=imperial&type=accurate&appid=e11862ae7905f24f99e779d8ffeed6c1'
    report = requests.get(url)
    wdata = report.json()
    temp = (wdata['main']['temp'] - 32)* 5/9
    wind = wdata['wind']
    name = wdata['name']


    
    print(geo_data['latitude'])
    print(geo_data['longitude'])
    data = {'latitude':geo_data['latitude']}
    payload = {'status': True, 'City' :name, 'temprature' : temp, 'wind' : wind['speed']}

    return JsonResponse(payload)


@login_required(login_url='/login')
def home(request):
    current_user = request.user
    # print current_user.id
    courses = Quiz.objects.filter(user_id=current_user.id)
    r = requests.get('https://get.geojs.io/')
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    ipAdd = ip_request.json()['ip']    
    url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
    geo_request = requests.get(url)
    geo_data = geo_request.json()
    url = 'https://api.openweathermap.org/data/2.5/weather?lat='+geo_data['latitude']+'&lon='+geo_data['longitude']+'&units=imperial&type=accurate&appid=e11862ae7905f24f99e779d8ffeed6c1'
    report = requests.get(url)
    wdata = report.json()
    temp = (wdata['main']['temp'] - 32)* 5/9
    wind = wdata['wind']
    name = wdata['name']
    context = {'courses' : courses, 'current_user' : current_user, 'City' :name, 'temprature' : temp, 'wind' : wind['speed']}
    return render(request , 'home.html' , context)
    

def api_question(request , id):
    raw_questions = Question.objects.filter(course =id)[:20]
    questions = []
    
    for raw_question in raw_questions:
        question = {}
        question['id'] = raw_question.id
        question['question'] = raw_question.question
        question['answer'] = raw_question.answer
        question['marks'] = raw_question.marks
        options = []
        options.append(raw_question.option_one)
        options.append(raw_question.option_two)
        if raw_question.option_three != '':
            options.append(raw_question.option_three)
        
        if raw_question.option_four != '':
            options.append(raw_question.option_four)
        
        question['options'] = options
         
        questions.append(question)
        
        
    return JsonResponse(questions , safe=False)
@login_required(login_url='/login')
def view_score(request):
    user = request.user
    score = ScoreBoard.objects.filter(user=user)
    context = {'score' : score}
    return render(request,'score.html' , context)

@login_required(login_url='/login')
def take_quiz(request , id):
    context = {'id' : id}
    return render(request , 'quiz2.html'  , context)

@csrf_exempt
@login_required(login_url='/login')
def check_score(request):
    data = json.loads(request.body)
    user = request.user
    course_id = data.get('course_id')
    solutions = json.loads(data.get('data'))
    course = Course.objects.get(id=course_id)
    score = 0
    for solution in solutions:
        question = Question.objects.filter(id = solution.get('question_id')).first()
      
        if (question.answer) == solution.get('option'):
            score = score + question.marks
   
    score_board = ScoreBoard(course = course , score = score  , user = user)
    score_board.save() 
    
    return JsonResponse({'message' : 'success' , 'status':True})


