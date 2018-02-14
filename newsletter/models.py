from django.db import models

# Create your models here.

class Newsletter(models.Model):
	email = models.CharField(max_length=100, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, blank=True)
	updated = models.DateTimeField(auto_now=True, blank=True, null=True)

	class Meta:
		db_table = "Newsletter"
		verbose_name = "Newsletter"
		verbose_name_plural = "Newsletters"

	def __str__(self):
		return self.email
    