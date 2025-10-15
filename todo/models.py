from django.utils import timezone
from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    completed = models.BooleanField(default=False, null=False, blank=False)
    created_date = models.DateField(auto_now_add=True, null=False, blank=False)
    due_date = models.DateField(null=False, blank=False, default=timezone.now)  # user sets manually, required
    position = models.PositiveIntegerField(default=0, null=False, blank=False)

    class Meta:
        ordering = ['completed', 'position']  # completed first, then by position

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.title or self.title.strip() == '':
            raise ValidationError({'title': 'Task title cannot be empty.'})
        if self.title and len(self.title.strip()) < 3:
            raise ValidationError({'title': 'Task title must be at least 3 characters long.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def is_overdue(self):
        return self.due_date and self.due_date < timezone.now().date() and not self.completed