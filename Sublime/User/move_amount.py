import sublime
import sublime_plugin

class MoveAmountCommand(sublime_plugin.TextCommand):
    def run(self, edit, amount=1, **kwargs):
        for _ in range(amount):
            self.view.run_command("move", args=kwargs)

class JumpVerticalCommand(sublime_plugin.TextCommand):
    def IsValid(self, row, col):
        return (row, col) == self.view.rowcol(self.view.text_point(row, col))

    def SetPos(self, row, col):
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(self.view.text_point(row, col)))
        self.view.show(self.view.text_point(row, col))

    def run(self, edit, up):
        if len(self.view.sel()) != 1: # multi selection is not supported yet
            return
        sel_section = self.view.sel()[0]
        #if not sel_section.empty(): # works for empty selection only
        #    return

        row_inc = -1 if up else 1
        row_col = self.view.rowcol(sel_section.begin())
        row = row_col[0]
        start_row = row

        last_valid_row = row
        prev_valid = True
        col = row_col[1]

        while True:
            row += row_inc
            if not self.IsValid(row, 0):
                break
            valid = self.IsValid(row, col)
            if not valid and prev_valid and (row != start_row + row_inc):
                break

            if valid:
                last_valid_row = row
            prev_valid = valid

        if last_valid_row != start_row:
            self.SetPos(last_valid_row, col)
