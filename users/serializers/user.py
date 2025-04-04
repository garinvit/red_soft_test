from rest_framework import serializers
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    mentees = serializers.SerializerMethodField()
    mentor = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), allow_null=True, required=False
    )
    mentor_username = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'email', 'mentor', 'mentor_username',  'mentees', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def get_mentees(self, obj):
        return obj.mentees.values_list('username', flat=True)

    def get_mentor_username(self, obj):
        return obj.mentor.username if obj.mentor else None

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)
        if password:
            for token in OutstandingToken.objects.filter(user=instance):
                try:
                    BlacklistedToken.objects.get_or_create(token=token)
                except:
                    pass
            instance.set_password(password)

        mentor = validated_data.get('mentor', None)
        if mentor:
            if mentor == instance:
                raise serializers.ValidationError("Нельзя быть ментором самому себе")
            instance.mentor = mentor

        for attr, value in validated_data.items():
            if attr not in ('password', 'mentor'):
                setattr(instance, attr, value)

        instance.save()
        return instance