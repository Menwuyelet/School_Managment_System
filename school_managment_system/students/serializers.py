from rest_framework import serializers
from .models import Student, StudentPayment
from users.serializers import UserSerializer
from parents.models import Parent
from parents.serializers import ParentSerializer
from users.models import Address, Contact

class StudentSerializer(UserSerializer):
    parents = ParentSerializer(many = True)
    class Meta(UserSerializer.Meta):
        model = Student
        fields = UserSerializer.Meta.fields + ['enrollment_date', 'class_assigned', 'parents']
        read_only_fields = ['user_id']

    def create(self, validated_data):
        contact_data = validated_data.pop('contact')
        address_data = validated_data.pop('address')
        parent_data = validated_data.pop('parents')

        contact = Contact(**contact_data)
        contact.save()
        address = Address(**address_data)
        address.save()

        student = Student.objects.create(contact = contact, address = address, **validated_data)

        parent_instances = []
        for parent_dict in parent_data:
            parent_id = parent_dict.get('user_id') 
            if parent_id:
                # Existing parent
                try:
                    parent = Parent.objects.get(user_id = parent_id)
                    parent_instances.append(parent)
                except Parent.DoesNotExist:
                    raise serializers.ValidationError(f"Parent with ID {parent_id} not found.")
            else:
                # New parent: create from nested data
                parent_serializer = ParentSerializer(data = parent_dict)
                parent_serializer.is_valid(raise_exception = True)
                parent = parent_serializer.save()
                parent_instances.append(parent)

        student.parents.set(parent_instances)
        return student
    
    def update(self, instance, validated_data):
        contact_data = validated_data.pop('contact', None)
        address_data = validated_data.pop('address', None)
        parent_data = validated_data.pop('parents', None)

        if contact_data:
            for attr, value in contact_data.items():
                setattr(instance.contact, attr, value)
            instance.contact.save()
        
        if address_data:
            for attr, value in address_data.items():
                setattr(instance.contact, attr, value)
            instance.address.save()
        
        if parent_data:
            for attr, value in parent_data.items():
                setattr(instance.parents, attr, value)
            instance.parents.save()
        
        if validated_data:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
        return instance
    
class StudentPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentPayment
        fields = ['payment_code','student', 'name', 'description', 'amount', 'payment_date', 'payment_method']
        read_only_fields = ['payment_code']

    def create(self, validated_data):
        return StudentPayment.objects.create(**validated_data)
    

