from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from university.response import *
from .serializers import *
from .models import *
from django.core.cache import cache
from django.db import transaction
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

# Create your views here.
class TeachingStaffApiView(APIView):
    CACHE_TIMEOUT = getattr(settings, 'CACHE_TIMEOUT', 60*60)
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return TeachingStaff.objects.select_related(
            'user', 
            'position', 
            'faculty', 
            'department').prefetch_related(
                'user__groups', 
                'areas_of_expertise')
    
    @staticmethod
    def clear_cache_teachingstaff(nip=None):
        keys=["teachingstaff_all"]
        if nip:
            keys.append(f"teachingstaff_{nip}")
        cache.delete_many(keys)
    
    @staticmethod
    def _user_in_groups_queryset(user, groupName):
        return user.groups.filter(name=groupName).exists()
    
    def _permissions_check(self, request, nip=None):
        user=request.user
        if TeachingStaffApiView._user_in_groups_queryset(user, 'Teaching Staff'):
            if nip != user.username or nip is None:
                raise PermissionDenied('Access Denied')
        elif TeachingStaffApiView._user_in_groups_queryset(user, 'Admin'):
           pass
        else:
            raise PermissionDenied('Access Denied')
    
    def get(self, request, nip=None):
        self._permissions_check(request, nip)
        cache_key=f"teachingstaff_{nip}" if nip else "teachingstaff_all"
        data = cache.get(cache_key)
        if not data: 
            if nip is not None:
                teaching_obj=get_object_or_404(self.get_queryset(), nip=nip)
                serializer=TeachingStaffSerializer_Get(teaching_obj)
            else:
                teaching_obj=self.get_queryset().all()
                serializer=TeachingStaffSerializer_Get(teaching_obj, many=True)
            data=serializer.data
            cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return success_response(data, message='success retrieve data')

    def post(self, request):
        user=request.user
        if not TeachingStaffApiView._user_in_groups_queryset(user, 'Admin'):
            raise PermissionDenied('Access Denied')
        serializer=TeachingStaffSerializer_Create(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                self.clear_cache_teachingstaff()
                return success_response(serializer.data, message="success create data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        
    def patch(self, request, nip):
        self._permissions_check(request, nip)
        teaching_obj=get_object_or_404(self.get_queryset(), nip=nip)
        serializer=TeachingStaffSerializer_Update(teaching_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                self.clear_cache_teachingstaff(nip)
                return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def delete(self, request, nip):
        user=request.user
        if not TeachingStaffApiView._user_in_groups_queryset(user, 'Admin'):
            raise PermissionDenied('Access Denied')
        teaching_obj=get_object_or_404(self.get_queryset(), nip=nip)
        try:
            with transaction.atomic():
                self.clear_cache_teachingstaff(nip)
                # teaching_obj.areas_of_expertise.clear()
                teaching_obj.user.delete()
                return delete_response()
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
class AdministrativeStaffApiView(APIView):
    CACHE_TIMEOUT=getattr(settings, 'CACHE_TIMEOUT', 60*60)
    permission_classes=[IsAuthenticated]
    
    @staticmethod
    def _user_in_groups_queryset(user, groupName):
        return user.groups.filter(name=groupName).exists()
    
    def _permission_check(self, request, nip= None):
        user=request.user
        if AdministrativeStaffApiView._user_in_groups_queryset(user, 'Administrative Staff'):
            if nip is None and nip != user.username:
                raise PermissionDenied('Access Denied')
        elif AdministrativeStaffApiView._user_in_groups_queryset(user, 'Admin'):
            pass
        else: raise PermissionDenied('Access Denied')
        
    def get_queryset(self):
        return AdministrativeStaff.objects.select_related('user', 'faculty', 'department').prefetch_related('user__groups')
    
    @staticmethod
    def clear_cache_administaff(nip=None):
        keys=['adminstaff_all']
        if nip:
            keys.append(f"adminstaff_{nip}")
        cache.delete_many(keys)
    
    def get(self, request, nip=None):
        self._permission_check(request, nip)
        cache_key=f"adminstaff_{nip}" if nip else "adminstaff_all"
        data=cache.get(cache_key)
        if not data:
            if nip is not None:
                administrative_obj=get_object_or_404(self.get_queryset(), nip=nip)
                serializer=AdminStaffSerializer_Get(administrative_obj)
            else:
                administrative_obj=self.get_queryset().all()
                serializer=AdminStaffSerializer_Get(administrative_obj, many=True)
            data=serializer.data
            cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return success_response(data, message='success retrieve data')

    def post(self, request):
        user=request.user
        if not AdministrativeStaffApiView._user_in_groups_queryset(user, 'Admin'):
            raise PermissionDenied('Access Denied')
        serializer=AdminStaffSerializer_Create(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                AdministrativeStaffApiView.clear_cache_administaff()
                return success_response(serializer.data, message="success create data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        
    def patch(self, request, nip):
        self._permission_check(request, nip)
        administrative_obj=get_object_or_404(self.get_queryset(), nip=nip)
        serializer=AdminStaffSerializer_Update(administrative_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                AdministrativeStaffApiView.clear_cache_administaff(nip)
                return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def delete(self, request, nip):
        user=request.user
        if not AdministrativeStaffApiView._user_in_groups_queryset(user, 'Admin'):
            raise PermissionDenied('Access Denied')
        administrative_obj=get_object_or_404(self.get_queryset(), nip=nip)
        try:
            with transaction.atomic():
                administrative_obj.user.delete()
                AdministrativeStaffApiView.clear_cache_administaff(nip)
                return delete_response()
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
     
class SuperAdminStaffApiView(APIView):
    CACHE_TIMEOUT=getattr(settings, 'CACHE_TIMEOUT', 60*60)
    permission_classes=[IsAuthenticated]
    
    @staticmethod
    def _user_in_groups_queryset(user, groupName):
        return user.groups.filter(name=groupName).exists()
    
    def _permission_check(self, request):
        user=request.user
        if AdministrativeStaffApiView._user_in_groups_queryset(user, 'Admin'):
            pass
        else: raise PermissionDenied('Access Denied')
    
    def get_queryset(self):
        return SuperAdminStaff.objects.prefetch_related('user', 'user__groups')
    
    @staticmethod
    def clear_cache_superadmin(nip=None):
        keys=["superadmin_all"]
        if nip:
            keys.append(f"superadmin_{nip}")
        cache.delete_many(keys)
    
    def get(self, request, nip=None):
        self._permission_check(request, nip)
        cache_key=f"superadmin_{nip}" if nip else "superadmin_all"
        data=cache.get(cache_key)
        if not data:
            if nip is not None:
                superadmin_obj=get_object_or_404(self.get_queryset(), nip=nip)
                serializer=SuperAdminSerializer_Get(superadmin_obj)
            else:
                superadmin_obj=self.get_queryset().all()
                serializer=SuperAdminSerializer_Get(superadmin_obj, many=True)
            data=serializer.data
            cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return success_response(data, message="success retrieve data")
    
    def post(self, request):
        user=request.user
        if not SuperAdminStaffApiView._user_in_groups_queryset(user, 'Admin'):
            raise PermissionDenied('Access Denied')
        serializer=SuperAdminSerializer_Create(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                SuperAdminStaffApiView.clear_cache_superadmin()
                return success_response(serializer.data, message="success create data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        
    def patch(self, request, nip):
        self._permission_check(request, nip)
        superadmin_obj=get_object_or_404(self.get_queryset(), nip=nip)
        serializer=SuperAdminSerializer_Update(superadmin_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                SuperAdminStaffApiView.clear_cache_superadmin(nip)
                return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def delete(self, request, nip):
        user=request.user
        if not SuperAdminStaffApiView._user_in_groups_queryset(user, 'Admin'):
            raise PermissionDenied('Access Denied')
        superadmin_obj=get_object_or_404(self.get_queryset(), nip=nip)
        try:
            with transaction.atomic():
                superadmin_obj.user.delete()
                SuperAdminStaffApiView.clear_cache_superadmin(nip)
                return delete_response()
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
                
class ExpertiseApiView(APIView):
    CACHE_TIMEOUT=getattr(settings, 'CACHE_TIMEOUT', 60*60)
    permission_classes=[IsAuthenticated]
    
    @staticmethod
    def _user_in_groups_queryset(user, groupName):
        return user.groups.filter(name=groupName).exists()
    
    def _permission_check(self, request):
        user=request.user
        if ExpertiseApiView._user_in_groups_queryset(user, 'Admin'):
            pass
        else: raise PermissionDenied('Access Denied')
    
    @staticmethod
    def clear_cache_AOE(expertise_id=None):
        keys=['AOE_all']
        if expertise_id:
            keys.append(f"AOE_{expertise_id}")
        cache.delete_many(keys)
        
    def get(self, request, expertise_id=None):
        self._permission_check(request)
        cache_key=f"AOE_{expertise_id}" if expertise_id else 'AOE_all'
        data=cache.get(cache_key)
        if not data:
            if expertise_id is not None:
                expertise_obj=get_object_or_404(AreaOfExpertise, id=expertise_id)
                serializer=ExpertiseSerializer(expertise_obj)
            else:
                expertise_obj=AreaOfExpertise.objects.all()
                serializer=ExpertiseSerializer(expertise_obj, many=True)
            data=serializer.data
            cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return success_response(serializer.data, message="success retrieve data")
    
    def post(self, request):
        user=request.user
        if not ExpertiseApiView._user_in_groups_queryset(user, 'Admin'):
            raise PermissionDenied('Access Denied')
        serializer=ExpertiseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                ExpertiseApiView.clear_cache_AOE()
                return created_response(serializer.data, message='success created data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def put(self, request, expertise_id):
        self._permission_check(request)
        expertise_obj=get_object_or_404(AreaOfExpertise, id=expertise_id)
        serializer=ExpertiseSerializer(expertise_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                ExpertiseApiView.clear_cache_AOE(expertise_id)
                return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def delete(self, request, expertise_id):
        user=request.user
        if not ExpertiseApiView._user_in_groups_queryset(user, 'Admin'):
            raise PermissionDenied('Access Denied')
        expertise_obj=get_object_or_404(AreaOfExpertise, id=expertise_id)
        try:
            with transaction.atomic():
                ExpertiseApiView.clear_cache_AOE(expertise_id)
                expertise_obj.delete()
                return delete_response()
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
class TeachingPositionApiView(APIView):
    CACHE_TIMEOUT=getattr(settings, 'CACHE_TIMEOUT', 60*60)
    permission_classes=[IsAuthenticated]
    
    @staticmethod
    def _user_in_groups_queryset(user, groupName):
        return user.groups.filter(name=groupName).exists()
    
    def _permission_check(self, request):
        user=request.user
        if ExpertiseApiView._user_in_groups_queryset(user, 'Admin'):
            pass
        else: raise PermissionDenied('Access Denied')
    
    def clear_cache_position(position_id):
        keys=["position_all"]
        if position_id:
            keys.append(f"position_{position_id}")
        cache.delete_many(keys)
        
    def get(self, request, position_id=None):
        self._permission_check(request)
        cache_key=f"position_{position_id}" if position_id else "position_all"
        data=cache.get(cache_key)
        if not data:
            if position_id is not None:
                position_obj=get_object_or_404(PositionTeachingStaff, id=position_id)
                serializer=PositionTeachingSerializer(position_obj)
            else:
                position_obj=PositionTeachingStaff.objects.all()
                serializer=PositionTeachingSerializer(position_obj, many=True)
            data=serializer.data
            cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return success_response(serializer.data, message='success retrieve data')
    
    def post(self, request):
        user=request.user
        if not TeachingPositionApiView._user_in_groups_queryset(user, 'Admin'):
            raise PermissionDenied('Access Denied')
        serializer=PositionTeachingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        try:
            with transaction.atomic():
                serializer.save()
                TeachingPositionApiView.clear_cache_position()
                return created_response(serializer.data, message='success created data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        
    def put(self, request, position_id):
        self._permission_check(request)
        position_obj=get_object_or_404(PositionTeachingStaff, id=position_id)
        serializer=PositionTeachingSerializer(position_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                TeachingPositionApiView.clear_cache_position(position_id)
                return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def delete(self, request, position_id):
        user=request.user
        if not TeachingPositionApiView._user_in_groups_queryset(user, 'Admin'):
            raise PermissionDenied('Access Denied')
        position_obj=get_object_or_404(PositionTeachingStaff, id=position_id)
        try:
            with transaction.atomic():
                position_obj.delete()
                TeachingPositionApiView.clear_cache_position(position_id)
                return delete_response()
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        