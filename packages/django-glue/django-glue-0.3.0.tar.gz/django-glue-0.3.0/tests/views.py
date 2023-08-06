import logging

from django.views.generic import TemplateView

from tests.models import TestModel
from tests.utils import generate_randomized_test_model, generate_big_test_model
from django_glue.glue import add_glue


class TestView(TemplateView):
    template_name = 'page/test_glue_page.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        test_model_object = generate_randomized_test_model()

        logging.warning(f'Added TestModel object.')

        add_glue(self.request, 'test_model_1', test_model_object, 'delete', exclude=('birth_date', 'anniversary_datetime'), methods=['is_lighter_than', 'get_full_name'])
        add_glue(self.request, 'test_model_2', test_model_object, 'change', exclude=('birth_date', 'anniversary_datetime'))
        add_glue(self.request, 'test_model_3', test_model_object, 'delete', exclude=('birth_date', 'anniversary_datetime'))
        add_glue(self.request, 'test_model_4', test_model_object, 'change', exclude=('birth_date', 'anniversary_datetime'))
        logging.warning('Added model object glue for TestModel Object in write mode')

        add_glue(self.request, 'test_query_1', TestModel.objects.filter(id__gte=1).filter(id__lte=10000), 'delete', exclude=('birth_date', 'anniversary_datetime'), methods=['is_lighter_than', 'get_full_name'])
        add_glue(self.request, 'test_query_2', TestModel.objects.filter(id__gte=1).filter(id__lte=10000), 'add', exclude=('birth_date', 'anniversary_datetime'))
        add_glue(self.request, 'test_query_3', TestModel.objects.filter(id__gte=1).filter(id__lte=10000), 'change', exclude=('birth_date', 'anniversary_datetime'))
        logging.warning('Added model query set glue for TestModel Object in read mode')

        big_test_model_object = generate_big_test_model()

        logging.warning(f'Added BigTestModel object.')

        return context_data


class OtherView(TemplateView):
    template_name = 'page/other_glue_page.html'
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        other_test_model_object = generate_randomized_test_model()

        logging.warning(f'Added Other TestModel object.')

        add_glue(self.request, 'other_test_model_1', other_test_model_object, 'change', exclude=('birth_date', 'anniversary_datetime',))

        logging.warning('Added model object glue for Other TestModel Object in write mode')

        return context_data

def benchmark_run_view(request):
    # this view should take an integer that determines how many glue connections to make.
    pass