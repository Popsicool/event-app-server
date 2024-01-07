from rest_framework import serializers
from django.utils import timezone, dateparse
from .models import EventObject, EventPicture, Guests
from django.utils.text import slugify
from random import  randint

class EventPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPicture
        fields = ['image']

class InviteSerializer(serializers.ModelSerializer):
    pictures = EventPictureSerializer(many=True, read_only=True)

    class Meta:
        model = EventObject
        fields = ['title', 'organizer_name', 'location', 'event_Date', 'event_time', 'list_of_items', 'slug', 'pictures']

class GuestRegisterGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guests
        fields = ['name','email', 'phone']

class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventObject
        fields = ['id', 'title', 'organizer_name', 'location', 'event_Date', 'event_time', 'list_of_items']
    def validate(self, attrs):
        event_date = str(attrs.get('event_Date', ''))
        valid_date = dateparse.parse_date(event_date)
        if not valid_date:
            raise serializers.ValidationError("event_Date must contain a valid date string")
        event_time = str(attrs.get('event_time', ''))
        valid_time = dateparse.parse_time(event_time)
        if not valid_time:
            raise serializers.ValidationError("event_time must contain a valid time string")

        if valid_date <= timezone.now().date():
            raise serializers.ValidationError('event_Date should be a future date')

        if valid_date > timezone.now().date() + timezone.timedelta(days=90):
            raise serializers.ValidationError('event_Date cannot be more than 3 months in the future')
        list_of_items = attrs.get("list_of_items",[])
        expected_keys = ['name', 'price']
        if len(list_of_items) >= 1:
            if not isinstance(list_of_items, list):
                raise serializers.ValidationError("Items must be a list")
            for item in list_of_items:
                if not isinstance(item, dict):
                    raise serializers.ValidationError("Items must be a list of dictionaries")
                keys = sorted(item.keys())
                if keys != expected_keys:
                    raise serializers.ValidationError(
                        "List of  items should be a map of 'name', 'price' ")
                if not isinstance(item['price'], int):
                    raise serializers.ValidationError("Price of all items must be integer only")
                if item['price'] < 1:
                    raise serializers.ValidationError("Price can not be less than 1")

        return attrs
    def create(self, validated_data):
        slug = f"{slugify(validated_data['title'])}-{validated_data['event_Date']}-{validated_data['event_time']}-{randint(0, 100)}"
        event = EventObject.objects.create(slug=slug,**validated_data)
        return event


class DonationItemSerializer(serializers.Serializer):
    item = serializers.CharField()
    quantity = serializers.IntegerField()

class DonationRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.EmailField()
    donations = DonationItemSerializer(many=True)

    def create(self, validated_data):
        # Custom logic for handling the creation of the donation record
        name = validated_data['name']
        phone = validated_data['phone']
        email = validated_data['email']
        donations_data = validated_data['donations']

        # Process the donations_data and create donation records as needed

        # Example: Creating a list of donation items
        donation_items = []
        for donation_data in donations_data:
            item = donation_data['item']
            quantity = donation_data['quantity']
            # Process the item and quantity as needed
            # Example: Create a donation item instance
            donation_item = {'item': item, 'quantity': quantity}
            donation_items.append(donation_item)

        # Example: Creating a donation record with the processed data
        donation_record = {
            'name': name,
            'email': email,
            'donations': donation_items
        }

        # Your custom logic to save the donation record to the database or perform other actions

        return donation_record

    def update(self, instance, validated_data):
        # Custom logic for handling the update of the donation record
        # This method is optional and can be implemented if needed
        pass
