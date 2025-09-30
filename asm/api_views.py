from django.http import JsonResponse
from django.apps import apps

def get_chained_options(request):
    child_model_name = request.GET.get("child_model")  # e.g., 'zonemanager.District'
    parent_field = request.GET.get("parent_field")     # e.g., 'state'
    parent_id = request.GET.get("parent_id")           # selected parent ID

    if not all([child_model_name, parent_field, parent_id]):
        return JsonResponse([], safe=False)

    app_label, model_name = child_model_name.split(".")
    ChildModel = apps.get_model(app_label, model_name)
    
    queryset = ChildModel.objects.filter(**{f"{parent_field}_id": parent_id})
    data = [{"id": obj.id, "name": str(obj)} for obj in queryset]
    
    return JsonResponse(data, safe=False)
