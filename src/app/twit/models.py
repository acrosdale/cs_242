from djongo import models
from django import forms

# created_at: utc_String
# text	: String
# user		: use r -obj
# coordinates	: coordinate s -obj
#
# entities 	: Entities obj <---HashTag
# are
# here
# "lang"	: "en"


class TwitUser(models.Model):
    user_id = models.PositiveIntegerField()
    name = models.CharField()
    screen_name = models.CharField()
    location = models.CharField()
    description = models.TextField()
    verified = models.BooleanField(default=False)
    followers_count = models.PositiveIntegerField()
    friends_count = models.PositiveIntegerField()

    class Meta:
        abstract = True


class TwitUserForm(forms.ModelForm):
    class Meta:
        model = TwitUser
        fields = (
            "user_id",
            "name",
            "screen_name",
            "location",
            "description",
            "verified",
            "followers_count",
            "friends_count"
        )


# class HashTag(models.Model):
#     text = models.CharField()
#
#     class Meta:
#         abstract = True
#
#
# class HashTagForm(forms.ModelForm):
#
#     class Meta:
#         model = HashTag
#         exclude = (
#             "id","_id",
#         )


class Tweet(models.Model):
    date_created = models.DateTimeField()
    text = models.TextField()
    coordinates = models.ListField()
    hashtags = models.ListField()
    user = models.EmbeddedField(
        model_container=TwitUser,
        model_form_class=TwitUserForm
    )

    objects = models.DjongoManager()

#
# class Blog(models.Model):
#     name = models.CharField(max_length=100)
#     tagline = models.TextField()
#
#     class Meta:
#         abstract = True
#
#
# class BlogForm(forms.ModelForm):
#     class Meta:
#         model = Blog
#         fields = (
#             'name', 'tagline'
#         )
#
#
# class Author(models.Model):
#     name = models.CharField(max_length=200)
#     email = models.EmailField()
#
#     class Meta:
#         abstract = True
#
#
# class AuthorForm(forms.ModelForm):
#     class Meta:
#         model = Author
#         fields = (
#             'name', 'email'
#         )
#
#
# class Entry(models.Model):
#     blog = models.EmbeddedField(
#         model_container=Blog,
#         model_form_class=BlogForm
#     )
#
#     headline = models.CharField(max_length=255)
#     authors = models.ArrayField(
#         model_container=Author,
#         model_form_class=AuthorForm
#     )
#
#     objects = models.DjongoManager()
