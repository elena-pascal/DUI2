"""
DUI's command simple stacked widgets

Author: Luis Fuentes-Montero (Luiso)
With strong help from DIALS and CCP4 teams

copyright (c) CCP4 - DLS
"""

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os, sys, requests

try:
    from shared_modules import format_utils

except ModuleNotFoundError:
    '''
    This trick to import the format_utils module can be
    removed once the project gets properly packaged
    '''
    comm_path = os.path.abspath(__file__)[0:-21] + "shared_modules"
    print("comm_path: ", comm_path)
    sys.path.insert(1, comm_path)
    import format_utils

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2 import QtUiTools
from PySide2.QtGui import *

from gui_utils import TreeDirScene, widgets_defs
from reindex_table import ReindexTable
from exec_utils import (
    build_advanced_params_widget,
    copy_lst_nodes,
    json_data_request,
    Run_n_Output,
    CommandParamControl,
    uni_url
)

from simpler_param_widgets import ImportTmpWidg as ImportWidget
from simpler_param_widgets import (
    FindspotsSimplerParameterTab, IndexSimplerParamTab,
    RefineBravaiSimplerParamTab, RefineSimplerParamTab,
    IntegrateSimplerParamTab, SymmetrySimplerParamTab,
    ScaleSimplerParamTab, CombineExperimentSimplerParamTab
)


class MainObject(QObject):
    def __init__(self, parent = None):
        super(MainObject, self).__init__(parent)
        ui_path = os.path.dirname(os.path.abspath(__file__))
        ui_path += os.sep + "client.ui"
        self.window = QtUiTools.QUiLoader().load(ui_path)
        self.window.setWindowTitle("CCP4 DUI Cloud")
        try:
            imp_widg = ImportWidget()
            imp_widg.item_changed.connect(self.item_param_changed)
            self.window.ImportScrollArea.setWidget(imp_widg)

            find_simpl_widg = FindspotsSimplerParameterTab()
            find_simpl_widg.item_changed.connect(self.item_param_changed)
            self.window.FindspotsSimplerScrollArea.setWidget(find_simpl_widg)
            fd_advanced_parameters = build_advanced_params_widget("find_spots_params")
            fd_advanced_parameters.item_changed.connect(self.item_param_changed)
            self.window.FindspotsAdvancedScrollArea.setWidget(fd_advanced_parameters)

            fd_advanced_parameters.twin_widg = find_simpl_widg
            find_simpl_widg.twin_widg = fd_advanced_parameters

            index_simpl_widg = IndexSimplerParamTab()
            index_simpl_widg.item_changed.connect(self.item_param_changed)
            self.window.IndexSimplerScrollArea.setWidget(index_simpl_widg)
            id_advanced_parameters = build_advanced_params_widget("index_params")
            id_advanced_parameters.item_changed.connect(self.item_param_changed)
            self.window.IndexAdvancedScrollArea.setWidget(id_advanced_parameters)

            id_advanced_parameters.twin_widg = index_simpl_widg
            index_simpl_widg.twin_widg = id_advanced_parameters

            refi_brv_simpl_widg = RefineBravaiSimplerParamTab()
            refi_brv_simpl_widg.item_changed.connect(self.item_param_changed)
            self.window.RefineBravaiSimplerScrollArea.setWidget(refi_brv_simpl_widg)
            rb_advanced_parameters = build_advanced_params_widget("refine_bravais_settings_params")
            rb_advanced_parameters.item_changed.connect(self.item_param_changed)
            self.window.RefineBravaiAdvancedScrollArea.setWidget(rb_advanced_parameters)

            rb_advanced_parameters.twin_widg = refi_brv_simpl_widg
            refi_brv_simpl_widg.twin_widg = rb_advanced_parameters

            self.r_index_widg = ReindexTable()
            self.window.ReindexTableScrollArea.setWidget(self.r_index_widg)

            ref_simpl_widg = RefineSimplerParamTab()
            ref_simpl_widg.item_changed.connect(self.item_param_changed)
            self.window.RefineSimplerScrollArea.setWidget(ref_simpl_widg)
            rf_advanced_parameters = build_advanced_params_widget("refine_params")
            rf_advanced_parameters.item_changed.connect(self.item_param_changed)
            self.window.RefineAdvancedScrollArea.setWidget(rf_advanced_parameters)

            rf_advanced_parameters.twin_widg = ref_simpl_widg
            ref_simpl_widg.twin_widg = rf_advanced_parameters

            integr_simpl_widg = IntegrateSimplerParamTab()
            integr_simpl_widg.item_changed.connect(self.item_param_changed)
            self.window.IntegrateSimplerScrollArea.setWidget(integr_simpl_widg)
            it_advanced_parameters = build_advanced_params_widget("integrate_params")
            it_advanced_parameters.item_changed.connect(self.item_param_changed)
            self.window.IntegrateAdvancedScrollArea.setWidget(it_advanced_parameters)

            it_advanced_parameters.twin_widg = integr_simpl_widg
            integr_simpl_widg.twin_widg = it_advanced_parameters

            sym_simpl_widg = SymmetrySimplerParamTab()
            sym_simpl_widg.item_changed.connect(self.item_param_changed)
            self.window.SymmetrySimplerScrollArea.setWidget(sym_simpl_widg)
            sm_advanced_parameters = build_advanced_params_widget("symmetry_params")
            sm_advanced_parameters.item_changed.connect(self.item_param_changed)
            self.window.SymmetryAdvancedScrollArea.setWidget(sm_advanced_parameters)

            sm_advanced_parameters.twin_widg = sym_simpl_widg
            sym_simpl_widg.twin_widg = sm_advanced_parameters

            scale_simpl_widg = ScaleSimplerParamTab()
            scale_simpl_widg.item_changed.connect(self.item_param_changed)
            self.window.ScaleSimplerScrollArea.setWidget(scale_simpl_widg)
            sc_advanced_parameters = build_advanced_params_widget("scale_params")
            sc_advanced_parameters.item_changed.connect(self.item_param_changed)
            self.window.ScaleAdvancedScrollArea.setWidget(sc_advanced_parameters)

            sc_advanced_parameters.twin_widg = scale_simpl_widg
            scale_simpl_widg.twin_widg = sc_advanced_parameters

            comb_simpl_widg = CombineExperimentSimplerParamTab()
            comb_simpl_widg.item_changed.connect(self.item_param_changed)
            self.window.CombineSimplerScrollArea.setWidget(comb_simpl_widg)
            ce_advanced_parameters = build_advanced_params_widget("combine_experiments_params")
            ce_advanced_parameters.item_changed.connect(self.item_param_changed)
            self.window.CombineAdvancedScrollArea.setWidget(ce_advanced_parameters)

            ce_advanced_parameters.twin_widg = comb_simpl_widg
            comb_simpl_widg.twin_widg = ce_advanced_parameters

        except TypeError:
            print("failed to connect to server")
            sys.exit()

        self.param_widgets = widgets_defs

        self.param_widgets["import"]["simple"] = imp_widg
        self.param_widgets["import"]["advanced"] = None
        self.param_widgets["import"]["main_page"] = self.window.ImportPage

        self.param_widgets["find_spots"]["simple"] = find_simpl_widg
        self.param_widgets["find_spots"]["advanced"] = fd_advanced_parameters
        self.param_widgets["find_spots"]["main_page"] = self.window.FindspotsPage

        self.param_widgets["index"]["simple"] = index_simpl_widg
        self.param_widgets["index"]["advanced"] = id_advanced_parameters
        self.param_widgets["index"]["main_page"] = self.window.IndexPage

        self.param_widgets["refine_bravais_settings"]["simple"] = refi_brv_simpl_widg
        self.param_widgets["refine_bravais_settings"]["advanced"] = rb_advanced_parameters
        self.param_widgets["refine_bravais_settings"]["main_page"] = self.window.RefinBrabPage

        self.param_widgets["reindex"]["simple"] = self.r_index_widg
        self.param_widgets["reindex"]["advanced"] = None
        self.param_widgets["reindex"]["main_page"] = self.window.ReindexPage

        self.param_widgets["refine"]["simple"] = ref_simpl_widg
        self.param_widgets["refine"]["advanced"] = rf_advanced_parameters
        self.param_widgets["refine"]["main_page"] = self.window.RefinePage

        self.param_widgets["integrate"]["simple"] = integr_simpl_widg
        self.param_widgets["integrate"]["advanced"] = it_advanced_parameters
        self.param_widgets["integrate"]["main_page"] = self.window.IntegratePage

        self.param_widgets["symmetry"]["simple"] = sym_simpl_widg
        self.param_widgets["symmetry"]["advanced"] = sm_advanced_parameters
        self.param_widgets["symmetry"]["main_page"] = self.window.SimmetryPage

        self.param_widgets["scale"]["simple"] = scale_simpl_widg
        self.param_widgets["scale"]["advanced"] = sc_advanced_parameters
        self.param_widgets["scale"]["main_page"] = self.window.ScalePage

        self.param_widgets["combine_experiments"]["simple"] = comb_simpl_widg
        self.param_widgets["combine_experiments"]["advanced"] = ce_advanced_parameters
        self.param_widgets["combine_experiments"]["main_page"] = self.window.CombinePage

        self.window.incoming_text.setFont(QFont("Monospace"))
        self.tree_obj = format_utils.TreeShow()
        self.tree_scene = TreeDirScene(self)
        self.window.treeView.setScene(self.tree_scene)

        self.window.Next2RunLayout.addWidget(QLabel("                  . . .       "))
        self.current_next_buttons = 0
        self.parent_nums_lst = []

        self.font_point_size = QFont().pointSize()

        self.tree_scene.node_clicked.connect(self.on_node_click)
        self.window.RetryButton.clicked.connect(self.on_retry)
        self.window.CmdSend2server.clicked.connect(self.request_launch)
        self.window.ReqStopButton.clicked.connect(self.req_stop)
        self.window.Reset2DefaultPushButton.clicked.connect(self.reset_param)
        self.window.ClearParentButton.clicked.connect(self.clear_parent_list)
        self.r_index_widg.opt_signal.connect(self.launch_reindex)

        self.tree_scene.draw_tree_graph([])
        self.new_node = None
        self.lst_node_info_out = [] #{"lin_num": int, "log_line_lst": [str]}
        self.current_lin_num = 0
        self.request_display()
        self.local_nod_lst = copy_lst_nodes(self.server_nod_lst)
        self.current_params_widget = "import"
        self.change_widget(self.current_params_widget)
        self.thrd_lst = []
        self.window.show()

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

                else:
                    self.clearLayout(item.layout())

    def clear_parent_list(self):
        try:
            only_one = int(self.new_node["parent_node_lst"][0])
            self.new_node["parent_node_lst"] = [only_one]
            self.parent_nums_lst = [only_one]
            self.local_nod_lst = copy_lst_nodes(self.server_nod_lst)
            self.add_new_node()

        except TypeError:
            print("should NOT clear parents from already combined experiments")

    def clicked_4_navigation(self, nod_num):
        self.current_lin_num = nod_num
        try:
            cur_nod = self.server_nod_lst[nod_num]
            self.display_log(nod_num)
            self.parent_nums_lst = [nod_num]

        except IndexError:
            print("nod_num ", nod_num, "not ran yet")
            cur_nod = self.local_nod_lst[nod_num]
            self.window.incoming_text.clear()
            self.window.incoming_text.insertPlainText("Ready to run ...")
            self.parent_nums_lst = []
            for par_nod_num in cur_nod["parent_node_lst"]:
                self.parent_nums_lst.append(int(par_nod_num))


        cmd_ini = cur_nod["cmd2show"][0]
        key2find = cmd_ini[6:]
        try:
            self.change_widget(key2find)

        except KeyError:
            print("command widget not there yet")
            return

        self.display()

    def clicked_4_combine(self, nod_num):
        prev_lst = self.parent_nums_lst
        print("\n prev_lst =", prev_lst)
        if nod_num in prev_lst:
            if len(prev_lst) > 1:
                new_par_lst = []
                for in_nod_num in prev_lst:
                    if in_nod_num != nod_num:
                        new_par_lst.append(in_nod_num)

                self.new_node["parent_node_lst"] = new_par_lst
                self.parent_nums_lst = new_par_lst

                for node in self.local_nod_lst:
                    for pos, in_nod_num in enumerate(node["child_node_lst"]):
                        if(
                            in_nod_num == self.current_lin_num and
                            node["lin_num"] == nod_num
                        ):
                            left = node["child_node_lst"][:pos]
                            right = node["child_node_lst"][pos+1:]
                            node["child_node_lst"] =  left + right

                self.display(self.local_nod_lst)

            else:
                print("not removing only parent node")

        else:
            self.parent_nums_lst.append(nod_num)
            self.new_node["parent_node_lst"] = list(self.parent_nums_lst)
            self.add_new_node()

        print("self.parent_nums_lst =", self.parent_nums_lst, "\n")

    def on_node_click(self, nod_num):
        if nod_num != self.current_lin_num:
            if(
                self.new_node is not None
                and
                self.new_node["cmd2show"][0] == "dials.combine_experiments"
                and
                self.new_node["status"] == "Ready"
                and
                self.window.NodeSelecCheck.checkState()
            ):
                self.clicked_4_combine(nod_num)

            else:
                self.clicked_4_navigation(nod_num)

        else:
            print("clicked current node, no need to do anything")

    def add_line(self, new_line, nod_lin_num):
        found_lin_num = False
        for log_node in self.lst_node_info_out:
            if log_node["lin_num"] == nod_lin_num:
                log_node["log_line_lst"].append(new_line[0:-1])
                found_lin_num = True

        if not found_lin_num:
            self.lst_node_info_out.append(
                {
                    "lin_num"       : nod_lin_num,
                    "log_line_lst"  : [new_line]
                }
            )

        if self.current_lin_num == nod_lin_num:
            self.window.incoming_text.moveCursor(QTextCursor.End)
            self.window.incoming_text.insertPlainText(new_line)
            self.window.incoming_text.moveCursor(QTextCursor.End)

    def item_param_changed(self, str_path, str_value):
        sender_twin = self.sender().twin_widg
        sender_twin.update_param(str_path, str_value)
        print("item paran changed")
        print("str_path, str_value: ", str_path, str_value)
        str_key = self.current_params_widget
        cmd2run = self.param_widgets[str_key]["main_cmd"]
        self.cmd_par.set_parameter(str_path, str_value)

    def display(self, in_lst_nodes = None):
        if in_lst_nodes is None:
            self.tree_scene.new_lin_num(self.current_lin_num)

        else:
            lst_str = self.tree_obj(lst_nod = in_lst_nodes)
            lst_2d_dat = self.tree_obj.get_tree_data()
            self.tree_scene.draw_tree_graph(lst_2d_dat, self.current_lin_num)

    def line_n1_in(self, lin_num_in):
        print("new busy node = ", lin_num_in)
        self.request_display()
        self.parent_nums_lst = [lin_num_in]

    def display_log(self, nod_lin_num = 0):
        found_lin_num = False
        for log_node in self.lst_node_info_out:
            if log_node["lin_num"] == nod_lin_num:
                found_lin_num = True
                lst_log_lines = log_node["log_line_lst"]

        if not found_lin_num:
            cmd = {"nod_lst":[nod_lin_num], "cmd_lst":["display_log"]}
            json_log = json_data_request(uni_url, cmd)
            lst_log_lines = json_log[0]
            self.lst_node_info_out.append(
                {
                    "lin_num"       : nod_lin_num,
                    "log_line_lst"  : lst_log_lines
                }
            )
        self.window.incoming_text.clear()
        for single_log_line in lst_log_lines:
            self.window.incoming_text.insertPlainText(single_log_line + "\n")
            self.window.incoming_text.moveCursor(QTextCursor.End)

    def reset_param(self):
        print("reset_param")
        str_key = self.current_params_widget
        self.param_widgets[str_key]["simple"].reset_pars()
        try:
            self.param_widgets[str_key]["advanced"].reset_pars()

        except AttributeError:
            print("No advanced pars")

        #TODO reset the variable "self.cmd_par"
        #self.cmd_par = CommandParamControl(self.new_node["cmd2show"][0])

    def change_widget(self, str_key):
        self.window.BoxControlWidget.setTitle(str_key)
        self.window.StackedParamsWidget.setCurrentWidget(
            self.param_widgets[str_key]["main_page"]
        )
        self.clearLayout(self.window.Next2RunLayout)
        self.update_nxt_butt(str_key)

    def check_nxt_btn(self):
        try:
            print("trying to << check_nxt_btn >> on node", self.current_lin_num)
            str_key = self.server_nod_lst[self.current_lin_num]["cmd2show"][0][6:]
            print("str_key =", str_key)
            self.update_nxt_butt(str_key)

        except AttributeError:
            print("NO current_lin_num (AttributeError)")

        except IndexError:
            print("NO current_lin_num (IndexError)")

    def update_nxt_butt(self, str_key):
        small_f_size = int(self.font_point_size * 0.85)
        small_font = QFont("OldEnglish", pointSize = small_f_size, italic=True)
        try:
            if self.server_nod_lst[self.current_lin_num]["status"] == "Succeeded":
                self.clearLayout(self.window.Next2RunLayout)
                self.window.Next2RunLayout.addStretch()
                for bt_labl in self.param_widgets[str_key]["nxt_widg_lst"]:
                    nxt_butt = QPushButton(bt_labl)
                    nxt_butt.cmd_str = bt_labl
                    nxt_butt.setFont(small_font)
                    nxt_butt.clicked.connect(self.nxt_clicked)
                    self.window.Next2RunLayout.addWidget(nxt_butt)

        except IndexError:
            print("no need to add next button")

    def add_new_node(self):
        self.local_nod_lst.append(self.new_node)
        for node in self.local_nod_lst:
            if node["lin_num"] in self.new_node["parent_node_lst"]:
                node["child_node_lst"].append(int(self.new_node["lin_num"]))

        self.display(self.local_nod_lst)
        self.cmd_par = CommandParamControl(self.new_node["cmd2show"][0])

    def request_display(self):
        print("\n request_display \n")
        cmd = {"nod_lst":"", "cmd_lst":["display"]}
        self.server_nod_lst = json_data_request(uni_url, cmd)
        if self.new_node is None:
            self.display(self.server_nod_lst)
            print("self.new_node is None")

        else:
            self.local_nod_lst = copy_lst_nodes(self.server_nod_lst)
            self.add_new_node()
            print("self.new_node =", self.new_node)

    def request_launch(self):
        cmd_str = self.cmd_par.get_full_command_string()
        print("\n cmd_str", cmd_str)
        nod_lst = self.parent_nums_lst
        lst_of_node_str = []
        for nod_num in nod_lst:
            lst_of_node_str.append(str(nod_num))

        cmd = {"nod_lst":lst_of_node_str, "cmd_lst":[cmd_str]}
        print("cmd =", cmd)
        self.window.incoming_text.clear()

        try:
            new_req_get = requests.get(uni_url, stream = True, params = cmd)
            #TODO make sure when client is relaunched,
            #TODO somehow it know about busy nodes
            new_thrd = Run_n_Output(new_req_get)
            new_thrd.new_line_out.connect(self.add_line)
            new_thrd.first_line.connect(self.line_n1_in)
            new_thrd.finished.connect(self.request_display)
            new_thrd.finished.connect(self.check_nxt_btn)
            new_thrd.start()
            self.thrd_lst.append(new_thrd)
            self.new_node = None

        except requests.exceptions.RequestException:
            print("something went wrong with the request launch")

    def launch_reindex(self, sol_rei):
        print("reindex solution", sol_rei)
        self.cmd_par.set_custom_parameter(str(sol_rei))

    def nxt_clicked(self):
        print("nxt_clicked")
        str_key = self.sender().cmd_str
        print("str_key: ", str_key)

        if str_key == "reindex":
            cmd = {"nod_lst":[self.current_lin_num], "cmd_lst":["get_bravais_sum"]}
            json_data_lst = json_data_request(uni_url, cmd)
            self.r_index_widg.add_opts_lst(
                json_data=json_data_lst[0]
            )

        self.local_nod_lst = copy_lst_nodes(self.server_nod_lst)
        par_lin_num = int(self.current_lin_num)
        max_lin_num = 0
        for node in self.local_nod_lst:
            if node["lin_num"] > max_lin_num:
                max_lin_num = node["lin_num"]

        self.current_lin_num = max_lin_num + 1

        self.new_node = {
            'lin_num': int(self.current_lin_num),
            'status': 'Ready',
            'cmd2show': ["dials." + str(str_key)],
            'child_node_lst': [],
            'parent_node_lst': [par_lin_num]
        }
        self.add_new_node()
        self.change_widget(str_key)
        self.current_params_widget = str_key
        self.window.incoming_text.clear()
        self.window.incoming_text.insertPlainText("Ready to run: ")

    def on_retry(self):
        print("on_retry")
        nod2clone = dict(self.server_nod_lst[int(self.current_lin_num)])
        str_key = str(nod2clone["cmd2show"][0][6:])
        print("str_key: ", str_key)
        #TODO put here the cloned parameters
        self.local_nod_lst = copy_lst_nodes(self.server_nod_lst)
        max_lin_num = 0
        for node in self.local_nod_lst:
            if node["lin_num"] > max_lin_num:
                max_lin_num = node["lin_num"]

        self.current_lin_num = max_lin_num + 1
        self.new_node = {
            'lin_num': int(self.current_lin_num),
            'status': 'Ready',
            'cmd2show': list(nod2clone["cmd2show"]),
            'child_node_lst': [],
            'parent_node_lst': list(nod2clone["parent_node_lst"])
        }
        self.add_new_node()
        self.window.incoming_text.clear()
        self.window.incoming_text.insertPlainText("Ready to run: ")

        self.change_widget(str_key)
        self.current_params_widget = str_key
        self.parent_nums_lst = []
        for par_nod_num in self.new_node["parent_node_lst"]:
            self.parent_nums_lst.append(int(par_nod_num))


    def req_stop(self):
        print("req_stop")
        self.window.incoming_text.clear()
        nod_lst = [str(self.current_lin_num)]
        print("\n nod_lst", nod_lst)
        cmd = {"nod_lst":nod_lst, "cmd_lst":["stop"]}
        print("cmd =", cmd)

        try:
            lst_params = json_data_request(uni_url, cmd)

        except requests.exceptions.RequestException:
            print("something went wrong with the request launch")


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    m_obj = MainObject()
    sys.exit(app.exec_())

