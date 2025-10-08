# views.py
from rest_framework import generics, permissions
from .models import SDCollection
from .serializer import SDCollectionSerializer
from zonemanager.models import ZoneManager

class SDCollectionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = SDCollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = SDCollection.objects.filter(is_deleted=False)

        if user.is_superuser:
            return qs
        elif user.groups.filter(name="Zonal Manager").exists():
            try:
                zm = ZoneManager.objects.get(user=user)
                return qs.filter(zone_manager=zm)
            except ZoneManager.DoesNotExist:
                return SDCollection.objects.none()
        elif user.groups.filter(name="Area Sales Manager").exists() and hasattr(user, "asm"):
            return qs.filter(asm=user.asm)
        else:
            return SDCollection.objects.none()
        
        
class SDCollectionRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = SDCollectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = SDCollection.objects.filter(is_deleted=False)
