"""
All the REST resources related to a movie api will be defined in this module.
"""
from rest_framework import mixins, viewsets, filters
from rest_framework.permissions import IsAuthenticated

from .models import Movie
from .permissions import UserAccessPermission
from .serializers import MovieSerializer


class MovieViewSet(viewsets.ModelViewSet):
    """
    This is a django class based view which act as a controller to handle various methods: get, post etc. which are encapsulated by the rest framework. 
    Below metioned is the detail of various supported handler requests:
        * `GET /`: List all the available movies.
        * `GET /id/`: Get the details of a specific movie.
        * `POST /`: Create a movie.
        * `PUT /id/`: Update a movie entirely.
        * `DELETE /id/`: Delete a movie.
        * `PATCH /id/`: Update a movie.
    
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated, UserAccessPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'imdb_score', 'popularity', 'director__name', 'genre__name',)
    ordering_fields = ('name', )
