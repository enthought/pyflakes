# (c) 2005 Divmod, Inc.  See LICENSE file for details

class Message(object):
    _message = ''
    level = 'N'
    severity = 0

    message = property(fget=lambda self: self._message % self.message_args)

    def __init__(self, filename, loc, use_column=True, message_args=()):
        self.filename = filename
        self.lineno = loc.lineno
        self.col = getattr(loc, 'col_offset', None) if use_column else None
        self.message_args = message_args 

    def __str__(self):
        if self.col is not None:
            return '%s:%s(%d): [%s] %s' % (self.filename, self.lineno, self.col, self.level, self._message % self.message_args)
        else:
            return '%s:%s: [%s] %s' % (self.filename, self.lineno, self.level, self._message % self.message_args)

class Warning(Message):
    level = 'W'
    severity = 0

class Error(Message):
    level = 'E'
    # All errors have the highest severity
    severity = 5

class UnusedImport(Warning):
    _message = '%r imported but unused'
    severity = 0

    def __init__(self, filename, loc, name):
        Warning.__init__(self, filename, loc, use_column=False, message_args=(name,))
        self.name = name

class RedefinedWhileUnused(Warning):
    _message = 'redefinition of unused %r from line %r'
    severity = 1

    def __init__(self, filename, loc, name, orig_loc):
        Warning.__init__(self, filename, loc, message_args=(name, orig_loc.lineno))
        self.name = name
        self.orig_loc = orig_loc

class ImportShadowedByLoopVar(Warning):
    _message = 'import %r from line %r shadowed by loop variable'
    severity = 2

    def __init__(self, filename, loc, name, orig_loc):
        Warning.__init__(self, filename, loc, message_args=(name, orig_loc.lineno))
        self.name = name
        self.orig_loc = orig_loc

class ImportStarUsed(Warning):
    _message = "'from %s import *' used; unable to detect undefined names"
    severity = 0

    def __init__(self, filename, loc, modname):
        Warning.__init__(self, filename, loc, message_args=(modname,))
        self.name = modname

class UndefinedName(Error):
    _message = 'undefined name %r'

    def __init__(self, filename, loc, name):
        Error.__init__(self, filename, loc, message_args=(name,))
        self.name = name

class UndefinedExport(Error):
    _message = 'undefined name %r in __all__'

    def __init__(self, filename, loc, name):
        Error.__init__(self, filename, loc, message_args=(name,))
        self.name = name

class UndefinedLocal(Error):
    _message = "local variable %r (defined in enclosing scope on line %r) referenced before assignment"

    def __init__(self, filename, loc, name, orig_loc):
        Error.__init__(self, filename, loc, message_args=(name, orig_loc.lineno))
        self.name = name
        self.orig_loc = orig_loc

class DuplicateArgument(Error):
    _message = 'duplicate argument %r in function definition'

    def __init__(self, filename, loc, name):
        Error.__init__(self, filename, loc, message_args=(name,))
        self.name = name

class RedefinedFunction(Warning):
    _message = 'redefinition of function %r from line %r'
    severity = 2

    def __init__(self, filename, loc, name, orig_loc):
        Warning.__init__(self, filename, loc, message_args=(name, orig_loc.lineno))
        self.name = name
        self.orig_loc = orig_loc

class CouldNotCompile(Error):
    def __init__(self, filename, loc, msg=None, line=None):
        if msg and line:
            self._message = 'could not compile: %s\n%s'
            message_args = (msg, line)
        elif msg:
            self._message = 'could not compile: %s'
            message_args = (msg,)
        else:
            self._message = 'could not compile'
            message_args = ()
        Error.__init__(self, filename, loc, message_args=message_args)
        self.msg = msg
        self.line = line

class LateFutureImport(Warning):
    severity = 1
    _message = 'future import(s) %r after other statements'

    def __init__(self, filename, loc, names):
        Warning.__init__(self, filename, loc, message_args=(names,))
        self.names = names

class UnusedVariable(Warning):
    """
    Indicates that a variable has been explicity assigned to but not actually
    used.
    """

    _message = 'local variable %r is assigned to but never used'
    severity = 3

    def __init__(self, filename, loc, name):
        Warning.__init__(self, filename, loc, message_args=(name,))
        self.name = name
