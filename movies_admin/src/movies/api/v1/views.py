from config.settings import PAGE_SIZE, HTTPMethods
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from movies.models import Filmwork, RoleType


class MoviesApiMixin:
    model = Filmwork
    http_method_names = (HTTPMethods.GET,)

    def get_queryset(self):

        queryset = Filmwork.objects \
            .values('id', 'title', 'description', 'creation_date', 'rating', 'type') \
            .annotate(
                genres=ArrayAgg('genres__name', distinct=True),
                actors=ArrayAgg('persons__full_name', distinct=True, filter=Q(personfilmwork__role=RoleType.ACTOR)),
                directors=ArrayAgg('persons__full_name', distinct=True,
                                   filter=Q(personfilmwork__role=RoleType.DIRECTOR)),
                writers=ArrayAgg('persons__full_name', distinct=True, filter=Q(personfilmwork__role=RoleType.WRITER)),)

        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = PAGE_SIZE

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        return {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return self.object
