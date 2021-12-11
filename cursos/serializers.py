from rest_framework import serializers
from django.db.models import Avg

from .models import Curso, Avaliacao


class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            # somente na hora do input, não permite consulta pois é um campo sensível
            'email': {'write_only': True}
        }
        model = Avaliacao
        fields = (
            'id',
            'curso',
            'nome',
            'email',
            'comentario',
            'avaliacao',
            'criacao',
            'ativo'
        )

    # validate_<field>
    def validate_avaliacao(self, valor):
        if valor in range(1,6):
            return valor
        raise serializers.ValidationError('A avaliação precisa ser um inteiro entre 1 a 5')


class CursoSerializer(serializers.ModelSerializer):
    # Nested Relationship - all information inside a list
    # WARNING: if the quantity are too big, maybe its not a good use (DB Relationships)
    # avaliacoes = AvaliacaoSerializer(many=True, read_only=True)

    # Hyperlinked Related Field - Transforms the nested relationships in hyperlinks
    """
    avaliacoes = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='avaliacao-detail'
    )
    """
    # Primary Key related Field - Just the ID number
    avaliacoes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    media_avaliacoes = serializers.SerializerMethodField()  # Gonna be generated by a function

    class Meta:
        model = Curso
        fields = (
            'id',
            'titulo',
            'url',
            'criacao',
            'ativo',
            'avaliacoes',
            'media_avaliacoes'
        )

    # Get_<field> | This block could be done on models, here will calculate everytime, dropping performance
    def get_media_avaliacoes(self, obj):
        # obj is curso, and avaliacoes is the class model, and do the average
        media = obj.avaliacoes.aggregate(Avg('avaliacao')).get('avaliacao__avg')

        if media is None:
            return 0
        # this makes always be something .5
        return round(media * 2)/2
