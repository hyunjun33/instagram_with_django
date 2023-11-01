from django.shortcuts import render, redirect
from posts.models import Post, Comment, PostImage
from posts.forms import CommentForm, PostForm
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse

# Create your views here.
def feeds(request):
    if not request.user.is_authenticated:
        return redirect("users:login")

    # 모든 글 목록을 템플릿으로 전달
    posts = Post.objects.all()
    comment_form = CommentForm()

    context = {"posts": posts,
               "comment_form": comment_form,

               }

    return render(request, "posts/feeds.html", context)

@require_POST
def comment_add(request):
    # request.POST로 전달된 데이터를 사용해 CommentForm 인스턴스를 생성
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # commit=False 옵션으로 메모리상에 Comment 객체 생성
        comment = form.save(commit=False)

        # Comment 생성에 필요한 사용자 정보를 request에서 가져와 할당
        comment.user = request.user

        # DB에 Comment 객체 저장
        comment.save()

        # 생성한 comment에서 연결된 post 정보를 가져와서 id값을 사용
        url = reverse("posts:feeds") + f"#posts-{comment.post.id}"
        return HttpResponseRedirect(url)
        # return HttpResponseRedirect(f"/posts/feeds/#post-{comment.post.id}")

@require_POST
def comment_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.user == request.user:
        comment.delete()

        url = reverse("posts/feeds") + f"#post-{comment.post.id}"
        return HttpResponseRedirect(url)
        # return HttpResponseRedirect(f"/posts/feeds/#post-{comment.post.id}")
    else:
        return HttpResponseForbidden("이 댓글을 삭제할 권한이 없습니다")


def post_add(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            for image_file in request.FILES.getlist("images"):
                PostImage.objects.create(
                    post=post,
                    photo=image_file,
                )

            url = reverse("posts:feeds") + f"#post-{post.id}"
            # url = f"/posts/feeds/#post-{post.id}"
            return HttpResponseRedirect(url)
    else:
        form = PostForm()

    context = {"form": form}
    return render(request, "posts/post_add.html", context)