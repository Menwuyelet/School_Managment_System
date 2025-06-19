from rest_framework import serializers
from .models import Staff, BankAccount
from users.serializers import UserSerializer
from users.models import Address, Contact

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['bank_name', 'account_number'] 


class StaffSerializer(UserSerializer):
    bank_account = BankAccountSerializer()
    class Meta(UserSerializer.Meta):
        model = Staff
        fields = UserSerializer.Meta.fields + [
            'role',
            'hiring_date',
            'salary',
            'bank_account'
        ]
        read_only_fields = ['user_id']
    
    def create(self, validated_data):
        contact = validated_data.pop('contact')
        address = validated_data.pop('address')
        bank_account_data = validated_data.pop('bank_account')
        
        contact = Contact(**contact)
        contact.save()
        address = Address(**address)
        address.save()
        bank_account = BankAccount(**bank_account_data)
        bank_account.save()

        staff = Staff.objects.create(contact = contact, address = address, bank_account = bank_account, **validated_data)

        return staff

    def update(self, instance,validated_data):
        contact_data = validated_data.pop('contact', None)
        address_data = validated_data.pop('address', None)
        bank_account_data = validated_data.pop('bank_account', None)

        if contact_data:
            for attr, value in contact_data.items():
                setattr(instance.contact, attr, value)
            instance.contact.save()
        
        if address_data:
            for attr, value in address_data.items():
                setattr(instance.address, attr, value)
            instance.address.save()

        if bank_account_data:
            for attr, value in bank_account_data.items():
                setattr(instance.bank_account, attr, value)
            instance.bank_account.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
