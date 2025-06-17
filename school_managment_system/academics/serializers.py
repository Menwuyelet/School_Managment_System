from rest_framework import serializers
from .models import Subject, Schedule, Classes, Grade, History

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['subject_id', 'subject_name', 'teachers']
    
    def create(self, validated_data):
        return Subject.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        teachers_data = validated_data.pop('teachers')

        if teachers_data:
            for attr, value in teachers_data.items():
                setattr(instance.teachers, attr, value)
            instance.teachers.save()
        
        if validated_data:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
        return instance
    

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['schedule_id', 'details']

    def create(self, validated_data):
        return Schedule.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        if validated_data:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
        return instance

class ClassesSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many = True)
    schedule = ScheduleSerializer()

    class Meta:
        model = Classes
        fields = ['class_id', 'class_name', 'academic_year', 'subjects', 'schedule']

    def create(self, validated_data):
        subject_data = validated_data.pop('subjects')
        schedule_data = validated_data.pop('schedule')


        schedule = Schedule.objects.create(**schedule_data)

        classes = Classes.objects.create(schedule = schedule, **validated_data)

        subject_instances = []
        for subject_dict in subject_data:
            subject_id = subject_dict.get('subject_id')
            if subject_id:
                try:
                    subject = Subject.objects.get(subject_id = subject_id)
                    subject_instances.append(subject)
                except Subject.DoesNotExist:
                    raise serializers.ValidationError(f"Subject with id {subject_id} not found.")
            else:
                raise serializers.ValidationError(f"create the subject first before assigning it to a class.")
        classes.subjects.set(subject_instances)
        return classes
    
    def update(self, instance, validated_data):
        subject_data = validated_data.pop('subjects')
        schedule_data = validated_data.pop('schedule')

        if schedule_data:
            for attr, value in schedule_data.items():
                setattr(instance.schedule, attr, value)
            instance.schedule.save()

        if subject_data:
            subject_instances = []
            for subject_dict in subject_data:
                subject_id = subject_dict.get('subject_id')
                if subject_id:
                    try:
                        subject = Subject.objects.get(subject_id=subject_id)
                        subject_instances.append(subject)
                    except Subject.DoesNotExist:
                        raise serializers.ValidationError(f"Subject with id {subject_id} not found.")
            instance.subjects.set(subject_instances)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
