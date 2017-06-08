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
        tokens = { 'windows': '\r\n',
                   'mac'    : '\r',
                   'unix'   : '\n'}
        line_endings = self.view.settings().get('default_line_ending')
        rtnl = tokens.get(line_endings, '\n')
        original = self.view.substr( currentSelection )
        lines = filter(None, map(lambda s: s.rstrip(), original.split(rtnl)))  # strip the trailing spaces
        if surplus:
            rtnl *= 2
        output = rtnl.join(lines)
        self.view.replace( edit, currentSelection, output )

        return sublime.Region( currentSelection.begin(), currentSelection.begin() + len(output) )
