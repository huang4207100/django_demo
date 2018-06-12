from django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('algo_sync_tools/',views.algo_sync_tools,name='algo_sync_tools'),
    path('algo_sync_tool_result/',views.algo_sync_tool_result,name='result_algo_tools'),
    path('interface_test/',views.interface_test,name='interface_test'),
    path('interface_test_result/',views.interface_test_result,name='result_interface')
]
