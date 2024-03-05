from rest_framework import generics, permissions,mixins,status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from . import models, serializers


class PostList(generics.ListCreateAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    gueryset =models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def delete(self, request, *args, **kwargs):
        post = models.Post.objects.filter(
            pk=kwargs['pk'], user=self.request.user
        )
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_("You can only delete your own content."))
        

    def put(self, request, *args, **kwargs):
        post = models.Post.objects.filter(
            pk=kwargs['pk'], user=self.request.user
        )
        if post.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_("You can only edit your own content"))


class CommentList(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, post=post)

    def get_queryset(self):
        queryset = super().get_queryset()
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        return queryset.filter(post=post)   


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        comment = models.Comment.objects.filter(
            pk=kwargs['pk'], user=self.request.user
        )
        if comment.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_("You can only delete your own content"))
        
    def put(self, request, *args, **kwargs):
        comment = models.Comment.objects.filter(
            pk=kwargs['pk'], user=self.request.user
        )
        if comment.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_("You can only edit your content"))
        

class PostLike(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = serializers.PostLikeserializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = models.PostLike.objects.all()
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        return queryset.filter(post=post, user=self.request.user)
    
    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError(_("You olready like this"))
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(post=post, user=self.request.user)

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError(_("You must already like this to unlike this"))   


class CommentLike(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = serializers.CommentLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = models.CommentLike.objects.all()
        comment = models.Comment.objects.get(pk=self.kwargs['pk'])
        return queryset.filter(comment=comment, user=self.request.user)
    
    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError(_("You already like this"))
        comment = models.Comment.objects.get(pk=self.kwargs['pk'])
        serializer.save(comment=comment, user=self.request.user)

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            queryset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError(_("You must already like this to unlike this"))

            


