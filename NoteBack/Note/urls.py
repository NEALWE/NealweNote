from django.urls import path
from django.conf.urls import url
from .froala_editor_view import *
from . import views

app_name = "Note"
urlpatterns = [
    # add
    path('add_label/', views.add_label),
    path('add_note/', views.add_note),
    path('add_file/', views.add_file),

    # del
    path('del_file/', views.del_file),
    path('del_label/', views.del_label),
    path('del_note/', views.del_note),

    # update
    path('update_file/', views.update_file),
    path('update_label/', views.update_label),
    path('update_note/', views.update_note),

    # search
    path('search/', views.search),
    path('get_title/', views.get_title),
    path('get_label/', views.get_label),
    path('get_note_content/', views.get_note_content),
    path('get_note_content_by_id/', views.get_note_content_by_id),
    path('getTree/', views.getTree),

    # saveTree
    path('saveTree/', views.saveTree),
    path('updateTree/', views.updateTree),

    # saveContent
    path('saveNodeContent/', views.saveNodeContent),

    # login
    path('login/', views.login),

    # path('image_upload/', image_upload),
    path('upload/', file_upload),
    # path('download/', views.download),




    #     path('list_darkwebmonitor_task/', views.list_darkwebmonitor_task, name='api_list_darkwebmonitor_task'),
    #     path('list_keyword_task/', views.list_keyword_task, name='list_keyword_task'),
    #     path('add_darkwebmonitor_task/', views.add_darkwebmonitor_task, name='api_list_darkwebmonitor_task'),
    #     path('del_darkwebmonitor_task/', views.del_darkwebmonitor_task, name='del_darkwebmonitor_task'),
    #     path('update_darkwebmonitor_task/', views.update_darkwebmonitor_task, name='update_darkwebmonitor_task'),
    #     path('get_keyword_info/', views.get_keyword_info, name='get_keyword_info'),
    #     path('get_salers_info/', views.get_salers_info, name='get_salers_info'),
    #     path('get_recent_info/', views.get_recent_info, name='get_recent_info'),
    #     path('get_person_info/', views.get_person_info, name='get_person_info'),
    #
    #
    # # 数据总览
    #     path('get_area_sum/', views.get_area_sum, name='get_area_sum'),
    #     path('get_map_data/', views.get_map_data, name='get_map_data'),
    #     path('get_sum_data/', views.get_sum_data, name='get_1sum_data'),
    #     path('get_n_days_data/', views.get_n_days_data, name='get_n_days_data'),
    #
    #
    # # 周报查看
    #     path('upload_report/', views.upload_report, name='upload_report'),
    #     path('download_report/', views.download_report, name='upload_report'),
    #     path('get_report_detail/', views.get_report_detail, name='get_report_detail'),
    #     path('download_num/', views.download_num, name='download_num'),
    #
    #
    # # 意见反馈
    #     path('add_user_feedback/', views.add_user_feedback, name='add_user_feedback'),
    #     path('del_user_feedback/', views.del_user_feedback, name='del_user_feedback'),
    #     path('list_user_feedback/', views.list_user_feedback, name='list_user_feedback'),
    #
    #
    # # 系统设置
    #     path('get_personal_history/', views.get_personal_history, name='get_personal_history'),
    #     path('login/', views.login, name='login'),
    #     path('logincheck/', views.logincheck, name='logincheck'),
    #     path('logout/', views.logout, name='logout'),
    #
    #
    # # 导出结果
    #     path('dump_details/', views.dump_details, name='dump_details'),
    #     path('dump_province/', views.dump_province, name='dump_province'),
    #
    #
    # # 管理员
    #     path('add_user/', views.add_user, name='add_user'),
    #     path('list_user/', views.list_user, name='list_user'),
    #     path('list_user_log/', views.list_user_log, name='list_user_log'),
    #     path('update_user/', views.update_user, name='update_user'),
    #     path('del_user/', views.del_user, name='del_user'),
    #
    #
    # # 普通用户
    #     path('list_normal_user/', views.list_normal_user, name='list_normal_user'),
    #     path('update_normal_user/', views.update_normal_user, name='update_normal_user'),
    #
    #     # path('add_githubperson_task/', views.add_githubperson_task, name='add_githubperson_task'),
    #     # path('del_githubperson_task/', views.del_githubperson_task, name='del_githubperson_task'),
    #     # path('update_githubperson_task/', views.update_githubperson_task, name='update_githubperson_task'),
    #     # path('list_githubperson_task/', views.list_githubperson_task, name='list_githubperson_task'),
    #     # path('run_githubperson_task/', views.run_githubperson_task, name='run_githubperson_task'),
    #     # path('list_githubperson_info/', views.list_githubperson_info, name='list_githubperson_info'),
    #     # path('update_darkwebmonitor_result/', views.update_darkwebmonitor_result, name='update_darkwebmonitor_result'),
    #     # path('api1/<func>/', views.Masscan, name='api_list_darkwebmonitor_task'),
]
