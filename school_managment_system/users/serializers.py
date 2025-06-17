from rest_framework import serializers
from .models import User, Contact, Address


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['contact_id', 'email', 'phone']
        read_only_fields = ['contact_id']
        
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address_id', 'city', 'kebele', 'home_number', 'postal_number']
        read_only_fields = ['address_id']

class UserSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    address = AddressSerializer()
    
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'date_of_birth', 'contact', 'address', 'gender']

