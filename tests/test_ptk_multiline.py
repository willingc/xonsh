# -*- coding: utf-8 -*-
"""Tests sample inputs to PTK multiline and checks parser response"""
import nose
from nose.tools import assert_equal, with_setup
from unittest.mock import MagicMock, patch

from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.document import Document
from prompt_toolkit.buffer import Buffer, AcceptAction
from xonsh.environ import Env

def setup():
    global indent_
    global buffer
    global bufaccept
    global cli
    global carriage_return
    global builtins
    
    import builtins

    builtins.__xonsh_env__ = Env()
    builtins.__xonsh_env__['INDENT'] = '    '

    from xonsh.ptk.key_bindings import carriage_return

    indent_ = '    '
    buffer = Buffer()
    bufaccept = MagicMock(name='accept', spec=AcceptAction)
    cli = MagicMock(name='cli', spec=CommandLineInterface)
    buffer.accept_action = bufaccept

def teardown():
    global indent_
    global buffer
    global bufaccept
    global cli
    global carriage_return
    global builtins
    
    del indent_
    del buffer
    del bufaccept
    del cli
    del carriage_return
    del builtins

def test_colon_indent():
    document = Document('for i in range(5):')
    buffer.set_document(document)
    carriage_return(buffer, cli)
    assert_equal(buffer.document.current_line, indent_)

def test_dedent():
    document = Document(indent_+'pass')
    buffer.set_document(document)
    carriage_return(buffer, cli)
    assert_equal(buffer.document.current_line, '')

    document = Document(2*indent_+'continue')
    buffer.set_document(document)
    carriage_return(buffer, cli)
    assert_equal(buffer.document.current_line,indent_)

def test_continuation_line():
    document = Document('\nsecond line')
    buffer.set_document(document)
    carriage_return(buffer, cli)
    assert_equal(buffer.document.current_line, '')

def test_trailing_slash():
    document = Document('this line will \\')
    buffer.set_document(document)
    carriage_return(buffer, cli)
    assert_equal(buffer.document.current_line, '')

def test_cant_compile_newline():
    mock = MagicMock(return_value = False)
    with patch('xonsh.ptk.key_bindings.can_compile', mock):
        document = Document('for i in (1, 2, ')
        buffer.set_document(document)
        carriage_return(buffer, cli)
        assert_equal(buffer.document.current_line, '')

def test_can_compile_and_executes():
    mock = MagicMock(return_value = True)
    with patch('xonsh.ptk.key_bindings.can_compile', mock):
        document = Document('ls')
        buffer.set_document(document)
        carriage_return(buffer, cli)
        assert bufaccept.mock_calls is not None

if __name__ == '__main__':
    nose.runmodule()
