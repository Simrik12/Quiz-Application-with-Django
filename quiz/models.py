from django.db import models

class Subject(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Question (models.Model):
    subject = models.ForeignKey (Subject, on_delete=models.CASCADE)
    question_text= models.CharField (max_length=500)
    option_a= models.CharField (max_length=200)
    option_b= models.CharField (max_length=200)
    option_c= models.CharField (max_length=200)
    option_d= models.CharField (max_length=200)
    correct_option = models.CharField (max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ])

    def get_options(self):
        return {
            'A': self.option_a,
            'B': self.option_b,
            'C': self.option_c,
            'D': self.option_d,
        }

    def __str__(self):
        return self.question_text

