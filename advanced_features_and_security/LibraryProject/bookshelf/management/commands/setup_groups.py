from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book, Library


class Command(BaseCommand):
    help = 'Creates default groups and assigns permissions'

    def handle(self, *args, **options):
        # Get content types for our models
        book_content_type = ContentType.objects.get_for_model(Book)
        library_content_type = ContentType.objects.get_for_model(Library)

        # Get all permissions for our models
        book_permissions = Permission.objects.filter(content_type=book_content_type)
        library_permissions = Permission.objects.filter(content_type=library_content_type)

        # Create Viewers group - can only view
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        can_view_book = Permission.objects.get(codename='can_view_book')
        can_view_library = Permission.objects.get(codename='can_view_library')
        viewers_group.permissions.add(can_view_book, can_view_library)
        self.stdout.write(
            self.style.SUCCESS('Successfully created/updated Viewers group')
        )

        # Create Editors group - can view, create, and edit
        editors_group, created = Group.objects.get_or_create(name='Editors')
        editor_perms = [
            'can_view_book', 'can_create_book', 'can_edit_book',
            'can_view_library'
        ]
        for perm in editor_perms:
            permission = Permission.objects.get(codename=perm)
            editors_group.permissions.add(permission)
        self.stdout.write(
            self.style.SUCCESS('Successfully created/updated Editors group')
        )

        # Create Admins group - all permissions
        admins_group, created = Group.objects.get_or_create(name='Admins')
        for perm in book_permissions:
            admins_group.permissions.add(perm)
        for perm in library_permissions:
            admins_group.permissions.add(perm)
        self.stdout.write(
            self.style.SUCCESS('Successfully created/updated Admins group')
        )