import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from blog.models import Post

User = get_user_model()

@pytest.mark.django_db
def test_index_view_displays_posts(client):
    user = User.objects.create_user(username='writer', password='12345')
    Post.objects.create(title='Post 1', content='Hello world', author=user)
    response = client.get(reverse('index'))
    assert response.status_code == 200
    assert b'Post 1' in response.content
