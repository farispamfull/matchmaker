from django_filters import rest_framework as filters


class UserFilter(filters.FilterSet):
    gender = filters.CharFilter(field_name='gender', lookup_expr='contains')
    first_name = filters.CharFilter(field_name='first_name',
                                    lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='last_name',
                                   lookup_expr='icontains')
    is_swiped = filters.BooleanFilter(method='filter_is_swiped')
    is_swiper = filters.BooleanFilter(method='filter_is_swiper')

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
