from .models import User
import rest_framework.serializers as serializers

class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid', 'first_name', 'last_name', 'email', 'role', 'created_at', 'updated_at']
        extra_kwargs = {
            'uuid': { 'read_only': True },
            'created_at': { 'read_only': True },
            'updated_at': { 'read_only': True },
        }

class UpdateUserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid', 'role']

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid', 'first_name', 'last_name', 'username', 'email', 'password']
        extra_kwargs = {
            'uuid': { 'read_only': True },
            'password': { 'write_only': True }
        }

    def create(self, validated_data):
        '''
        Overriding the default 'create' implementation to ensure 'set_password' sets encrypted 
        password onto the database
        '''
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()