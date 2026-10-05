"""Verificare simplificată a rolurilor fără autentificare web."""
PERMISSIONS = {
    'reader': {'search', 'reserve', 'cancel', 'view_own'},
    'librarian': {'search', 'manage_catalog', 'issue', 'return', 'report'},
    'administrator': {'manage_accounts'},
}

def require_permission(role, action):
    if action not in PERMISSIONS.get(role, set()):
        raise PermissionError('Rolul nu permite această operație')
    return True
