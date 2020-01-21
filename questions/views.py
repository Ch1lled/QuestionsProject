from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
#from django.views.generic import TemplateView
#from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Question, Answer, Tag
from .forms import QuestionForm, AnswerForm, AddTagForm
from django.utils import timezone


def main(request):
    return render(request, 'main.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password1']
            # user = authenticate(username=username, password=password)
            # login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form' : form})

def logout(request):
    logout(request)
    return redirect('logout')

def questions(request):
    questions = Question.objects.filter(creation_date__lte=timezone.now()).order_by('-creation_date')
    return render(request, 'questions/questions.html', {'questions' : questions})

def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answer_set.all().order_by('creation_date')
    current_user = request.user.id
    # answers = Answer.objects.filter(question=question).order_by('creation_date')
    return render(request, 'questions/question.html', {'answers' : answers, 'question': question})

def asking(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.creation_date = timezone.now()
            question.save()

            # tags = [x.strip().lower() for x in form.cleaned_data['tag_list'].split(',')]
            for raw_tag in form.cleaned_data['tag_list'].split(','):
                raw_tag = raw_tag.strip().lower()
                tag = Tag()
                if raw_tag in Tag.objects.values_list('title', flat=True):
                    tag = Tag.objects.get(title = raw_tag)  
                else:
                    tag = Tag.objects.create(title=raw_tag, slug=raw_tag)
                question.tags.add(tag)
            return redirect('question', question_id = question.pk)
    else:
        form = QuestionForm()
    return render(request, 'questions/asking.html', { 'form' : form })

def replying(request, question_id):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = Question.objects.get(pk=question_id)
            answer.author = request.user
            answer.creation_date = timezone.now()
            answer.save()
            return redirect('question', question_id=question_id)
    else:
        form = AnswerForm()
    return render(request, 'questions/replying.html', { 'form': form, 'question_id': question_id })


def question_like(request, question_id):
    if request.user.is_authenticated:
        question = Question.objects.get(id = question_id)
        current_user = request.user.id
        if current_user != question.author_id:
            if current_user not in Question.objects.values_list('voted_user', flat=True).filter(id=question_id):
                try:
                    question = Question.objects.get(pk=question_id)
                    question.likes +=1
                    question.voted_user.add(current_user)
                    question.rating = question.likes - question.dislikes
                    question.save()
                    return redirect('question', question_id=question_id)
                except ObjectDoesNotExist:
                    return redirect('question', question_id=question_id)
            else:
                return redirect('question', question_id=question_id)
        else:
            return redirect('question', question_id=question_id)
    else:
        return redirect('question', question_id=question_id)

def question_dislike(request, question_id):
    if request.user.is_authenticated:
        question = Question.objects.get(id = question_id)
        current_user = request.user.id
        if current_user != question.author_id:
            if current_user not in Question.objects.values_list('voted_user', flat=True).filter(id=question_id):
                try:
                    question = Question.objects.get(pk=question_id)
                    question.dislikes +=1
                    question.voted_user.add(current_user)
                    question.rating = question.likes - question.dislikes
                    question.save()
                    return redirect('question', question_id=question_id)
                except ObjectDoesNotExist:
                    return redirect('question', question_id=question_id)
            else:
                return redirect('question', question_id=question_id)
        else:
            return redirect('question', question_id=question_id)
    else:
        return redirect('question', question_id=question_id)

def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'questions/tags_list.html', { 'tags' : tags })

def tag(request, slug):
    tag = Tag.objects.get(slug__iexact=slug)
    return render(request, 'questions/tag.html', { 'tag' : tag })

# def add_tag(request, question_id):
#     if request.method == 'POST':
#         form = AddTagForm(request.POST)
#         question = Question.objects.get(id = question_id)
#         if form.is_valid():
#             tag = form.save(commit=False)
#             a_t = tag.title
#             a_t = a_t.lower()
#             tag.title - a_t
#             tag.slug =  a_t
#             question.tags.add(a_t)
#             if a_t not in Tag.objects.values_list('title', flat=True):
#                 Tag.objects.create(title=a_t, slug=a_t)
#                 tag.save()
#                 return redirect('question', question_id=question_id)
#             else:
#                 return redirect('question', question_id=question_id)
#     else:
#         form = AddTagForm()
#     return render(request, 'questions/question.html', { 'form': form, 'question_id': question_id, 'tag' : tag })




# def question_dislike(request, question_id):
#     if not request.user.is_authenticated:
#          return redirect('question', question_id=question_id)
    
#     try:
#         question = Question.objects.get(pk=question_id)
#     except ObjectDoesNotExist:
#         return redirect('question', question_id=question_id)

#     current_user_id = request.user.id

#     if current_user_id != question.author.id:
#          return redirect('question', question_id=question_id)

#     if current_user_id not in Question.objects.values_list('voted_user', flat=True).filter(id=question_id):
#         question.dislikes +=1
#         question.voted_user.add(current_user_id)
#         question.rating = question.likes - question.dislikes
#         question.save()
#         return redirect('question', question_id=question_id)
#     else:
#         return redirect('question', question_id=question_id)

def answer_like(request, question_id, answer_id):
    if request.user.is_authenticated:
        answer = Answer.objects.get(id = answer_id)
        current_user = request.user.id
        if current_user != answer.author_id:
            if current_user not in Answer.objects.values_list('voted_user', flat=True).filter(id=answer_id):
                try:
                    answer = Answer.objects.get(pk=answer_id)
                    answer.likes += 1
                    answer.voted_user.add(current_user)
                    answer.rating = answer.likes - answer.dislikes
                    answer.save()
                    return redirect('question', question_id=question_id)
                except ObjectDoesNotExist:
                    return redirect('question', question_id=question_id)
            else:
                return redirect('question', question_id=question_id)
        else:
            return redirect('question', question_id=question_id)
    else:
        return redirect('question', question_id=question_id)

def answer_dislike(request, question_id, answer_id):
    if request.user.is_authenticated:
        answer = Answer.objects.get(id = answer_id)
        current_user = request.user.id
        if current_user != answer.author_id:
            if current_user not in Answer.objects.values_list('voted_user', flat=True).filter(id=answer_id):
                try:
                    answer = Answer.objects.get(pk=answer_id)
                    answer.dislikes += 1
                    answer.voted_user.add(current_user)
                    answer.rating = answer.likes - answer.dislikes
                    answer.save()
                    return redirect('question', question_id=question_id)
                except ObjectDoesNotExist:
                    return redirect('question', question_id=question_id)
            else:
                return redirect('question', question_id=question_id)
        else:
            return redirect('question', question_id=question_id)
    else:
        return redirect('question', question_id=question_id)




def test(request):
    #if request.user != answer.user
    return render(request, 'test.html', {})


# class MainView(TemplateView):
#     template_name = 'main.html'

#     # def auth(self, request):
#     #     if request.user.is_authenticated:
#     #         return redirect('question_list/')
#     #     else:
#     #         return HttpResponse('Требуется авторизация')

# class RegisterFormView(FormView):
#     form_class = UserCreationForm
#     template_name = 'register.html'
#     success_url = '/questions/login/'

#     def form_valid(self, form):
#         form.save()
#         return super(RegisterFormView, self).form_valid(form)

#     def form_invalid(self, form):
#         return super(RegisterFormView, self).form_invalid(form)

# class LoginView(FormView):
#     form_class = AuthenticationForm
#     template_name = 'login.html'
    
#     #success_url = '/questions/question_list/'

#     # def login(request):
#     #     username = request.POST['username']
#     #     password = request.POST['password']
#     #     user = authenticate(request, username=username, password=password)
       
#     #     if user is not None:
#     #         login(request, user)
#     #         return redirect('/questions/question_list/')
#     #     else:
#     #         return HttpResponse('Неверный логин или пароль') #redirect('/questions/login/')
       
# class LogoutView(FormView):
#     template_name = 'logout.html'
#     success_url = '/questions/login/'

#     def logout_success(request):
#         logout(request)

# class QuestionListView(LoginRequiredMixin, TemplateView):
#     login_url = '/questions/login/'
#     template_name = 'question_list.html'

#     # def auth(request):
#     #     if request.user.is_authenticated:
#     #         return redirect('question_list/')
#     #     else:
#     #         return HttpResponse('Требуется авторизация')
