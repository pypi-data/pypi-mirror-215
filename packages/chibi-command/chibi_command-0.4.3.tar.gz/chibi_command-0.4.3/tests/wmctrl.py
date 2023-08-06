from unittest import TestCase
from chibi_command.wmctrl import (
    Wmctrl, Wmctrl_list, Wmctrl_window, Wmctrl_desktop, Wmctrl_desktop_obj
)


class Test_wmctrl( TestCase ):

    def test_should_return_wmctrl_list( self ):
        result = Wmctrl.list().run()
        self.assertIsInstance( result, Wmctrl_list )

    def test_the_list_should_be_wmctrl_windows( self ):
        result = Wmctrl.list().run()
        for window in result:
            self.assertIsInstance( window, Wmctrl_window )

    def test_the_destops_should_be_wmctrl_desktop( self ):
        result = Wmctrl.desktop().run()
        self.assertIsInstance( result, Wmctrl_desktop )

    def test_the_destops_should_be_wmctrl_desktop_obj( self ):
        result = Wmctrl.desktop().run()
        for window in result:
            self.assertIsInstance( window, Wmctrl_desktop_obj )

    def test_select_should_add_the_parameters( self ):
        result = Wmctrl.select( '0x04e00003' )
        expected = "wmctrl -i -r 0x04e00003"
        self.assertEqual( result.preview(), expected )

    def test_toggle_should_add_the_parameters( self ):
        result = Wmctrl.select( '0x04e00003' ).toggle(
            'maximized_vert', 'maximized_horz' )
        expected = (
            "wmctrl -i -r 0x04e00003 -b "
        "toggle,maximized_vert,maximized_horz" )
        self.assertEqual( result.preview(), expected )


class Test_wmctrl_desktop_obj( TestCase ):
    def setUp( self ):
        r = "0  * DG: 5464x3072  VP: 2732,0  WA: 0,31 1366x737  principal"
        r = r.split( maxsplit=9 )
        self.example = Wmctrl_desktop_obj( *r )

    def test_columns_should_be_4( self ):
        self.assertEqual( self.example.columns, 4 )

    def test_rows_should_be_4( self ):
        self.assertEqual( self.example.rows, 4 )

    def test_current_columns_should_be_2( self ):
        self.assertEqual( self.example.current_column, 2 )

    def test_current_rows_should_be_2( self ):
        self.assertEqual( self.example.current_row, 0 )


class Test_wmctrl_window( TestCase ):
    def setUp( self ):
        r = ( "0x04a00003  0 130371 -5120 43   2560 1397 "
        "termite.Termite       lise-meitner dem4ply@lise-meitner:"
        "~/Documentos/proyectos/work/shneider/mercury_gates_xml_parser_py" )
        r = r.split( maxsplit=9 )
        self.example_move = Wmctrl_window( *r )

        r = ( "0x04a00003  -1 130371 -5120 43   2560 1397 "
        "termite.Termite       lise-meitner dem4ply@lise-meitner:"
        "~/Documentos/proyectos/work/shneider/mercury_gates_xml_parser_py" )
        r = r.split( maxsplit=9 )
        self.example_cannot_move = Wmctrl_window( *r )

    def test_can_move_is_correct( self ):
        self.assertTrue( self.example_move.can_move )
        self.assertFalse( self.example_cannot_move.can_move )
