from users.serializers import UserSerializer
from .models import Parent
from users.models import Address, Contact

class ParentSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Parent
        fields = UserSerializer.Meta.fields
        read_only_fields = ['user_id']
    

    def create(self, validated_data):
        contact_data = validated_data.pop('contact')
        address_data = validated_data.pop('address')

        contact = Contact(**contact_data)
        contact.save()
        address = Address(**address_data)
        address.save()
        
        parent = Parent.objects.create(contact = contact, address = address, **validated_data)
        return parent

    def update(self, instance, validated_data):
        contact_data = validated_data.pop('contact', None)
        address_data = validated_data.pop('address', None)

        if contact_data:
            for attr, value in contact_data.items():
                setattr(instance.contact, attr, value)
            instance.contact.save()

        if address_data:
            for attr, value in address_data.items():
                setattr(instance.address, attr, value)
            instance.address.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance