from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
from django.core import serializers
import json
import markdown2
import bleach

def index(request):
    if request.user.is_authenticated:
        context = {}
        questions = models.Question.objects.all()
        count= models.Question.objects.all().count()
    
        context= {'count':count,'questions':questions}
    else:
        messages.info(request, 'Please Login first')
        return redirect("/")
    return render(request, 'index.html', context)

def askquestion(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            context ={}
            count= models.Question.objects.all().count()
    
            context= {'count':count}
            try:
                title = request.POST.get('title')
                question = request.POST.get('question')
                posted_by = request.POST.get('posted_by')
                q = models.Question(question_title=title, question_text=question, posted_by=posted_by)
                q.save()
                return redirect(viewquestion, q.qid, q.slug)
            except Exception as e:
                return render(request, 'ask_question.html', { 'error': 'Something is wrong with the form!' })
        else:
            return render(request, 'ask_question.html', {})
        return render(request, 'ask_question.html',context)
    else:
        messages.info(request, 'Please Login first')
        return redirect("/")

# def viewquestion(request, qid, qslug):
#     if request.user.is_authenticated:
#         context = {}
#         question = models.Question.objects.get(qid=qid, slug=qslug)
#         question_json = json.loads(serializers.serialize('json', [ question ]))[0]['fields']
#         question_json['date_posted'] = question.date_posted
#         question_json['qid'] = question.qid
#         question_json['question_text'] = bleach.clean(markdown2.markdown(question_json['question_text']), tags=['p', 'pre','code', 'sup', 'strong', 'hr', 'sub', 'a'])
#         context['question'] = question_json
#         context['answers'] = []
#         answers = models.Answer.objects.filter(qid=qid)
#         for answer in answers:
#             answer.answer_text = bleach.clean(markdown2.markdown(answer.answer_text), tags=['p', 'pre','code', 'sup', 'strong', 'hr', 'sub', 'a'])
#             context['answers'].append(answer)
#         return render(request, 'view-question.html', context)
#     else:
#         messages.info(request, 'Please Login first')
#         return redirect("/")
@csrf_exempt
def ajaxanswerquestion(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            answer = json_data['answer']
            posted_by = json_data['posted_by']
            qid = json_data['qid']
            a = models.Answer(answer_text=answer, posted_by=posted_by, qid=models.Question.objects.get(qid=qid))
            a.save()
            return JsonResponse({'Success': 'Answer posted successfully.'})
        except Exception as e:
            print(e)
            return JsonResponse({'Error': 'Something went wrong when posting your answer.'})
            