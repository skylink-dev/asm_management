
from rest_framework.views import APIView
from rest_framework import status

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ZMDailyTarget
from .serializers import ZMDailyTargetSerializer, ZoneManagerSerializer
from django.utils.dateparse import parse_date



class ZMDailyTargetCreateAPIView(APIView):
    def post(self, request):
        serializer = ZMDailyTargetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "status": "error",
                "errors": serializer.errors
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
