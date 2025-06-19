from staffs.serializers import StaffSerializer
from .models import Teacher

class TeacherSerializer(StaffSerializer):
    class Meta(StaffSerializer.Meta):
        model = Teacher
        fields = StaffSerializer.Meta.fields + [
            'specialization',
            'class_assigned',
            'home_room'
        ]
        read_only_fields = StaffSerializer.Meta.read_only_fields
    def create(self, validated_data):
        class_assigned = validated_data.pop('class_assigned', None) 
        home_room = validated_data.pop('home_room', None)

        teacher = super().create(validated_data)

        if class_assigned:
            teacher.class_assigned.set(class_assigned)
        if home_room:
            teacher.home_room.set(home_room)

        return teacher
    

    def update(self, instance, validated_data):
        class_assigned = validated_data.pop('class_assigned', None)
        home_room = validated_data.pop('home_room', None)  

        instance = super().update(instance, validated_data) 

        if class_assigned is not None:
            instance.class_assigned.set(class_assigned)

        if home_room is not None:
            instance.home_room.set(home_room)
    
        return instance 