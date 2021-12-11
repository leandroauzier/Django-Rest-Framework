# libs from API v1
from rest_framework import generics
from rest_framework.generics import get_object_or_404

# libs from API v2
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins

from rest_framework import permissions

# Used from both
from .models import Curso, Avaliacao
from .serializers import CursoSerializer, AvaliacaoSerializer
from .permissions import EhSuperUser

'''
API V1
'''


class CursosAPIView(generics.ListCreateAPIView):    # LIST - get, CREATE - post
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class CursoAPIView(generics.RetrieveUpdateDestroyAPIView):  # Retrieve - return, Update - update, Destroy - delete
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class AvaliacoesAPIView(generics.ListCreateAPIView):    # LIST - get, CREATE - post
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer

    def get_queryset(self):
        if self.kwargs.get('curso_pk'):
            return self.queryset.filter(curso_id=self.kwargs.get('curso_pk'))
        return self.queryset.all()


class AvaliacaoAPIView(generics.RetrieveUpdateDestroyAPIView):  # Retrieve - return, Update - update, Destroy - delete
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer

    def get_object(self):
        if self.kwargs.get('curso_pk'):     # if has kwargs (id from one curso on url)
            return get_object_or_404(self.get_queryset(),
                                     # filtering the spefic queryset
                                     curso_id=self.kwargs.get('curso_pk'),
                                     pk=self.kwargs.get('avaliacao_pk'))
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('avaliacao_pk'))


'''
API V2

Viewset: Groups all the logic of a resource in a class, in this case, Viewset.
Routers: Automate criation of endpoints for APIs.

'''


class CursoViewSet(viewsets.ModelViewSet):
    # Permissions from DjangoModel differs from Global permission on settings.py
    # WARNING: attention for the parameters order, if the first solve, it won't will consult the next one
    permission_classes = (
        EhSuperUser,
        permissions.DjangoModelPermissions, )
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    # Creating a new route avaliacoes from cursos
    @action(detail=True, methods=['get'])       # Validate criation and give only get method
    def avaliacoes(self, request, pk=None):     # Function that return all avaliacoes from curso
        self.pagination_class.page_size = 1
        avaliacoes = Avaliacao.objects.filter(curso_id=pk)
        page = self.paginate_queryset(avaliacoes)

        if page is not None:
            serializer = AvaliacaoSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AvaliacaoSerializer(avaliacoes, many=True)
        return Response(serializer.data)

'''
class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
'''


class AvaliacaoViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
    ):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
