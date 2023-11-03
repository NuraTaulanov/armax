from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .models import Request
from .serializers import RequestSerializer


class CreateRequestView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RequestSerializer
    queryset = Request.objects.all()

class CreateTGBotRequestView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RequestSerializer
    queryset = Request.objects.all()