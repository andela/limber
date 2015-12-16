from django.db import models

class CharFieldCaseInsensitive(models.CharField):

	def get_db_prep_save(self, value, connection, prepared=False):
		"""
		This method ensures the uniqueness of values in a model field by enforcing the use of lowercase
		for all entries made in CharFields.
		This is meant to cater for case insensitivity in databases such as PostgreSQL.
		"""
		return value.lower()

class EmailFieldCaseInsensitive(models.EmailField):

	def get_db_prep_save(self, value, connection, prepared=False):
		"""
		This method ensures the uniqueness of values in a model field by enforcing the use of lowercase
		for all entries made in EmailFields.
		This is meant to cater for case insensitivity in databases such as PostgreSQL.
		"""
		return value.lower()