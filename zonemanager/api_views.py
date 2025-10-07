
from rest_framework.views import APIView
from rest_framework import status

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ZMDailyTarget, ZoneManager
from asm.models import ASM
from .serializers import ZMDailyTargetSerializer, ZoneManagerSerializer
from django.utils.dateparse import parse_date

from django.db import IntegrityError


class ZMDailyTargetCreateAPIView(APIView):
    def post(self, request):
        user = request.user

        # Get ZoneManager for logged-in user
        try:
            zonemanager = ZoneManager.objects.get(user=user)
        except ZoneManager.DoesNotExist:
            return Response({
                "status": "error",
                "message": "ZoneManager not found for this user."
            }, status=status.HTTP_404_NOT_FOUND)

        # Get ASM from request and validate belongs to this ZoneManager
        asm_id = request.data.get("asm_id")
        try:
            asm = ASM.objects.get(id=asm_id, zone_manager=zonemanager)
        except ASM.DoesNotExist:
            return Response({
                "status": "error",
                "message": "ASM not found under your ZoneManager."
            }, status=status.HTTP_404_NOT_FOUND)

        # Set zone_manager_id automatically
        request.data['zone_manager_id'] = zonemanager.id

        serializer = ZMDailyTargetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({
                    "status": "success",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            except IntegrityError:
                # Catch any DB-level unique_together violation
                return Response({
                    "status": "error",
                    "message": "A target for this ZoneManager, ASM, and date already exists."
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Simplified error format
            first_error = list(serializer.errors.values())[0]
            if isinstance(first_error, list):
                first_error = first_error[0]  # Get first message from the list

            return Response({
                "status": "error",
                "message": first_error
            }, status=status.HTTP_400_BAD_REQUEST)




class ZMDailyTargetListAPIView(generics.ListAPIView):
    serializer_class = ZMDailyTargetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ZMDailyTarget.objects.all()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            start_date = parse_date(start_date)
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            end_date = parse_date(end_date)
            queryset = queryset.filter(date__lte=end_date)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # data=[]
        # for dailytarget from serializer.data:
        #     tempZoneManagerSerializer = ZoneManagerSerializer(data=dailytarget["zone_manager"])
        #     if temp
        #     resp={
        #
        #     }

        # zoneManager = ZoneManagerSerializer(id=serializer.data['zone_manager']["id"])
        return Response({
            "status": "success",
            "data": serializer.data
        })
