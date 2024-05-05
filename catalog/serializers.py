# serializers.py
from rest_framework import serializers
from .models import SalesRecord

class SalesRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesRecord
        fields = '__all__'  # 你也可以指定需要序列化的字段
