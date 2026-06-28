from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor')
    full_name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.full_name


class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='learner')
    full_name = models.CharField(max_length=200)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Enrollment(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('learner', 'course')

    def __str__(self):
        return f"{self.learner.full_name} enrolled in {self.course.name}"


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='submissions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='submissions')
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('enrollment', 'question')

    def __str__(self):
        return f"Submission by {self.enrollment.learner.full_name} - {self.question.question_text[:50]}"


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
