# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.db import connection
from django.db import models
from django.core.validators import RegexValidator

class Person(models.Model):
	male = 'M'
	female = 'F'
	CHOICES = ((male,'MALE'),(female,'FEMALE'))
	alpha = RegexValidator(r'^[a-zA-Z ]*$', 'Only alphabetic characters are allowed.')
	user_id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=250, validators = [alpha])
	username = models.CharField(unique=True, max_length=250)
	password = models.CharField(max_length=250)
	gender = models.CharField(max_length=1, choices = CHOICES)
	emailid = models.CharField(unique=True, max_length=250)

	class Meta:
		managed = False
		db_table = 'person'

	def set_password(self,password):
		self.password = password

	def insert(self):
		cursor = connection.cursor()
		#cursor.execute('INSERT INTO Person VALUES(%s,%s,%s,%s,%s,%s)',[self.user_id,self.name,self.username,self.password,self.gender,self.emailid])
		cursor.execute('INSERT INTO Person(name,username,password,gender,emailid) VALUES(%s,%s,%s,%s,%s)',[self.name,self.username,self.password,self.gender,self.emailid])
class Friends(models.Model):
    sender = models.ForeignKey('Person',  models.DO_NOTHING,related_name="sender")
    recipient = models.ForeignKey('Person', models.DO_NOTHING,related_name="recipient")
    accepted = models.IntegerField()
    rejected = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'friends'
            

