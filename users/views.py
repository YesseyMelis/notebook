import json

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from openpyxl.writer.excel import save_virtual_workbook
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.models import User
from users.producer import publish, UserInfoRpcClient
from users.serializers import UserSerializer, UserUpdateSerializer
from users.services import UserService


class UserViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    model = get_user_model()
    permission_classes = [AllowAny,]
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'update':
            return UserUpdateSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # publish -------------
        serializer.validated_data['id'] = serializer.data['id']
        del serializer.validated_data['login']
        del serializer.validated_data['password']
        publish('user_created', serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer.validated_data['id'] = instance.id
        # publish ---------------
        publish('user_updated', serializer.validated_data)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(methods=['GET'], detail=False, permission_classes=(IsAuthenticated, ))
    def users_info(self, request, *args, **kwargs):
        info_rpc = UserInfoRpcClient()
        response = info_rpc.call()
        print(json.loads(response))
        return Response(json.loads(response))

    @action(methods=['GET'], detail=False)
    def download_excel(self, request, *args, **kwargs):
        info_rpc = UserInfoRpcClient()
        response = info_rpc.call()
        print(json.loads(response))
        stock_service = UserService()
        workbook = stock_service.download_user_info(data=json.loads(response))
        response = HttpResponse(
            content=save_virtual_workbook(workbook),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=user_info.xlsx'
        return response
