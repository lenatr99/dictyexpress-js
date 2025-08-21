#!/usr/bin/env python
"""
Script to populate Resolwe database with data from the mock data files
"""
import os
import sys
import django
from pathlib import Path
from resolwe_bio.kb.models import Feature

# Setup Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dictyexpress_backend.settings")
django.setup()

from resolwe.flow.models import Data, DescriptorSchema, Collection, Process, Entity, Relation, RelationType, RelationPartition, Storage
from django.contrib.auth.models import User, Group
from resolwe.permissions.models import Permission

# Import the mock data
from api.time_series import TIME_SERIES
from api.expression_data import EXPRESSION_DATA
from api.storage_data import STORAGE_DATA
from api.descriptor_schema_data import DESCRIPTOR_SCHEMA
from api.features_data import FEATURES_DATA

def get_or_create_group(name):
    """Get or create a group and return it"""
    group, created = Group.objects.get_or_create(name=name)
    return group

def setup_standard_groups():
    """Create standard groups needed for permissions"""
    public_group = get_or_create_group("public")
    admin_group = get_or_create_group("administrators")
    return public_group, admin_group

def get_or_create_entity(entity):
    """Get or create an entity and return it"""
    entity, created = Entity.objects.get_or_create(entity)
    return entity

def update_entity(data):
    """Update an entity with proper permissions"""
    data['contributor'] = admin_user
    data.pop("data_count", None)
    data.pop("status", None)
    data['collection'] = Collection.objects.get(id=data['collection'])
    entity, created = Entity.objects.update_or_create(
        id=data['id'],
        defaults=data
    )
    return entity

def get_or_create_admin_user():
    """Get or create an admin user for data ownership"""
    user, created = User.objects.get_or_create(
        username="admin",
        defaults={
            "first_name": "Data",
            "last_name": "Admin",
            "email": "admin@dictyexpress.org",
            "is_staff": True,
            "is_superuser": True,
        },
    )
    if created:
        user.set_password("admin123")
        user.save()
    return user

def create_collections(collections):
    """Create collections with proper permissions"""
    for raw in collections:
        data = raw.copy()
        data["contributor"] = admin_user
        data.pop("created", None)
        data.pop("entity_count", None)
        data.pop("data_count", None)
        data.pop("modified", None)
        if 'descriptor_schema' in data and isinstance(data['descriptor_schema'], dict):
            data['descriptor_schema'] = DescriptorSchema.objects.get(id=data['descriptor_schema']['id'])
        slug = raw.get("slug") or data.get("slug")
        if not slug:
            continue  # skip items without a slug
        data.pop("slug", None)  # slug is the lookup, not a default
        data_id = data.pop('id', None)
        c, created = Collection.objects.update_or_create(id=data_id, defaults=data)
    print("Collections upserted.")



def create_relation_partitions(partitions_data, relation, admin_user):
    """Create relation partitions with proper permissions and associations"""
    for partition_data in partitions_data:
        partition_copy = partition_data.copy()
        # Get or create entity if entity ID is provided
        if 'entity' in partition_copy and partition_copy['entity'] is not None:
            entity, entity_created = Entity.objects.get_or_create(
                id=partition_copy['entity'],
                defaults={'contributor': admin_user}
            )
            partition_copy['entity'] = entity
        else:
            partition_copy['entity'] = None
        
        # Set the relation
        partition_copy['relation'] = relation
        
        # Use individual fields for get_or_create
        partition_defaults = {k: v for k, v in partition_copy.items() if k != 'id'}
        partition, partition_created = RelationPartition.objects.get_or_create(
            id=partition_copy.get('id'), 
            defaults=partition_defaults
        )
    print("Relation partitions upserted.")


def create_descriptor_schemas():
    """Create descriptor schemas with proper permissions"""

    for raw in DESCRIPTOR_SCHEMA:
        data = raw.copy()
        # Remove invalid fields that don't exist in the Django model
        data.pop("current_user_permissions", None)
        data.pop("created", None)  # created is auto-generated
        data.pop("modified", None)  # modified is auto-generated
        
        # Set the contributor to the admin user instance (not the dict from mock data)
        data["contributor"] = admin_user

        data.pop("slug", None)  # slug is the lookup, not a default
        ds, created = DescriptorSchema.objects.update_or_create(id=data['id'], defaults=data)
        
        # Set public view permissions using the Permission enum
        try:
            ds.set_permission(Permission.VIEW, public_group)
        except Exception as e:
            print(f"  - Error setting permissions: {e}")

    print("Descriptor schemas upserted.")

def create_relation():
    """Create relation with proper permissions"""
    # Set up groups and users first
    for raw in TIME_SERIES:
        data = raw.copy()
        data["contributor"] = admin_user
        data.pop("created", None)
        data.pop("modified", None)
        # Get the actual DescriptorSchema instance
        if 'descriptor_schema' in data and isinstance(data['descriptor_schema'], dict):
            data['descriptor_schema'] = DescriptorSchema.objects.get(id=data['descriptor_schema']['id'])
        if 'collection' in data and isinstance(data['collection'], dict):
            create_collections([data['collection']])
            data['collection'] = Collection.objects.get(id=data['collection']['id'])
        
        # Store partitions data temporarily and remove from relation data
        partitions_data = data.pop('partitions', [])
        
        if 'type' in data:
            try:
                data['type'] = RelationType.objects.get(name=data['type'])
            except RelationType.DoesNotExist:
                data.pop('type', None)

        # Create the relation first
        r, created = Relation.objects.update_or_create(id=data['id'], defaults=data)
        
        # Now create partitions and associate them with the relation
        if partitions_data:
            create_relation_partitions(partitions_data, r, admin_user)

def get_or_create_process(input_data):
    """Create process with proper permissions"""
    process_slug = input_data.get('slug')
    data = input_data.copy()
    data["contributor"] = admin_user
    data.pop("created", None)
    data.pop("current_user_permissions", None)
    p, created = Process.objects.get_or_create(id=data["id"], defaults=data)
    return p

def create_data(input_data):
    """Create data with proper permissions"""
    for raw in input_data:
        data = raw.copy()
        data["contributor"] = admin_user
        data.pop("created", None)
        data.pop("current_user_permissions", None)
        if 'process' in data:
            #check if process exists
            process_slug = data['process'].get('slug')
            if process_slug:
                data['process'] = get_or_create_process(data['process'])
            else:
                data.pop('process', None)
        if 'collection' in data:
            #check if collection exists
            collection_id = data['collection'].get('id')
            if collection_id:
                try:
                    data['collection'] = Collection.objects.get(id=collection_id)
                except Collection.DoesNotExist:
                    #create collection
                    create_collections([data['collection']])
                    data['collection'] = Collection.objects.get(id=data['collection']['id'])
        if 'descriptor_schema' in data:
            if data['descriptor_schema'] is not None:
                try: 
                    data['descriptor_schema'] = DescriptorSchema.objects.get(id=data['descriptor_schema']['id'])
                except DescriptorSchema.DoesNotExist:
                    create_descriptor_schemas([data['descriptor_schema']])
                    data['descriptor_schema'] = DescriptorSchema.objects.get(id=data['descriptor_schema']['id'])
            else:
                data.pop('descriptor_schema', None)
            
        if 'entity' in data:
            if data['entity'] is not None:
                data['entity'] = update_entity(data['entity'])

        d, created = Data.objects.update_or_create(id=data['id'], defaults=data)

def create_storage(input_data):
    """Create storage with proper permissions"""
    print("Creating storage...")
    for row in input_data:
        row["contributor"] = admin_user
        row.pop("created", None)
        row.pop("current_user_permissions", None)
        
        # Handle many-to-many data field separately
        data_objects = []
        if "data" in row:
            data_ids = row.pop("data")  # Remove from row before object creation
            for data_id in data_ids:
                try:
                    data_obj = Data.objects.get(id=data_id)
                    data_objects.append(data_obj)
                except Data.DoesNotExist:
                    print(f"Data with id {data_id} does not exist")
        
        # Create storage without many-to-many field
        s, created = Storage.objects.get_or_create(id=row['id'], defaults=row)
        
        # Set many-to-many relationships after creation
        if data_objects:
            s.data.set(data_objects)
        
        print(f"Created storage: {s}")


def create_features(input_data):
    """Create features with proper permissions"""
    print("Creating features...")
    for row in input_data:
        f, created = Feature.objects.get_or_create(feature_id=row['feature_id'], defaults=row)

def main():
    """Main function to populate all data"""
    print("Starting data population for Resolwe database...")
    global public_group, admin_group
    global admin_user
    admin_user = get_or_create_admin_user()
    public_group, admin_group = setup_standard_groups()
    admin_user.groups.add(admin_group)

    create_descriptor_schemas()

    create_relation()

    create_data(EXPRESSION_DATA)

    create_storage(STORAGE_DATA)

    create_features(FEATURES_DATA)

    print("\n=== Data Population Summary ===")
    print(f"Total Entities: {Entity.objects.count()}")
    print(f"Total Collections: {Collection.objects.count()}")
    print(f"Total Data Objects: {Data.objects.count()}")
    print(f"Total Processes: {Process.objects.count()}")
    print(f"Total Relations: {Relation.objects.count()}")
    print("\nData population completed successfully!")


if __name__ == "__main__":
    main()
