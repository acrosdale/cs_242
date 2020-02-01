from djongo import models
<<<<<<< HEAD
=======
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

    objects = models.DjongoManager()


