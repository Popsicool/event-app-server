from django.shortcuts import render
from rest_framework import (generics)
from rest_framework.decorators import permission_classes
from rest_framework.filters import SearchFilter
from rest_framework import (parsers,permissions,authentication)
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from .serializers import (CreateEventSerializer, EventPictureSerializer,
                          GuestRegisterGetSerializer, InviteSerializer,
                          DonationRequestSerializer)
from .models import EventObject, EventPicture, Guests
from django.db import transaction
# Create your views here.

ALLOWABLE_PICTURE_TYPES = ['image/jpeg', 'image/jpg', 'image/png']

class CreateEvent(generics.GenericAPIView):
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateEventSerializer
    def post(self, request):
        images = request.FILES.getlist('pictures')
        verified_pictures = []
        for picture in images:
            content_type = picture.content_type
            if content_type not in ALLOWABLE_PICTURE_TYPES:
                return Response(data={"message":"picture not in proper format"}, status=status.HTTP_400_BAD_REQUEST)
            if picture.size > 8388608:
                return Response(data={"message":"picture larger than 8mb"}, status=status.HTTP_400_BAD_REQUEST)
            verified_pictures.append(picture)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                instance = serializer.save(owner=request.user)
                created_images = []
                for image in verified_pictures:
                    new_pict = EventPicture.objects.create(event = instance, image=image)
                    new_pict.save()
                    created_images.append(new_pict)
                data=serializer.data
                data['pictures'] = EventPictureSerializer(created_images, many=True)
            return Response(data=serializer.data, status=200)
        return Response(data=serializer.data, status=200)


class ModifyEvent(generics.GenericAPIView):
    serializer_class = CreateEventSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = EventObject.objects.all()
    def patch(self, request, pk):
        event = get_object_or_404(EventObject, pk=pk)
        if event.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.serializer_class(event, data=request.data, partial=True)
        serializer.save()
        return Response(data=serializer.data, status=200)
    def delete(self, request, pk):
        event = get_object_or_404(EventObject, pk=pk)
        if event.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        event.is_archieved = True
        event.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Invite(generics.GenericAPIView):
    serializer_class = InviteSerializer
    queryset = EventObject.objects.all()
    def get(self, request, slug):
        event = get_object_or_404(EventObject, slug=slug)
        serializer = self.serializer_class(event)
        return Response(data =serializer.data, status=200)

class Register(generics.GenericAPIView):
    serializer_class = GuestRegisterGetSerializer
    def post(self, request, slug):
        event = get_object_or_404(EventObject, slug=slug)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        phone = serializer.validated_data.get('phone')
        if Guests.objects.filter(event=event, email=email).exists():
            return Response(data={"message":"User with this email already registered for this event"}, status=status.HTTP_400_BAD_REQUEST)
        if Guests.objects.filter(event=event, phone=phone).exists():
            return Response(data={"message":"User with this phone number already registered for this event"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(event=event)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
class Donation(generics.GenericAPIView):
    serializer_class = DonationRequestSerializer
    def post(self, request, slug):
        event = get_object_or_404(EventObject, slug=slug)
        data = request.data
        email = data.get("email")
        serializer = self.serializer_class(data = data)
        serializer.is_valid(raise_exception=True)
        res = serializer.data
        donations = serializer.validated_data['donations']
        event_items = event.list_of_items
        result_dict = {item['name']: item['price'] for item in event.list_of_items}
        total_amount = 0
        for i in donations:
            item = i["item"]
            quantity = i['quantity']
            if item not in result_dict.keys():
                continue
            amt = result_dict[item]  * quantity
            total_amount += amt
        # proceed to pay stack with user details
        return Response(data={"message": "ok"}, status=status.HTTP_200_OK)
        