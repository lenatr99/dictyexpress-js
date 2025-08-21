"""
Custom permissions module for Resolwe integration
"""

from rest_framework.permissions import AllowAny


class ResolwePermissions(AllowAny):
    """
    Simple permissions class that allows all access.
    Can be customized later for more restrictive permissions.
    """
    pass
