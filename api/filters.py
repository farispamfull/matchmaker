from django.contrib.gis.db.models.functions import GeometryDistance
from django.contrib.gis.measure import D
from django_filters import rest_framework as filters


class UserFilter(filters.FilterSet):
    gender = filters.CharFilter(field_name='gender', lookup_expr='contains')
    first_name = filters.CharFilter(field_name='first_name',
                                    lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='last_name',
                                   lookup_expr='icontains')
    is_swiped = filters.BooleanFilter(method='filter_is_swiped')
    is_swiper = filters.BooleanFilter(method='filter_is_swiper')
    distance = filters.NumberFilter(method='filter_distance')

    def filter_distance(self, queryset, name, value):

        ref_location = self.request.user.location
        distance = value
        result = queryset.filter(
            location__dwithin=(ref_location, D(km=distance))).annotate(
            distance=GeometryDistance("location", ref_location)).order_by(
            "distance")

        return result

    def filter_is_swiper(self, queryset, name, value):
        if value is True:
            user = self.request.user
            return queryset.filter(swiped__swiped=user)
        return queryset

    def filter_is_swiped(self, queryset, name, value):
        if value is True:
            user = self.request.user
            return queryset.filter(swiper__swiper=user)
        return queryset
