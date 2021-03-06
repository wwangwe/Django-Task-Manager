from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class TaskList(models.Model):
	title = models.CharField(max_length=20)
	created = models.DateTimeField(auto_now=True)
	creator = models.ForeignKey(User, null=True, related_name='tasklists', on_delete=models.CASCADE)

	class Meta:
		ordering = ('created',)

	def __str__(self):
		return self.title

	def count(self):
		"""Returns count of all tasks in related list"""
		return self.tasks.count()

	def count_complete(self):
		"""Returns count of all complete tasks in related list"""
		return self.tasks.filter(is_complete=True).count()

	def count_incomplete(self):
		"""Returns count of all incomplete tasks in related list"""
		return self.tasks.filter(is_complete=False).count()

class Task(models.Model):
	creator = models.ForeignKey(User, null=True, related_name='tasks', on_delete=models.CASCADE)
	tasklist = models.ForeignKey(TaskList, related_name='tasks', on_delete=models.CASCADE)
	description = models.CharField(max_length=255)
	created = models.DateTimeField(auto_now=True)
	completed_at = models.DateTimeField(null=True)
	is_complete = models.BooleanField(default=False)

	class Meta:
		ordering = ('tasklist', 'created', 'completed_at')

	def __str__(self):
		return self.description
	
	def complete(self):
		self.is_complete = True
		self.completed_at = timezone.now()
		self.save()

	def restart(self):
		self.is_complete = False
		self.completed_at = None
		self.save()