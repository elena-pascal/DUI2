import json

def print_list(main_obj):
    lst_nod = []
    for uni in main_obj.step_list:
        if uni.lst2run == []:
            cmd2show = ["None"]

        else:
            cmd2show = uni.lst2run[0]

        node = {"lin_num"           :uni.lin_num,
                "status"            :uni.status,
                "cmd2show"           :cmd2show,
                "next_step_list"    :uni.next_step_list}

        lst_nod.append(node)

    return lst_nod


class TreeShow(object):
    def __init__(self):
        self.ind_spc = "      "
        self.ind_lin = "------"

    def __call__(self, current_line = None, lst_nod = None):
        self.lst_nod = lst_nod

        self.lst_out = []
        self.lst_out.append("")
        self.lst_out.append("status: (R)eady  (B)usy  (F)ailed  (S)ucceeded")
        self.lst_out.append(" | ")
        self.lst_out.append(" |  line number ")
        self.lst_out.append(" |   | ")
        self.lst_out.append(" |   |  command ")
        self.lst_out.append(" |   |   | ")
        self.lst_out.append("--------------------------")

        self.max_indent = 0
        self.str_lst = []
        self._add_tree(step = self.lst_nod[0], indent=0)
        self._output_connect(current_line)

    def _add_tree(self, step=None, indent=None):
        if step["status"] == "Succeeded":
            stp_prn = " S "

        elif step["status"] == "Failed":
            stp_prn = " F "

        elif step["status"] == "Busy":
            stp_prn = " B "

        else:
            stp_prn = " R "

        str_lin_num = "{0:3}".format(int(step["lin_num"]))
        stp_prn += str_lin_num + self.ind_spc * indent + r"   \___"

        stp_prn += str(step["cmd2show"][0]) + "     "

        self.str_lst.append([stp_prn, indent, int(step["lin_num"])])
        new_indent = indent

        if len(step["next_step_list"]) > 0:
            for nxt_stp_lin_num in step["next_step_list"]:
                new_indent = indent + 1
                for node in self.lst_nod:
                    if nxt_stp_lin_num == node["lin_num"]:
                        self._add_tree(step=node, indent=new_indent)

        else:
            new_indent = int(new_indent)
            if new_indent > self.max_indent:
                self.max_indent = new_indent

    def _output_connect(self, current_line):
        tree_str_dat = []
        for tmp_lst in self.str_lst:
            tree_str_dat.append(tmp_lst)

        for pos, loc_lst in enumerate(tree_str_dat):
            if pos > 0:
                if loc_lst[1] < tree_str_dat[pos - 1][1]:
                    for up_pos in range(pos - 1, 0, -1):
                        pos_in_str = loc_lst[1] * len(self.ind_spc) + 9
                        left_side = tree_str_dat[up_pos][0][0:pos_in_str]
                        right_side = tree_str_dat[up_pos][0][pos_in_str + 1 :]
                        if tree_str_dat[up_pos][1] > loc_lst[1]:
                            tree_str_dat[up_pos][0] = left_side + "|" + right_side

                        elif tree_str_dat[up_pos][1] == loc_lst[1]:
                            break

            if loc_lst[2] == current_line:
                lng = len(self.ind_spc) * self.max_indent + 22
                lng_lft = lng - len(tree_str_dat[pos][0])
                str_here = lng_lft * " "
                tree_str_dat[pos][0] += str_here + "  <<< here "

        for prn_str in tree_str_dat:
            self.lst_out.append(prn_str[0])

        self.lst_out.append("---------------------" + self.max_indent * self.ind_lin)

    def print_output(self):
        for prn_str in self.lst_out:
            print(prn_str)

