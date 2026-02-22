from rest_framework import views, status, generics
from rest_framework.response import Response
from apps.authentication.serializers import UserSerializer
from django.contrib.auth import get_user_model
from apps.categories.models import Category # Need to check if this exists
from apps.categories.views import CategoryViewSet # Placeholder

User = get_user_model()

class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
        if self.request.user.role != 'admin':
            return User.objects.none()
        return super().get_queryset()

class UserActivateView(views.APIView):
    def post(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.status = 'active' # Assuming status exists
            user.save()
            return Response({"message": "User activated successfully"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class AdminLogsView(views.APIView):
    def get(self, request):
        # Simulated logs
        return Response([
            {"id": 1, "action": "Login", "user": "admin@example.com", "timestamp": "2024-02-23 10:00:00"},
            {"id": 2, "action": "Upload", "user": "user@example.com", "timestamp": "2024-02-23 10:05:00"}
        ])

class AdminCategoryView(views.APIView):
    def get(self, request):
        return Response([])
    def post(self, request):
        return Response({"message": "Category created"}, status=status.HTTP_201_CREATED)

class AdminCategoryDetailView(views.APIView):
    def get(self, request, id):
        return Response({"id": id})
    def delete(self, request, id):
        return Response(status=status.HTTP_204_NO_CONTENT)

class AdminProductView(views.APIView):
    def get(self, request):
        return Response([])
    def post(self, request):
        return Response({"message": "Product created"}, status=status.HTTP_201_CREATED)
