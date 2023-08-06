import save_results_win_design
import global_data
from PyQt5 import QtWidgets
import plotly.graph_objects as go
import os
import ctypes
import numpy as np
import webbrowser


class SaveResultsWin(QtWidgets.QMainWindow, save_results_win_design.Ui_MainWindow):
    def __init__(self, bin_file_dir):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Сохранение результатов")
        self.bin_file_dir = bin_file_dir[0: bin_file_dir.rfind(os.path.basename(bin_file_dir))]
        self.bin_file_name = os.path.basename(bin_file_dir)
        if "." in self.bin_file_name:
            self.bin_file_name = self.bin_file_name[0 : self.bin_file_name.rfind(".")]
        self.lineEdit_SaveAllData.setText(self.bin_file_name + "_all_data")
        self.lineEdit_SaveAverageData.setText(self.bin_file_name + "_average_data")
        self.checkBox_SaveAverageData.setChecked(True)
        self.checkBox_ShowDataInBrowser.setChecked(True)
        self.checkBox_SaveAllData.setChecked(False)
        self.pushButton_SaveAndExit.clicked.connect(self.__save_and_exit)

    def __save_and_exit(self):
        if self.checkBox_ShowDataInBrowser.isChecked():
            self.label_status.setText("Статус: визуализация результатов")
            QtWidgets.QApplication.processEvents()
            try:
                plots_to_show = []
                for i in range(global_data.channels_count):
                    if i in global_data.used_channels:
                        plots_to_show.append(go.Scatter(x=global_data.all_channels_average_time,
                                                        y=global_data.all_channels_average_vals[i],
                                                        name=("support_" + str(i + 1)) if i < 4 else ("lamel_" + str(i + 1))))
                fig = go.Figure(data=plots_to_show)
                html_to_be_shown = fig.to_html(include_plotlyjs='cdn')
                html_save_dir = self.bin_file_dir + self.bin_file_name + "_plot.html"
                f = open(html_save_dir, "w")
                f.write(html_to_be_shown)
                f.close()
                webbrowser.open(html_save_dir, new=0)
            except:
                ctypes.windll.user32.MessageBoxW(0, "Ошибка в процессе визуализации обработанных данных",
                                                 "Program error", 1)

        if self.checkBox_SaveAverageData.isChecked():
            expect_save_ave_data_dir = self.lineEdit_SaveAverageData.text()
            if expect_save_ave_data_dir == "" or expect_save_ave_data_dir == " ":
                ctypes.windll.user32.MessageBoxW(0, "Введите имя файла для сохранения усредненных данных",
                                                 "Program error", 1)
                return
            if "." in expect_save_ave_data_dir:
                ctypes.windll.user32.MessageBoxW(0, "Имя файла для сохранения усредненных данных не должно содержать .",
                                                 "Program error", 1)
                return
        if self.checkBox_SaveAllData.isChecked():
            expect_save_all_data_dir = self.lineEdit_SaveAllData.text()
            if expect_save_all_data_dir == "" or expect_save_all_data_dir == " ":
                ctypes.windll.user32.MessageBoxW(0, "Введите имя файла для сохранения всех экспериментальных данных",
                                                 "Program error", 1)
                return
            if "." in expect_save_all_data_dir:
                ctypes.windll.user32.MessageBoxW(0, "Имя файла для сохранения всех экспериментальных данных не должно содержать .",
                                                 "Program error", 1)
                return
        exit_message = ""
        try:
            if self.checkBox_SaveAverageData.isChecked():
                exit_message = "Программа успешно отработала."
                self.__save_average_data(self.bin_file_dir + self.lineEdit_SaveAverageData.text() + ".txt")
            if self.checkBox_SaveAllData.isChecked():
                exit_message = "Программа успешно отработала."
                self.__save_full_data(self.bin_file_dir + self.lineEdit_SaveAllData.text() + ".txt")
            if self.checkBox_SaveAverageData.isChecked() and self.checkBox_SaveAllData.isChecked():
                exit_message += ("Данные сохранены в файлы:\n" + self.bin_file_dir + self.lineEdit_SaveAverageData.text() +
                                 ".txt\n" + self.bin_file_dir + self.lineEdit_SaveAllData.text() + ".txt")
            elif self.checkBox_SaveAllData.isChecked():
                exit_message += ("Данные сохранены в файл:\n" + self.bin_file_dir + self.lineEdit_SaveAllData.text() + ".txt")
            elif self.checkBox_SaveAverageData.isChecked():
                exit_message += ("Данные сохранены в файл:\n" + self.bin_file_dir + self.lineEdit_SaveAverageData.text())
        except:
            exit_message = ""
            ctypes.windll.user32.MessageBoxW(0,"Ошибка в процессе сохранение данных в текстовом формате на диск",
                                             "Program error", 1)
        if exit_message != "":
            ctypes.windll.user32.MessageBoxW(0, exit_message, "Program finish", 1)
        self.close()

    def __save_average_data(self, average_data_file_dir):
        measures_count = len(global_data.all_channels_average_time)
        file_header = "time\t"
        for i in range(global_data.channels_count):
            if i in global_data.used_channels:
                file_header += ("channel_" + str(i + 1) + "\t")

        try:
            self.label_status.setText("Статус: сохранение усредненных результатов (0 %)")
            QtWidgets.QApplication.processEvents()
            global_data.all_channels_average_time = global_data.all_channels_average_time.reshape(measures_count, 1)
            global_data.all_channels_average_vals = np.transpose(global_data.all_channels_average_vals)
            global_data.all_channels_average_vals = global_data.all_channels_average_vals[:, global_data.used_channels]
            np.savetxt(average_data_file_dir, np.concatenate((global_data.all_channels_average_time, global_data.all_channels_average_vals), axis=1),
                       fmt = "%.7f", delimiter='\t', header=file_header, comments="")
        except:
            ctypes.windll.user32.MessageBoxW(0,
                                             "Ошибка в процессе сохранения усредненных результатов в файл: " + average_data_file_dir,
                                             "Program error", 1)
        return

    def __save_full_data(self, full_data_file_dir):
        self.label_status.setText("Статус: сохранение всех обработанных данных (0 %)")
        QtWidgets.QApplication.processEvents()
        saved_full_data_percents_shown = np.full((100), False, dtype=np.bool_)
        try:
            f = open(full_data_file_dir, "w")
            f.write("time" + "\tvoltage\t")
            for i in range(global_data.channels_count):
                f.write("channel_" + str(i + 1) + "\t")
            for i in range(global_data.channels_count):
                f.write("channel_" + str(i + 1) + "_average\t")
            f.write("average\n")

            max_buf_size = 1000
            str_buf = ""

            data_size = len(global_data.voltage_arr)
            for i in range(data_size):
                cur_saved_data_perc = np.clip(round(100.0 * i / data_size), 0, 99)
                if not saved_full_data_percents_shown[cur_saved_data_perc]:
                    saved_full_data_percents_shown[cur_saved_data_perc] = True
                    self.label_status.setText(
                        "Статус: сохранение всех обработанных данных (" + str(cur_saved_data_perc) + " %)")
                    QtWidgets.QApplication.processEvents()
                cur_channel = global_data.channels_arr[i]
                if cur_channel <= 0:
                    str_buf += ((format(global_data.analyzing_time_start + i / global_data.sample_freq, '.8f') + "\t" + format(global_data.voltage_arr[i], '.8f') + "\n").replace(".", ","))
                    continue
                cur_str = format(global_data.analyzing_time_start + i / global_data.sample_freq, '.8f') + "\t" + format(global_data.voltage_arr[i], '.8f') + cur_channel * "\t" + format(global_data.voltage_arr[i], '.8f')
                if global_data.channel_average_val_arr[i] > -0.9:
                    cur_str += global_data.channels_count * "\t" + format(global_data.channel_average_val_arr[i], '.8f') + (global_data.channels_count - cur_channel + 1) * "\t" + format(global_data.channel_average_val_arr[i], '.8f')
                cur_str += "\n"
                str_buf += (cur_str.replace(".", ","))
                if len(str_buf) > max_buf_size:
                    f.write(str_buf)
                    str_buf = ""
            if len(str_buf) != 0:
                f.write(str_buf)
            f.close()
        except:
            ctypes.windll.user32.MessageBoxW(0, "Ошибка в процессе сохранения результата в файл: " + full_data_file_dir,
                                             "Program error", 1)
            return
