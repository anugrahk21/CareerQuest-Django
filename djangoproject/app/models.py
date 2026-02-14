from django.db import models

class CareerApp(models.Model):
    BRANCH_CHOICES=[
        ('APPLIED', 'Applied'),
        ('OA','Online Assessment'),
        ('HR','HR'),
        ('TECHNICAL','Technical'),
        ('FINAL','Final'),
        ('ACCEPTED','Accepted'),
        ('REJECTED','Rejected'),
        ('PLACED','Placed'),
    ]

    JOB_TYPE=[('TECH','TECH'),('HR','HR'),('FINANCE','FINANCE'),('SALES','SALES'),('MARKETING','MARKETING'),('OTHER','OTHER')]

    PACKAGE=[('>3LPA','>3LPA'),('3-5LPA','3-5LPA'),('5-8LPA','5-8LPA'),('8-12LPA','8-12LPA'),('12-15LPA','12-15LPA'),('>15LPA','>15LPA')]

    id=models.IntegerField(primary_key=True)
    company=models.CharField(max_length=100)
    role=models.CharField(max_length=100)
    type=models.CharField(max_length=100,choices=JOB_TYPE)
    package=models.CharField(max_length=100,choices=PACKAGE)
    status=models.CharField(max_length=100,choices=BRANCH_CHOICES)
    date=models.DateField() # YYYY-MM-DD
    notes=models.TextField()

    def __str__(self):
        return f"{self.id} ({self.company}) - {self.status} {self.role} {self.package} {self.date} {self.notes}"
    
