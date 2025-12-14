from django.shortcuts import render, redirect, get_object_or_404
from .models import Sweet
from .serializers import SweetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import Sweet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
# ===============================
# TEMPLATE-BASED VIEWS
# ===============================
class SweetViewSet(viewsets.ModelViewSet):
    queryset = Sweet.objects.all()
    serializer_class = SweetSerializer
def sweet_list_view(request):
    """List all sweets (for shop page)"""
    sweets = Sweet.objects.all()
    return render(request, 'myshop.html', {'sweets': sweets})


def add_edit_sweet_view(request, sweet_id=None):
    """
    Add or Edit Sweet
    If sweet_id is provided → edit, else → add
    """
    sweet = None
    if sweet_id:
        sweet = get_object_or_404(Sweet, id=sweet_id)

    if request.method == 'POST':
        sweet_id_val = request.POST.get('sweet_id')
        name = request.POST.get('name')
        category = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        # Basic validation
        errors = []
        if not sweet_id_val:
            errors.append('Sweet ID is required.')
        else:
            qs = Sweet.objects.filter(sweet_id=sweet_id_val)
            if sweet:
                qs = qs.exclude(pk=sweet.pk)
            if qs.exists():
                errors.append('Sweet ID already exists. Choose a unique ID.')

        try:
            price_val = float(price)
            if price_val < 0:
                errors.append('Price must be non-negative.')
        except (TypeError, ValueError):
            errors.append('Price must be a number.')

        try:
            quantity_val = int(quantity)
            if quantity_val < 0:
                errors.append('Quantity must be non-negative.')
        except (TypeError, ValueError):
            errors.append('Quantity must be an integer.')

        if errors:
            # Re-render form with errors and previously entered values
            context = {'sweet': sweet or None, 'errors': errors,
                       'form_values': {'sweet_id': sweet_id_val, 'name': name, 'category': category,
                                       'description': description, 'price': price, 'quantity': quantity}}
            return render(request, 'sweet_form.html', context)

        if sweet:
            # Edit
            sweet.sweet_id = sweet_id_val
            sweet.name = name
            sweet.category = category
            sweet.description = description
            sweet.price = price_val
            sweet.quantity = quantity_val

            # Handle photo upload (optional)
            if 'photo' in request.FILES:
                photo = request.FILES['photo']
                fs = FileSystemStorage(location=settings.MEDIA_ROOT / 'sweet_image',
                                       base_url='/media/sweet_image/')
                filename = fs.save(photo.name, photo)
                sweet.photo = f'sweet_image/{filename}'

            sweet.save()
            return redirect('sweet:list')
        else:
            # Add
            sweet = Sweet(
                sweet_id=sweet_id_val,
                name=name,
                category=category,
                description=description,
                price=price_val,
                quantity=quantity_val
            )
            sweet.created_by = request.user if request.user.is_authenticated else None

            # Handle photo upload
            if 'photo' in request.FILES:
                photo = request.FILES['photo']
                fs = FileSystemStorage(location=settings.MEDIA_ROOT / 'sweet_image',
                                       base_url='/media/sweet_image/')
                filename = fs.save(photo.name, photo)
                sweet.photo = f'sweet_image/{filename}'  # saved relative to MEDIA_ROOT

            sweet.save()
            return redirect('sweet:list')

    return render(request, 'sweet_form.html', {'sweet': sweet})




def delete_sweet_view(request, sweet_id):
    """Delete sweet"""
    sweet = get_object_or_404(Sweet, id=sweet_id)
    sweet.delete()
    return redirect('sweet:list')


def restock_sweet_view(request, sweet_id):
    """Restock sweet (via form input from staff click)"""
    sweet = get_object_or_404(Sweet, id=sweet_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        sweet.quantity += quantity
        sweet.save()
    return redirect('sweet:list')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_sweets(request):
    # Get query parameters
    name = request.GET.get('name')
    category = request.GET.get('category')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    # Start queryset
    sweets = Sweet.objects.all()

    # Filter by name
    if name:
        sweets = sweets.filter(name__icontains=name)

    # Filter by category
    if category:
        sweets = sweets.filter(category__icontains=category)

    # Filter by price range
    if price_min:
        sweets = sweets.filter(price__gte=price_min)
    if price_max:
        sweets = sweets.filter(price__lte=price_max)

    serializer = SweetSerializer(sweets, many=True)
    return Response({
        'success': True,
        'results': serializer.data
    })

# ===============================
# API VIEWS
# ===============================

class SweetListAPI(APIView):
    """GET all sweets"""
    def get(self, request):
        sweets = Sweet.objects.all()
        serializer = SweetSerializer(sweets, many=True)
        return Response(serializer.data)


class SweetSearchAPI(APIView):
    """GET search sweets"""
    def get(self, request):
        query = request.GET.get('q', '')
        sweets = Sweet.objects.filter(name__icontains=query)
        serializer = SweetSerializer(sweets, many=True)
        return Response(serializer.data)


class SweetCreateAPI(APIView):
    """POST new sweet (Admin only)"""
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = SweetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({"message": "Sweet added successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SweetUpdateAPI(APIView):
    """PUT update sweet (Admin only)"""
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        sweet = get_object_or_404(Sweet, pk=pk)
        serializer = SweetSerializer(sweet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Sweet updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SweetDeleteAPI(APIView):
    """DELETE sweet (Admin only)"""
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        sweet = get_object_or_404(Sweet, pk=pk)
        sweet.delete()
        return Response({"message": "Sweet deleted successfully"})


class SweetPurchaseAPI(APIView):
    """POST purchase sweet (Authenticated users)"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        sweet = get_object_or_404(Sweet, pk=pk)
        quantity = int(request.data.get('quantity', 1))
        if quantity <= 0:
            return Response({"error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)
        if sweet.quantity < quantity:
            return Response({"error": "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST)
        sweet.quantity -= quantity
        sweet.save()
        return Response({"message": f"Purchased {quantity} {sweet.name}(s) successfully"})


class SweetRestockAPI(APIView):
    """POST restock sweet (Admin only)"""
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        sweet = get_object_or_404(Sweet, pk=pk)
        quantity = int(request.data.get('quantity', 0))
        if quantity <= 0:
            return Response({"error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)
        sweet.quantity += quantity
        sweet.save()
        return Response({"message": f"{sweet.name} restocked by {quantity}"})
