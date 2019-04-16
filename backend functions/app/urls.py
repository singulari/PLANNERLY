from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^token_name/caps$', views.compute_caps_by_token_name, name='token name caps'),
    url(r'^judge/module_code$', views.judge_module_code, name='judge module code'),
    url(r'^module_codes/honours$', views.compute_honours_by_module_codes, name='compute honours by module codes'),
    url(r'^mod_class_id/average$', views.get_average_by_mod_class_id, name='get average by mod class id'),
    url(r'^module_codes/caps$', views.compute_caps_by_module_codes, name='compute caps by module codes'),
    url(r'^recent_search_courses/title$', views.get_recent_courses_title, name='get recent courses title'),
    url(r'^token_name/module_codes$', views.get_module_codes_by_token_name, name='get module codes by token_name'),
    url(r'^module_code/final_marks$', views.get_final_marks_by_module_code, name='get final marks by module code'),
    url(r'^module_codes/core_ue_ge$', views.get_core_ue_ge_modules, name='get modules from core, ue and ge'),
    url(r'^module_code/add$', views.add_module, name='add module to store modules'),
    url(r'^module_codes/delete$', views.delete_module, name='delete module from store modules'),
]