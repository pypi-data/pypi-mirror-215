import analyzing_data_slice_win_design
import global_data
import numpy as np
import ctypes
from PyQt5 import QtWidgets


class AnalyzingDataSliceWin(QtWidgets.QMainWindow, analyzing_data_slice_win_design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.gridLayout_2.sizeHint())
        self.setWindowTitle("Анализ данных АЦП")
        self.__init_tools()
        self.pushButton_RunHandling.clicked.connect(self.__setting_set)

    def __init_tools(self):
        self.label_DataSizeVal.setText(str(len(global_data.voltage_arr)))
        measure_time = (len(global_data.voltage_arr) - 1) / global_data.sample_freq
        max_thrown_points = round(global_data.points_on_channel * 0.4)
        self.spinBox_ThrownPoints.setMaximum(max_thrown_points)
        self.spinBox_ThrownPoints.setMinimum(0)
        self.spinBox_ThrownPoints.setValue(min(3, max_thrown_points))
        self.label_MeasureTimeVal.setText(str(measure_time))
        self.spinBox_AnalyzingTStart.setDecimals(3)
        self.spinBox_AnalyzingTStart.setMinimum(0)
        self.spinBox_AnalyzingTStart.setMaximum(measure_time)
        self.spinBox_AnalyzingTStart.setValue(0)
        self.spinBox_AnalyzingTEnd.setDecimals(3)
        self.spinBox_AnalyzingTEnd.setMinimum(0)
        self.spinBox_AnalyzingTEnd.setMaximum(measure_time)
        self.spinBox_AnalyzingTEnd.setValue(measure_time)
        # self.sliderAnalyzingTime.setMaximum(measure_time * 1000)
        # self.sliderAnalyzingTime.setSliderPosition((0.0, measure_time * 1000))

    def __setting_set(self):
        global_data.analyzing_time_start = min(self.spinBox_AnalyzingTStart.value(), self.spinBox_AnalyzingTEnd.value())
        global_data.analyzing_time_end = max(self.spinBox_AnalyzingTStart.value(), self.spinBox_AnalyzingTEnd.value())
        self.spinBox_AnalyzingTStart.setValue(global_data.analyzing_time_start)
        self.spinBox_AnalyzingTEnd.setValue(global_data.analyzing_time_end)
        # global_data.analyzing_time_start, global_data.analyzing_time_end = self.sliderAnalyzingTime.sliderPosition()
        # global_data.analyzing_time_start /= 1000
        # global_data.analyzing_time_end /= 1000
        global_data.data_handle_success = self.__handle_bin_file()
        self.close()

    def __tools_in_handle_mode(self):
        self.pushButton_RunHandling.setEnabled(False)
        self.spinBox_ThrownPoints.setEnabled(False)
        self.spinBox_AnalyzingTStart.setEnabled(False)
        self.spinBox_AnalyzingTEnd.setEnabled(False)
        #self.sliderAnalyzingTime.setEnabled(False)
        QtWidgets.QApplication.processEvents()

    def __handle_bin_file(self):
        self.__tools_in_handle_mode()
        handle_success = False
        sample_freq_Hz = global_data.sample_freq
        one_support_signal_time_duration = global_data.one_channel_signal_duration
        points_to_throw_from_start_end = self.spinBox_ThrownPoints.value()
        measure_time = (len(global_data.voltage_arr) - 1) / global_data.sample_freq
        voltage_arr_start_ind = max(0, round(global_data.analyzing_time_start / measure_time * len(global_data.voltage_arr)))
        voltage_arr_end_ind = min(len(global_data.voltage_arr), round(global_data.analyzing_time_end / measure_time * len(global_data.voltage_arr)))
        global_data.voltage_arr = global_data.voltage_arr[voltage_arr_start_ind:voltage_arr_end_ind]
        global_data.analyzing_time_start = voltage_arr_start_ind / global_data.sample_freq
        global_data.analyzing_time_end = voltage_arr_end_ind / global_data.sample_freq

        # Step 1.0 - create ideal support signal
        data_size = len(global_data.voltage_arr)
        global_data.channels_arr = np.zeros((data_size), dtype=np.int8)  # 1,2,3,4 - support channels; 5,6,7,8 - lamels channels; 0 - thrown
        global_data.channel_average_val_arr = np.full((data_size), -1.0, dtype=global_data.voltage_arr.dtype)

        channel_size = round(sample_freq_Hz * one_support_signal_time_duration)
        ideal_support_signal = np.zeros((4 * channel_size), dtype=global_data.voltage_arr.dtype)
        for i in range(len(ideal_support_signal)):
            if 0 <= i < len(ideal_support_signal) / 4:
                ideal_support_signal[i] = 0.0
            elif len(ideal_support_signal) / 4 <= i < len(ideal_support_signal) / 2:
                ideal_support_signal[i] = 2.5 / 4
            elif len(ideal_support_signal) / 2 <= i < 3 * len(ideal_support_signal) / 4:
                ideal_support_signal[i] = 2.5 / 2
            else:
                ideal_support_signal[i] = 3 * 2.5 / 4

        # Step2 - cross-correlation search to find support signal areas
        self.label_status.setText("Статус: поиск опорных каналов в сигнале")
        QtWidgets.QApplication.processEvents()
        support_signal_areas = []
        try:
            ideal_support_signal_mean = np.mean(ideal_support_signal)
            shifted_ideal_support_signal = ideal_support_signal - ideal_support_signal_mean
            shifted_ideal_support_signal = np.flip(shifted_ideal_support_signal)
            shifted_voltage_arr = global_data.voltage_arr - ideal_support_signal_mean
            cross_corell_res = np.convolve(shifted_voltage_arr, shifted_ideal_support_signal, mode="valid")
            max_cross_corell_val = np.max(cross_corell_res)
            support_signal_areas = np.where(cross_corell_res >= 0.8 * max_cross_corell_val, 1.0, 0.0)
            support_signal_areas_tail = np.full((data_size - len(support_signal_areas)), 1.0)
            support_signal_areas = np.concatenate((support_signal_areas, support_signal_areas_tail))
        except:
            ctypes.windll.user32.MessageBoxW(0, "Ошибка в процессе применения кросс-корелляции для поиска опорного сигнала",
                                             "Program error", 1)
            return handle_success

        # Step3 - evaluate channels count
        self.label_status.setText("Статус: оценка кол-ва каналов")
        QtWidgets.QApplication.processEvents()
        channels_count = 8
        try:
            support_signals_starts = []
            is_zero_seq = False
            for i in range(30 * len(ideal_support_signal)):
                if support_signal_areas[i] == 0:
                    is_zero_seq = True
                else:
                    if is_zero_seq:
                        support_signals_starts.append(i)
                    is_zero_seq = False
            signal_periods = [abs(support_signals_starts[i - 1] - support_signals_starts[i]) for i in
                              range(1, len(support_signals_starts))]
            signal_period = np.median(signal_periods)
            channels_count = round(4.0 * signal_period / len(ideal_support_signal))
            if channels_count < 4:
                ctypes.windll.user32.MessageBoxW(0, "Слишком мало каналов данных: " + str(channels_count),
                                                 "Program error", 1)
                return handle_success
        except:
            return handle_success

        if channels_count != global_data.channels_count:
            ctypes.windll.user32.MessageBoxW(0, "Заявлено " + str(global_data.channels_count) +
                                             " канала. Определено при анализе сигнала: " + str(channels_count),
                                             "Program error", 1)
            return handle_success

        # Step4 - find first best support signal match
        self.label_status.setText("Статус: поиск первого опорного сигнала")
        QtWidgets.QApplication.processEvents()
        best_match = 10 ** 10
        best_match_ind = -1
        for i in range(round(3 * len(ideal_support_signal) * channels_count / 4)):
            if i + len(ideal_support_signal) > data_size:
                break
            cur_analyzing_subsignal = global_data.voltage_arr[i: i + len(ideal_support_signal)]
            cur_diff_with_ideal_signal = (ideal_support_signal - cur_analyzing_subsignal)
            cur_match = np.sum(cur_diff_with_ideal_signal * cur_diff_with_ideal_signal)
            if best_match_ind < 0 or cur_match < best_match:
                best_match = cur_match
                best_match_ind = i
        best_match_ind = max(0, best_match_ind)

        # Step5 - data separation by channels
        expect_average_data_size = round(1.5 * data_size / (channels_count * global_data.sample_freq * global_data.one_channel_signal_duration))
        global_data.all_channels_average_vals = np.zeros((channels_count, expect_average_data_size), dtype=global_data.voltage_arr.dtype)
        global_data.all_channels_average_time = np.zeros((expect_average_data_size))
        self.label_status.setText("Статус: распределение по каналам (0 %)")
        QtWidgets.QApplication.processEvents()
        handled_data_percents_shown = np.full((100), False, dtype = np.bool_)
        try:
            first_periods_count = int((len(list(range(best_match_ind, -1, -1 * channel_size))) - 1) / channels_count)
            counter = first_periods_count
            cur_channel = channels_count
            for i in range(best_match_ind, -1, -1 * channel_size):
                ch_start = max(0, i - channel_size + points_to_throw_from_start_end)
                ch_end = i - points_to_throw_from_start_end
                if ch_end > ch_start:
                    global_data.channels_arr[ch_start: ch_end] = cur_channel
                    ch_mean = np.mean(global_data.voltage_arr[ch_start: ch_end])
                    global_data.channel_average_val_arr[ch_start: ch_end] = ch_mean
                    if counter > 0:
                        global_data.all_channels_average_vals[cur_channel - 1][counter - 1] = ch_mean
                        if cur_channel == 1:
                            global_data.all_channels_average_time[counter - 1] = global_data.analyzing_time_start + max(0, i - channel_size) / sample_freq_Hz
                            counter -= 1
                cur_channel = channels_count if cur_channel == 1 else (cur_channel - 1)

            real_average_data_size = first_periods_count
            start_period_ind = best_match_ind
            while True:
                if start_period_ind == -1 or start_period_ind >= data_size:
                    break
                expected_next_start_period_ind = (start_period_ind + channels_count * channel_size)
                cur_handled_data_percent = np.clip(round(100.0 * expected_next_start_period_ind / data_size), 0, 99)
                if not handled_data_percents_shown[cur_handled_data_percent]:
                    handled_data_percents_shown[cur_handled_data_percent] = True
                    self.label_status.setText("Статус: распределение по каналам (" + str(cur_handled_data_percent) + " %)")
                    QtWidgets.QApplication.processEvents()
                next_start_period_ind = -1 if expected_next_start_period_ind >= data_size else expected_next_start_period_ind
                if next_start_period_ind != -1:
                    cur_best_match_ind = next_start_period_ind
                    for i in range(max(0, next_start_period_ind - 2), min(next_start_period_ind + 3, data_size)):
                        if support_signal_areas[i] > 0.5 and abs(global_data.voltage_arr[cur_best_match_ind]) > abs(global_data.voltage_arr[i]):
                            cur_best_match_ind = i
                    next_start_period_ind = cur_best_match_ind
                if real_average_data_size < expect_average_data_size:
                    global_data.all_channels_average_time[real_average_data_size] = global_data.analyzing_time_start + start_period_ind / sample_freq_Hz
                for i in range(channels_count - 1):
                    ch_start = min(start_period_ind + i * channel_size + points_to_throw_from_start_end, data_size)
                    ch_end = min(start_period_ind + (i + 1) * channel_size - points_to_throw_from_start_end, data_size)
                    if ch_end > ch_start:
                        global_data.channels_arr[ch_start: ch_end] = i + 1
                        ch_mean = np.mean(global_data.voltage_arr[ch_start: ch_end])
                        global_data.channel_average_val_arr[ch_start: ch_end] = ch_mean
                        if real_average_data_size < expect_average_data_size:
                            global_data.all_channels_average_vals[i][real_average_data_size] = ch_mean
                last_ch_start = min(start_period_ind + (channels_count - 1) * channel_size + points_to_throw_from_start_end, data_size) if next_start_period_ind > 0 else min(start_period_ind + (channels_count - 1) * channel_size + points_to_throw_from_start_end, data_size)
                last_ch_end = next_start_period_ind - points_to_throw_from_start_end if next_start_period_ind > 0 else min(start_period_ind + channels_count * channel_size - points_to_throw_from_start_end, data_size)
                if last_ch_end > last_ch_start:
                    global_data.channels_arr[last_ch_start: last_ch_end] = channels_count
                    last_ch_mean = np.mean(global_data.voltage_arr[last_ch_start: last_ch_end])
                    global_data.channel_average_val_arr[last_ch_start: last_ch_end] = last_ch_mean
                    if real_average_data_size < expect_average_data_size:
                        global_data.all_channels_average_vals[channels_count - 1][real_average_data_size] = last_ch_mean
                real_average_data_size += 1
                start_period_ind = next_start_period_ind

            global_data.all_channels_average_time.resize(real_average_data_size, refcheck=False)
            global_data.all_channels_average_vals = global_data.all_channels_average_vals[:, 0:real_average_data_size]
        except:
            ctypes.windll.user32.MessageBoxW(0, "Ошибка в процессе распределения данных по " + str(channels_count) + " каналам",
                                             "Program error", 1)
            return handle_success
        handle_success = True
        return handle_success
