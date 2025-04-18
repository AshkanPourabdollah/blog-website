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
