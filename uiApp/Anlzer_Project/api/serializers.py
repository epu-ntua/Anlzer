__author__ = 'mpetyx'

from django.contrib.auth.models import Group
from rest_framework import serializers

from api.models import  Project, User #, Team


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


# class TeamSerializer(serializers.HyperlinkedModelSerializer):
#     created_by = UserSerializer()
#
#     class Meta:
#         model = Team
#         fields = ('url', 'name', 'created_by', 'created')


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    # owned_by = serializers.HyperlinkedRelatedField(many=True, view_name='user', read_only=True)

    # owned_by = TeamSerializer()
    user = UserSerializer()

    class Meta:
        model = Project
        fields = ('url', 'description', 'title', 'pages', 'hashtags', 'user', 'created_on')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
