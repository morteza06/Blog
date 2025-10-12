import pytest
from django.contrib.auth import get_user_model

from blog.models import Post

User = get_user_model()


@pytest.mark.django_db
def test_create_post():
    user = User.objects.create_user(username="writer", password="pass123")
    post = Post.objects.create(title="Sample", content="This is a test", author=user)
    assert post.title == "Sample"
    assert str(post) == "Sample"
