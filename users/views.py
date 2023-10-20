from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from users.forms import LoginForm, SignupForm
from users.models import User

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect("/posts/feeds")

    if request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("/posts/feeds/")
            else:
                form.add_error(None, "입력한 자격증명에 해당하는 사용자가 없습니다")


        context = {"form": form}
        return render(request, "users/login.html", context)

    else:
        form = LoginForm()
        context = {"form": form}
        return render(request, "users/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("/users/login/")

def signup(request):
    if request.method == "POST":
        form = SignupForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            profile_image = form.cleaned_data["profile_image"]
            short_description = form.cleaned_data["short_description"]

            # 비밀번호와 비밀번호 확인의 값이 같은지 검사
            if password1 != password2:
                form.add_error("password2", "비밀번호와 비밀번호 확인란의 값이 다릅니다")

            # username을 사용 중인 User가 이미 있는지 검사
            if User.objects.filter(username=username).exists():
                form.add_error("username", "입력한 사용자명은 이미 사용 중입니다")

            # 에러가 존재한다면, 에러를 포함한 form을 사용해 회원가입 페이지를 다시 렌더링
            if form.errors:
                context = {"form": form}
                return render(request, "users/signup.html", context)

    form = SignupForm()
    context = {"form": form}
    return render(request, "users/signup.html", context)