from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    def has_permission(self, request, view):

        return view.queryset.get(pk=request.parser_context['kwargs']['pk']).owner.id == request.user.id


class IsAuthorOrModerator(IsAuthor):
    def has_permission(self, request, view):
        role = request.user.role

        return role == 'moderator' or role == 'admin' or super().has_permission(request, view)
