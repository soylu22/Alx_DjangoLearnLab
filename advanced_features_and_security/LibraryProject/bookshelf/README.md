# Permissions and Groups Setup

## Groups Created:
1. **Viewers**: can_view_book, can_view_library
2. **Editors**: can_view_book, can_create_book, can_edit_book, can_view_library  
3. **Admins**: All permissions (can_view, can_create, can_edit, can_delete)

## Permission Checks:
- Views use `@permission_required` decorators
- Templates use `{% if perms.app_name.permission_codename %}` checks
- Additional ownership checks for edit/delete operations

## Setup Commands:
- `python manage.py setup_groups` - Creates groups and assigns permissions
- Assign users to groups via Django admin

## Testing:
1. Create users and assign to different groups
2. Test accessing protected views
3. Verify permission-based UI elements