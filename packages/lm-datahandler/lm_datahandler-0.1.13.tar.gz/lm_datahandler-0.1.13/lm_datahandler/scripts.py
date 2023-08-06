import os.path
import pandas as pd
from lm_datahandler.data_download.data_download import download_lm_data_from_server
from lm_datahandler.datahandler import DataHandler


def download_and_full_analyse(download_params):
    data_save_path = download_params["save_path"]
    data_list = download_lm_data_from_server(download_params, data_save_path)
    sleep_variables_save_file_name = "sleep_variables_" + download_params["dateRange"][0] + "_" + \
                                     download_params["dateRange"][1] + ".csv"

    analysis_save_path = download_params["analysis_save_path"]

    show_plots = download_params["show_plots"]

    local_datas_full_analyse(data_save_path, data_list, analysis_save_path=analysis_save_path, sleep_variables_save_name=sleep_variables_save_file_name, show_plots=show_plots)




def local_datas_full_analyse(data_path, data_names, analysis_save_path=None, sleep_variables_save_name=None, show_plots=True):
    assert os.path.exists(data_path), "The input dir path does not exist."
    sleep_variables_df = pd.DataFrame({
        "data_name": [],
        "TST": [],
        "SOL": [],
        "GU": [],
        "WASO": [],
        "SE": [],
        "AR": []
    })

    if analysis_save_path is None:
        analysis_save_path = data_path
    else:
        if not os.path.exists(analysis_save_path):
            os.mkdir(analysis_save_path)
    for i, data_name in enumerate(data_names):
        if not os.path.exists(os.path.join(data_path, data_name)):
            print("data: \"{}\" not found, skipped.".format(data_name))
            continue
        data_handler = DataHandler()

        temp_data_path = os.path.join(data_path, data_name)

        data_analysis_save_path = os.path.join(analysis_save_path, data_name)

        if not os.path.exists(data_analysis_save_path):
            os.mkdir(data_analysis_save_path)
        sleep_fig_save_path = os.path.join(data_analysis_save_path, "sleep_fig.png")
        slow_wave_stim_sham_plot = os.path.join(data_analysis_save_path, "sw_stim_sham_fig.png")

        slow_wave_excel_save_path = os.path.join(data_analysis_save_path, "sw.csv")
        spindle_excel_save_path = os.path.join(data_analysis_save_path, "sp.csv")

        # 数据加载
        data_handler.load_data(data_name=data_name, data_path=temp_data_path)

        # 绘制慢波增强对比图，并保存
        data_handler.plot_sw_stim_sham(savefig=slow_wave_stim_sham_plot)

        # 进行睡眠分期，计算睡眠指标，绘制睡眠综合情况图，并保存
        data_handler.preprocess().sleep_staging().compute_sleep_variables().plot_sleep_data(savefig=sleep_fig_save_path)

        sleep_variables = data_handler.sleep_variables
        sleep_variables["data_name"] = data_name
        sleep_variables_df.loc[i + 1] = data_handler.sleep_variables
        # spindle检测和慢波检测，并导出结果成excel
        data_handler.spindle_detect().export_sp_results(slow_wave_excel_save_path)
        data_handler.sw_detect().export_sw_results(spindle_excel_save_path)

        if show_plots:
            data_handler.show_plots()


        sleep_variables_df.to_csv(os.path.join(temp_data_path, sleep_variables_save_name))




if __name__ == '__main__':
    day = '20230621'
    download_param = {
        # 刺激范式：1. 手动刺激，2. 音频刺激，3. N3闭环刺激，4. 纯记录模式，5. 记录模式， 6. 音频刺激
        'paradigms': None,
        # 用户手机号
        'phones': None,
        # 基座mac
        'macs': None,
        # 服务版本
        'serviceVersions': None,
        # 睡眠主观评分，1~5，-1表示未评分
        'sleepScores': None,
        # 停止类型， 0. 断连超时, 1. 用户手动, 2. 头贴放到基座上停止, 3. 关机指令触发, 4. 低电量, 5. 崩溃
        'stopTypes': None,
        # 时间范围，以停止记录的时间为准
        'dateRange': ['20230621', '20230621'],
        # 数据时长范围
        'dataLengthRange': [60 * 8, 60 * 12],
        # 翻身次数范围
        'turnoverCountRange': None,
        # 刺激次数范围
        'stimulationCountRange': None,
        # 下载保存路径
        'save_path': os.path.join('E:/dataset/x7_data_by_days/data', day),
        # 分析结果保存路径（为None表示保存在数据下载路径中）
        'analysis_save_path': os.path.join('E:/dataset/x7_data_by_days/analysis', day),
        'show_plots': True
    }
    download_and_full_analyse(download_param)

    # data_names = [
    #     "13651856616_0428-21_35_53_0429-06_16_38_0.00_4",
    #     "13651856616_0429-22_38_30_0430-05_06_56_0.00_4",
    #     "13651856616_0430-22_07_51_0501-05_44_42_0.00_4",
    #     "13651856616_0501-22_02_30_0502-05_03_52_0.00_4",
    #     "13651856616_0502-22_15_44_0503-05_29_35_0.02_4",
    #     "13651856616_0503-21_39_36_0504-05_05_05_0.00_4",
    #     "13651856616_20210102_20_05_07_20210103_04_21_55",
    #
    # ]
    # local_data_full_analyse(r"E:\dataset\sleep_disorders\1_13651856616_ZLZ", data_names, None, "sleep_variables_13651856616_ZLZ.csv")
