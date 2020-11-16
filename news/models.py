from django.db import models

class News(models.Model):
    create_date = models.DateTimeField()
    title = models.CharField(max_length=200)
    text = models.TextField()
    link_id = models.IntegerField()

    def publish(self):
        self.save()
