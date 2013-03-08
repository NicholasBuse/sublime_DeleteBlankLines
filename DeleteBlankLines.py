import sublime, sublime_plugin, re

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
        original = self.view.substr( currentSelection );

        output_last = original
        while (True):
            if (surplus):
                output = self.delete_surplus_blank_lines( output_last )
            else:
                output = self.delete_blank_lines( output_last )

            if (output == output_last):
                break
            else:
                output_last = output

        self.view.replace( edit, currentSelection, output )

        return sublime.Region( currentSelection.begin(), currentSelection.begin() + len(output) )

    def delete_blank_lines(self, string):
        line_endings = self.view.settings().get('default_line_ending')
        if line_endings == 'windows':
            string = string.replace('\r\n\r\n', '\r\n')
        elif line_endings == 'mac':
            string = string.replace('\r\r', '\r')
        else: # unix
            string = string.replace('\n\n', '\n')
        return string

    def delete_surplus_blank_lines(self, string):
        line_endings = self.view.settings().get('default_line_ending')
        if line_endings == 'windows':
            string = string.replace('\r\n\r\n\r\n', '\r\n\r\n')
        elif line_endings == 'mac':
            string = string.replace('\r\r\r', '\r\r')
        else: # unix
            string = string.replace('\n\n\n', '\n\n')
        return string
