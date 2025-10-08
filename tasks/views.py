from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import ASMTask
from .serializers import ASMTaskSerializer
from zonemanager.models import ZoneManager

class ASMTaskManageAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Only logged-in users can access

    def get_queryset(self, user):
        """
        Return tasks filtered based on logged-in user type:
        - Superuser: all tasks
        - Zone Manager: tasks they assigned
        - ASM: tasks assigned to them
        """
        qs = ASMTask.objects.filter(is_deleted=False) 

        if not user.is_superuser:
            if user.groups.filter(name="Zonal Manager").exists():
                # Filter tasks created by this Zone Manager
                try:
                    zm = ZoneManager.objects.get(user=user)
                    qs = qs.filter(zone_manager=zm)
                except ZoneManager.DoesNotExist:
                    qs = ASMTask.objects.none()
            elif user.groups.filter(name="Area Sales Manager").exists() and hasattr(user, "asm"):
                # ASM sees only their assigned tasks
                qs = qs.filter(asm=user.asm)
            else:
                qs = ASMTask.objects.none()

        return qs

    def get(self, request):
        """List all tasks visible to the logged-in user"""
        qs = self.get_queryset(request.user)
        serializer = ASMTaskSerializer(qs.order_by("-start_date"), many=True)
        return Response({
            "status": "success",
            "count": len(serializer.data),
            "data": serializer.data
        })

    def post(self, request):
        """Create a new task (Zone Manager only)"""
        user = request.user

        if not user.groups.filter(name="Zonal Manager").exists():
            return Response({
                "status": "error",
                "message": "Only Zone Manager can create tasks."
            }, status=status.HTTP_403_FORBIDDEN)

        zm = ZoneManager.objects.get(user=user)
        request.data['zone_manager'] = zm.id  # Assign Zone Manager automatically

        serializer = ASMTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Task created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Full update of a task (Zone Manager only)"""
        user = request.user
        if not user.groups.filter(name="Zonal Manager").exists():
            return Response({
                "status": "error",
                "message": "Only Zone Manager can edit tasks."
            }, status=status.HTTP_403_FORBIDDEN)

        task = get_object_or_404(ASMTask, pk=pk, zone_manager__user=user)
        serializer = ASMTaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Task updated successfully",
                "data": serializer.data
            })

        return Response({
            "status": "error",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """Partial update of a task (Zone Manager only)"""
        user = request.user
        if not user.groups.filter(name="Zonal Manager").exists():
            return Response({
                "status": "error",
                "message": "Only Zone Manager can edit tasks."
            }, status=status.HTTP_403_FORBIDDEN)

        task = get_object_or_404(ASMTask, pk=pk, zone_manager__user=user)
        serializer = ASMTaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Task updated successfully",
                "data": serializer.data
            })

        return Response({
            "status": "error",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk=None):
        if pk is None:
            return Response({
                "status": "error",
                "message": "Task ID required for deletion."
            }, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if not user.groups.filter(name="Zonal Manager").exists():
            return Response({
                "status": "error",
                "message": "Only Zone Manager can delete tasks."
            }, status=status.HTTP_403_FORBIDDEN)

        task = get_object_or_404(ASMTask, pk=pk, zone_manager__user=user)
        task.is_deleted = True
        task.status = "cancelled"
        task.save()

        return Response({
            "status": "success",
            "message": "Task soft deleted successfully."
        })