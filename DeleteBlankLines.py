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

        # Create an() edit object, demarcating an undo group.
        if (st_version == 2):
            edit = self.view.begin_edit()

        # Loop through user selections.
        for currentSelection in self.view.sel():
            # Strip blank lines
            newSelections.append( self.strip( edit, currentSelection, surplus ) )

        # Clear selections since they've been modified.
        self.view.sel().clear()

        for newSelection in newSelections:
            self.view.sel().add( newSelection )

        # A corresponding call to end_edit() is required.
        if (st_version == 2):
            self.view.end_edit( edit )

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
