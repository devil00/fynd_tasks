from .models import Movie, Director, Genre
from rest_framework import serializers


class DirectorSerialzer(serializers.ModelSerializer):
    """
    Serializer for a director model. The need of this serializer arises because director
    has one to many relationship with movie model and it may have different fields so a different approach for 
    serializing and deserializing data may require.
    """
    class Meta:
        model = Director()
        fields = ('name',)


class GenreField(serializers.Field):
    """
    Serializer field for genre field in the movie model.
    The need arises because genre holds many to one relationship which may need different approach for serializing and
    deserializing data.
    Also, some methods are implemented to allow ease in serialization and deserialization.
    """
    def to_representation(self, obj):
        return [g.name for g in obj.all()]

    def to_internal_value(self, data):
        return data


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for a movie model responsible for handling serialization and deserialization of model. It also defines 
    the implementation of action methods update/create which are triggered by put/post handlers respectively..
    """
    genre = GenreField()
    director = DirectorSerialzer()

    class Meta:
        model = Movie
        fields = ('name', 'score', 'popularity', 'genre', 'director', 'id')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """
        This method is triggered on a post request after successful validation. It is responsbile for saving a movie.
        :param validated_data: validated data obtained from incoming request.
        :type validated_data: dict
        :returns: newly created movie instance which will later be rendered as a json.
        """
        genres = validated_data.pop('genre')
        director = validated_data.pop('director')['name']
        
        # create director instance.
        created_director = Director.objects.create(name=director)
        validated_data.update({'director': created_director})

        created_genres = []
        
        # Create genre instances.
        for genre in genres:
            created_genre = Genre.objects.create(name=genre)
            created_genres.append(created_genre)

        movie = Movie.objects.create(**validated_data)

        if movie:
            [movie.genre.add(genre) for genre in created_genres]

        movie.save()

        return movie

    def update(self, instance, validated_data):
        """
        This method is triggered on PUT/PATCH request after successful validation.
        It is responsbile for updating a specific movie identified
        by its id.
        :param instance: Movie instance obtained from a given id.
        :type instance: An instance of a `movies_api.models.Movie`.
        :param validated_data: validated data obtained from incoming request.
        :type validated_data: dict
        :returns: an updated movie instance.
        """
        genres = validated_data.pop('genre')
        director = validated_data.pop('director')['name']

        for g in genres:
            instance.genre.update_or_create(name=g)

        instance.director.name = director
        instance.score = validated_data.get('score')
        instance.name = validated_data.get('name')
        instance.popularity = validated_data.get('popularity')

        instance.save()

        return instance

