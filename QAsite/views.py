from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
from django.core import serializers
import json
import markdown2
import bleach
from django.contrib.auth.models import User

solved = False

count= models.Question.objects.all().count()
count_answer = models.Answer.objects.all().count()
users = User.objects.all()

# if models.Answer.objects.exists():
latest = models.Question.objects.order_by('date_posted').reverse()[0]
latest1 = models.Question.objects.order_by('date_posted').reverse()[1]

def index(request):
    # global count
    # global count_answer
    
    if request.user.is_authenticated:
        count= models.Question.objects.all().count()
        count_answer = models.Answer.objects.all().count()
        users = User.objects.all()
        questionss = models.Question.objects.all()
        # answers = models.Answer.objects.order_by('date_posted').reverse()
        count_answer_per_q=[]
        solved = []
        context = {}
        for question in questionss:
            count_answer_per= models.Answer.objects.filter(qid=question.qid).count()
            if count_answer_per == 0:
                solve = False
                solved.append(solve)
            else:
                solve = True
                solved.append(solve)

            count_answer_per_q.append(count_answer_per)
        questions = zip(questionss,count_answer_per_q,solved)
        

        
        context= {'count':count,'count_answer':count_answer,'questions':questions, 'latest':latest,"latest1":latest1,"users":users, 'solved':solved}
        return render(request, 'index.html', context)
        
    else:
        messages.info(request, 'Please Login first')
        return redirect("/")
    # questions = zip(questionss,count_answer_per_q,solved,answers)
    # context= {'count':count,'count_answer':count_answer,'questions':questionss, 'latest':latest,"latest1":latest1,"users":users, 'solved':solved}
    

def askquestion(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                context = {}
                title = request.POST.get('title')
                question = request.POST.get('question')
                posted_by = request.user.username
                q = models.Question(question_title=title, question_text=question, posted_by=posted_by)
                q.save()
                # return redirect(viewquestion, q.qid, q.slug)
                return redirect("/")
            except Exception as e:
                return render(request, 'ask_question.html', { 'error': 'Something is wrong with the form!' })
        else:
            context= {'count':count,'count_answer':count_answer,'latest':latest,"latest1":latest1,"users":users,'solved':solved}
            return render(request, 'ask_question.html',context)
    else:
        messages.info(request, 'Please Login first')
        return redirect("/")
    
def contact(request):
    context= {'count':count,'count_answer':count_answer,'latest':latest,"latest1":latest1,"users":users,'solved':solved}
    return render(request,"contact_us.html",context)

def user_profile(request):
    if request.user.is_authenticated:
        user_q = models.Question.objects.filter(posted_by=request.user).count()
        user_a = models.Answer.objects.filter(posted_by=request.user).count()
        context= {'count':count,'count_answer':count_answer,'latest':latest,"latest1":latest1,"users":users,'solved':solved,"user_q":user_q,"user_a":user_a}
        return render(request,"user_profile.html",context)
    else:
        return redirect("/")

def user_answers(request):
    if request.user.is_authenticated:
        user_ans = models.Answer.objects.filter(posted_by=request.user)
        user_answ = {}
        qids = models.Answer.objects.values_list("qid")
        qids =list(dict.fromkeys(qids))
        out = [item for t in qids for item in t]
        for i in out:
            user_answ[out.index(i)] = models.Question.objects.filter(qid=i)
            # user_answ.append(user_an) 
        count_answer_per_q=[]
        solved = []
        for key,value in user_answ.items():
            for question in value:
                count_answer_per= models.Answer.objects.filter(qid=question.qid).count()
                if count_answer_per == 0:
                    solve = False
                    solved.append(solve)
                else:
                    solve = True
                    solved.append(solve)

                count_answer_per_q.append(count_answer_per)
        user_answs = zip(user_answ,count_answer_per_q,solved)    
        
       
        # user_answ = models.Question.objects.filter(qid=qids[0])
        # print(user_answ)
        user_q = models.Question.objects.filter(posted_by=request.user).count()
        user_a = models.Answer.objects.filter(posted_by=request.user).count()
        context= {'count':count,'count_answer':count_answer,'latest':latest,"latest1":latest1,"users":users,"user_answs":user_answs,"user_answ":user_answ,'solved':solved,"user_q":user_q,"user_a":user_a}
        return render(request,"user_answers.html",context)
    else:
        return redirect("/")


def user_questions(request):
    if request.user.is_authenticated:
        user_ques = models.Question.objects.filter(posted_by=request.user)
        count_answer_per_q=[]
        solved = []
        for question in user_ques:
            count_answer_per= models.Answer.objects.filter(qid=question.qid).count()
            if count_answer_per == 0:
                solve = False
                solved.append(solve)
            else:
                solve = True
                solved.append(solve)

            count_answer_per_q.append(count_answer_per)
        user_quest = zip(user_ques,count_answer_per_q,solved) 
        
        user_q = models.Question.objects.filter(posted_by=request.user).count()
        user_a = models.Answer.objects.filter(posted_by=request.user).count()
        context= {'count':count,'count_answer':count_answer,'latest':latest,"latest1":latest1,"users":users,"user_quest":user_quest,'solved':solved,"user_q":user_q,"user_a":user_a}
        return render(request,"user_questions.html",context)
    else:
        return redirect("/")

def user_points(request):
    if request.user.is_authenticated:
        user_q = models.Question.objects.filter(posted_by=request.user).count()
        user_a = models.Answer.objects.filter(posted_by=request.user).count()
        context= {'count':count,'count_answer':count_answer,'latest':latest,"latest1":latest1,"users":users,'solved':solved,"user_q":user_q,"user_a":user_a}
        return render(request,"user_points.html",context)
    else:
        return redirect("/")


def viewquestion(request, qid, qslug):
    if request.user.is_authenticated:
        context = {}
        context1= {'count':count,'count_answer':count_answer,'latest':latest,"latest1":latest1,"users":users}
        question = models.Question.objects.get(qid=qid, slug=qslug)
        question_json = json.loads(serializers.serialize('json', [ question ]))[0]['fields']
        question_json['date_posted'] = question.date_posted
        question_json['qid'] = question.qid
        question_json['question_text'] = bleach.clean(markdown2.markdown(question_json['question_text']), tags=['p', 'pre','code', 'sup', 'strong', 'hr', 'sub', 'a'])
        context['question'] = question_json
        context['answers'] = []
        answers = models.Answer.objects.filter(qid=qid)
        # posted_by=request.user.username
        # a = models.Answer(posted_by=posted_by,qid=models.Question.objects.get(qid=qid))
        # a.save()
        for answer in answers:
            answer.answer_text = bleach.clean(markdown2.markdown(answer.answer_text), tags=['p', 'pre','code', 'sup', 'strong', 'hr', 'sub', 'a'])
            context['answers'].append(answer)
        return render(request, 'view-question.html', context)
    else:
        messages.info(request, 'Please Login first')
        return redirect("/")
@csrf_exempt
def ajaxanswerquestion(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            answer = json_data['answer']
            posted_by = request.user.username
            qid = json_data['qid']
            a = models.Answer(answer_text=answer, posted_by=posted_by, qid=models.Question.objects.get(qid=qid))
            a.save()
            return JsonResponse({'Success': 'Answer posted successfully.'})
        except Exception as e:
            print(e)
            return JsonResponse({'Error': 'Something went wrong when posting your answer.'})
            