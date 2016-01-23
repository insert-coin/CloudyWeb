from django.shortcuts import render
from rest_framework import viewsets, generics
from cloudygames.serializers import GameSerializer

class GameViewSet(viewsets.ModelViewSet):
	queryset = Game.objects.all().order_by('name')
	serializer_class = GameSerializer

class GameList(generics.ListAPIView):
	serializer_class = GameSerializer

	def get_queryset(self):
		_user = self.request.user
		return Game.objects.filter(user=_user)

