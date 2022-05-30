# encoding: utf-8
import json
import requests
import os
def send(url):
    """
    以任务成功/失败的粒度上传报告
    """
    models=os.getenv('models_list')
    models_list=[]
    for model in (models.split(',')):
        models_list.append(model)

    os.chdir(os.getenv('logs_path'))
    os.system('pwd')
    models_result=[]
    for model in models_list:
        cmd_grep=" ls | grep -i fail | grep {}" .format(model)
        cmd_res = os.system(cmd_grep)
        if cmd_res == 0 :
            kpi_status = "Failed"
        else:
            kpi_status = "Passed"

        models_result.append(
            {
                "model_name": model,
                "kpi_name": model,
                "kpi_status": kpi_status,
                "kpi_base": 0,
                "kpi_value": 0,
                "threshold": 0,
                "ratio": 0
            })
    print(models_result)
        
    params = {
        "build_type_id": os.getenv('build_type_id'),
        "build_id": os.getenv('build_id'),
        "commit_id": os.getenv('build_commit_id'),
        "commit_time": os.getenv('build_commit_time'),
        "repo": os.getenv('build_repo_name'),
        "branch": os.getenv('build_repo_name'),
        "duration": 1,
        "exit_code": os.getenv('build_exit_code'),
        "status": os.getenv('build_status'),

        "case_detail": json.dumps(models_result)
    }
    res = requests.post(url, data=params)
    result =res.json()
    if result['code'] == 200 and result['message'] == 'success':
       print("ok")
    else:
       print('error')
if __name__ == "__main__":
    #url需配置在环境变量中，不允许上传到github；
    url = os.getenv('build_url')
    send(url)
