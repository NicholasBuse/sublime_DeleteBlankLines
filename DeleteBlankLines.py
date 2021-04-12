import sublime
import sublime_plugin

st_version = 2

# Warn about out-dated versions of ST3
if sublime.version() == '':
    st_version = 3
    print('Package Control: Please upgrade to Sublime Text 3 build 3012 or newer')

elif int(sublime.version()) > 3000:
    st_version = 3


class DeleteBlankLinesCommand( sublime_plugin.TextCommand ):
    def run( self, edit, surplus=False):
        newSelections = []

        col, row = self.view.viewport_position()

        settings = sublime.load_settings('DeleteBlankLines.sublime-settings')

        # Create an() edit object, demarcating an undo group.
        if (st_version == 2):
            edit = self.view.begin_edit()

        # If there is no (empty) selection, operate on the whole file.
        #     else, operate only on each selection (update the selection for changes)
        if len(self.view.sel()) == 1 and self.view.substr(self.view.sel()[0]) == "":
            if (settings and
                settings.has('operate_on_whole_file_when_selection_empty') and
                settings.get("operate_on_whole_file_when_selection_empty") is True):
                self.strip( edit, sublime.Region(0, self.view.size()), surplus )
        else:
            # Loop through user selections.
            for currentSelection in self.view.sel():
                # Strip blank lines
                newSelections.append( self.strip( edit, currentSelection, surplus ) )

            # Clear selections since they've been modified.
            self.view.sel().clear()

            for newSelection in newSelections:
                self.view.sel().add( newSelection )
        # END: if len()...

        # A corresponding call to end_edit() is required.
        if (st_version == 2):
            self.view.end_edit( edit )

        self.view.set_viewport_position([0, row])

    def strip( self, edit, currentSelection, surplus ):
        # Convert the input range to a string, this represents the original selection.
        orig  = self.view.substr(currentSelection)
        lines = orig.splitlines()

        i = 0
        haveBlank = False

        while i < len(lines)-1:
            if lines[i].rstrip() == '':
                if not surplus or haveBlank:
                    del lines[i]
                else:
                    i += 1
                haveBlank = True
            else:
                haveBlank = False
                i += 1
            # END: if not surplus
        # END: while

        output = '\n'.join(lines)

        self.view.replace( edit, currentSelection, output )

        return sublime.Region( currentSelection.begin(), currentSelection.begin() + len(output) )


class DeleteBlankLines(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        settings = sublime.load_settings('DeleteBlankLines.sublime-settings')
        if settings:
            if (settings.has('delete_surplus_blank_lines_on_save') and
                settings.get("delete_surplus_blank_lines_on_save") is True):
                view.run_command("delete_blank_lines", { "surplus": True })

            elif (settings.has('delete_blank_lines_on_save') and
                  settings.get("delete_blank_lines_on_save") is True):
                view.run_command("delete_blank_lines")

