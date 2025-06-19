from rest_framework import serializers
from .models import Subject, Schedule, Classes, Grade, History
from students.serializers import StudentSerializer
from teachers.serializers import TeacherSerializer
from students.models import Student
from teachers.models import Teacher


class SubjectSerializer(serializers.ModelSerializer):
    teachers = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Teacher.objects.all()
    )
    class Meta:
        model = Subject
        fields = ['subject_id', 'subject_name', 'teachers']
    
    def create(self, validated_data):
        teachers = validated_data.pop('teachers', [])
        subject = Subject.objects.create(**validated_data)
        subject.teachers.set(teachers)
        return subject
    
    def update(self, instance, validated_data):
        teachers_data = validated_data.pop('teachers',  None)        
      
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if teachers_data is not None:
            instance.teachers.set(teachers_data)
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


class GradeSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())

    class Meta:
        model = Grade
        fields = ['student', 'subject', 'teacher', 'assessment_type', 'score', 'grade_id']

    def create(self, validated_data):
        return Grade.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class HistorySerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    class Meta:
        model = History
        fields = ['student', 'academic_year', 'summary', 'overall_status']

    def create(self, validated_data):
        return History.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance