import global_data
import SettingsWin
import AnalyzingDataSliceWin
import SaveResultsWin
from PyQt5 import QtWidgets, Qt
import numpy as np
import ctypes
import sys


def parse_voltage_arr(bin_file_path):
    handle_success = True
    try:
        f = open(bin_file_path, "rb")
        global_data.voltage_arr = np.fromfile(f, dtype=global_data.float_coding_bytes)
        f.close()
    except:
        ctypes.windll.user32.MessageBoxW(0, "Ошибка в процессе чтения данных из бинарного файла: " + bin_file_dir,
                                         "Program error", 1)
        handle_success = False
    return handle_success


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    bin_file_dir = QtWidgets.QFileDialog.getOpenFileName(None, "Укажите исходный бинарный файл", filter = "vlt(*.vlt)")[0]
    if bin_file_dir == "":
        ctypes.windll.user32.MessageBoxW(0, "Бинарный файл не выбран", "Program error", 1)
        sys.exit(0)
    settings_win = SettingsWin.SetSettingsWin()
    settings_win.setAttribute(Qt.Qt.WA_DeleteOnClose)
    loop = Qt.QEventLoop()
    settings_win.destroyed.connect(loop.quit)
    settings_win.show()
    loop.exec()

    are_settings_valid = global_data.channels_count >= 4 and global_data.sample_freq >= 1 and \
                         global_data.one_channel_signal_duration > 10**(-20) and \
                         len(global_data.used_channels) >= 1 and global_data.points_on_channel >= 1
    if not are_settings_valid:
        sys.exit(0)
    if not parse_voltage_arr(bin_file_dir):
        sys.exit(0)

    set_time_slice_win = AnalyzingDataSliceWin.AnalyzingDataSliceWin()
    set_time_slice_win.setAttribute(Qt.Qt.WA_DeleteOnClose)
    loop = Qt.QEventLoop()
    set_time_slice_win.destroyed.connect(loop.quit)
    set_time_slice_win.show()
    loop.exec()
    if not global_data.data_handle_success:
        sys.exit(0)

    save_results_win = SaveResultsWin.SaveResultsWin(bin_file_dir)
    save_results_win.setAttribute(Qt.Qt.WA_DeleteOnClose)
    loop = Qt.QEventLoop()
    save_results_win.destroyed.connect(loop.quit)
    save_results_win.show()
    loop.exec()

    sys.exit(0)
