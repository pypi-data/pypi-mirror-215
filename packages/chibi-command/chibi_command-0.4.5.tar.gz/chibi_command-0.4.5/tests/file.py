from unittest import TestCase

from chibi_command.file import Tar


class Test_tar( TestCase ):
    def test_should_return_the_preview_expected( self ):
        expected = 'tar -v -x -f file.tar -C /tmp/'
        command = Tar.verbose().extract().file( 'file.tar' )
        command = command.output_directory( '/tmp/' )
        self.assertEqual( command.preview(), expected )

    def test_create_new_archive_should_be_the_expected( self ):
        expected = 'tar -v -c -f file.tar /tmp/'
        command = Tar.verbose().create().file( 'file.tar' )
        command = command.input_directory( '/tmp/' )
        self.assertEqual( command.preview(), expected )
