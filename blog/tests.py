from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post
from django.shortcuts import reverse


class BlogPostTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # initialize the objects that we want to use in test

        # User
        cls.user = User.objects.create(username='user1')
        # Posts
        cls.post1 = Post.objects.create(
            title="Post1 Title",
            text="Post1 Text",
            author=cls.user,
            status=Post.STATUS_CHOICES[0][0],
        )
        cls.post2 = Post.objects.create(
            title="Post2 Title",
            text="Post2 Text",
            author=cls.user,
            status=Post.STATUS_CHOICES[1][0],
        )

    # def setUp(self):

#######################################################################################################################
    def test_post_list_view_urls_by_url(self):
        response = self.client.get("/blog/")
        self.assertEqual(response.status_code, 200)

    def test_post_list_view_urls_by_name(self):
        response = self.client.get(reverse("posts_list"))
        self.assertEqual(response.status_code, 200)

    def test_post_list_has_post_title(self):
        response = self.client.get("/blog/")
        self.assertContains(response, self.post1.title)

    def test_doesnt_show_draft_posts_in_post_list_page(self):
        response = self.client.get(reverse("posts_list"))
        self.assertContains(response, self.post1.title)
        self.assertNotContains(response, self.post2.title)

#######################################################################################################################
    def test_post_details_view_urls_by_url(self):
        response = self.client.get(f'/blog/{self.post1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_details_view_urls_by_name(self):
        response = self.client.get(reverse("post_detail", args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_details_has_post_text_and_title(self):
        response = self.client.get(reverse("post_detail", args=[self.post1.id]))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)

    def test_post_detail_error_404_if_post_does_not_exist(self):
        response = self.client.get(reverse("post_detail", args=[self.post1.id + 2]))
        self.assertEqual(response.status_code, 404)

#######################################################################################################################
    def test_check_post_str_is_equal_with_title(self):
        self.assertEqual(self.post1.title, str(self.post1))

#######################################################################################################################
    def test_delete_view_urls_by_url(self):
        response = self.client.get(f'/blog/{self.post1.id}/delete/')
        self.assertEqual(response.status_code, 200)

    def test_delete_view_urls_by_name(self):
        response = self.client.get(reverse('delete_post', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)

    def test_check_delete_post_id_is_exists(self):
        response = self.client.get(f'/blog/{self.post1.id}/delete/')
        self.assertContains(response, self.post1.title)

    def test_delete_post(self):
        response = self.client.post(reverse('delete_post', args=[self.post2.id]))
        self.assertEqual(response.status_code, 302)

#######################################################################################################################
    def test_update_view_urls_by_url(self):
        response = self.client.get(f'/blog/{self.post1.id}/update/')
        self.assertEqual(response.status_code, 200)

    def test_update_view_urls_by_name(self):
        response = self.client.get(reverse('update_post', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)

    def test_check_update_post_id_is_exists(self):
        response = self.client.get(f'/blog/{self.post1.id}/update/')
        self.assertContains(response, self.post1.title)

    def test_update_post(self):
        response = self.client.post(reverse('update_post', args=[self.post1.id]), {
            'title': 'Post1 updated!',
            'text': 'Post1 text updated!',
            'status': 'pub',
            'author': self.post1.author.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.get(id=self.post1.id).title, 'Post1 updated!')
        self.assertEqual(Post.objects.get(id=self.post1.id).text, 'Post1 text updated!')

#######################################################################################################################
    def test_create_post(self):
        response = self.client.post(reverse('add_new_post'), {
            'title': 'test post',
            'text': 'this is a test for test post!',
            'author': self.user.id,
            'status': 'pub',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'test post')
        self.assertEqual(Post.objects.last().text, 'this is a test for test post!')
        self.assertEqual(Post.objects.last().author, self.user)
        self.assertEqual(Post.objects.last().status, 'pub')
