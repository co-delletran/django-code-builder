import json
from django.http import HttpResponse
from django.shortcuts import render

# Generate model code


def generate_models(json_data):
    models_code = []

    for model in json_data['models']:
        model_name = model['model_name']
        fields_code = []

        for field in model['fields']:
            field_type = field['type']
            field_name = field['name']

            if field_type == "ForeignKey":
                related_model = field['related_model']
                on_delete = field['on_delete']
                fields_code.append(
                    f"{field_name} = models.{field_type}('{related_model}', on_delete=models.{on_delete})")
            else:
                field_params = ", ".join(
                    [f"{key}={value}" for key, value in field.items() if key != 'name' and key != 'type'])
                fields_code.append(
                    f"{field_name} = models.{field_type}({field_params})")

        model_code = f"class {model_name}(models.Model):\n    " + \
            "\n    ".join(fields_code) + "\n"
        models_code.append(model_code)

    return "\n".join(models_code)

# Generate serializer code


def generate_serializers(json_data):
    serializers_code = []

    for model in json_data['models']:
        model_name = model['model_name']
        serializer_code = f"class {model_name}Serializer(serializers.ModelSerializer):\n"
        serializer_code += f"    class Meta:\n"
        serializer_code += f"        model = {model_name}\n"
        serializer_code += f"        fields = '__all__'\n"
        serializers_code.append(serializer_code)

    return "\n".join(serializers_code)

# Generate views code


def generate_views(json_data):
    views_code = []

    for model in json_data['models']:
        model_name = model['model_name']
        view_code = f"class {model_name}ListCreateAPIView(generics.ListCreateAPIView):\n"
        view_code += f"    queryset = {model_name}.objects.all()\n"
        view_code += f"    serializer_class = {model_name}Serializer\n\n"

        view_code += f"class {model_name}RetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):\n"
        view_code += f"    queryset = {model_name}.objects.all()\n"
        view_code += f"    serializer_class = {model_name}Serializer\n"

        views_code.append(view_code)

    return "\n\n".join(views_code)

# Main view for handling the generation


def codegen_view(request):
    if request.method == 'POST':
        json_input = request.POST.get('json_input')

        try:
            json_data = json.loads(json_input)

            models_code = generate_models(json_data)
            serializers_code = generate_serializers(json_data)
            views_code = generate_views(json_data)

            complete_code = f"# models.py\n\n{models_code}\n\n" \
                            f"# serializers.py\n\n{serializers_code}\n\n" \
                            f"# views.py\n\n{views_code}\n"

            return HttpResponse(complete_code, content_type="text/plain")
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON input", status=400)

    return render(request, 'generator/codegen.html')
