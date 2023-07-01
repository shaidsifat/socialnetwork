from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Comment, Connection,CustomUser, Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
    #username = serializers.CharField(max_length=150)
    #password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    #email = serializers.EmailField()
        model = CustomUser
        fields = ('username', 'email')
    '''
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user
    '''

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username','email',)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
       
        instance.save()
        return instance
    
class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'image', 'created_at']

    def create(self, validated_data):
        author = self.context['author']
        post = Post.objects.create(author=author, **validated_data)
        return post
    '''
    def create(self, validated_data):
        user = self.context['request'].user
        post = Post.objects.create(createduser=user, **validated_data)
        return post
    '''
class  CommentSerializer(serializers.ModelSerializer):
    
    post = serializers.ReadOnlyField(source='comment.post')
    class Meta:
        model = Comment
        fields = '__all__'
    def create(self, validated_data):
        post = self.context['post']
        comment = Comment.objects.create(post=post, **validated_data)
        return f"{comment}"

class ConnectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Connection
        fields = '__all__'
