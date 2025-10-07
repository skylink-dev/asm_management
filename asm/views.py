from dal import autocomplete
from zonemanager.models import ZoneManager
from django.contrib.auth.models import User, Group


# views.py
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from .models import ASM
from .serializers import ASMUserSerializer, UserSerializer,ASMSerializer,ASMSerializerByZonalManager
from .permissions import IsAdminUser, IsASMUser, IsOwnerOrAdmin, IsAdminAPI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ASMLoginSerializer

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError



class ZoneManagerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ZoneManager.objects.all()
        if self.q:
            qs = qs.filter(user__username__icontains=self.q)
        return qs

# Optional: You can reuse your existing district & office autocomplete views


class ASMViewSet(ModelViewSet):
    queryset = ASM.objects.all()
    serializer_class = ASMUserSerializer

    def get_permissions(self):
        """
        Assign permissions based on action:
        - List: Admin only
        - Retrieve: Owner or Admin
        - Create: Admin only (or allow registration via different endpoint)
        - Update: Owner or Admin
        - Delete: Admin only
        """
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        elif self.action == 'create':
            permission_classes = [IsAdminUser]  # Or [permissions.AllowAny] for registration
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [IsOwnerOrAdmin]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]  # ✅ CORRECT: uses imported permissions module

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Filter queryset based on user role:
        - Admin users see all ASM records
        - ASM users only see their own record
        """
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return ASM.objects.all()

        try:
            asm_profile = ASM.objects.get(user=user)
            return ASM.objects.filter(id=asm_profile.id)
        except ASM.DoesNotExist:
            return ASM.objects.none()

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's ASM profile - allowed for all authenticated ASM users"""
        try:
            asm = ASM.objects.get(user=request.user)
            serializer = self.get_serializer(asm)
            return Response({
                'success': True,
                'data': serializer.data
            })
        except ASM.DoesNotExist:
            return Response({
                'success': False,
                'error': 'ASM profile not found'
            }, status=status.HTTP_404_NOT_FOUND)


# Example of a view that only admins can access
class AdminOnlyViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    # ... your admin-only view logic


# Example of a view that both admins and ASM users can access
class SharedAccessViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]  # ✅ CORRECT: uses imported permissions module
        return [permission() for permission in permission_classes]




class ASMLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ASMLoginSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']
            asm_profile = serializer.validated_data['asm']

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Prepare response
            response = Response({
                'success': True,
                'message': 'Login successful',
                'data': {
                    'user': user.username,
                    'asm_code': asm_profile.code,
                }
            }, status=status.HTTP_200_OK)

            # ✅ Set refresh token in HttpOnly cookie
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,       # JS cannot access
                secure=False,        # set True in production with HTTPS
                samesite="Lax",      # or "Strict" / "None" depending on frontend
                max_age=7*24*60*60   # 7 days
            )

            # ✅ Send access token in header
            response["Authorization"] = f"Bearer {access_token}"

            return response

        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"detail": "Refresh token missing"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            response = Response({
                "success": True,
                "access": access_token
            }, status=status.HTTP_200_OK)

            # Optional: reset the refresh token with new expiry
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=False,     # 🔒 change to True in production
                samesite="Lax",
                max_age=7*24*60*60
            )

            # Return new access token also in header
            response["Authorization"] = f"Bearer {access_token}"

            return response
        except TokenError:
            return Response({"detail": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        response = Response({"success": True}, status=status.HTTP_200_OK)
        response.delete_cookie("refresh_token")
        return response


class UserListView(APIView):
    permission_classes = [permissions.IsAuthenticated,IsAdminAPI]
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        response = Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        return response



class GetASMBasedOnZonalManager(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        response = Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        return response


class ASMByZoneManagerAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user  # Logged-in user
        try:
            # Get the ZoneManager associated with this user
            zonemanager = ZoneManager.objects.get(user=user)
        except ZoneManager.DoesNotExist:
            return Response({
                "success":False,
                "detail": "ZoneManager not found for this user."}, status=status.HTTP_404_NOT_FOUND)
        # Get all ASMs linked to this ZoneManager
        asms = ASM.objects.filter(zone_manager=zonemanager)
        serializer = ASMSerializerByZonalManager(asms, many=True)
        data = []
        for asmdata in serializer.data:

            data.append({
                "id": asmdata["id"],
                "user_id": asmdata["user"]["id"],
                "user_name": asmdata["user"]["username"],
                "email":asmdata["user"]["email"],
                "full_name":asmdata["user"]["first_name"]+" "+asmdata["user"]["last_name"],
                "role":asmdata["group"]["name"],
                "state":asmdata["states"],
                "districts":asmdata["districts"],
                "offices":asmdata["offices"],
            })

        response = Response({
            "success": True,
            "data": data
        }, status=status.HTTP_200_OK)
        return response
        return Response(serializer.data)



# from rest_framework import generics, status
# from rest_framework.response import Response
# from .models import ASMDailyTarget
# from .serializers import ASMDailyTargetSerializer
#
#
# class ASMDailyTargetCreateAPIView(generics.CreateAPIView):
#     queryset = ASMDailyTarget.objects.all()
#     serializer_class = ASMDailyTargetSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#
#         return Response({
#             "status": "success",
#             "message": "ASM Daily Target created successfully",
#             "data": serializer.data
#         }, status=status.HTTP_201_CREATED)