from django.db import models

class User(models.Model):
    ID = models.CharField(max_length=100)
    name = models.TextField()
    email = models.EmailField()
    password = models.CharField(max_length=100)
    role = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

class Reservation(models.Model):
    ID = models.ForeignKey(User, on_delete=models.CASCADE)
    pickupsate = models.DateField()
    returndate = models.DateField()
    typeofinsurance = models.CharField(max_length=100)

    def __str__(self):
        return f"Reservation {self.id} for {self.user.name} - {self.course.title}"
