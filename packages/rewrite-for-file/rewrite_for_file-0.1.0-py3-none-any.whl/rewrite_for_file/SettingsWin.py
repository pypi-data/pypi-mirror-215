import settings_win_design
import global_data
import numpy as np
from PyQt5 import QtWidgets, QtCore


class SetSettingsWin(QtWidgets.QMainWindow, settings_win_design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.gridLayout_2.sizeHint())
        self.setWindowTitle("Установите настройки")
        self.__init_tools()
        self.spinBox_DataSampleFreq.valueChanged.connect(self.__sample_freq_changed)
        self.SpinBox_SignalDuration.valueChanged.connect(self.__signal_duration_changed)
        self.spinBox_ChannelsCount.valueChanged.connect(self.__handle_channels_count_changed)
        self.pushButton_RunHandling.clicked.connect(self.__setting_set)

    def __handle_channels_count_changed(self, new_channels_count):
        self.comboBox_UsedChannels.clear()
        for i in range(new_channels_count):
            self.comboBox_UsedChannels.addItem(str(i + 1))
            item = self.comboBox_UsedChannels.model().item(i, 0)
            item.setCheckState(QtCore.Qt.Checked)

    def __sample_freq_changed(self, new_sample_freq):
        points_on_channel = round(new_sample_freq * self.SpinBox_SignalDuration.value())
        self.label_PointsCountOnChannelVal.setText(str(points_on_channel))

    def __signal_duration_changed(self, new_signal_duration):
        points_on_channel = round(self.spinBox_DataSampleFreq.value() * new_signal_duration)
        self.label_PointsCountOnChannelVal.setText(str(points_on_channel))

    def __init_tools(self):
        self.spinBox_ChannelsCount.setMinimum(4)
        self.spinBox_ChannelsCount.setMaximum(1024)
        self.spinBox_ChannelsCount.setValue(64)

        for i in range(self.spinBox_ChannelsCount.value()):
            self.comboBox_UsedChannels.addItem(str(i + 1))
            item = self.comboBox_UsedChannels.model().item(i, 0)
            item.setCheckState(QtCore.Qt.Checked)

        self.spinBox_DataSampleFreq.setMinimum(1)
        self.spinBox_DataSampleFreq.setMaximum(100000000)
        self.spinBox_DataSampleFreq.setValue(10000000)

        self.SpinBox_SignalDuration.setDecimals(10)
        self.SpinBox_SignalDuration.setMinimum(10**-10)
        self.SpinBox_SignalDuration.setMaximum(100)
        self.SpinBox_SignalDuration.setValue(2.0 * 10 ** (-6))

        points_on_channel = round(self.spinBox_DataSampleFreq.value() * self.SpinBox_SignalDuration.value())
        self.label_PointsCountOnChannelVal.setText(str(points_on_channel))

    def __setting_set(self):
        global_data.channels_count = self.spinBox_ChannelsCount.value()
        global_data.sample_freq = self.spinBox_DataSampleFreq.value()
        global_data.one_channel_signal_duration = self.SpinBox_SignalDuration.value()
        global_data.float_coding_bytes = np.float32 if "4" in self.comboBox_BinFileCoding.currentText() else np.float64
        global_data.points_on_channel = round(self.spinBox_DataSampleFreq.value() * self.SpinBox_SignalDuration.value())
        global_data.used_channels = []
        for i in range(global_data.channels_count):
            if self.comboBox_UsedChannels.itemChecked(i):
                global_data.used_channels.append(i)
        self.close()
