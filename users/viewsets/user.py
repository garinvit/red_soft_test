from rest_framework import mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance)

        data = serializer.data

        if request.user == instance:
            refresh = RefreshToken.for_user(request.user)
            data['access'] = str(refresh.access_token)
            data['refresh'] = str(refresh)

        return Response(data)

    def update(self, request, *args, **kwargs):
        user = self.get_object()

        if user != request.user:
            raise PermissionDenied("Можно редактировать только свой профиль")

        return super().update(request, *args, **kwargs)
