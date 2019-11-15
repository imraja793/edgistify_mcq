from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    qualification = models.CharField(max_length=200, null=True, blank=True)
    applicant = models.BooleanField(default=True)  # if True applicant, False for Admin
    mcq_assigned = models.CharField(default=False, max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'user_profile'
        ordering = ['pk']

    def __str__(self):
        """__str__."""
        return self.user.username + " || " + self.applicant


class AddQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # who create the question i.e admin
    question = models.TextField(null=True)
    option1 = models.TextField(null=True, blank=True)
    option2 = models.TextField(null=True, blank=True)
    option3 = models.TextField(null=True, blank=True)
    option4 = models.TextField(null=True, blank=True)
    correct_ans = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.question

    class Meta:
        managed = True
        db_table = 'addquestion'
        ordering = ['pk']


class ApplicantMCQTest(models.Model):

    applicant = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    mark_scored = models.CharField(max_length=50, null=True, blank=True)
    assign_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(auto_now=True)
    response = JSONField(null=True, blank=True)

    class Meta:
        managed = True
        ordering = ['pk']

    def __str__(self):
        return str(self.pk) + " || " + str(self.mark_scored)
