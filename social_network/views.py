from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import CommentSerializer, ConnectionSerializer,  PostSerializer, UserProfileSerializer, UserSerializer
from .models import Connection, CustomUser, Profile, Post
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken



@api_view(['POST'])
def token_user(request):
    # Your login logic here

    # Generate token pair
    user=CustomUser.objects.get(email=request.data['email'])
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
    })
class register_user(APIView):
    
    def post(self,request,format=None):
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']

            # Create a new user
            user = CustomUser.objects.create_user(username=username, password=password, email=email)
            user.save()

            # Return success response
            return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)

        # Return error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({'message': 'User logged in successfully.'}, status=status.HTTP_200_OK)
    
    return Response({'message': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    # Handle viewing and updating user profile here
    user = request.user

    if request.method == 'GET':
        if request.user.username==None:
            return Response({"message":"No username found"})
        data = CustomUser.objects.filter(id=request.user.id).values('id','email','username','is_active','is_staff','is_superuser')
        
        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    
    serializer = PostSerializer(data=request.data, context={'author': request.user})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def view_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PostSerializer(post)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    # Handle post liking here
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    post.likes.add(request.user)
    post.save()

    return Response({'message': 'Post liked successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_on_post(request, post_id):
    # Handle post commenting here
    try:
        print(post_id)
        post = Post.objects.get(id=post_id)
        
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CommentSerializer(data=request.data,context={'post':post})

    if serializer.is_valid():
        serializer.save(user=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share_post(request, post_id):
    # Handle post sharing here
    try:
        original_post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    # Create a new post based on the original post
    shared_post = Post.objects.create(
        user=request.user,
        text=f"Shared: {original_post.text}",
        image=original_post.image,
        # Copy other relevant fields as needed
    )

    return Response({'message': 'Post shared successfully'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def search_posts(request):
    # Handle post search by keyword here
    keyword = request.GET.get('keyword', '')

    # Search posts by keyword
    posts = Post.objects.filter(content__icontains=keyword)

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_connections(request):
    # Handle user connections and connection management here
 
    user = request.user

    # Retrieve the connections of the user
    connections = Connection.objects.filter(currentuser=user)

    serializer = ConnectionSerializer(connections, many=True)
    return Response(serializer.data)