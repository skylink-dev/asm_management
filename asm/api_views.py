from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import ASMDailyTarget, ZMDailyTarget
from asm.models import ASM
from .serializers import (
    ASMDailyTargetSerializer,
    ASMDailyTargetListSerializer
)
#zm set value for asm
class ASMTargetsListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Get ASM profile
        try:
            asm = ASM.objects.get(user=user)
        except ASM.DoesNotExist:
            return Response({"status": "error", "message": "ASM profile not found."}, status=404)

        # Filter by date if provided
        date = request.query_params.get("date")
        targets = ZMDailyTarget.objects.filter(asm=asm)
        if date:
            targets = targets.filter(date=date)

        serializer = ASMDailyTargetSerializer(targets, many=True)
        return Response({"status": "success", "data": serializer.data})


# asm set values
class ASMSetTargetAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ASMDailyTargetSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            instance = serializer.save()
            return Response({
                "status": "success",
                "data": ASMDailyTargetSerializer(instance).data
            }, status=201)
        else:
            first_error = list(serializer.errors.values())[0]
            if isinstance(first_error, list):
                first_error = first_error[0]
            return Response({"status": "error", "message": first_error}, status=400)
        
# Asm list value 
from django.utils.dateparse import parse_date

class ASMDailyTargetAchievementListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Ensure ASM profile
        try:
            asm = ASM.objects.get(user=user)
        except ASM.DoesNotExist:
            return Response({
                "status": "error",
                "message": "ASM profile not found."
            }, status=404)

        # Get date range params
        start_date = request.query_params.get("start_date")  # YYYY-MM-DD
        end_date = request.query_params.get("end_date")      # YYYY-MM-DD

        filters = {"asm": asm}

        if start_date:
            start_date = parse_date(start_date)
            if start_date:
                filters["date__gte"] = start_date

        if end_date:
            end_date = parse_date(end_date)
            if end_date:
                filters["date__lte"] = end_date

        queryset = ASMDailyTarget.objects.filter(**filters).order_by("-date")
        serializer = ASMDailyTargetListSerializer(queryset, many=True)

        return Response({
            "status": "success",
            "count": len(serializer.data),
            "data": serializer.data
        })


