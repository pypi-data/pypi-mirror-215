("Hissp's bundled macros.\n"
 '\n'
 'To help keep macro definitions and expansions manageable in complexity,\n'
 'these macros lack some of the extra features their equivalents have in\n'
 'Python or in other Lisps. These are not intended to be a standard\n'
 'library for general use, but do bring Hissp up to a basic standard of\n'
 'utility without adding dependencies, which may suffice in some cases.\n'
 '\n'
 'Because of certain deliberate restrictions in design, there are no\n'
 'dependencies in their expansions either, meaning compiled Hissp code\n'
 'utilizing the bundled macros need not have Hissp installed to work, only\n'
 'the Python standard library. All helper code must therefore be inlined,\n'
 'resulting in larger expansions than might otherwise be necessary.\n'
 '\n'
 'They also have no prerequisite initialization, beyond what is available\n'
 'in a standard Python module. For example, a ``_macro_`` namespace need\n'
 "not be available for ``defmacro``. It's smart enough to check for the\n"
 'presence of ``_macro_`` (at compile time) in its expansion context, and\n'
 'inline the initialization code when required.\n'
 '\n'
 'As a convenience, the bundled macros are automatically made available\n'
 'unqualified in the Lissp REPL, but this does not apply to modules. A\n'
 'Hissp module with better alternatives need not use the bundled macros at\n'
 'all.\n'
 '\n'
 'They also eschew any expansions of subexpressions to non-atomic Python\n'
 'code strings, relying only on the built-in special forms ``quote`` and\n'
 '``lambda``, which makes their expansions compatible with advanced\n'
 'rewriting macros that process the Hissp expansions of other macros. (`[#\n'
 '<QzLSQB_QzHASH_>` is something of an exception, as one subexpression is\n'
 'written in Python to begin with.) Note that this need not apply to\n'
 'inlined helper functions that contain no user code. `if-else\n'
 '<ifQz_else>` is one such example, expanding to a lambda containing a\n'
 'Python `conditional expression<if_expr>`, immediately called with the\n'
 'subexpressions as arguments.\n')

globals().update(
  _macro_=__import__('types').ModuleType(
            ('{}._macro_').format(
              __name__)))

__import__('operator').setitem(
  __import__('sys').modules,
  _macro_.__name__,
  _macro_)

setattr(
  _macro_,
  'defmacro',
  (lambda name,parameters,docstring,*body:
    (lambda * _: _)(
      (lambda * _: _)(
        'lambda',
        (lambda * _: _)(
          ':',
          '_Qz643R6CNUz_G',
          (lambda * _: _)(
            'lambda',
            parameters,
            *body)),
        (lambda * _: _)(
          'builtins..setattr',
          '_Qz643R6CNUz_G',
          (lambda * _: _)(
            'quote',
            '__doc__'),
          docstring),
        (lambda * _: _)(
          'builtins..setattr',
          '_Qz643R6CNUz_G',
          (lambda * _: _)(
            'quote',
            '__qualname__'),
          (lambda * _: _)(
            '.join',
            "('.')",
            (lambda * _: _)(
              'quote',
              (lambda * _: _)(
                '_macro_',
                name)))),
        (lambda * _: _)(
          'builtins..setattr',
          'hissp.macros.._macro_',
          (lambda * _: _)(
            'quote',
            name),
          '_Qz643R6CNUz_G')))))

# defmacro
(lambda _Qz643R6CNUz_G=(lambda test,consequent,alternate:
  (lambda * _: _)(
    (lambda * _: _)(
      'lambda',
      'bca',
      'c()if b else a()'),
    test,
    (lambda * _: _)(
      'lambda',
      ':',
      consequent),
    (lambda * _: _)(
      'lambda',
      ':',
      alternate))):(
  __import__('builtins').setattr(
    _Qz643R6CNUz_G,
    '__doc__',
    ('``if-else`` Basic ternary branching construct.\n'
     '\n'
     "  Like Python's conditional expressions, the 'else' clause is required.\n"
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     "     #> (any-map c 'ab\n"
     "     #..  (if-else (op#eq c 'b)            ;ternary conditional\n"
     "     #..    (print 'Yes)\n"
     "     #..    (print 'No)))\n"
     '     >>> # anyQz_map\n'
     "     ... __import__('builtins').any(\n"
     "     ...   __import__('builtins').map(\n"
     '     ...     (lambda c:\n'
     '     ...       # ifQz_else\n'
     '     ...       (lambda b,c,a:c()if b else a())(\n'
     "     ...         __import__('operator').eq(\n"
     '     ...           c,\n'
     "     ...           'b'),\n"
     '     ...         (lambda :\n'
     '     ...           print(\n'
     "     ...             'Yes')),\n"
     '     ...         (lambda :\n'
     '     ...           print(\n'
     "     ...             'No')))),\n"
     "     ...     'ab'))\n"
     '     No\n'
     '     Yes\n'
     '     False\n'
     '\n'
     '  See also: `when`, `cond`, `any-map <anyQz_map>`, `if_expr`.\n'
     '  ')),
  __import__('builtins').setattr(
    _Qz643R6CNUz_G,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'ifQz_else',))),
  __import__('builtins').setattr(
    __import__('builtins').globals()['_macro_'],
    'ifQz_else',
    _Qz643R6CNUz_G))[-1])()

# defmacro
(lambda _Qz643R6CNUz_G=(lambda *body:
  (lambda * _: _)(
    (lambda * _: _)(
      'lambda',
      ':',
      *body))):(
  __import__('builtins').setattr(
    _Qz643R6CNUz_G,
    '__doc__',
    ('Evaluates each body expression in sequence (for side effects),\n'
     '  resulting in the value of the last (or ``()`` if empty).\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> (print (progn (print 1)             ;Sequence for side effects, eval '
     'to last.\n'
     '     #..              (print 2)\n'
     '     #..              3))\n'
     '     >>> print(\n'
     '     ...   # progn\n'
     '     ...   (lambda :(\n'
     '     ...     print(\n'
     '     ...       (1)),\n'
     '     ...     print(\n'
     '     ...       (2)),\n'
     '     ...     (3))[-1])())\n'
     '     1\n'
     '     2\n'
     '     3\n'
     '\n'
     '  See also: `prog1`, `Expression statements <exprstmts>`.\n'
     '  ')),
  __import__('builtins').setattr(
    _Qz643R6CNUz_G,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'progn',))),
  __import__('builtins').setattr(
    __import__('builtins').globals()['_macro_'],
    'progn',
    _Qz643R6CNUz_G))[-1])()

# defmacro
(lambda _Qz643R6CNUz_G=(lambda condition,*body:
  (lambda * _: _)(
    (lambda * _: _)(
      'lambda',
      'bc',
      'c()if b else()'),
    condition,
    (lambda * _: _)(
      'lambda',
      ':',
      *body))):(
  __import__('builtins').setattr(
    _Qz643R6CNUz_G,
    '__doc__',
    ('When the condition is true,\n'
     '  evaluates each expression in sequence for side effects,\n'
     '  resulting in the value of the last.\n'
     '  Otherwise, skips them and returns ``()``.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     "     #> (any-map c 'abcd\n"
     '     #..  (print c)\n'
     "     #..  (when (op#eq c 'b)\n"
     "     #..    (print 'found)\n"
     '     #..    :break))\n'
     '     >>> # anyQz_map\n'
     "     ... __import__('builtins').any(\n"
     "     ...   __import__('builtins').map(\n"
     '     ...     (lambda c:(\n'
     '     ...       print(\n'
     '     ...         c),\n'
     '     ...       # when\n'
     '     ...       (lambda b,c:c()if b else())(\n'
     "     ...         __import__('operator').eq(\n"
     '     ...           c,\n'
     "     ...           'b'),\n"
     '     ...         (lambda :(\n'
     '     ...           print(\n'
     "     ...             'found'),\n"
     "     ...           ':break')[-1])))[-1]),\n"
     "     ...     'abcd'))\n"
     '     a\n'
     '     b\n'
     '     found\n'
     '     True\n'
     '\n'
     '  See also: `if-else<ifQz_else>`, `unless`, `if`.\n'
     '  ')),
  __import__('builtins').setattr(
    _Qz643R6CNUz_G,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'when',))),
  __import__('builtins').setattr(
    __import__('builtins').globals()['_macro_'],
    'when',
    _Qz643R6CNUz_G))[-1])()

# defmacro
(lambda _Qz643R6CNUz_G=(lambda condition,*body:
  (lambda * _: _)(
    (lambda * _: _)(
      'lambda',
      'ba',
      '()if b else a()'),
    condition,
    (lambda * _: _)(
      'lambda',
      ':',
      *body))):(
  __import__('builtins').setattr(
    _Qz643R6CNUz_G,
    '__doc__',
    ('Unless the condition is true,\n'
     '  evaluates each expression in sequence for side effects,\n'
     '  resulting in the value of the last.\n'
     '  Otherwise, skips them and returns ``()``.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     "     #> (any-map c 'abcd\n"
     "     #..  (unless (op#eq c 'b)\n"
     '     #..    (print c)))\n'
     '     >>> # anyQz_map\n'
     "     ... __import__('builtins').any(\n"
     "     ...   __import__('builtins').map(\n"
     '     ...     (lambda c:\n'
     '     ...       # unless\n'
     '     ...       (lambda b,a:()if b else a())(\n'
     "     ...         __import__('operator').eq(\n"
     '     ...           c,\n'
     "     ...           'b'),\n"
     '     ...         (lambda :\n'
     '     ...           print(\n'
     '     ...             c)))),\n'
     "     ...     'abcd'))\n"
     '     a\n'
     '     c\n'
     '     d\n'
     '     False\n'
     '\n'
     '  See also: `when`.\n'
     '  ')),
  __import__('builtins').setattr(
    _Qz643R6CNUz_G,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'unless',))),
  __import__('builtins').setattr(
    __import__('builtins').globals()['_macro_'],
    'unless',
    _Qz643R6CNUz_G))[-1])()

# defmacro
(lambda _Qz643R6CNUz_G=(lambda pairs,*body:
  (lambda * _: _)(
    (lambda * _: _)(
      'lambda',
      (lambda * _: _)(
        ':',
        *pairs),
      *body))):(
  __import__('builtins').setattr(
    _Qz643R6CNUz_G,
    '__doc__',
    ('Creates local variables. Pairs are implied by position.\n'
     '\n'
     '  Locals are not in scope until the body.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     "     #> (let (x 'a                          ;Create locals.\n"
     "     #..      y 'b )                        ;Any number of pairs.\n"
     '     #..  (print x y)\n'
     "     #..  (let (x 'x\n"
     '     #..        y (op#concat x x))          ;Not in scope until body.\n'
     '     #..    (print x y))                    ;Outer variables shadowed.\n'
     '     #..  (print x y))                      ;Inner went out of scope.\n'
     '     >>> # let\n'
     "     ... (lambda x='a',y='b':(\n"
     '     ...   print(\n'
     '     ...     x,\n'
     '     ...     y),\n'
     '     ...   # let\n'
     "     ...   (lambda x='x',y=__import__('operator').concat(\n"
     '     ...     x,\n'
     '     ...     x):\n'
     '     ...     print(\n'
     '     ...       x,\n'
     '     ...       y))(),\n'
     '     ...   print(\n'
     '     ...     x,\n'
     '     ...     y))[-1])()\n'
     '     a b\n'
     '     x aa\n'
     '     a b\n'
     '\n'
     '  See also: `let-from<letQz_from>`, `my#<myQzHASH_>`, `locals`.\n'
     '  ')),
  __import__('builtins').setattr(
    _Qz643R6CNUz_G,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'let',))),
  __import__('builtins').setattr(
    __import__('builtins').globals()['_macro_'],
    'let',
    _Qz643R6CNUz_G))[-1])()

# defmacro
(lambda _Qz643R6CNUz_G=(lambda name,parameters,docstring=(),*body:
  # let
  (lambda QzDOLR_fn='_QzX3UIMF7Uz_fn':
    # let
    (lambda fn=(lambda * _: _)(
      'lambda',
      parameters,
      docstring,
      *body),ns=# unless
    (lambda b,a:()if b else a())(
      __import__('operator').contains(
        __import__('hissp.compiler',fromlist='?').NS.get(),
        '_macro_'),
      (lambda :
        (lambda * _: _)(
          (lambda * _: _)(
            '.update',
            (lambda * _: _)(
              'builtins..globals'),
            ':',
            'hissp.macros.._macro_',
            (lambda * _: _)(
              'types..ModuleType',
              (lambda * _: _)(
                'quote',
                '_macro_')))))),dc=# when
    (lambda b,c:c()if b else())(
      __import__('hissp.reader',fromlist='?').is_hissp_string(
        docstring),
      (lambda :
        (lambda * _: _)(
          (lambda * _: _)(
            'builtins..setattr',
            QzDOLR_fn,
            (lambda * _: _)(
              'quote',
              '__doc__'),
            docstring)))),qn=(lambda * _: _)(
      'builtins..setattr',
      QzDOLR_fn,
      (lambda * _: _)(
        'quote',
        '__qualname__'),
      (lambda * _: _)(
        '.join',
        "('.')",
        (lambda * _: _)(
          'quote',
          (lambda * _: _)(
            '_macro_',
            name)))):
      (lambda * _: _)(
        'hissp.macros.._macro_.let',
        (lambda * _: _)(
          QzDOLR_fn,
          fn),
        *ns,
        *dc,
        qn,
        (lambda * _: _)(
          'builtins..setattr',
          (lambda * _: _)(
            'operator..getitem',
            (lambda * _: _)(
              'builtins..globals'),
            (lambda * _: _)(
              'quote',
              '_macro_')),
          (lambda * _: _)(
            'quote',
            name),
          QzDOLR_fn)))())()):(
  __import__('builtins').setattr(
    _Qz643R6CNUz_G,
    '__doc__',
    ('Creates a new macro for the current module.\n'
     '\n'
     "  If there's no local ``_macro_`` namespace (at compile time), creates\n"
     "  one using `types.ModuleType` (at runtime). If there's a docstring,\n"
     "  stores it as the new lambda's ``__doc__``. Adds the ``_macro_`` prefix\n"
     "  to the lambda's ``__qualname__``. Saves the lambda in ``_macro_``\n"
     '  using the given attribute name.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> (defmacro p123 (sep)\n'
     '     #..  <<#;Prints 1 2 3 with the given separator\n'
     '     #..  `(print 1 2 3 : sep ,sep))\n'
     '     >>> # defmacro\n'
     '     ... # hissp.macros.._macro_.let\n'
     '     ... (lambda _QzAW22OE5Kz_fn=(lambda sep:(\n'
     "     ...   'Prints 1 2 3 with the given separator',\n"
     '     ...   (lambda * _: _)(\n'
     "     ...     'builtins..print',\n"
     '     ...     (1),\n'
     '     ...     (2),\n'
     '     ...     (3),\n'
     "     ...     ':',\n"
     "     ...     '__main__..sep',\n"
     '     ...     sep))[-1]):(\n'
     "     ...   __import__('builtins').setattr(\n"
     '     ...     _QzAW22OE5Kz_fn,\n'
     "     ...     '__doc__',\n"
     "     ...     'Prints 1 2 3 with the given separator'),\n"
     "     ...   __import__('builtins').setattr(\n"
     '     ...     _QzAW22OE5Kz_fn,\n'
     "     ...     '__qualname__',\n"
     "     ...     ('.').join(\n"
     "     ...       ('_macro_',\n"
     "     ...        'p123',))),\n"
     "     ...   __import__('builtins').setattr(\n"
     "     ...     __import__('operator').getitem(\n"
     "     ...       __import__('builtins').globals(),\n"
     "     ...       '_macro_'),\n"
     "     ...     'p123',\n"
     '     ...     _QzAW22OE5Kz_fn))[-1])()\n'
     '\n'
     '     #> (p123 ::)\n'
     '     >>> # p123\n'
     "     ... __import__('builtins').print(\n"
     '     ...   (1),\n'
     '     ...   (2),\n'
     '     ...   (3),\n'
     "     ...   sep='::')\n"
     '     1::2::3\n'
     '\n'
     '  See also:\n'
     '  `<\\<# <QzLT_QzLT_QzHASH_>`, `attach`,\n'
     '  `lambda <hissp.compiler.Compiler.function>`.\n'
     '  ')),
  __import__('builtins').setattr(
    _Qz643R6CNUz_G,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'defmacro',))),
  __import__('builtins').setattr(
    __import__('builtins').globals()['_macro_'],
    'defmacro',
    _Qz643R6CNUz_G))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda comment:
  (lambda * _: _)(
    'quote',
    comment.contents())):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'QzLT_QzLT_QzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'QzLT_QzLT_QzHASH_',
    _QzX3UIMF7Uz_fn))[-1])()

setattr(
  _macro_.QzLT_QzLT_QzHASH_,
  '__doc__',
  ("``<<#`` 'comment string' reader macro.\n"
   '\n'
   'Converts a block of line comments to a raw string.\n'
   '\n'
   '.. code-block:: REPL\n'
   '\n'
   '   #> <<#\n'
   "   #..;; You won't have to\n"
   '   #..;; escape the "quotes".\n'
   '   #..\n'
   '   >>> \'You won\\\'t have to\\nescape the "quotes".\'\n'
   '   \'You won\\\'t have to\\nescape the "quotes".\'\n'
   '\n'
   'See also: `triple-quoted string`.\n'))

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda name,value:(
  ('Assigns a global the value in the current module.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   "     #> (define SPAM 'tomato)\n"
   '     >>> # define\n'
   "     ... __import__('builtins').globals().update(\n"
   "     ...   SPAM='tomato')\n"
   '\n'
   '     #> SPAM\n'
   '     >>> SPAM\n'
   "     'tomato'\n"
   '\n'
   '  See also:\n'
   '  `globals`, `dict.update`, `defonce`, `def`, `assignment`, `global`.\n'
   '  '),
  (lambda * _: _)(
    '.update',
    (lambda * _: _)(
      'builtins..globals'),
    ':',
    name,
    value))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('Assigns a global the value in the current module.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     "     #> (define SPAM 'tomato)\n"
     '     >>> # define\n'
     "     ... __import__('builtins').globals().update(\n"
     "     ...   SPAM='tomato')\n"
     '\n'
     '     #> SPAM\n'
     '     >>> SPAM\n'
     "     'tomato'\n"
     '\n'
     '  See also:\n'
     '  `globals`, `dict.update`, `defonce`, `def`, `assignment`, `global`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'define',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'define',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda name,value:(
  ('Assigns a global the value in the current module, unless it exists.\n'
   '\n'
   "  Like `define`, but won't overwrite an existing global.\n"
   '  Useful when sending the whole file to the REPL repeatedly or when\n'
   '  using `importlib.reload` and you want to cache an expensive object\n'
   '  instead of re-initializing it every time.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> (defonce CACHE (types..SimpleNamespace : x 1))\n'
   '     >>> # defonce\n'
   '     ... # hissp.macros.._macro_.unless\n'
   '     ... (lambda b,a:()if b else a())(\n'
   "     ...   __import__('operator').contains(\n"
   "     ...     __import__('builtins').globals(),\n"
   "     ...     'CACHE'),\n"
   '     ...   (lambda :\n'
   '     ...     # hissp.macros.._macro_.define\n'
   "     ...     __import__('builtins').globals().update(\n"
   "     ...       CACHE=__import__('types').SimpleNamespace(\n"
   '     ...               x=(1)))))\n'
   '\n'
   "     #> (setattr CACHE 'x 42)\n"
   '     >>> setattr(\n'
   '     ...   CACHE,\n'
   "     ...   'x',\n"
   '     ...   (42))\n'
   '\n'
   "     #> (defonce CACHE (progn (print 'not 'evaluated)\n"
   '     #..                      (types..SimpleNamespace : x 1)))\n'
   '     >>> # defonce\n'
   '     ... # hissp.macros.._macro_.unless\n'
   '     ... (lambda b,a:()if b else a())(\n'
   "     ...   __import__('operator').contains(\n"
   "     ...     __import__('builtins').globals(),\n"
   "     ...     'CACHE'),\n"
   '     ...   (lambda :\n'
   '     ...     # hissp.macros.._macro_.define\n'
   "     ...     __import__('builtins').globals().update(\n"
   '     ...       CACHE=# progn\n'
   '     ...             (lambda :(\n'
   '     ...               print(\n'
   "     ...                 'not',\n"
   "     ...                 'evaluated'),\n"
   "     ...               __import__('types').SimpleNamespace(\n"
   '     ...                 x=(1)))[-1])())))\n'
   '     ()\n'
   '\n'
   '     #> CACHE ; The second defonce had no effect.\n'
   '     >>> CACHE\n'
   '     namespace(x=42)\n'
   '\n'
   '  '),
  (lambda * _: _)(
    'hissp.macros.._macro_.unless',
    (lambda * _: _)(
      'operator..contains',
      (lambda * _: _)(
        'builtins..globals'),
      (lambda * _: _)(
        'quote',
        name)),
    (lambda * _: _)(
      'hissp.macros.._macro_.define',
      name,
      value)))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('Assigns a global the value in the current module, unless it exists.\n'
     '\n'
     "  Like `define`, but won't overwrite an existing global.\n"
     '  Useful when sending the whole file to the REPL repeatedly or when\n'
     '  using `importlib.reload` and you want to cache an expensive object\n'
     '  instead of re-initializing it every time.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> (defonce CACHE (types..SimpleNamespace : x 1))\n'
     '     >>> # defonce\n'
     '     ... # hissp.macros.._macro_.unless\n'
     '     ... (lambda b,a:()if b else a())(\n'
     "     ...   __import__('operator').contains(\n"
     "     ...     __import__('builtins').globals(),\n"
     "     ...     'CACHE'),\n"
     '     ...   (lambda :\n'
     '     ...     # hissp.macros.._macro_.define\n'
     "     ...     __import__('builtins').globals().update(\n"
     "     ...       CACHE=__import__('types').SimpleNamespace(\n"
     '     ...               x=(1)))))\n'
     '\n'
     "     #> (setattr CACHE 'x 42)\n"
     '     >>> setattr(\n'
     '     ...   CACHE,\n'
     "     ...   'x',\n"
     '     ...   (42))\n'
     '\n'
     "     #> (defonce CACHE (progn (print 'not 'evaluated)\n"
     '     #..                      (types..SimpleNamespace : x 1)))\n'
     '     >>> # defonce\n'
     '     ... # hissp.macros.._macro_.unless\n'
     '     ... (lambda b,a:()if b else a())(\n'
     "     ...   __import__('operator').contains(\n"
     "     ...     __import__('builtins').globals(),\n"
     "     ...     'CACHE'),\n"
     '     ...   (lambda :\n'
     '     ...     # hissp.macros.._macro_.define\n'
     "     ...     __import__('builtins').globals().update(\n"
     '     ...       CACHE=# progn\n'
     '     ...             (lambda :(\n'
     '     ...               print(\n'
     "     ...                 'not',\n"
     "     ...                 'evaluated'),\n"
     "     ...               __import__('types').SimpleNamespace(\n"
     '     ...                 x=(1)))[-1])())))\n'
     '     ()\n'
     '\n'
     '     #> CACHE ; The second defonce had no effect.\n'
     '     >>> CACHE\n'
     '     namespace(x=42)\n'
     '\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'defonce',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'defonce',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda name,bases,*body:(
  ('Defines a type (class) in the current module.\n'
   '\n'
   'Key-value pairs are implied by position in the body.\n'
   '\n'
   '.. code-block:: REPL\n'
   '\n'
   '   #> (deftype Point2D (tuple)\n'
   '   #..  __doc__ "Simple ordered pair."\n'
   '   #..  __new__ (lambda (cls x y)\n'
   '   #..            (.__new__ tuple cls `(,x ,y)))\n'
   '   #..  __repr__ (lambda (self)\n'
   '   #..             (.format "Point2D({!r}, {!r})" : :* self)))\n'
   '   >>> # deftype\n'
   '   ... # hissp.macros.._macro_.define\n'
   "   ... __import__('builtins').globals().update(\n"
   "   ...   Point2D=__import__('builtins').type(\n"
   "   ...             'Point2D',\n"
   '   ...             (lambda * _: _)(\n'
   '   ...               tuple),\n'
   "   ...             __import__('builtins').dict(\n"
   "   ...               __doc__=('Simple ordered pair.'),\n"
   '   ...               __new__=(lambda cls,x,y:\n'
   '   ...                         tuple.__new__(\n'
   '   ...                           cls,\n'
   '   ...                           (lambda * _: _)(\n'
   '   ...                             x,\n'
   '   ...                             y))),\n'
   '   ...               __repr__=(lambda self:\n'
   "   ...                          ('Point2D({!r}, {!r})').format(\n"
   '   ...                            *self)))))\n'
   '\n'
   '   #> (Point2D 1 2)\n'
   '   >>> Point2D(\n'
   '   ...   (1),\n'
   '   ...   (2))\n'
   '   Point2D(1, 2)\n'
   '\n'
   'Also supports kwds in the bases tuple for\n'
   '`object.__init_subclass__`. Separate with a ``:``.\n'
   '\n'
   '.. code-block:: REPL\n'
   '\n'
   '   #> (deftype Foo ()\n'
   '   #..  __init_subclass__ (lambda (cls :/ : :** kwargs)\n'
   '   #..                      (print kwargs)))\n'
   '   >>> # deftype\n'
   '   ... # hissp.macros.._macro_.define\n'
   "   ... __import__('builtins').globals().update(\n"
   "   ...   Foo=__import__('builtins').type(\n"
   "   ...         'Foo',\n"
   '   ...         (lambda * _: _)(),\n'
   "   ...         __import__('builtins').dict(\n"
   '   ...           __init_subclass__=(lambda cls,/,**kwargs:\n'
   '   ...                               print(\n'
   '   ...                                 kwargs)))))\n'
   '\n'
   '   #> (deftype Bar (Foo : a 1  b 2))\n'
   '   >>> # deftype\n'
   '   ... # hissp.macros.._macro_.define\n'
   "   ... __import__('builtins').globals().update(\n"
   "   ...   Bar=__import__('builtins').type(\n"
   "   ...         'Bar',\n"
   '   ...         (lambda * _: _)(\n'
   '   ...           Foo),\n'
   "   ...         __import__('builtins').dict(),\n"
   '   ...         a=(1),\n'
   '   ...         b=(2)))\n'
   "   {'a': 1, 'b': 2}\n"
   '\n'
   'See also: `attach`, `type`, `@#!<QzAT_QzHASH_>`, :keyword:`class`,\n'
   '`types.new_class`\n'),
  # let
  (lambda ibases=iter(
    bases):
    (lambda * _: _)(
      'hissp.macros.._macro_.define',
      name,
      (lambda * _: _)(
        'builtins..type',
        (lambda * _: _)(
          'quote',
          name),
        (lambda * _: _)(
          __import__('hissp.reader',fromlist='?').ENTUPLE,
          *__import__('itertools').takewhile(
             (lambda x:
               __import__('operator').ne(
                 x,
                 ':')),
             ibases)),
        (lambda * _: _)(
          'builtins..dict',
          ':',
          *body),
        ':',
        *ibases)))())[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('Defines a type (class) in the current module.\n'
     '\n'
     'Key-value pairs are implied by position in the body.\n'
     '\n'
     '.. code-block:: REPL\n'
     '\n'
     '   #> (deftype Point2D (tuple)\n'
     '   #..  __doc__ "Simple ordered pair."\n'
     '   #..  __new__ (lambda (cls x y)\n'
     '   #..            (.__new__ tuple cls `(,x ,y)))\n'
     '   #..  __repr__ (lambda (self)\n'
     '   #..             (.format "Point2D({!r}, {!r})" : :* self)))\n'
     '   >>> # deftype\n'
     '   ... # hissp.macros.._macro_.define\n'
     "   ... __import__('builtins').globals().update(\n"
     "   ...   Point2D=__import__('builtins').type(\n"
     "   ...             'Point2D',\n"
     '   ...             (lambda * _: _)(\n'
     '   ...               tuple),\n'
     "   ...             __import__('builtins').dict(\n"
     "   ...               __doc__=('Simple ordered pair.'),\n"
     '   ...               __new__=(lambda cls,x,y:\n'
     '   ...                         tuple.__new__(\n'
     '   ...                           cls,\n'
     '   ...                           (lambda * _: _)(\n'
     '   ...                             x,\n'
     '   ...                             y))),\n'
     '   ...               __repr__=(lambda self:\n'
     "   ...                          ('Point2D({!r}, {!r})').format(\n"
     '   ...                            *self)))))\n'
     '\n'
     '   #> (Point2D 1 2)\n'
     '   >>> Point2D(\n'
     '   ...   (1),\n'
     '   ...   (2))\n'
     '   Point2D(1, 2)\n'
     '\n'
     'Also supports kwds in the bases tuple for\n'
     '`object.__init_subclass__`. Separate with a ``:``.\n'
     '\n'
     '.. code-block:: REPL\n'
     '\n'
     '   #> (deftype Foo ()\n'
     '   #..  __init_subclass__ (lambda (cls :/ : :** kwargs)\n'
     '   #..                      (print kwargs)))\n'
     '   >>> # deftype\n'
     '   ... # hissp.macros.._macro_.define\n'
     "   ... __import__('builtins').globals().update(\n"
     "   ...   Foo=__import__('builtins').type(\n"
     "   ...         'Foo',\n"
     '   ...         (lambda * _: _)(),\n'
     "   ...         __import__('builtins').dict(\n"
     '   ...           __init_subclass__=(lambda cls,/,**kwargs:\n'
     '   ...                               print(\n'
     '   ...                                 kwargs)))))\n'
     '\n'
     '   #> (deftype Bar (Foo : a 1  b 2))\n'
     '   >>> # deftype\n'
     '   ... # hissp.macros.._macro_.define\n'
     "   ... __import__('builtins').globals().update(\n"
     "   ...   Bar=__import__('builtins').type(\n"
     "   ...         'Bar',\n"
     '   ...         (lambda * _: _)(\n'
     '   ...           Foo),\n'
     "   ...         __import__('builtins').dict(),\n"
     '   ...         a=(1),\n'
     '   ...         b=(2)))\n'
     "   {'a': 1, 'b': 2}\n"
     '\n'
     'See also: `attach`, `type`, `@#!<QzAT_QzHASH_>`, :keyword:`class`,\n'
     '`types.new_class`\n')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'deftype',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'deftype',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda syms,itr,*body:(
  ('``let-from`` Create listed locals from iterable.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   "     #> (let-from (a b : :* cs) 'ABCDEFG\n"
   '     #..  (print cs b a))\n'
   '     >>> # letQz_from\n'
   '     ... (lambda a,b,*cs:\n'
   '     ...   print(\n'
   '     ...     cs,\n'
   '     ...     b,\n'
   '     ...     a))(\n'
   "     ...   *'ABCDEFG')\n"
   "     ('C', 'D', 'E', 'F', 'G') B A\n"
   '\n'
   '  See also: `let`, `let*from<letQzSTAR_from>`, `assignment`.\n'
   '  '),
  (lambda * _: _)(
    (lambda * _: _)(
      'lambda',
      syms,
      *body),
    ':',
    ':*',
    itr))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('``let-from`` Create listed locals from iterable.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     "     #> (let-from (a b : :* cs) 'ABCDEFG\n"
     '     #..  (print cs b a))\n'
     '     >>> # letQz_from\n'
     '     ... (lambda a,b,*cs:\n'
     '     ...   print(\n'
     '     ...     cs,\n'
     '     ...     b,\n'
     '     ...     a))(\n'
     "     ...   *'ABCDEFG')\n"
     "     ('C', 'D', 'E', 'F', 'G') B A\n"
     '\n'
     '  See also: `let`, `let*from<letQzSTAR_from>`, `assignment`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'letQz_from',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'letQz_from',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda pairs,*body:(
  ("``let*from`` 'let star from' Nested `let-from<letQz_from>`.\n"
   '\n'
   '  Can unpack nested iterables by using multiple stages.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   "     #> (dict : A 'B  C 'D)\n"
   '     >>> dict(\n'
   "     ...   A='B',\n"
   "     ...   C='D')\n"
   "     {'A': 'B', 'C': 'D'}\n"
   '\n'
   '     #> (let*from ((ab cd) (.items _)    ;Nested let-froms.\n'
   "     #..           (a b) ab              ;Unpacks first item ('A', 'B')\n"
   "     #..           (c d) cd)             ;Unpacks second item ('C', 'D')\n"
   '     #..  (print a b c d))\n'
   '     >>> # letQzSTAR_from\n'
   '     ... # hissp.macros.._macro_.letQz_from\n'
   '     ... (lambda ab,cd:\n'
   '     ...   # hissp.macros..QzMaybe_.letQzSTAR_from\n'
   '     ...   # hissp.macros.._macro_.letQz_from\n'
   '     ...   (lambda a,b:\n'
   '     ...     # hissp.macros..QzMaybe_.letQzSTAR_from\n'
   '     ...     # hissp.macros.._macro_.letQz_from\n'
   '     ...     (lambda c,d:\n'
   '     ...       # hissp.macros..QzMaybe_.letQzSTAR_from\n'
   '     ...       # hissp.macros.._macro_.progn\n'
   '     ...       (lambda :\n'
   '     ...         print(\n'
   '     ...           a,\n'
   '     ...           b,\n'
   '     ...           c,\n'
   '     ...           d))())(\n'
   '     ...       *cd))(\n'
   '     ...     *ab))(\n'
   '     ...   *_.items())\n'
   '     A B C D\n'
   '\n'
   '\n'
   '     #> (let*from ((ab cd) (.items _)    ;Fewer stack frames.\n'
   '     #..           (a b c d) `(,@ab ,@cd)) ;Leveraging ,@ splicing.\n'
   '     #..  (print a b c d))\n'
   '     >>> # letQzSTAR_from\n'
   '     ... # hissp.macros.._macro_.letQz_from\n'
   '     ... (lambda ab,cd:\n'
   '     ...   # hissp.macros..QzMaybe_.letQzSTAR_from\n'
   '     ...   # hissp.macros.._macro_.letQz_from\n'
   '     ...   (lambda a,b,c,d:\n'
   '     ...     # hissp.macros..QzMaybe_.letQzSTAR_from\n'
   '     ...     # hissp.macros.._macro_.progn\n'
   '     ...     (lambda :\n'
   '     ...       print(\n'
   '     ...         a,\n'
   '     ...         b,\n'
   '     ...         c,\n'
   '     ...         d))())(\n'
   '     ...     *(lambda * _: _)(\n'
   '     ...        *ab,\n'
   '     ...        *cd)))(\n'
   '     ...   *_.items())\n'
   '     A B C D\n'
   '\n'
   '\n'
   "     #> (let-from (a c b d) ; Didn't really need let*from this time.\n"
   '     #..          `(,@(.keys _) ,@(.values _)) ; Not always this easy.\n'
   '     #..  (print a b c d))\n'
   '     >>> # letQz_from\n'
   '     ... (lambda a,c,b,d:\n'
   '     ...   print(\n'
   '     ...     a,\n'
   '     ...     b,\n'
   '     ...     c,\n'
   '     ...     d))(\n'
   '     ...   *(lambda * _: _)(\n'
   '     ...      *_.keys(),\n'
   '     ...      *_.values()))\n'
   '     A B C D\n'
   '\n'
   '  '),
  # ifQz_else
  (lambda b,c,a:c()if b else a())(
    pairs,
    (lambda :
      (lambda * _: _)(
        'hissp.macros.._macro_.letQz_from',
        __import__('operator').getitem(
          pairs,
          (0)),
        __import__('operator').getitem(
          pairs,
          (1)),
        (lambda * _: _)(
          'hissp.macros..QzMaybe_.letQzSTAR_from',
          __import__('operator').getitem(
            pairs,
            slice(
              (2),
              None)),
          *body))),
    (lambda :
      (lambda * _: _)(
        'hissp.macros.._macro_.progn',
        *body))))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ("``let*from`` 'let star from' Nested `let-from<letQz_from>`.\n"
     '\n'
     '  Can unpack nested iterables by using multiple stages.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     "     #> (dict : A 'B  C 'D)\n"
     '     >>> dict(\n'
     "     ...   A='B',\n"
     "     ...   C='D')\n"
     "     {'A': 'B', 'C': 'D'}\n"
     '\n'
     '     #> (let*from ((ab cd) (.items _)    ;Nested let-froms.\n'
     "     #..           (a b) ab              ;Unpacks first item ('A', 'B')\n"
     "     #..           (c d) cd)             ;Unpacks second item ('C', 'D')\n"
     '     #..  (print a b c d))\n'
     '     >>> # letQzSTAR_from\n'
     '     ... # hissp.macros.._macro_.letQz_from\n'
     '     ... (lambda ab,cd:\n'
     '     ...   # hissp.macros..QzMaybe_.letQzSTAR_from\n'
     '     ...   # hissp.macros.._macro_.letQz_from\n'
     '     ...   (lambda a,b:\n'
     '     ...     # hissp.macros..QzMaybe_.letQzSTAR_from\n'
     '     ...     # hissp.macros.._macro_.letQz_from\n'
     '     ...     (lambda c,d:\n'
     '     ...       # hissp.macros..QzMaybe_.letQzSTAR_from\n'
     '     ...       # hissp.macros.._macro_.progn\n'
     '     ...       (lambda :\n'
     '     ...         print(\n'
     '     ...           a,\n'
     '     ...           b,\n'
     '     ...           c,\n'
     '     ...           d))())(\n'
     '     ...       *cd))(\n'
     '     ...     *ab))(\n'
     '     ...   *_.items())\n'
     '     A B C D\n'
     '\n'
     '\n'
     '     #> (let*from ((ab cd) (.items _)    ;Fewer stack frames.\n'
     '     #..           (a b c d) `(,@ab ,@cd)) ;Leveraging ,@ splicing.\n'
     '     #..  (print a b c d))\n'
     '     >>> # letQzSTAR_from\n'
     '     ... # hissp.macros.._macro_.letQz_from\n'
     '     ... (lambda ab,cd:\n'
     '     ...   # hissp.macros..QzMaybe_.letQzSTAR_from\n'
     '     ...   # hissp.macros.._macro_.letQz_from\n'
     '     ...   (lambda a,b,c,d:\n'
     '     ...     # hissp.macros..QzMaybe_.letQzSTAR_from\n'
     '     ...     # hissp.macros.._macro_.progn\n'
     '     ...     (lambda :\n'
     '     ...       print(\n'
     '     ...         a,\n'
     '     ...         b,\n'
     '     ...         c,\n'
     '     ...         d))())(\n'
     '     ...     *(lambda * _: _)(\n'
     '     ...        *ab,\n'
     '     ...        *cd)))(\n'
     '     ...   *_.items())\n'
     '     A B C D\n'
     '\n'
     '\n'
     "     #> (let-from (a c b d) ; Didn't really need let*from this time.\n"
     '     #..          `(,@(.keys _) ,@(.values _)) ; Not always this easy.\n'
     '     #..  (print a b c d))\n'
     '     >>> # letQz_from\n'
     '     ... (lambda a,c,b,d:\n'
     '     ...   print(\n'
     '     ...     a,\n'
     '     ...     b,\n'
     '     ...     c,\n'
     '     ...     d))(\n'
     '     ...   *(lambda * _: _)(\n'
     '     ...      *_.keys(),\n'
     '     ...      *_.values()))\n'
     '     A B C D\n'
     '\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'letQzSTAR_from',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'letQzSTAR_from',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda e:(
  ('``my#`` Anaphoric. `let` ``my`` be a fresh `types.SimpleNamespace`\n'
   '  in a lexical scope surrounding e.\n'
   '\n'
   '  Creates a local namespace for imperative-style reassignments,\n'
   '  typically combined with  `set@<setQzAT_>` for an assignment.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> my#(print (set@ my.x (op#add 1 1))\n'
   '     #..           my.x)\n'
   '     >>> # hissp.macros.._macro_.let\n'
   "     ... (lambda my=__import__('types').SimpleNamespace():\n"
   '     ...   print(\n'
   '     ...     # setQzAT_\n'
   '     ...     # hissp.macros.._macro_.let\n'
   "     ...     (lambda _QzRMG5GSSIz_val=__import__('operator').add(\n"
   '     ...       (1),\n'
   '     ...       (1)):(\n'
   "     ...       __import__('builtins').setattr(\n"
   '     ...         my,\n'
   "     ...         'x',\n"
   '     ...         _QzRMG5GSSIz_val),\n'
   '     ...       _QzRMG5GSSIz_val)[-1])(),\n'
   '     ...     my.x))()\n'
   '     2 2\n'
   '\n'
   '  ``my#my`` is a shorthand for a new empty namespace.\n'
   '\n'
   '  Often combined with branching macros to reuse the results of an\n'
   "  expression, with uses similar to Python's 'walrus' operator ``:=``.\n"
   '\n'
   '  See also, `attach`, `python-grammar:assignment_expression`.\n'
   '  '),
  (lambda * _: _)(
    'hissp.macros.._macro_.let',
    (lambda * _: _)(
      'my',
      (lambda * _: _)(
        'types..SimpleNamespace')),
    e))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('``my#`` Anaphoric. `let` ``my`` be a fresh `types.SimpleNamespace`\n'
     '  in a lexical scope surrounding e.\n'
     '\n'
     '  Creates a local namespace for imperative-style reassignments,\n'
     '  typically combined with  `set@<setQzAT_>` for an assignment.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> my#(print (set@ my.x (op#add 1 1))\n'
     '     #..           my.x)\n'
     '     >>> # hissp.macros.._macro_.let\n'
     "     ... (lambda my=__import__('types').SimpleNamespace():\n"
     '     ...   print(\n'
     '     ...     # setQzAT_\n'
     '     ...     # hissp.macros.._macro_.let\n'
     "     ...     (lambda _QzRMG5GSSIz_val=__import__('operator').add(\n"
     '     ...       (1),\n'
     '     ...       (1)):(\n'
     "     ...       __import__('builtins').setattr(\n"
     '     ...         my,\n'
     "     ...         'x',\n"
     '     ...         _QzRMG5GSSIz_val),\n'
     '     ...       _QzRMG5GSSIz_val)[-1])(),\n'
     '     ...     my.x))()\n'
     '     2 2\n'
     '\n'
     '  ``my#my`` is a shorthand for a new empty namespace.\n'
     '\n'
     '  Often combined with branching macros to reuse the results of an\n'
     "  expression, with uses similar to Python's 'walrus' operator ``:=``.\n"
     '\n'
     '  See also, `attach`, `python-grammar:assignment_expression`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'myQzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'myQzHASH_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda e:(
  ("``O#`` 'thunk' Make ``e`` an anonymous function with no parameters.\n"
   '\n'
   '  See also: `X#<XQzHASH_>`.\n'
   '  '),
  (lambda * _: _)(
    'lambda',
    ':',
    e))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ("``O#`` 'thunk' Make ``e`` an anonymous function with no parameters.\n"
     '\n'
     '  See also: `X#<XQzHASH_>`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'OQzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'OQzHASH_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda e:(
  ('``X#`` Anaphoric. Make ``e`` an anonymous function with paramter X.\n'
   '\n'
   'Examples:\n'
   '\n'
   'Convert macro to function.\n'
   '\n'
   '.. code-block:: REPL\n'
   '\n'
   '   #> (list (map X#(@ X) "abc")) ; en#list would also work here.\n'
   '   >>> list(\n'
   '   ...   map(\n'
   '   ...     (lambda X:\n'
   '   ...       # QzAT_\n'
   '   ...       (lambda *xs:[*xs])(\n'
   '   ...         X)),\n'
   "   ...     ('abc')))\n"
   "   [['a'], ['b'], ['c']]\n"
   '\n'
   'Compact function definition using Python operators.\n'
   '\n'
   '.. code-block:: REPL\n'
   '\n'
   '   #> (define teen? X#.#"13<=X<20")\n'
   '   >>> # define\n'
   "   ... __import__('builtins').globals().update(\n"
   '   ...   teenQzQUERY_=(lambda X:13<=X<20))\n'
   '\n'
   '   #> (teen? 12.5)\n'
   '   >>> teenQzQUERY_(\n'
   '   ...   (12.5))\n'
   '   False\n'
   '\n'
   '   #> (teen? 19.5)\n'
   '   >>> teenQzQUERY_(\n'
   '   ...   (19.5))\n'
   '   True\n'
   '\n'
   'Get an attribute without calling it.\n'
   '\n'
   '.. code-block:: REPL\n'
   '\n'
   '   #> (X#X.upper "shout")\n'
   '   >>> (lambda X:X.upper)(\n'
   "   ...   ('shout'))\n"
   '   <built-in method upper of str object at ...>\n'
   '\n'
   '   #> (_)\n'
   '   >>> _()\n'
   "   'SHOUT'\n"
   '\n'
   '   #> (define class-name X#X.__class__.__name__) ; Attributes chain.\n'
   '   >>> # define\n'
   "   ... __import__('builtins').globals().update(\n"
   '   ...   classQz_name=(lambda X:X.__class__.__name__))\n'
   '\n'
   '   #> (class-name object)\n'
   '   >>> classQz_name(\n'
   '   ...   object)\n'
   "   'type'\n"
   '\n'
   '   #> (class-name "foo")\n'
   '   >>> classQz_name(\n'
   "   ...   ('foo'))\n"
   "   'str'\n"
   '\n'
   'See also:\n'
   '`en#<enQzHASH_>`, `O#<OQzHASH_>`, `XY#<XYQzHASH_>`, `getattr`,\n'
   '`operator.attrgetter`, `lambda`, `^#<QzHAT_QzHASH_>`.\n'),
  (lambda * _: _)(
    'lambda',
    'X',
    e))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('``X#`` Anaphoric. Make ``e`` an anonymous function with paramter X.\n'
     '\n'
     'Examples:\n'
     '\n'
     'Convert macro to function.\n'
     '\n'
     '.. code-block:: REPL\n'
     '\n'
     '   #> (list (map X#(@ X) "abc")) ; en#list would also work here.\n'
     '   >>> list(\n'
     '   ...   map(\n'
     '   ...     (lambda X:\n'
     '   ...       # QzAT_\n'
     '   ...       (lambda *xs:[*xs])(\n'
     '   ...         X)),\n'
     "   ...     ('abc')))\n"
     "   [['a'], ['b'], ['c']]\n"
     '\n'
     'Compact function definition using Python operators.\n'
     '\n'
     '.. code-block:: REPL\n'
     '\n'
     '   #> (define teen? X#.#"13<=X<20")\n'
     '   >>> # define\n'
     "   ... __import__('builtins').globals().update(\n"
     '   ...   teenQzQUERY_=(lambda X:13<=X<20))\n'
     '\n'
     '   #> (teen? 12.5)\n'
     '   >>> teenQzQUERY_(\n'
     '   ...   (12.5))\n'
     '   False\n'
     '\n'
     '   #> (teen? 19.5)\n'
     '   >>> teenQzQUERY_(\n'
     '   ...   (19.5))\n'
     '   True\n'
     '\n'
     'Get an attribute without calling it.\n'
     '\n'
     '.. code-block:: REPL\n'
     '\n'
     '   #> (X#X.upper "shout")\n'
     '   >>> (lambda X:X.upper)(\n'
     "   ...   ('shout'))\n"
     '   <built-in method upper of str object at ...>\n'
     '\n'
     '   #> (_)\n'
     '   >>> _()\n'
     "   'SHOUT'\n"
     '\n'
     '   #> (define class-name X#X.__class__.__name__) ; Attributes chain.\n'
     '   >>> # define\n'
     "   ... __import__('builtins').globals().update(\n"
     '   ...   classQz_name=(lambda X:X.__class__.__name__))\n'
     '\n'
     '   #> (class-name object)\n'
     '   >>> classQz_name(\n'
     '   ...   object)\n'
     "   'type'\n"
     '\n'
     '   #> (class-name "foo")\n'
     '   >>> classQz_name(\n'
     "   ...   ('foo'))\n"
     "   'str'\n"
     '\n'
     'See also:\n'
     '`en#<enQzHASH_>`, `O#<OQzHASH_>`, `XY#<XYQzHASH_>`, `getattr`,\n'
     '`operator.attrgetter`, `lambda`, `^#<QzHAT_QzHASH_>`.\n')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'XQzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'XQzHASH_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda e:(
  ('``XY#`` Anaphoric. Make ``e`` an anonymous function with paramters X Y.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   "     #> (functools..reduce XY#(op#concat Y X) 'abcd)\n"
   "     >>> __import__('functools').reduce(\n"
   '     ...   (lambda X,Y:\n'
   "     ...     __import__('operator').concat(\n"
   '     ...       Y,\n'
   '     ...       X)),\n'
   "     ...   'abcd')\n"
   "     'dcba'\n"
   '\n'
   '  See also: `X#<XQzHASH_>`, `XYZ#<XYZQzHASH_>`, `^^#<QzHAT_QzHAT_QzHASH_>`.\n'
   '  '),
  (lambda * _: _)(
    'lambda',
    'XY',
    e))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('``XY#`` Anaphoric. Make ``e`` an anonymous function with paramters X Y.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     "     #> (functools..reduce XY#(op#concat Y X) 'abcd)\n"
     "     >>> __import__('functools').reduce(\n"
     '     ...   (lambda X,Y:\n'
     "     ...     __import__('operator').concat(\n"
     '     ...       Y,\n'
     '     ...       X)),\n'
     "     ...   'abcd')\n"
     "     'dcba'\n"
     '\n'
     '  See also: `X#<XQzHASH_>`, `XYZ#<XYZQzHASH_>`, `^^#<QzHAT_QzHAT_QzHASH_>`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'XYQzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'XYQzHASH_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda e:(
  ('``XYZ#`` Anaphoric. Make ``e`` an anonymous function with paramters X Y Z.\n'
   '\n'
   '.. code-block:: REPL\n'
   '\n'
   '   #> (XYZ#.#"X*Y == Z" : X math..pi  Y 2  Z math..tau)\n'
   '   >>> (lambda X,Y,Z:X*Y == Z)(\n'
   "   ...   X=__import__('math').pi,\n"
   '   ...   Y=(2),\n'
   "   ...   Z=__import__('math').tau)\n"
   '   True\n'
   '\n'
   'See also: `XY#<XYQzHASH_>`, `XYZW#<XYZWQzHASH_>`,\n'
   '`^^^#<QzHAT_QzHAT_QzHAT_QzHASH_>`.\n'),
  (lambda * _: _)(
    'lambda',
    'XYZ',
    e))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('``XYZ#`` Anaphoric. Make ``e`` an anonymous function with paramters X Y Z.\n'
     '\n'
     '.. code-block:: REPL\n'
     '\n'
     '   #> (XYZ#.#"X*Y == Z" : X math..pi  Y 2  Z math..tau)\n'
     '   >>> (lambda X,Y,Z:X*Y == Z)(\n'
     "   ...   X=__import__('math').pi,\n"
     '   ...   Y=(2),\n'
     "   ...   Z=__import__('math').tau)\n"
     '   True\n'
     '\n'
     'See also: `XY#<XYQzHASH_>`, `XYZW#<XYZWQzHASH_>`,\n'
     '`^^^#<QzHAT_QzHAT_QzHAT_QzHASH_>`.\n')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'XYZQzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'XYZQzHASH_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda e:(
  ('``XYZW#`` Anaphoric. Make ``e`` an anonymous function with paramters X Y Z '
   'W.\n'
   '\n'
   '.. code-block:: REPL\n'
   '\n'
   '   #> (XYZW#.#"X[Y:Z:W]" "QuaoblcldefHg" -2 1 -2)\n'
   '   >>> (lambda X,Y,Z,W:X[Y:Z:W])(\n'
   "   ...   ('QuaoblcldefHg'),\n"
   '   ...   (-2),\n'
   '   ...   (1),\n'
   '   ...   (-2))\n'
   "   'Hello'\n"
   '\n'
   'See also: `XYZ#<XYZQzHASH_>`, `en#<enQzHASH_>`, `X#<XQzHASH_>`.\n'
   '`^^^^#<QzHAT_QzHAT_QzHAT_QzHAT_QzHASH_>`.\n'),
  (lambda * _: _)(
    'lambda',
    'XYZW',
    e))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('``XYZW#`` Anaphoric. Make ``e`` an anonymous function with paramters X Y Z '
     'W.\n'
     '\n'
     '.. code-block:: REPL\n'
     '\n'
     '   #> (XYZW#.#"X[Y:Z:W]" "QuaoblcldefHg" -2 1 -2)\n'
     '   >>> (lambda X,Y,Z,W:X[Y:Z:W])(\n'
     "   ...   ('QuaoblcldefHg'),\n"
     '   ...   (-2),\n'
     '   ...   (1),\n'
     '   ...   (-2))\n'
     "   'Hello'\n"
     '\n'
     'See also: `XYZ#<XYZQzHASH_>`, `en#<enQzHASH_>`, `X#<XQzHASH_>`.\n'
     '`^^^^#<QzHAT_QzHAT_QzHAT_QzHAT_QzHASH_>`.\n')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'XYZWQzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'XYZWQzHASH_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda abbreviation,qualifier:(
  ('Defines a reader macro abbreviation of a qualifier.\n'
   '\n'
   '.. code-block:: REPL\n'
   '\n'
   '   #> (hissp.._macro_.alias H: hissp.._macro_)\n'
   '   >>> # hissp.._macro_.alias\n'
   '   ... # hissp.macros.._macro_.defmacro\n'
   '   ... # hissp.macros.._macro_.let\n'
   '   ... (lambda _QzAW22OE5Kz_fn=(lambda '
   '_QzARAQTXTEz_prime,_QzARAQTXTEz_reader=None,*_QzARAQTXTEz_args:(\n'
   "   ...   'Aliases ``hissp.._macro_`` as ``HQzCOLON_#``.',\n"
   '   ...   # hissp.macros.._macro_.ifQz_else\n'
   '   ...   (lambda b,c,a:c()if b else a())(\n'
   '   ...     _QzARAQTXTEz_reader,\n'
   '   ...     (lambda :\n'
   "   ...       __import__('builtins').getattr(\n"
   "   ...         __import__('hissp')._macro_,\n"
   "   ...         ('{}{}').format(\n"
   '   ...           _QzARAQTXTEz_reader,\n'
   '   ...           # hissp.macros.._macro_.ifQz_else\n'
   '   ...           (lambda b,c,a:c()if b else a())(\n'
   "   ...             'hissp.._macro_'.endswith(\n"
   "   ...               '._macro_'),\n"
   "   ...             (lambda :'QzHASH_'),\n"
   "   ...             (lambda :('')))))(\n"
   '   ...         _QzARAQTXTEz_prime,\n'
   '   ...         *_QzARAQTXTEz_args)),\n'
   '   ...     (lambda :\n'
   "   ...       ('{}.{}').format(\n"
   "   ...         'hissp.._macro_',\n"
   '   ...         _QzARAQTXTEz_prime))))[-1]):(\n'
   "   ...   __import__('builtins').setattr(\n"
   '   ...     _QzAW22OE5Kz_fn,\n'
   "   ...     '__doc__',\n"
   "   ...     'Aliases ``hissp.._macro_`` as ``HQzCOLON_#``.'),\n"
   "   ...   __import__('builtins').setattr(\n"
   '   ...     _QzAW22OE5Kz_fn,\n'
   "   ...     '__qualname__',\n"
   "   ...     ('.').join(\n"
   "   ...       ('_macro_',\n"
   "   ...        'HQzCOLON_QzHASH_',))),\n"
   "   ...   __import__('builtins').setattr(\n"
   "   ...     __import__('operator').getitem(\n"
   "   ...       __import__('builtins').globals(),\n"
   "   ...       '_macro_'),\n"
   "   ...     'HQzCOLON_QzHASH_',\n"
   '   ...     _QzAW22OE5Kz_fn))[-1])()\n'
   '\n'
   "   #> 'H:#alias\n"
   "   >>> 'hissp.._macro_.alias'\n"
   "   'hissp.._macro_.alias'\n"
   '\n'
   '   #> H:#b\\#                              ;b# macro callable\n'
   "   >>> __import__('hissp')._macro_.bQzHASH_\n"
   '   <function _macro_.bQzHASH_ at ...>\n'
   '\n'
   '   #> (H:#b\\# "b# macro at compile time")\n'
   '   >>> # hissp.._macro_.bQzHASH_\n'
   "   ... b'b# macro at compile time'\n"
   "   b'b# macro at compile time'\n"
   '\n'
   '   #> hissp.._macro_.b#"Fully-qualified b# macro at read time."\n'
   "   >>> b'Fully-qualified b# macro at read time.'\n"
   "   b'Fully-qualified b# macro at read time.'\n"
   '\n'
   '   #> H:#!b"Read-time b# via alias."      ;Extra arg for alias with (!)\n'
   "   >>> b'Read-time b# via alias.'\n"
   "   b'Read-time b# via alias.'\n"
   '\n'
   'The bundled `op#<opQzHASH_>` and `i#<iQzHASH_>` reader macros are aliases\n'
   'for `operator` and `itertools`, respectively.\n'
   '\n'
   'See also: `prelude`, `attach`.\n'),
  (lambda * _: _)(
    'hissp.macros.._macro_.defmacro',
    ('{}{}').format(
      abbreviation,
      'QzHASH_'),
    (lambda * _: _)(
      '_QzT7EX5TKYz_prime',
      ':',
      '_QzT7EX5TKYz_reader',
      None,
      ':*',
      '_QzT7EX5TKYz_args'),
    (lambda * _: _)(
      'quote',
      ('Aliases ``{}`` as ``{}#``.').format(
        qualifier,
        abbreviation)),
    (lambda * _: _)(
      'hissp.macros.._macro_.ifQz_else',
      '_QzT7EX5TKYz_reader',
      (lambda * _: _)(
        (lambda * _: _)(
          'builtins..getattr',
          qualifier,
          (lambda * _: _)(
            '.format',
            "('{}{}')",
            '_QzT7EX5TKYz_reader',
            (lambda * _: _)(
              'hissp.macros.._macro_.ifQz_else',
              (lambda * _: _)(
                '.endswith',
                (lambda * _: _)(
                  'quote',
                  qualifier),
                (lambda * _: _)(
                  'quote',
                  '._macro_')),
              (lambda * _: _)(
                'quote',
                'QzHASH_'),
              "('')"))),
        '_QzT7EX5TKYz_prime',
        ':',
        ':*',
        '_QzT7EX5TKYz_args'),
      (lambda * _: _)(
        '.format',
        "('{}.{}')",
        (lambda * _: _)(
          'quote',
          qualifier),
        '_QzT7EX5TKYz_prime'))))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('Defines a reader macro abbreviation of a qualifier.\n'
     '\n'
     '.. code-block:: REPL\n'
     '\n'
     '   #> (hissp.._macro_.alias H: hissp.._macro_)\n'
     '   >>> # hissp.._macro_.alias\n'
     '   ... # hissp.macros.._macro_.defmacro\n'
     '   ... # hissp.macros.._macro_.let\n'
     '   ... (lambda _QzAW22OE5Kz_fn=(lambda '
     '_QzARAQTXTEz_prime,_QzARAQTXTEz_reader=None,*_QzARAQTXTEz_args:(\n'
     "   ...   'Aliases ``hissp.._macro_`` as ``HQzCOLON_#``.',\n"
     '   ...   # hissp.macros.._macro_.ifQz_else\n'
     '   ...   (lambda b,c,a:c()if b else a())(\n'
     '   ...     _QzARAQTXTEz_reader,\n'
     '   ...     (lambda :\n'
     "   ...       __import__('builtins').getattr(\n"
     "   ...         __import__('hissp')._macro_,\n"
     "   ...         ('{}{}').format(\n"
     '   ...           _QzARAQTXTEz_reader,\n'
     '   ...           # hissp.macros.._macro_.ifQz_else\n'
     '   ...           (lambda b,c,a:c()if b else a())(\n'
     "   ...             'hissp.._macro_'.endswith(\n"
     "   ...               '._macro_'),\n"
     "   ...             (lambda :'QzHASH_'),\n"
     "   ...             (lambda :('')))))(\n"
     '   ...         _QzARAQTXTEz_prime,\n'
     '   ...         *_QzARAQTXTEz_args)),\n'
     '   ...     (lambda :\n'
     "   ...       ('{}.{}').format(\n"
     "   ...         'hissp.._macro_',\n"
     '   ...         _QzARAQTXTEz_prime))))[-1]):(\n'
     "   ...   __import__('builtins').setattr(\n"
     '   ...     _QzAW22OE5Kz_fn,\n'
     "   ...     '__doc__',\n"
     "   ...     'Aliases ``hissp.._macro_`` as ``HQzCOLON_#``.'),\n"
     "   ...   __import__('builtins').setattr(\n"
     '   ...     _QzAW22OE5Kz_fn,\n'
     "   ...     '__qualname__',\n"
     "   ...     ('.').join(\n"
     "   ...       ('_macro_',\n"
     "   ...        'HQzCOLON_QzHASH_',))),\n"
     "   ...   __import__('builtins').setattr(\n"
     "   ...     __import__('operator').getitem(\n"
     "   ...       __import__('builtins').globals(),\n"
     "   ...       '_macro_'),\n"
     "   ...     'HQzCOLON_QzHASH_',\n"
     '   ...     _QzAW22OE5Kz_fn))[-1])()\n'
     '\n'
     "   #> 'H:#alias\n"
     "   >>> 'hissp.._macro_.alias'\n"
     "   'hissp.._macro_.alias'\n"
     '\n'
     '   #> H:#b\\#                              ;b# macro callable\n'
     "   >>> __import__('hissp')._macro_.bQzHASH_\n"
     '   <function _macro_.bQzHASH_ at ...>\n'
     '\n'
     '   #> (H:#b\\# "b# macro at compile time")\n'
     '   >>> # hissp.._macro_.bQzHASH_\n'
     "   ... b'b# macro at compile time'\n"
     "   b'b# macro at compile time'\n"
     '\n'
     '   #> hissp.._macro_.b#"Fully-qualified b# macro at read time."\n'
     "   >>> b'Fully-qualified b# macro at read time.'\n"
     "   b'Fully-qualified b# macro at read time.'\n"
     '\n'
     '   #> H:#!b"Read-time b# via alias."      ;Extra arg for alias with (!)\n'
     "   >>> b'Read-time b# via alias.'\n"
     "   b'Read-time b# via alias.'\n"
     '\n'
     'The bundled `op#<opQzHASH_>` and `i#<iQzHASH_>` reader macros are aliases\n'
     'for `operator` and `itertools`, respectively.\n'
     '\n'
     'See also: `prelude`, `attach`.\n')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'alias',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'alias',
    _QzX3UIMF7Uz_fn))[-1])()

# alias
# hissp.macros.._macro_.defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda _QzT7EX5TKYz_prime,_QzT7EX5TKYz_reader=None,*_QzT7EX5TKYz_args:(
  'Aliases ``itertools.`` as ``i#``.',
  # hissp.macros.._macro_.ifQz_else
  (lambda b,c,a:c()if b else a())(
    _QzT7EX5TKYz_reader,
    (lambda :
      __import__('builtins').getattr(
        __import__('itertools'),
        ('{}{}').format(
          _QzT7EX5TKYz_reader,
          # hissp.macros.._macro_.ifQz_else
          (lambda b,c,a:c()if b else a())(
            'itertools.'.endswith(
              '._macro_'),
            (lambda :'QzHASH_'),
            (lambda :('')))))(
        _QzT7EX5TKYz_prime,
        *_QzT7EX5TKYz_args)),
    (lambda :
      ('{}.{}').format(
        'itertools.',
        _QzT7EX5TKYz_prime))))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    'Aliases ``itertools.`` as ``i#``.'),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'iQzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'iQzHASH_',
    _QzX3UIMF7Uz_fn))[-1])()

# alias
# hissp.macros.._macro_.defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda _QzT7EX5TKYz_prime,_QzT7EX5TKYz_reader=None,*_QzT7EX5TKYz_args:(
  'Aliases ``operator.`` as ``op#``.',
  # hissp.macros.._macro_.ifQz_else
  (lambda b,c,a:c()if b else a())(
    _QzT7EX5TKYz_reader,
    (lambda :
      __import__('builtins').getattr(
        __import__('operator'),
        ('{}{}').format(
          _QzT7EX5TKYz_reader,
          # hissp.macros.._macro_.ifQz_else
          (lambda b,c,a:c()if b else a())(
            'operator.'.endswith(
              '._macro_'),
            (lambda :'QzHASH_'),
            (lambda :('')))))(
        _QzT7EX5TKYz_prime,
        *_QzT7EX5TKYz_args)),
    (lambda :
      ('{}.{}').format(
        'operator.',
        _QzT7EX5TKYz_prime))))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    'Aliases ``operator.`` as ``op#``.'),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'opQzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'opQzHASH_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda itr:(
  ('``chain#`` Abbreviation for `itertools.chain.from_iterable`'),
  (lambda * _: _)(
    'itertools..chain.from_iterable',
    itr))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('``chain#`` Abbreviation for `itertools.chain.from_iterable`')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'chainQzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'chainQzHASH_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda e:(
  ("``get#`` 'itemgetter-' Makes an `operator.itemgetter` function from ``e``.\n"
   '\n'
   '.. code-block:: REPL\n'
   '\n'
   '   #> (define first get#0)                ;Gets an item by key.\n'
   '   >>> # define\n'
   "   ... __import__('builtins').globals().update(\n"
   "   ...   first=__import__('operator').itemgetter(\n"
   '   ...           (0)))\n'
   '\n'
   '   #> (first "abc")\n'
   '   >>> first(\n'
   "   ...   ('abc'))\n"
   "   'a'\n"
   '\n'
   '   #> (get#(slice None None -1) "abc")    ;Slicing without injection.\n'
   "   >>> __import__('operator').itemgetter(\n"
   '   ...   slice(\n'
   '   ...     None,\n'
   '   ...     None,\n'
   '   ...     (-1)))(\n'
   "   ...   ('abc'))\n"
   "   'cba'\n"
   '\n'
   "   #> (get#'+ (dict : foo 2  + 1))        ;These also work on dicts.\n"
   "   >>> __import__('operator').itemgetter(\n"
   "   ...   'QzPLUS_')(\n"
   '   ...   dict(\n'
   '   ...     foo=(2),\n'
   '   ...     QzPLUS_=(1)))\n'
   '   1\n'
   '\n'
   'See also: `operator.getitem`, `[#<QzLSQB_QzHASH_>`,\n'
   '`set!<setQzBANG_>`, `^*#<QzHAT_QzSTAR_QzHASH_>`.\n'),
  (lambda * _: _)(
    'operator..itemgetter',
    e))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ("``get#`` 'itemgetter-' Makes an `operator.itemgetter` function from ``e``.\n"
     '\n'
     '.. code-block:: REPL\n'
     '\n'
     '   #> (define first get#0)                ;Gets an item by key.\n'
     '   >>> # define\n'
     "   ... __import__('builtins').globals().update(\n"
     "   ...   first=__import__('operator').itemgetter(\n"
     '   ...           (0)))\n'
     '\n'
     '   #> (first "abc")\n'
     '   >>> first(\n'
     "   ...   ('abc'))\n"
     "   'a'\n"
     '\n'
     '   #> (get#(slice None None -1) "abc")    ;Slicing without injection.\n'
     "   >>> __import__('operator').itemgetter(\n"
     '   ...   slice(\n'
     '   ...     None,\n'
     '   ...     None,\n'
     '   ...     (-1)))(\n'
     "   ...   ('abc'))\n"
     "   'cba'\n"
     '\n'
     "   #> (get#'+ (dict : foo 2  + 1))        ;These also work on dicts.\n"
     "   >>> __import__('operator').itemgetter(\n"
     "   ...   'QzPLUS_')(\n"
     '   ...   dict(\n'
     '   ...     foo=(2),\n'
     '   ...     QzPLUS_=(1)))\n'
     '   1\n'
     '\n'
     'See also: `operator.getitem`, `[#<QzLSQB_QzHASH_>`,\n'
     '`set!<setQzBANG_>`, `^*#<QzHAT_QzSTAR_QzHASH_>`.\n')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'getQzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'getQzHASH_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda definition,decoration:(
  ("``@#!`` 'decorator' applies ``decoration`` to a global and reassigns.\n"
   '\n'
   '  ``definition`` form must assign a global identified by its first arg.\n'
   '  Expands to a `define`, meaning decorators can stack.\n'
   '\n'
   '  Decorator syntax is for global definitions, like `define` and\n'
   '  `deftype`, and would work on any global definition macro that has\n'
   '  the (unqualified) defined name as its first argument.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> @#!str.swapcase\n'
   '     #..@#!str.title\n'
   "     #..(define spam 'spam) ; Unlike Python def, not always a function.\n"
   '     >>> # hissp.macros.._macro_.define\n'
   "     ... __import__('builtins').globals().update(\n"
   '     ...   spam=# hissp.macros.._macro_.progn\n'
   '     ...        (lambda :(\n'
   '     ...          # hissp.macros.._macro_.define\n'
   "     ...          __import__('builtins').globals().update(\n"
   '     ...            spam=# hissp.macros.._macro_.progn\n'
   '     ...                 (lambda :(\n'
   '     ...                   # define\n'
   "     ...                   __import__('builtins').globals().update(\n"
   "     ...                     spam='spam'),\n"
   '     ...                   str.title(\n'
   '     ...                     spam))[-1])()),\n'
   '     ...          str.swapcase(\n'
   '     ...            spam))[-1])())\n'
   '\n'
   '     #> spam\n'
   '     >>> spam\n'
   "     'sPAM'\n"
   '\n'
   '  '),
  # let
  (lambda name=__import__('operator').itemgetter(
    (1))(
    definition):
    (lambda * _: _)(
      'hissp.macros.._macro_.define',
      name,
      (lambda * _: _)(
        'hissp.macros.._macro_.progn',
        definition,
        (lambda * _: _)(
          decoration,
          name))))())[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ("``@#!`` 'decorator' applies ``decoration`` to a global and reassigns.\n"
     '\n'
     '  ``definition`` form must assign a global identified by its first arg.\n'
     '  Expands to a `define`, meaning decorators can stack.\n'
     '\n'
     '  Decorator syntax is for global definitions, like `define` and\n'
     '  `deftype`, and would work on any global definition macro that has\n'
     '  the (unqualified) defined name as its first argument.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> @#!str.swapcase\n'
     '     #..@#!str.title\n'
     "     #..(define spam 'spam) ; Unlike Python def, not always a function.\n"
     '     >>> # hissp.macros.._macro_.define\n'
     "     ... __import__('builtins').globals().update(\n"
     '     ...   spam=# hissp.macros.._macro_.progn\n'
     '     ...        (lambda :(\n'
     '     ...          # hissp.macros.._macro_.define\n'
     "     ...          __import__('builtins').globals().update(\n"
     '     ...            spam=# hissp.macros.._macro_.progn\n'
     '     ...                 (lambda :(\n'
     '     ...                   # define\n'
     "     ...                   __import__('builtins').globals().update(\n"
     "     ...                     spam='spam'),\n"
     '     ...                   str.title(\n'
     '     ...                     spam))[-1])()),\n'
     '     ...          str.swapcase(\n'
     '     ...            spam))[-1])())\n'
     '\n'
     '     #> spam\n'
     '     >>> spam\n'
     "     'sPAM'\n"
     '\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'QzAT_QzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'QzAT_QzHASH_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda e:(
  ("``[#`` 'subscript' Injection. Python's subscription operator.\n"
   '\n'
   '  Creates a function from the Python expression ``e`` prepended with\n'
   '  the argument and a ``[``.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   "     #> ([#1][::2] '(foo bar))\n"
   '     >>> (lambda _Qz5GEAOGSQz_G:(_Qz5GEAOGSQz_G[1][::2]))(\n'
   "     ...   ('foo',\n"
   "     ...    'bar',))\n"
   "     'br'\n"
   '\n'
   '  See also:\n'
   '  `get#<getQzHASH_>`, `-><Qz_QzGT_>`, `slice`, `subscriptions`, `slicings`.\n'
   '  '),
  (lambda * _: _)(
    'lambda',
    (lambda * _: _)(
      '_QzJXZWCGIRz_G'),
    ('({}[{})').format(
      '_QzJXZWCGIRz_G',
      __import__('hissp').demunge(
        e))))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ("``[#`` 'subscript' Injection. Python's subscription operator.\n"
     '\n'
     '  Creates a function from the Python expression ``e`` prepended with\n'
     '  the argument and a ``[``.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     "     #> ([#1][::2] '(foo bar))\n"
     '     >>> (lambda _Qz5GEAOGSQz_G:(_Qz5GEAOGSQz_G[1][::2]))(\n'
     "     ...   ('foo',\n"
     "     ...    'bar',))\n"
     "     'br'\n"
     '\n'
     '  See also:\n'
     '  `get#<getQzHASH_>`, `-><Qz_QzGT_>`, `slice`, `subscriptions`, `slicings`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'QzLSQB_QzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'QzLSQB_QzHASH_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda coll,key,val:(
  ("``set!`` 'setbang' Assigns an item, returns the value.\n"
   '  Mnemonic: set !tem.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> (define spam (dict))\n'
   '     >>> # define\n'
   "     ... __import__('builtins').globals().update(\n"
   '     ...   spam=dict())\n'
   '\n'
   '     #> (set! spam 2 10) ; Like operator.setitem, but returns value given.\n'
   '     #..\n'
   '     >>> # setQzBANG_\n'
   '     ... # hissp.macros.._macro_.let\n'
   '     ... (lambda _QzE3BPTV2Tz_val=(10):(\n'
   "     ...   __import__('operator').setitem(\n"
   '     ...     spam,\n'
   '     ...     (2),\n'
   '     ...     _QzE3BPTV2Tz_val),\n'
   '     ...   _QzE3BPTV2Tz_val)[-1])()\n'
   '     10\n'
   '\n'
   '     #> spam\n'
   '     >>> spam\n'
   '     {2: 10}\n'
   '\n'
   '  See also: `operator.setitem`, `operator.delitem`, `zap!<zapQzBANG_>`.\n'
   '  '),
  (lambda * _: _)(
    'hissp.macros.._macro_.let',
    (lambda * _: _)(
      '_QzIDSB6NBHz_val',
      val),
    (lambda * _: _)(
      'operator..setitem',
      coll,
      key,
      '_QzIDSB6NBHz_val'),
    '_QzIDSB6NBHz_val'))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ("``set!`` 'setbang' Assigns an item, returns the value.\n"
     '  Mnemonic: set !tem.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> (define spam (dict))\n'
     '     >>> # define\n'
     "     ... __import__('builtins').globals().update(\n"
     '     ...   spam=dict())\n'
     '\n'
     '     #> (set! spam 2 10) ; Like operator.setitem, but returns value given.\n'
     '     #..\n'
     '     >>> # setQzBANG_\n'
     '     ... # hissp.macros.._macro_.let\n'
     '     ... (lambda _QzE3BPTV2Tz_val=(10):(\n'
     "     ...   __import__('operator').setitem(\n"
     '     ...     spam,\n'
     '     ...     (2),\n'
     '     ...     _QzE3BPTV2Tz_val),\n'
     '     ...   _QzE3BPTV2Tz_val)[-1])()\n'
     '     10\n'
     '\n'
     '     #> spam\n'
     '     >>> spam\n'
     '     {2: 10}\n'
     '\n'
     '  See also: `operator.setitem`, `operator.delitem`, `zap!<zapQzBANG_>`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'setQzBANG_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'setQzBANG_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda op,coll,key,*args:(
  ("``zap!`` 'zapbang' Augmented item assignment operator.\n"
   '\n'
   '  The current item value becomes the first argument.\n'
   '  Returns the value.\n'
   '  Mnemonic: zap !tem.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> (define spam (dict : b 10))\n'
   '     >>> # define\n'
   "     ... __import__('builtins').globals().update(\n"
   '     ...   spam=dict(\n'
   '     ...          b=(10)))\n'
   '\n'
   "     #> (zap! operator..iadd spam 'b 1) ; Augmented item assignment, like "
   '+=.\n'
   '     #..\n'
   '     >>> # zapQzBANG_\n'
   '     ... # hissp.macros.._macro_.let\n'
   "     ... (lambda _QzRDZYRDXSz_coll=spam,_QzRDZYRDXSz_key='b':\n"
   '     ...   # hissp.macros.._macro_.setQzBANG_\n'
   '     ...   # hissp.macros.._macro_.let\n'
   "     ...   (lambda _QzE3BPTV2Tz_val=__import__('operator').iadd(\n"
   "     ...     __import__('operator').getitem(\n"
   '     ...       _QzRDZYRDXSz_coll,\n'
   '     ...       _QzRDZYRDXSz_key),\n'
   '     ...     (1)):(\n'
   "     ...     __import__('operator').setitem(\n"
   '     ...       _QzRDZYRDXSz_coll,\n'
   '     ...       _QzRDZYRDXSz_key,\n'
   '     ...       _QzE3BPTV2Tz_val),\n'
   '     ...     _QzE3BPTV2Tz_val)[-1])())()\n'
   '     11\n'
   '\n'
   '     #> spam\n'
   '     >>> spam\n'
   "     {'b': 11}\n"
   '\n'
   '  See also: `set!<setQzBANG_>`, `zap@<zapQzAT_>`, `augassign`.\n'
   '  '),
  (lambda * _: _)(
    'hissp.macros.._macro_.let',
    (lambda * _: _)(
      '_QzYG6VGYQYz_coll',
      coll,
      '_QzYG6VGYQYz_key',
      key),
    (lambda * _: _)(
      'hissp.macros.._macro_.setQzBANG_',
      '_QzYG6VGYQYz_coll',
      '_QzYG6VGYQYz_key',
      (lambda * _: _)(
        op,
        (lambda * _: _)(
          'operator..getitem',
          '_QzYG6VGYQYz_coll',
          '_QzYG6VGYQYz_key'),
        *args))))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ("``zap!`` 'zapbang' Augmented item assignment operator.\n"
     '\n'
     '  The current item value becomes the first argument.\n'
     '  Returns the value.\n'
     '  Mnemonic: zap !tem.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> (define spam (dict : b 10))\n'
     '     >>> # define\n'
     "     ... __import__('builtins').globals().update(\n"
     '     ...   spam=dict(\n'
     '     ...          b=(10)))\n'
     '\n'
     "     #> (zap! operator..iadd spam 'b 1) ; Augmented item assignment, like "
     '+=.\n'
     '     #..\n'
     '     >>> # zapQzBANG_\n'
     '     ... # hissp.macros.._macro_.let\n'
     "     ... (lambda _QzRDZYRDXSz_coll=spam,_QzRDZYRDXSz_key='b':\n"
     '     ...   # hissp.macros.._macro_.setQzBANG_\n'
     '     ...   # hissp.macros.._macro_.let\n'
     "     ...   (lambda _QzE3BPTV2Tz_val=__import__('operator').iadd(\n"
     "     ...     __import__('operator').getitem(\n"
     '     ...       _QzRDZYRDXSz_coll,\n'
     '     ...       _QzRDZYRDXSz_key),\n'
     '     ...     (1)):(\n'
     "     ...     __import__('operator').setitem(\n"
     '     ...       _QzRDZYRDXSz_coll,\n'
     '     ...       _QzRDZYRDXSz_key,\n'
     '     ...       _QzE3BPTV2Tz_val),\n'
     '     ...     _QzE3BPTV2Tz_val)[-1])())()\n'
     '     11\n'
     '\n'
     '     #> spam\n'
     '     >>> spam\n'
     "     {'b': 11}\n"
     '\n'
     '  See also: `set!<setQzBANG_>`, `zap@<zapQzAT_>`, `augassign`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'zapQzBANG_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'zapQzBANG_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda name,val:(
  ("``set@`` 'setat' Assigns an attribute, returns the value.\n"
   '  Mnemonic: set @tribute.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> (define spam (types..SimpleNamespace))\n'
   '     >>> # define\n'
   "     ... __import__('builtins').globals().update(\n"
   "     ...   spam=__import__('types').SimpleNamespace())\n"
   '\n'
   '     #> (set@ spam.foo 10)\n'
   '     >>> # setQzAT_\n'
   '     ... # hissp.macros.._macro_.let\n'
   '     ... (lambda _QzRMG5GSSIz_val=(10):(\n'
   "     ...   __import__('builtins').setattr(\n"
   '     ...     spam,\n'
   "     ...     'foo',\n"
   '     ...     _QzRMG5GSSIz_val),\n'
   '     ...   _QzRMG5GSSIz_val)[-1])()\n'
   '     10\n'
   '\n'
   '     #> spam\n'
   '     >>> spam\n'
   '     namespace(foo=10)\n'
   '\n'
   '  See also: `attach`, `delattr`, `zap@<zapQzAT_>`, `setattr`.\n'
   '  '),
  # letQz_from
  (lambda ns,_,attr:
    (lambda * _: _)(
      'hissp.macros.._macro_.let',
      (lambda * _: _)(
        '_QzWBHN72I2z_val',
        val),
      (lambda * _: _)(
        'builtins..setattr',
        ns,
        (lambda * _: _)(
          'quote',
          attr),
        '_QzWBHN72I2z_val'),
      '_QzWBHN72I2z_val'))(
    *name.rpartition(
       ('.'))))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ("``set@`` 'setat' Assigns an attribute, returns the value.\n"
     '  Mnemonic: set @tribute.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> (define spam (types..SimpleNamespace))\n'
     '     >>> # define\n'
     "     ... __import__('builtins').globals().update(\n"
     "     ...   spam=__import__('types').SimpleNamespace())\n"
     '\n'
     '     #> (set@ spam.foo 10)\n'
     '     >>> # setQzAT_\n'
     '     ... # hissp.macros.._macro_.let\n'
     '     ... (lambda _QzRMG5GSSIz_val=(10):(\n'
     "     ...   __import__('builtins').setattr(\n"
     '     ...     spam,\n'
     "     ...     'foo',\n"
     '     ...     _QzRMG5GSSIz_val),\n'
     '     ...   _QzRMG5GSSIz_val)[-1])()\n'
     '     10\n'
     '\n'
     '     #> spam\n'
     '     >>> spam\n'
     '     namespace(foo=10)\n'
     '\n'
     '  See also: `attach`, `delattr`, `zap@<zapQzAT_>`, `setattr`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'setQzAT_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'setQzAT_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda op,name,*args:(
  ("``zap@`` 'zapat' Augmented attribute assignment operator.\n"
   '\n'
   '  The current attribute value becomes the first argument.\n'
   '  Returns the value.\n'
   '  Mnemonic: zap @tribute.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> (define spam (types..SimpleNamespace : foo 10))\n'
   '     >>> # define\n'
   "     ... __import__('builtins').globals().update(\n"
   "     ...   spam=__import__('types').SimpleNamespace(\n"
   '     ...          foo=(10)))\n'
   '\n'
   '     #> (zap@ operator..iadd spam.foo 1)\n'
   '     >>> # zapQzAT_\n'
   '     ... # hissp.macros.._macro_.setQzAT_\n'
   '     ... # hissp.macros.._macro_.let\n'
   "     ... (lambda _QzRMG5GSSIz_val=__import__('operator').iadd(\n"
   '     ...   spam.foo,\n'
   '     ...   (1)):(\n'
   "     ...   __import__('builtins').setattr(\n"
   '     ...     spam,\n'
   "     ...     'foo',\n"
   '     ...     _QzRMG5GSSIz_val),\n'
   '     ...   _QzRMG5GSSIz_val)[-1])()\n'
   '     11\n'
   '\n'
   '     #> spam\n'
   '     >>> spam\n'
   '     namespace(foo=11)\n'
   '\n'
   '\n'
   '  See also:\n'
   '  `set@<setQzAT_>`, `zap!<zapQzBANG_>`, `operator.iadd`, `augassign`.\n'
   '  '),
  (lambda * _: _)(
    'hissp.macros.._macro_.setQzAT_',
    name,
    (lambda * _: _)(
      op,
      name,
      *args)))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ("``zap@`` 'zapat' Augmented attribute assignment operator.\n"
     '\n'
     '  The current attribute value becomes the first argument.\n'
     '  Returns the value.\n'
     '  Mnemonic: zap @tribute.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> (define spam (types..SimpleNamespace : foo 10))\n'
     '     >>> # define\n'
     "     ... __import__('builtins').globals().update(\n"
     "     ...   spam=__import__('types').SimpleNamespace(\n"
     '     ...          foo=(10)))\n'
     '\n'
     '     #> (zap@ operator..iadd spam.foo 1)\n'
     '     >>> # zapQzAT_\n'
     '     ... # hissp.macros.._macro_.setQzAT_\n'
     '     ... # hissp.macros.._macro_.let\n'
     "     ... (lambda _QzRMG5GSSIz_val=__import__('operator').iadd(\n"
     '     ...   spam.foo,\n'
     '     ...   (1)):(\n'
     "     ...   __import__('builtins').setattr(\n"
     '     ...     spam,\n'
     "     ...     'foo',\n"
     '     ...     _QzRMG5GSSIz_val),\n'
     '     ...   _QzRMG5GSSIz_val)[-1])()\n'
     '     11\n'
     '\n'
     '     #> spam\n'
     '     >>> spam\n'
     '     namespace(foo=11)\n'
     '\n'
     '\n'
     '  See also:\n'
     '  `set@<setQzAT_>`, `zap!<zapQzBANG_>`, `operator.iadd`, `augassign`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'zapQzAT_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'zapQzAT_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda target,*args:(
  ('Attaches the named variables to the target as attributes.\n'
   '\n'
   '  Positional arguments must be identifiers. The identifier name becomes\n'
   '  the attribute name. Names after the ``:`` are identifier-value pairs.\n'
   '  Returns the target.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   "     #> (attach (types..SimpleNamespace) _macro_.attach : a 1  b 'Hi)\n"
   '     >>> # attach\n'
   '     ... # hissp.macros.._macro_.let\n'
   '     ... (lambda '
   "_QzWG5WN73Wz_target=__import__('types').SimpleNamespace():(\n"
   "     ...   __import__('builtins').setattr(\n"
   '     ...     _QzWG5WN73Wz_target,\n'
   "     ...     'attach',\n"
   '     ...     _macro_.attach),\n'
   "     ...   __import__('builtins').setattr(\n"
   '     ...     _QzWG5WN73Wz_target,\n'
   "     ...     'a',\n"
   '     ...     (1)),\n'
   "     ...   __import__('builtins').setattr(\n"
   '     ...     _QzWG5WN73Wz_target,\n'
   "     ...     'b',\n"
   "     ...     'Hi'),\n"
   '     ...   _QzWG5WN73Wz_target)[-1])()\n'
   "     namespace(a=1, attach=<function _macro_.attach at 0x...>, b='Hi')\n"
   '\n'
   '  See also: `setattr`, `set@<setQzAT_>`, `vars`.\n'
   '  '),
  # let
  (lambda iargs=iter(
    args),QzDOLR_target='_QzZAVQQ4JMz_target':
    # let
    (lambda args=__import__('itertools').takewhile(
      (lambda X:
        __import__('operator').ne(
          X,
          ':')),
      iargs):
      (lambda * _: _)(
        'hissp.macros.._macro_.let',
        (lambda * _: _)(
          QzDOLR_target,
          target),
        *map(
           (lambda X:
             (lambda * _: _)(
               'builtins..setattr',
               QzDOLR_target,
               (lambda * _: _)(
                 'quote',
                 X.split('.')[-1]),
               X)),
           args),
        *map(
           (lambda X:
             (lambda * _: _)(
               'builtins..setattr',
               QzDOLR_target,
               (lambda * _: _)(
                 'quote',
                 X),
               next(
                 iargs))),
           iargs),
        QzDOLR_target))())())[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('Attaches the named variables to the target as attributes.\n'
     '\n'
     '  Positional arguments must be identifiers. The identifier name becomes\n'
     '  the attribute name. Names after the ``:`` are identifier-value pairs.\n'
     '  Returns the target.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     "     #> (attach (types..SimpleNamespace) _macro_.attach : a 1  b 'Hi)\n"
     '     >>> # attach\n'
     '     ... # hissp.macros.._macro_.let\n'
     '     ... (lambda '
     "_QzWG5WN73Wz_target=__import__('types').SimpleNamespace():(\n"
     "     ...   __import__('builtins').setattr(\n"
     '     ...     _QzWG5WN73Wz_target,\n'
     "     ...     'attach',\n"
     '     ...     _macro_.attach),\n'
     "     ...   __import__('builtins').setattr(\n"
     '     ...     _QzWG5WN73Wz_target,\n'
     "     ...     'a',\n"
     '     ...     (1)),\n'
     "     ...   __import__('builtins').setattr(\n"
     '     ...     _QzWG5WN73Wz_target,\n'
     "     ...     'b',\n"
     "     ...     'Hi'),\n"
     '     ...   _QzWG5WN73Wz_target)[-1])()\n'
     "     namespace(a=1, attach=<function _macro_.attach at 0x...>, b='Hi')\n"
     '\n'
     '  See also: `setattr`, `set@<setQzAT_>`, `vars`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'attach',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'attach',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda self,*invocations:(
  ('Configure an object.\n'
   '\n'
   "  Calls multiple 'methods' on one 'self'.\n"
   '\n'
   '  Evaluates the given ``self``, then injects it as the first argument to\n'
   '  a sequence of invocations. Returns ``self``.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> (doto (list)\n'
   "     #..  (.extend 'bar)\n"
   '     #..  .sort\n'
   "     #..  (.append 'foo))\n"
   '     >>> # doto\n'
   '     ... (lambda _QzKIUMBHNZz_self=list():(\n'
   '     ...   _QzKIUMBHNZz_self.extend(\n'
   "     ...     'bar'),\n"
   '     ...   _QzKIUMBHNZz_self.sort(),\n'
   '     ...   _QzKIUMBHNZz_self.append(\n'
   "     ...     'foo'),\n"
   '     ...   _QzKIUMBHNZz_self)[-1])()\n'
   "     ['a', 'b', 'r', 'foo']\n"
   '\n'
   '  See also: `attach`, `progn`, `-> <Qz_QzGT_>`.\n'
   '  '),
  # let
  (lambda QzDOLR_self='_Qz3GN5LTOBz_self':
    (lambda * _: _)(
      (lambda * _: _)(
        'lambda',
        (lambda * _: _)(
          ':',
          QzDOLR_self,
          self),
        *map(
           (lambda X:
             (lambda * _: _)(
               __import__('operator').itemgetter(
                 (0))(
                 X),
               QzDOLR_self,
               *(lambda _QzJXZWCGIRz_G:(_QzJXZWCGIRz_G[1:]))(
                  X))),
           map(
             (lambda X:X if type(X) is tuple else (X,)),
             invocations)),
        QzDOLR_self)))())[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('Configure an object.\n'
     '\n'
     "  Calls multiple 'methods' on one 'self'.\n"
     '\n'
     '  Evaluates the given ``self``, then injects it as the first argument to\n'
     '  a sequence of invocations. Returns ``self``.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> (doto (list)\n'
     "     #..  (.extend 'bar)\n"
     '     #..  .sort\n'
     "     #..  (.append 'foo))\n"
     '     >>> # doto\n'
     '     ... (lambda _QzKIUMBHNZz_self=list():(\n'
     '     ...   _QzKIUMBHNZz_self.extend(\n'
     "     ...     'bar'),\n"
     '     ...   _QzKIUMBHNZz_self.sort(),\n'
     '     ...   _QzKIUMBHNZz_self.append(\n'
     "     ...     'foo'),\n"
     '     ...   _QzKIUMBHNZz_self)[-1])()\n'
     "     ['a', 'b', 'r', 'foo']\n"
     '\n'
     '  See also: `attach`, `progn`, `-> <Qz_QzGT_>`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'doto',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'doto',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda expr,*forms:(
  ("``->`` 'Thread-first'.\n"
   '\n'
   '  Converts a pipeline to function calls by recursively threading\n'
   '  expressions as the first argument of the next form.\n'
   '  Non-tuple forms (typically function identifiers) will be wrapped\n'
   '  in a tuple. Can make chained method calls easier to read.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   "     #> (.-> _macro_ : :* '(x (A b) (C d e)))\n"
   '     >>> _macro_.Qz_QzGT_(\n'
   "     ...   *('x',\n"
   "     ...     ('A',\n"
   "     ...      'b',),\n"
   "     ...     ('C',\n"
   "     ...      'd',\n"
   "     ...      'e',),))\n"
   "     ('C', ('A', 'x', 'b'), 'd', 'e')\n"
   '\n'
   "     #> (-> 'a set (en#list 'bc) (en#tuple 'de))\n"
   '     >>> # Qz_QzGT_\n'
   '     ... (lambda *_Qz6RFWTTVXz_xs:\n'
   '     ...   tuple(\n'
   '     ...     _Qz6RFWTTVXz_xs))(\n'
   '     ...   (lambda *_Qz6RFWTTVXz_xs:\n'
   '     ...     list(\n'
   '     ...       _Qz6RFWTTVXz_xs))(\n'
   '     ...     set(\n'
   "     ...       'a'),\n"
   "     ...     'bc'),\n"
   "     ...   'de')\n"
   "     ([{'a'}, 'bc'], 'de')\n"
   '\n'
   '  See also:\n'
   '  `-\\<>><Qz_QzLT_QzGT_QzGT_>`, `X#<XQzHASH_>`, `get#<getQzHASH_>`.\n'
   '  '),
  __import__('functools').reduce(
    (lambda X,Y:(Y[0],X,*Y[1:],)),
    map(
      (lambda X:X if type(X) is tuple else (X,)),
      forms),
    expr))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ("``->`` 'Thread-first'.\n"
     '\n'
     '  Converts a pipeline to function calls by recursively threading\n'
     '  expressions as the first argument of the next form.\n'
     '  Non-tuple forms (typically function identifiers) will be wrapped\n'
     '  in a tuple. Can make chained method calls easier to read.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     "     #> (.-> _macro_ : :* '(x (A b) (C d e)))\n"
     '     >>> _macro_.Qz_QzGT_(\n'
     "     ...   *('x',\n"
     "     ...     ('A',\n"
     "     ...      'b',),\n"
     "     ...     ('C',\n"
     "     ...      'd',\n"
     "     ...      'e',),))\n"
     "     ('C', ('A', 'x', 'b'), 'd', 'e')\n"
     '\n'
     "     #> (-> 'a set (en#list 'bc) (en#tuple 'de))\n"
     '     >>> # Qz_QzGT_\n'
     '     ... (lambda *_Qz6RFWTTVXz_xs:\n'
     '     ...   tuple(\n'
     '     ...     _Qz6RFWTTVXz_xs))(\n'
     '     ...   (lambda *_Qz6RFWTTVXz_xs:\n'
     '     ...     list(\n'
     '     ...       _Qz6RFWTTVXz_xs))(\n'
     '     ...     set(\n'
     "     ...       'a'),\n"
     "     ...     'bc'),\n"
     "     ...   'de')\n"
     "     ([{'a'}, 'bc'], 'de')\n"
     '\n'
     '  See also:\n'
     '  `-\\<>><Qz_QzLT_QzGT_QzGT_>`, `X#<XQzHASH_>`, `get#<getQzHASH_>`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'Qz_QzGT_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'Qz_QzGT_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda expr,*forms:(
  ("``-<>>`` 'Thread-through'.\n"
   '\n'
   '  Converts a pipeline to function calls by recursively threading\n'
   '  expressions into the next form at the first point indicated with\n'
   '  ``:<>``, or at the last if no ``:<>`` is found. Non-tuple forms\n'
   '  (typically function identifiers) will be wrapped in a tuple first.\n'
   '  Can replace partial application in some cases.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   "     #> (.-<>> _macro_ : :* '(x Y (:<> A b) (C d e)))\n"
   '     >>> _macro_.Qz_QzLT_QzGT_QzGT_(\n'
   "     ...   *('x',\n"
   "     ...     'Y',\n"
   "     ...     (':<>',\n"
   "     ...      'A',\n"
   "     ...      'b',),\n"
   "     ...     ('C',\n"
   "     ...      'd',\n"
   "     ...      'e',),))\n"
   "     ('C', 'd', 'e', (('Y', 'x'), 'A', 'b'))\n"
   '\n'
   "     #> (-<>> 'a set (en#list 'bc) (en#tuple 'de :<> 'fg :<>))\n"
   '     >>> # Qz_QzLT_QzGT_QzGT_\n'
   '     ... (lambda *_Qz6RFWTTVXz_xs:\n'
   '     ...   tuple(\n'
   '     ...     _Qz6RFWTTVXz_xs))(\n'
   "     ...   'de',\n"
   '     ...   (lambda *_Qz6RFWTTVXz_xs:\n'
   '     ...     list(\n'
   '     ...       _Qz6RFWTTVXz_xs))(\n'
   "     ...     'bc',\n"
   '     ...     set(\n'
   "     ...       'a')),\n"
   "     ...   'fg',\n"
   "     ...   ':<>')\n"
   "     ('de', ['bc', {'a'}], 'fg', ':<>')\n"
   '\n'
   '  See also: `-><Qz_QzGT_>`.\n'
   '  '),
  __import__('functools').reduce(
    (lambda X,Y:
      # let
      (lambda i=iter(
        Y):
        (lambda * _: _)(
          *__import__('itertools').takewhile(
             (lambda X:
               __import__('operator').ne(
                 X,
                 ':<>')),
             i),
          X,
          *i))()),
    map(
      (lambda X:X if type(X) is tuple else (X,)),
      forms),
    expr))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ("``-<>>`` 'Thread-through'.\n"
     '\n'
     '  Converts a pipeline to function calls by recursively threading\n'
     '  expressions into the next form at the first point indicated with\n'
     '  ``:<>``, or at the last if no ``:<>`` is found. Non-tuple forms\n'
     '  (typically function identifiers) will be wrapped in a tuple first.\n'
     '  Can replace partial application in some cases.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     "     #> (.-<>> _macro_ : :* '(x Y (:<> A b) (C d e)))\n"
     '     >>> _macro_.Qz_QzLT_QzGT_QzGT_(\n'
     "     ...   *('x',\n"
     "     ...     'Y',\n"
     "     ...     (':<>',\n"
     "     ...      'A',\n"
     "     ...      'b',),\n"
     "     ...     ('C',\n"
     "     ...      'd',\n"
     "     ...      'e',),))\n"
     "     ('C', 'd', 'e', (('Y', 'x'), 'A', 'b'))\n"
     '\n'
     "     #> (-<>> 'a set (en#list 'bc) (en#tuple 'de :<> 'fg :<>))\n"
     '     >>> # Qz_QzLT_QzGT_QzGT_\n'
     '     ... (lambda *_Qz6RFWTTVXz_xs:\n'
     '     ...   tuple(\n'
     '     ...     _Qz6RFWTTVXz_xs))(\n'
     "     ...   'de',\n"
     '     ...   (lambda *_Qz6RFWTTVXz_xs:\n'
     '     ...     list(\n'
     '     ...       _Qz6RFWTTVXz_xs))(\n'
     "     ...     'bc',\n"
     '     ...     set(\n'
     "     ...       'a')),\n"
     "     ...   'fg',\n"
     "     ...   ':<>')\n"
     "     ('de', ['bc', {'a'}], 'fg', ':<>')\n"
     '\n'
     '  See also: `-><Qz_QzGT_>`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'Qz_QzLT_QzGT_QzGT_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'Qz_QzLT_QzGT_QzGT_',
    _QzX3UIMF7Uz_fn))[-1])()

# define
__import__('builtins').globals().update(
  _TAO=(lambda s:
         # Qz_QzGT_
         (' ').join(
           __import__('re').findall(
             ('(?m)^# (.*)~$'),
             s(
               __import__('hissp')))).replace(
           (':'),
           ('\n'))))

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda *pairs:(
  ('Multiple condition branching.\n'
   '\n'
   '  Pairs are implied by position. Default is ``()``, use something always\n'
   '  truthy to change it, like ``:else`` or `True`. For example,\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> (any-map x (@ -0.6 -0.0 42.0 math..nan)\n'
   '     #..  (cond (op#lt x 0) (print :Negative) ;if-else cascade\n'
   '     #..        (op#eq x 0) (print :Zero)\n'
   '     #..        (op#gt x 0) (print :Positive)\n'
   '     #..        :else (print :Not-a-Number)))\n'
   '     >>> # anyQz_map\n'
   "     ... __import__('builtins').any(\n"
   "     ...   __import__('builtins').map(\n"
   '     ...     (lambda x:\n'
   '     ...       # cond\n'
   '     ...       (lambda x0,x1,x2,x3,x4,x5,x6,x7:x1()if x0 else x3()if '
   'x2()else x5()if x4()else x7()if x6()else())(\n'
   "     ...         __import__('operator').lt(\n"
   '     ...           x,\n'
   '     ...           (0)),\n'
   '     ...         (lambda :\n'
   '     ...           print(\n'
   "     ...             ':Negative')),\n"
   '     ...         (lambda :\n'
   "     ...           __import__('operator').eq(\n"
   '     ...             x,\n'
   '     ...             (0))),\n'
   '     ...         (lambda :\n'
   '     ...           print(\n'
   "     ...             ':Zero')),\n"
   '     ...         (lambda :\n'
   "     ...           __import__('operator').gt(\n"
   '     ...             x,\n'
   '     ...             (0))),\n'
   '     ...         (lambda :\n'
   '     ...           print(\n'
   "     ...             ':Positive')),\n"
   "     ...         (lambda :':else'),\n"
   '     ...         (lambda :\n'
   '     ...           print(\n'
   "     ...             ':Not-a-Number')))),\n"
   '     ...     # QzAT_\n'
   '     ...     (lambda *xs:[*xs])(\n'
   '     ...       (-0.6),\n'
   '     ...       (-0.0),\n'
   '     ...       (42.0),\n'
   "     ...       __import__('math').nan)))\n"
   '     :Negative\n'
   '     :Zero\n'
   '     :Positive\n'
   '     :Not-a-Number\n'
   '     False\n'
   '\n'
   '  See also: `if-else<ifQz_else>`, `case`, `any-map<anyQz_map>`, `elif`.\n'
   '  '),
  # when
  (lambda b,c:c()if b else())(
    pairs,
    (lambda :
      (lambda * _: _)(
        (lambda * _: _)(
          'lambda',
          (lambda * _: _)(
            *map(
               (lambda X:f'x{X}'),
               range(
                 (lambda X:X+1&-2)(
                   len(
                     pairs))))),
          __import__('operator').concat(
            ('else ').join(
              (lambda * _: _)(
                ('x1()if x0 '),
                *map(
                   (lambda X:f'x{X+1}()if x{X}()'),
                   range(
                     (2),
                     len(
                       pairs),
                     (2))))),
            ('else()'))),
        (lambda _QzJXZWCGIRz_G:(_QzJXZWCGIRz_G[0]))(
          pairs),
        *map(
           (lambda X:
             (lambda * _: _)(
               'lambda',
               ':',
               X)),
           (lambda _QzJXZWCGIRz_G:(_QzJXZWCGIRz_G[1:]))(
             pairs))))))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('Multiple condition branching.\n'
     '\n'
     '  Pairs are implied by position. Default is ``()``, use something always\n'
     '  truthy to change it, like ``:else`` or `True`. For example,\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> (any-map x (@ -0.6 -0.0 42.0 math..nan)\n'
     '     #..  (cond (op#lt x 0) (print :Negative) ;if-else cascade\n'
     '     #..        (op#eq x 0) (print :Zero)\n'
     '     #..        (op#gt x 0) (print :Positive)\n'
     '     #..        :else (print :Not-a-Number)))\n'
     '     >>> # anyQz_map\n'
     "     ... __import__('builtins').any(\n"
     "     ...   __import__('builtins').map(\n"
     '     ...     (lambda x:\n'
     '     ...       # cond\n'
     '     ...       (lambda x0,x1,x2,x3,x4,x5,x6,x7:x1()if x0 else x3()if '
     'x2()else x5()if x4()else x7()if x6()else())(\n'
     "     ...         __import__('operator').lt(\n"
     '     ...           x,\n'
     '     ...           (0)),\n'
     '     ...         (lambda :\n'
     '     ...           print(\n'
     "     ...             ':Negative')),\n"
     '     ...         (lambda :\n'
     "     ...           __import__('operator').eq(\n"
     '     ...             x,\n'
     '     ...             (0))),\n'
     '     ...         (lambda :\n'
     '     ...           print(\n'
     "     ...             ':Zero')),\n"
     '     ...         (lambda :\n'
     "     ...           __import__('operator').gt(\n"
     '     ...             x,\n'
     '     ...             (0))),\n'
     '     ...         (lambda :\n'
     '     ...           print(\n'
     "     ...             ':Positive')),\n"
     "     ...         (lambda :':else'),\n"
     '     ...         (lambda :\n'
     '     ...           print(\n'
     "     ...             ':Not-a-Number')))),\n"
     '     ...     # QzAT_\n'
     '     ...     (lambda *xs:[*xs])(\n'
     '     ...       (-0.6),\n'
     '     ...       (-0.0),\n'
     '     ...       (42.0),\n'
     "     ...       __import__('math').nan)))\n"
     '     :Negative\n'
     '     :Zero\n'
     '     :Positive\n'
     '     :Not-a-Number\n'
     '     False\n'
     '\n'
     '  See also: `if-else<ifQz_else>`, `case`, `any-map<anyQz_map>`, `elif`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'cond',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'cond',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda variable,xs,*body:(
  ('``any-map``\n'
   '  Bind the variable and evaluate the body for each x from xs\n'
   '  until any result is true (and return ``True``), or until xs is\n'
   '  exhausted (and return ``False``).\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> (any-map index (range 1 11)         ;Imperative loop with break.\n'
   '     #..  (print index : end :)\n'
   '     #..  (not (op#mod index 7)))\n'
   '     >>> # anyQz_map\n'
   "     ... __import__('builtins').any(\n"
   "     ...   __import__('builtins').map(\n"
   '     ...     (lambda index:(\n'
   '     ...       print(\n'
   '     ...         index,\n'
   "     ...         end=':'),\n"
   '     ...       not(\n'
   "     ...         __import__('operator').mod(\n"
   '     ...           index,\n'
   '     ...           (7))))[-1]),\n'
   '     ...     range(\n'
   '     ...       (1),\n'
   '     ...       (11))))\n'
   '     1:2:3:4:5:6:7:True\n'
   '\n'
   '  See also: `any`, `map`, `any*map<anyQzSTAR_map>`, `for`, `break`,\n'
   '  `functools.reduce`.\n'
   '  '),
  (lambda * _: _)(
    'builtins..any',
    (lambda * _: _)(
      'builtins..map',
      (lambda * _: _)(
        'lambda',
        (lambda * _: _)(
          variable),
        *body),
      xs)))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('``any-map``\n'
     '  Bind the variable and evaluate the body for each x from xs\n'
     '  until any result is true (and return ``True``), or until xs is\n'
     '  exhausted (and return ``False``).\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> (any-map index (range 1 11)         ;Imperative loop with break.\n'
     '     #..  (print index : end :)\n'
     '     #..  (not (op#mod index 7)))\n'
     '     >>> # anyQz_map\n'
     "     ... __import__('builtins').any(\n"
     "     ...   __import__('builtins').map(\n"
     '     ...     (lambda index:(\n'
     '     ...       print(\n'
     '     ...         index,\n'
     "     ...         end=':'),\n"
     '     ...       not(\n'
     "     ...         __import__('operator').mod(\n"
     '     ...           index,\n'
     '     ...           (7))))[-1]),\n'
     '     ...     range(\n'
     '     ...       (1),\n'
     '     ...       (11))))\n'
     '     1:2:3:4:5:6:7:True\n'
     '\n'
     '  See also: `any`, `map`, `any*map<anyQzSTAR_map>`, `for`, `break`,\n'
     '  `functools.reduce`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'anyQz_map',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'anyQz_map',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda variables,xss,*body:(
  ("``any*map`` 'any star map'\n"
   '  Bind each x to a variable and evaluate the body for each xs from xss\n'
   '  until any result is true (and return ``True``), or until xss is\n'
   '  exhausted (and return ``False``).\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   "     #> (any*map (i c) (enumerate 'abc 1)  ;As any-map, but with starmap.\n"
   '     #..  (print (op#mul i c)))\n'
   '     >>> # anyQzSTAR_map\n'
   "     ... __import__('builtins').any(\n"
   "     ...   __import__('itertools').starmap(\n"
   '     ...     (lambda i,c:\n'
   '     ...       print(\n'
   "     ...         __import__('operator').mul(\n"
   '     ...           i,\n'
   '     ...           c))),\n'
   '     ...     enumerate(\n'
   "     ...       'abc',\n"
   '     ...       (1))))\n'
   '     a\n'
   '     bb\n'
   '     ccc\n'
   '     False\n'
   '\n'
   '  See also:\n'
   '  `itertools.starmap`, `any-map<anyQz_map>`, `loop-from<loopQz_from>`.\n'
   '  '),
  (lambda * _: _)(
    'builtins..any',
    (lambda * _: _)(
      'itertools..starmap',
      (lambda * _: _)(
        'lambda',
        variables,
        *body),
      xss)))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ("``any*map`` 'any star map'\n"
     '  Bind each x to a variable and evaluate the body for each xs from xss\n'
     '  until any result is true (and return ``True``), or until xss is\n'
     '  exhausted (and return ``False``).\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     "     #> (any*map (i c) (enumerate 'abc 1)  ;As any-map, but with starmap.\n"
     '     #..  (print (op#mul i c)))\n'
     '     >>> # anyQzSTAR_map\n'
     "     ... __import__('builtins').any(\n"
     "     ...   __import__('itertools').starmap(\n"
     '     ...     (lambda i,c:\n'
     '     ...       print(\n'
     "     ...         __import__('operator').mul(\n"
     '     ...           i,\n'
     '     ...           c))),\n'
     '     ...     enumerate(\n'
     "     ...       'abc',\n"
     '     ...       (1))))\n'
     '     a\n'
     '     bb\n'
     '     ccc\n'
     '     False\n'
     '\n'
     '  See also:\n'
     '  `itertools.starmap`, `any-map<anyQz_map>`, `loop-from<loopQz_from>`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'anyQzSTAR_map',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'anyQzSTAR_map',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda syms,inits,*body:(
  ('``loop-from`` Anaphoric. Loop/recur with trampoline.\n'
   '\n'
   '  Set local values for the first loop with an iterable as\n'
   '  `let-from<letQz_from>`.\n'
   '\n'
   '  Creates a stack to schedule future loops. Call the ``recur-from``\n'
   '  anaphor with an iterable of values for the locals to push another loop\n'
   '  to the schedule. Call with None to abort any remaining schedule.\n'
   '\n'
   '  Returns the value of the final loop.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   "     #> (loop-from x '(3)                   ;Unpacks as let-from.\n"
   '     #..  (when x\n'
   '     #..    (print x)\n'
   '     #..    (recur-from (@ (op#sub x 1)))))\n'
   '     >>> # loopQz_from\n'
   '     ... # hissp.macros.._macro_.let\n'
   '     ... (lambda _QzDKFIH6Z2z_stack=# hissp.macros..QzMaybe_.QzAT_\n'
   '     ... (lambda *xs:[*xs])(\n'
   '     ...   (),\n'
   '     ...   None,\n'
   '     ...   ((3),)):\n'
   '     ...   # hissp.macros.._macro_.let\n'
   '     ...   (lambda recurQz_from=_QzDKFIH6Z2z_stack.append:(\n'
   '     ...     # hissp.macros.._macro_.anyQzSTAR_map\n'
   "     ...     __import__('builtins').any(\n"
   "     ...       __import__('itertools').starmap(\n"
   '     ...         (lambda x:(\n'
   "     ...           __import__('operator').setitem(\n"
   '     ...             _QzDKFIH6Z2z_stack,\n'
   '     ...             (0),\n'
   '     ...             # hissp.macros.._macro_.progn\n'
   '     ...             (lambda :\n'
   '     ...               # when\n'
   '     ...               (lambda b,c:c()if b else())(\n'
   '     ...                 x,\n'
   '     ...                 (lambda :(\n'
   '     ...                   print(\n'
   '     ...                     x),\n'
   '     ...                   recurQz_from(\n'
   '     ...                     # QzAT_\n'
   '     ...                     (lambda *xs:[*xs])(\n'
   "     ...                       __import__('operator').sub(\n"
   '     ...                         x,\n'
   '     ...                         (1)))))[-1])))()),\n'
   '     ...           None)[-1]),\n'
   "     ...         __import__('builtins').iter(\n"
   '     ...           _QzDKFIH6Z2z_stack.pop,\n'
   '     ...           None))),\n'
   "     ...     __import__('operator').itemgetter(\n"
   '     ...       (0))(\n'
   '     ...       _QzDKFIH6Z2z_stack))[-1])())()\n'
   '     3\n'
   '     2\n'
   '     1\n'
   '     ()\n'
   '\n'
   '  See also: `any*map<anyQzSTAR_map>`, `Ensue`_, `while`.\n'
   '  '),
  (lambda * _: _)(
    'hissp.macros.._macro_.let',
    (lambda * _: _)(
      '_QzZYW5MCGMz_stack',
      (lambda * _: _)(
        'hissp.macros..QzMaybe_.QzAT_',
        (),
        None,
        inits)),
    (lambda * _: _)(
      'hissp.macros.._macro_.let',
      (lambda * _: _)(
        'recurQz_from',
        '_QzZYW5MCGMz_stack.append'),
      (lambda * _: _)(
        'hissp.macros.._macro_.anyQzSTAR_map',
        syms,
        (lambda * _: _)(
          'builtins..iter',
          '_QzZYW5MCGMz_stack.pop',
          None),
        (lambda * _: _)(
          'operator..setitem',
          '_QzZYW5MCGMz_stack',
          (0),
          (lambda * _: _)(
            'hissp.macros.._macro_.progn',
            *body)),
        None),
      (lambda * _: _)(
        (lambda * _: _)(
          'operator..itemgetter',
          (0)),
        '_QzZYW5MCGMz_stack'))))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('``loop-from`` Anaphoric. Loop/recur with trampoline.\n'
     '\n'
     '  Set local values for the first loop with an iterable as\n'
     '  `let-from<letQz_from>`.\n'
     '\n'
     '  Creates a stack to schedule future loops. Call the ``recur-from``\n'
     '  anaphor with an iterable of values for the locals to push another loop\n'
     '  to the schedule. Call with None to abort any remaining schedule.\n'
     '\n'
     '  Returns the value of the final loop.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     "     #> (loop-from x '(3)                   ;Unpacks as let-from.\n"
     '     #..  (when x\n'
     '     #..    (print x)\n'
     '     #..    (recur-from (@ (op#sub x 1)))))\n'
     '     >>> # loopQz_from\n'
     '     ... # hissp.macros.._macro_.let\n'
     '     ... (lambda _QzDKFIH6Z2z_stack=# hissp.macros..QzMaybe_.QzAT_\n'
     '     ... (lambda *xs:[*xs])(\n'
     '     ...   (),\n'
     '     ...   None,\n'
     '     ...   ((3),)):\n'
     '     ...   # hissp.macros.._macro_.let\n'
     '     ...   (lambda recurQz_from=_QzDKFIH6Z2z_stack.append:(\n'
     '     ...     # hissp.macros.._macro_.anyQzSTAR_map\n'
     "     ...     __import__('builtins').any(\n"
     "     ...       __import__('itertools').starmap(\n"
     '     ...         (lambda x:(\n'
     "     ...           __import__('operator').setitem(\n"
     '     ...             _QzDKFIH6Z2z_stack,\n'
     '     ...             (0),\n'
     '     ...             # hissp.macros.._macro_.progn\n'
     '     ...             (lambda :\n'
     '     ...               # when\n'
     '     ...               (lambda b,c:c()if b else())(\n'
     '     ...                 x,\n'
     '     ...                 (lambda :(\n'
     '     ...                   print(\n'
     '     ...                     x),\n'
     '     ...                   recurQz_from(\n'
     '     ...                     # QzAT_\n'
     '     ...                     (lambda *xs:[*xs])(\n'
     "     ...                       __import__('operator').sub(\n"
     '     ...                         x,\n'
     '     ...                         (1)))))[-1])))()),\n'
     '     ...           None)[-1]),\n'
     "     ...         __import__('builtins').iter(\n"
     '     ...           _QzDKFIH6Z2z_stack.pop,\n'
     '     ...           None))),\n'
     "     ...     __import__('operator').itemgetter(\n"
     '     ...       (0))(\n'
     '     ...       _QzDKFIH6Z2z_stack))[-1])())()\n'
     '     3\n'
     '     2\n'
     '     1\n'
     '     ()\n'
     '\n'
     '  See also: `any*map<anyQzSTAR_map>`, `Ensue`_, `while`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'loopQz_from',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'loopQz_from',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda *exprs:(
  ("``&&`` 'and'. Shortcutting logical AND.\n"
   '  Returns the first false value, otherwise the last value.\n'
   '  There is an implicit initial value of ``True``.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> (&& True True False) ; and finds the False\n'
   '     >>> # QzET_QzET_\n'
   '     ... (lambda x0,x1,x2:x0 and x1()and x2())(\n'
   '     ...   True,\n'
   '     ...   (lambda :True),\n'
   '     ...   (lambda :False))\n'
   '     False\n'
   '\n'
   "     #> (&& False (print 'oops)) ; Shortcutting.\n"
   '     >>> # QzET_QzET_\n'
   '     ... (lambda x0,x1:x0 and x1())(\n'
   '     ...   False,\n'
   '     ...   (lambda :\n'
   '     ...     print(\n'
   "     ...       'oops')))\n"
   '     False\n'
   '\n'
   '     #> (&& True 42)\n'
   '     >>> # QzET_QzET_\n'
   '     ... (lambda x0,x1:x0 and x1())(\n'
   '     ...   True,\n'
   '     ...   (lambda :(42)))\n'
   '     42\n'
   '\n'
   '     #> (&&)\n'
   '     >>> # QzET_QzET_\n'
   '     ... True\n'
   '     True\n'
   '\n'
   '     #> (&& 42)\n'
   '     >>> # QzET_QzET_\n'
   '     ... (42)\n'
   '     42\n'
   '\n'
   '  See also: `||<QzVERT_QzVERT_>`, `and`.\n'
   '  '),
  # cond
  (lambda x0,x1,x2,x3,x4,x5:x1()if x0 else x3()if x2()else x5()if x4()else())(
    not(
      exprs),
    (lambda :True),
    (lambda :
      __import__('operator').eq(
        len(
          exprs),
        (1))),
    (lambda :
      __import__('operator').itemgetter(
        (0))(
        exprs)),
    (lambda :':else'),
    (lambda :
      (lambda * _: _)(
        (lambda * _: _)(
          'lambda',
          (lambda * _: _)(
            *map(
               (lambda X:f'x{X}'),
               range(
                 len(
                   exprs)))),
          ('and ').join(
            (lambda * _: _)(
              ('x0 '),
              *map(
                 (lambda X:f'x{X}()'),
                 range(
                   (1),
                   len(
                     exprs)))))),
        (lambda _QzJXZWCGIRz_G:(_QzJXZWCGIRz_G[0]))(
          exprs),
        *map(
           (lambda X:
             (lambda * _: _)(
               'lambda',
               ':',
               X)),
           (lambda _QzJXZWCGIRz_G:(_QzJXZWCGIRz_G[1:]))(
             exprs))))))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ("``&&`` 'and'. Shortcutting logical AND.\n"
     '  Returns the first false value, otherwise the last value.\n'
     '  There is an implicit initial value of ``True``.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> (&& True True False) ; and finds the False\n'
     '     >>> # QzET_QzET_\n'
     '     ... (lambda x0,x1,x2:x0 and x1()and x2())(\n'
     '     ...   True,\n'
     '     ...   (lambda :True),\n'
     '     ...   (lambda :False))\n'
     '     False\n'
     '\n'
     "     #> (&& False (print 'oops)) ; Shortcutting.\n"
     '     >>> # QzET_QzET_\n'
     '     ... (lambda x0,x1:x0 and x1())(\n'
     '     ...   False,\n'
     '     ...   (lambda :\n'
     '     ...     print(\n'
     "     ...       'oops')))\n"
     '     False\n'
     '\n'
     '     #> (&& True 42)\n'
     '     >>> # QzET_QzET_\n'
     '     ... (lambda x0,x1:x0 and x1())(\n'
     '     ...   True,\n'
     '     ...   (lambda :(42)))\n'
     '     42\n'
     '\n'
     '     #> (&&)\n'
     '     >>> # QzET_QzET_\n'
     '     ... True\n'
     '     True\n'
     '\n'
     '     #> (&& 42)\n'
     '     >>> # QzET_QzET_\n'
     '     ... (42)\n'
     '     42\n'
     '\n'
     '  See also: `||<QzVERT_QzVERT_>`, `and`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'QzET_QzET_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'QzET_QzET_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda *exprs:(
  ("``||`` 'or'. Shortcutting logical OR.\n"
   '  Returns the first true value, otherwise the last value.\n'
   '  There is an implicit initial value of ``()``.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   "     #> (|| True (print 'oops)) ; Shortcutting.\n"
   '     >>> # QzVERT_QzVERT_\n'
   '     ... (lambda x0,x1:x0 or x1())(\n'
   '     ...   True,\n'
   '     ...   (lambda :\n'
   '     ...     print(\n'
   "     ...       'oops')))\n"
   '     True\n'
   '\n'
   '     #> (|| 42 False)\n'
   '     >>> # QzVERT_QzVERT_\n'
   '     ... (lambda x0,x1:x0 or x1())(\n'
   '     ...   (42),\n'
   '     ...   (lambda :False))\n'
   '     42\n'
   '\n'
   '     #> (|| () False 0 1)  ; or seeks the truth\n'
   '     >>> # QzVERT_QzVERT_\n'
   '     ... (lambda x0,x1,x2,x3:x0 or x1()or x2()or x3())(\n'
   '     ...   (),\n'
   '     ...   (lambda :False),\n'
   '     ...   (lambda :(0)),\n'
   '     ...   (lambda :(1)))\n'
   '     1\n'
   '\n'
   '     #> (|| False)\n'
   '     >>> # QzVERT_QzVERT_\n'
   '     ... False\n'
   '     False\n'
   '\n'
   '     #> (||)\n'
   '     >>> # QzVERT_QzVERT_\n'
   '     ... ()\n'
   '     ()\n'
   '\n'
   '  See also: `&&<QzET_QzET_>`, `bool`, `or`.\n'
   '  '),
  # cond
  (lambda x0,x1,x2,x3:x1()if x0 else x3()if x2()else())(
    __import__('operator').eq(
      len(
        exprs),
      (1)),
    (lambda :
      __import__('operator').itemgetter(
        (0))(
        exprs)),
    (lambda :exprs),
    (lambda :
      (lambda * _: _)(
        (lambda * _: _)(
          'lambda',
          (lambda * _: _)(
            *map(
               (lambda X:f'x{X}'),
               range(
                 len(
                   exprs)))),
          ('or ').join(
            (lambda * _: _)(
              ('x0 '),
              *map(
                 (lambda X:f'x{X}()'),
                 range(
                   (1),
                   len(
                     exprs)))))),
        (lambda _QzJXZWCGIRz_G:(_QzJXZWCGIRz_G[0]))(
          exprs),
        *map(
           (lambda X:
             (lambda * _: _)(
               'lambda',
               ':',
               X)),
           (lambda _QzJXZWCGIRz_G:(_QzJXZWCGIRz_G[1:]))(
             exprs))))))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ("``||`` 'or'. Shortcutting logical OR.\n"
     '  Returns the first true value, otherwise the last value.\n'
     '  There is an implicit initial value of ``()``.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     "     #> (|| True (print 'oops)) ; Shortcutting.\n"
     '     >>> # QzVERT_QzVERT_\n'
     '     ... (lambda x0,x1:x0 or x1())(\n'
     '     ...   True,\n'
     '     ...   (lambda :\n'
     '     ...     print(\n'
     "     ...       'oops')))\n"
     '     True\n'
     '\n'
     '     #> (|| 42 False)\n'
     '     >>> # QzVERT_QzVERT_\n'
     '     ... (lambda x0,x1:x0 or x1())(\n'
     '     ...   (42),\n'
     '     ...   (lambda :False))\n'
     '     42\n'
     '\n'
     '     #> (|| () False 0 1)  ; or seeks the truth\n'
     '     >>> # QzVERT_QzVERT_\n'
     '     ... (lambda x0,x1,x2,x3:x0 or x1()or x2()or x3())(\n'
     '     ...   (),\n'
     '     ...   (lambda :False),\n'
     '     ...   (lambda :(0)),\n'
     '     ...   (lambda :(1)))\n'
     '     1\n'
     '\n'
     '     #> (|| False)\n'
     '     >>> # QzVERT_QzVERT_\n'
     '     ... False\n'
     '     False\n'
     '\n'
     '     #> (||)\n'
     '     >>> # QzVERT_QzVERT_\n'
     '     ... ()\n'
     '     ()\n'
     '\n'
     '  See also: `&&<QzET_QzET_>`, `bool`, `or`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'QzVERT_QzVERT_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'QzVERT_QzVERT_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda *exception:(
  ("``throw*`` 'throw star' Creates a closed generator and calls .throw.\n"
   '\n'
   '  Despite PEP 3109, .throw still seems to accept multiple arguments.\n'
   '  Avoid using this form except when implementing throw method overrides.\n'
   '  Prefer `throw` instead.\n'
   '  '),
  (lambda * _: _)(
    "(lambda g:g.close()or g.throw)(c for c in'')",
    *exception))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ("``throw*`` 'throw star' Creates a closed generator and calls .throw.\n"
     '\n'
     '  Despite PEP 3109, .throw still seems to accept multiple arguments.\n'
     '  Avoid using this form except when implementing throw method overrides.\n'
     '  Prefer `throw` instead.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'throwQzSTAR_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'throwQzSTAR_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda exception:(
  ('Raise an exception.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> (throw Exception)                   ;Raise exception objects or '
   'classes.\n'
   '     >>> # throw\n'
   '     ... # hissp.macros.._macro_.throwQzSTAR_\n'
   "     ... (lambda g:g.close()or g.throw)(c for c in'')(\n"
   '     ...   Exception)\n'
   '     Traceback (most recent call last):\n'
   '       ...\n'
   '     Exception\n'
   '\n'
   "     #> (throw (TypeError 'message))\n"
   '     >>> # throw\n'
   '     ... # hissp.macros.._macro_.throwQzSTAR_\n'
   "     ... (lambda g:g.close()or g.throw)(c for c in'')(\n"
   '     ...   TypeError(\n'
   "     ...     'message'))\n"
   '     Traceback (most recent call last):\n'
   '       ...\n'
   '     TypeError: message\n'
   '\n'
   '  See also: `throw-from<throwQz_from>`, `engarde`_, `raise`.\n'
   '  '),
  (lambda * _: _)(
    'hissp.macros.._macro_.throwQzSTAR_',
    exception))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('Raise an exception.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> (throw Exception)                   ;Raise exception objects or '
     'classes.\n'
     '     >>> # throw\n'
     '     ... # hissp.macros.._macro_.throwQzSTAR_\n'
     "     ... (lambda g:g.close()or g.throw)(c for c in'')(\n"
     '     ...   Exception)\n'
     '     Traceback (most recent call last):\n'
     '       ...\n'
     '     Exception\n'
     '\n'
     "     #> (throw (TypeError 'message))\n"
     '     >>> # throw\n'
     '     ... # hissp.macros.._macro_.throwQzSTAR_\n'
     "     ... (lambda g:g.close()or g.throw)(c for c in'')(\n"
     '     ...   TypeError(\n'
     "     ...     'message'))\n"
     '     Traceback (most recent call last):\n'
     '       ...\n'
     '     TypeError: message\n'
     '\n'
     '  See also: `throw-from<throwQz_from>`, `engarde`_, `raise`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'throw',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'throw',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda exception,cause:(
  ('``throw-from`` Raise an exception with a cause, which can be None.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   "     #> (throw-from Exception (Exception 'message)) ;Explicit chaining.\n"
   '     #..\n'
   '     >>> # throwQz_from\n'
   '     ... # hissp.macros.._macro_.throwQzSTAR_\n'
   "     ... (lambda g:g.close()or g.throw)(c for c in'')(\n"
   '     ...   # hissp.macros.._macro_.let\n'
   '     ...   (lambda _Qz2IKKUCBWz_G=(lambda _Qz2IKKUCBWz_x:\n'
   '     ...     # hissp.macros.._macro_.ifQz_else\n'
   '     ...     (lambda b,c,a:c()if b else a())(\n'
   '     ...       # hissp.macros.._macro_.QzET_QzET_\n'
   '     ...       (lambda x0,x1:x0 and x1())(\n'
   "     ...         __import__('builtins').isinstance(\n"
   '     ...           _Qz2IKKUCBWz_x,\n'
   "     ...           __import__('builtins').type),\n"
   '     ...         (lambda :\n'
   "     ...           __import__('builtins').issubclass(\n"
   '     ...             _Qz2IKKUCBWz_x,\n'
   "     ...             __import__('builtins').BaseException))),\n"
   '     ...       (lambda :_Qz2IKKUCBWz_x()),\n'
   '     ...       (lambda :_Qz2IKKUCBWz_x))):\n'
   '     ...     # hissp.macros.._macro_.attach\n'
   '     ...     # hissp.macros.._macro_.let\n'
   '     ...     (lambda _QzWG5WN73Wz_target=_Qz2IKKUCBWz_G(\n'
   '     ...       Exception):(\n'
   "     ...       __import__('builtins').setattr(\n"
   '     ...         _QzWG5WN73Wz_target,\n'
   "     ...         '__cause__',\n"
   '     ...         _Qz2IKKUCBWz_G(\n'
   '     ...           Exception(\n'
   "     ...             'message'))),\n"
   '     ...       _QzWG5WN73Wz_target)[-1])())())\n'
   '     Traceback (most recent call last):\n'
   '       ...\n'
   '     Exception\n'
   '\n'
   '  See also: `throw`, `throw*<throwQzSTAR_>`.\n'
   '  '),
  (lambda * _: _)(
    'hissp.macros.._macro_.throwQzSTAR_',
    (lambda * _: _)(
      'hissp.macros.._macro_.let',
      (lambda * _: _)(
        '_Qz4ESVE2P2z_G',
        (lambda * _: _)(
          'lambda',
          (lambda * _: _)(
            '_Qz4ESVE2P2z_x'),
          (lambda * _: _)(
            'hissp.macros.._macro_.ifQz_else',
            (lambda * _: _)(
              'hissp.macros.._macro_.QzET_QzET_',
              (lambda * _: _)(
                'builtins..isinstance',
                '_Qz4ESVE2P2z_x',
                'builtins..type'),
              (lambda * _: _)(
                'builtins..issubclass',
                '_Qz4ESVE2P2z_x',
                'builtins..BaseException')),
            (lambda * _: _)(
              '_Qz4ESVE2P2z_x'),
            '_Qz4ESVE2P2z_x'))),
      (lambda * _: _)(
        'hissp.macros.._macro_.attach',
        (lambda * _: _)(
          '_Qz4ESVE2P2z_G',
          exception),
        ':',
        '__cause__',
        (lambda * _: _)(
          '_Qz4ESVE2P2z_G',
          cause)))))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('``throw-from`` Raise an exception with a cause, which can be None.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     "     #> (throw-from Exception (Exception 'message)) ;Explicit chaining.\n"
     '     #..\n'
     '     >>> # throwQz_from\n'
     '     ... # hissp.macros.._macro_.throwQzSTAR_\n'
     "     ... (lambda g:g.close()or g.throw)(c for c in'')(\n"
     '     ...   # hissp.macros.._macro_.let\n'
     '     ...   (lambda _Qz2IKKUCBWz_G=(lambda _Qz2IKKUCBWz_x:\n'
     '     ...     # hissp.macros.._macro_.ifQz_else\n'
     '     ...     (lambda b,c,a:c()if b else a())(\n'
     '     ...       # hissp.macros.._macro_.QzET_QzET_\n'
     '     ...       (lambda x0,x1:x0 and x1())(\n'
     "     ...         __import__('builtins').isinstance(\n"
     '     ...           _Qz2IKKUCBWz_x,\n'
     "     ...           __import__('builtins').type),\n"
     '     ...         (lambda :\n'
     "     ...           __import__('builtins').issubclass(\n"
     '     ...             _Qz2IKKUCBWz_x,\n'
     "     ...             __import__('builtins').BaseException))),\n"
     '     ...       (lambda :_Qz2IKKUCBWz_x()),\n'
     '     ...       (lambda :_Qz2IKKUCBWz_x))):\n'
     '     ...     # hissp.macros.._macro_.attach\n'
     '     ...     # hissp.macros.._macro_.let\n'
     '     ...     (lambda _QzWG5WN73Wz_target=_Qz2IKKUCBWz_G(\n'
     '     ...       Exception):(\n'
     "     ...       __import__('builtins').setattr(\n"
     '     ...         _QzWG5WN73Wz_target,\n'
     "     ...         '__cause__',\n"
     '     ...         _Qz2IKKUCBWz_G(\n'
     '     ...           Exception(\n'
     "     ...             'message'))),\n"
     '     ...       _QzWG5WN73Wz_target)[-1])())())\n'
     '     Traceback (most recent call last):\n'
     '       ...\n'
     '     Exception\n'
     '\n'
     '  See also: `throw`, `throw*<throwQzSTAR_>`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'throwQz_from',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'throwQz_from',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda expr1,*body:(
  ('Evaluates each expression in sequence (for side effects),\n'
   '  resulting in the value of the first.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> (print (prog1 0                     ;Sequence for side effects, eval '
   'to first.\n'
   '     #..         (print 1)\n'
   '     #..         (print 2)))\n'
   '     >>> print(\n'
   '     ...   # prog1\n'
   '     ...   # hissp.macros.._macro_.let\n'
   '     ...   (lambda _Qz46BJ7IW6z_value1=(0):(\n'
   '     ...     print(\n'
   '     ...       (1)),\n'
   '     ...     print(\n'
   '     ...       (2)),\n'
   '     ...     _Qz46BJ7IW6z_value1)[-1])())\n'
   '     1\n'
   '     2\n'
   '     0\n'
   '\n'
   '  Combine with `progn` for a value in the middle of the sequence.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> (prog1                              ;Sequence for side effects, eval '
   'to first.\n'
   '     #..  (progn (print 1)                  ;Sequence for side effects, eval '
   'to last.\n'
   '     #..         3)\n'
   '     #..  (print 2))\n'
   '     >>> # prog1\n'
   '     ... # hissp.macros.._macro_.let\n'
   '     ... (lambda _Qz46BJ7IW6z_value1=# progn\n'
   '     ... (lambda :(\n'
   '     ...   print(\n'
   '     ...     (1)),\n'
   '     ...   (3))[-1])():(\n'
   '     ...   print(\n'
   '     ...     (2)),\n'
   '     ...   _Qz46BJ7IW6z_value1)[-1])()\n'
   '     1\n'
   '     2\n'
   '     3\n'
   '\n'
   '  See also: `doto`.\n'
   '  '),
  (lambda * _: _)(
    'hissp.macros.._macro_.let',
    (lambda * _: _)(
      '_QzVPVO77CDz_value1',
      expr1),
    *body,
    '_QzVPVO77CDz_value1'))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('Evaluates each expression in sequence (for side effects),\n'
     '  resulting in the value of the first.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> (print (prog1 0                     ;Sequence for side effects, eval '
     'to first.\n'
     '     #..         (print 1)\n'
     '     #..         (print 2)))\n'
     '     >>> print(\n'
     '     ...   # prog1\n'
     '     ...   # hissp.macros.._macro_.let\n'
     '     ...   (lambda _Qz46BJ7IW6z_value1=(0):(\n'
     '     ...     print(\n'
     '     ...       (1)),\n'
     '     ...     print(\n'
     '     ...       (2)),\n'
     '     ...     _Qz46BJ7IW6z_value1)[-1])())\n'
     '     1\n'
     '     2\n'
     '     0\n'
     '\n'
     '  Combine with `progn` for a value in the middle of the sequence.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> (prog1                              ;Sequence for side effects, eval '
     'to first.\n'
     '     #..  (progn (print 1)                  ;Sequence for side effects, eval '
     'to last.\n'
     '     #..         3)\n'
     '     #..  (print 2))\n'
     '     >>> # prog1\n'
     '     ... # hissp.macros.._macro_.let\n'
     '     ... (lambda _Qz46BJ7IW6z_value1=# progn\n'
     '     ... (lambda :(\n'
     '     ...   print(\n'
     '     ...     (1)),\n'
     '     ...   (3))[-1])():(\n'
     '     ...   print(\n'
     '     ...     (2)),\n'
     '     ...   _Qz46BJ7IW6z_value1)[-1])()\n'
     '     1\n'
     '     2\n'
     '     3\n'
     '\n'
     '  See also: `doto`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'prog1',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'prog1',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda raw:(
  ('``b#`` `bytes` literal reader macro\n'
   '\n'
   '.. code-block:: REPL\n'
   '\n'
   '   #> b#"bytes\n'
   '   #..with\\nnewlines"\n'
   "   >>> b'bytes\\nwith\\nnewlines'\n"
   "   b'bytes\\nwith\\nnewlines'\n"),
  # Qz_QzGT_
  __import__('ast').literal_eval(
    # Qz_QzLT_QzGT_QzGT_
    ("b'{}'").format(
      __import__('ast').literal_eval(
        raw).replace(
        ("'"),
        ("\\'")).replace(
        ('\n'),
        ('\\n')))))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('``b#`` `bytes` literal reader macro\n'
     '\n'
     '.. code-block:: REPL\n'
     '\n'
     '   #> b#"bytes\n'
     '   #..with\\nnewlines"\n'
     "   >>> b'bytes\\nwith\\nnewlines'\n"
     "   b'bytes\\nwith\\nnewlines'\n")),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'bQzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'bQzHASH_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda f:(
  ('``en#`` reader macro.\n'
   'Wrap a function applicable to a tuple as a function of its elements.\n'
   '\n'
   '.. code-block:: REPL\n'
   '\n'
   '   #> (en#list 1 2 3)\n'
   '   >>> (lambda *_Qz6RFWTTVXz_xs:\n'
   '   ...   list(\n'
   '   ...     _Qz6RFWTTVXz_xs))(\n'
   '   ...   (1),\n'
   '   ...   (2),\n'
   '   ...   (3))\n'
   '   [1, 2, 3]\n'
   '\n'
   '   #> (en#.extend _ 4 5 6) ; Methods too.\n'
   '   #..\n'
   '   >>> (lambda _Qz4LWLAFU3z_self,*_Qz4LWLAFU3z_xs:\n'
   '   ...   _Qz4LWLAFU3z_self.extend(\n'
   '   ...     _Qz4LWLAFU3z_xs))(\n'
   '   ...   _,\n'
   '   ...   (4),\n'
   '   ...   (5),\n'
   '   ...   (6))\n'
   '\n'
   '   #> _\n'
   '   >>> _\n'
   '   [1, 2, 3, 4, 5, 6]\n'
   '\n'
   '   #> (define enjoin en#X#(.join "" (map str X)))\n'
   '   >>> # define\n'
   "   ... __import__('builtins').globals().update(\n"
   '   ...   enjoin=(lambda *_Qz6RFWTTVXz_xs:\n'
   '   ...            (lambda X:\n'
   "   ...              ('').join(\n"
   '   ...                map(\n'
   '   ...                  str,\n'
   '   ...                  X)))(\n'
   '   ...              _Qz6RFWTTVXz_xs)))\n'
   '\n'
   '   #> (enjoin "Sum: "(op#add 2 3)". Product: "(op#mul 2 3)".")\n'
   '   >>> enjoin(\n'
   "   ...   ('Sum: '),\n"
   "   ...   __import__('operator').add(\n"
   '   ...     (2),\n'
   '   ...     (3)),\n'
   "   ...   ('. Product: '),\n"
   "   ...   __import__('operator').mul(\n"
   '   ...     (2),\n'
   '   ...     (3)),\n'
   "   ...   ('.'))\n"
   "   'Sum: 5. Product: 6.'\n"
   '\n'
   'There are no bundled reader macros for a quinary, senary, etc. but\n'
   'the en#X# variadic or a normal lambda form can be used instead.\n'
   '\n'
   'See also: `X# <XQzHASH_>`.\n'),
  # ifQz_else
  (lambda b,c,a:c()if b else a())(
    # QzET_QzET_
    (lambda x0,x1:x0 and x1())(
      __import__('operator').is_(
        str,
        type(
          f)),
      (lambda :
        f.startswith(
          ('.')))),
    (lambda :
      (lambda * _: _)(
        'lambda',
        (lambda * _: _)(
          '_QzVSCV7QGLz_self',
          ':',
          ':*',
          '_QzVSCV7QGLz_xs'),
        (lambda * _: _)(
          f,
          '_QzVSCV7QGLz_self',
          '_QzVSCV7QGLz_xs'))),
    (lambda :
      (lambda * _: _)(
        'lambda',
        (lambda * _: _)(
          ':',
          ':*',
          '_QzGWAZDPD6z_xs'),
        (lambda * _: _)(
          f,
          '_QzGWAZDPD6z_xs')))))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('``en#`` reader macro.\n'
     'Wrap a function applicable to a tuple as a function of its elements.\n'
     '\n'
     '.. code-block:: REPL\n'
     '\n'
     '   #> (en#list 1 2 3)\n'
     '   >>> (lambda *_Qz6RFWTTVXz_xs:\n'
     '   ...   list(\n'
     '   ...     _Qz6RFWTTVXz_xs))(\n'
     '   ...   (1),\n'
     '   ...   (2),\n'
     '   ...   (3))\n'
     '   [1, 2, 3]\n'
     '\n'
     '   #> (en#.extend _ 4 5 6) ; Methods too.\n'
     '   #..\n'
     '   >>> (lambda _Qz4LWLAFU3z_self,*_Qz4LWLAFU3z_xs:\n'
     '   ...   _Qz4LWLAFU3z_self.extend(\n'
     '   ...     _Qz4LWLAFU3z_xs))(\n'
     '   ...   _,\n'
     '   ...   (4),\n'
     '   ...   (5),\n'
     '   ...   (6))\n'
     '\n'
     '   #> _\n'
     '   >>> _\n'
     '   [1, 2, 3, 4, 5, 6]\n'
     '\n'
     '   #> (define enjoin en#X#(.join "" (map str X)))\n'
     '   >>> # define\n'
     "   ... __import__('builtins').globals().update(\n"
     '   ...   enjoin=(lambda *_Qz6RFWTTVXz_xs:\n'
     '   ...            (lambda X:\n'
     "   ...              ('').join(\n"
     '   ...                map(\n'
     '   ...                  str,\n'
     '   ...                  X)))(\n'
     '   ...              _Qz6RFWTTVXz_xs)))\n'
     '\n'
     '   #> (enjoin "Sum: "(op#add 2 3)". Product: "(op#mul 2 3)".")\n'
     '   >>> enjoin(\n'
     "   ...   ('Sum: '),\n"
     "   ...   __import__('operator').add(\n"
     '   ...     (2),\n'
     '   ...     (3)),\n'
     "   ...   ('. Product: '),\n"
     "   ...   __import__('operator').mul(\n"
     '   ...     (2),\n'
     '   ...     (3)),\n'
     "   ...   ('.'))\n"
     "   'Sum: 5. Product: 6.'\n"
     '\n'
     'There are no bundled reader macros for a quinary, senary, etc. but\n'
     'the en#X# variadic or a normal lambda form can be used instead.\n'
     '\n'
     'See also: `X# <XQzHASH_>`.\n')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'enQzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'enQzHASH_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda *xs:(
  ("``@`` 'list of' Mnemonic: @rray list.\n"
   '\n'
   "Creates the `list` from each expresssion's result.\n"
   'A ``:*`` unpacks the next argument.\n'
   '\n'
   '.. code-block:: REPL\n'
   '\n'
   '   #> (@ :* "AB" (math..sqrt 9) :* "XY" 2 1)\n'
   '   >>> # QzAT_\n'
   '   ... (lambda *xs:[*xs])(\n'
   "   ...   *('AB'),\n"
   "   ...   __import__('math').sqrt(\n"
   '   ...     (9)),\n'
   "   ...   *('XY'),\n"
   '   ...   (2),\n'
   '   ...   (1))\n'
   "   ['A', 'B', 3.0, 'X', 'Y', 2, 1]\n"
   '\n'
   'See also: `#<QzHASH_>`, `%<QzPCENT_>`.\n'),
  # when
  (lambda b,c:c()if b else())(
    # QzET_QzET_
    (lambda x0,x1:x0 and x1())(
      xs,
      (lambda :
        __import__('operator').eq(
          ':*',
          __import__('operator').itemgetter(
            (-1))(
            xs)))),
    (lambda :
      # throw
      # hissp.macros.._macro_.throwQzSTAR_
      (lambda g:g.close()or g.throw)(c for c in'')(
        SyntaxError(
          ('trailing :*'))))),
  # let
  (lambda ixs=iter(
    xs):
    (lambda * _: _)(
      (lambda * _: _)(
        'lambda',
        (lambda * _: _)(
          ':',
          ':*',
          'xs'),
        '[*xs]'),
      ':',
      *__import__('itertools').chain.from_iterable(
         map(
           (lambda X:
             # ifQz_else
             (lambda b,c,a:c()if b else a())(
               __import__('operator').eq(
                 X,
                 (':*')),
               (lambda :
                 (lambda * _: _)(
                   X,
                   next(
                     ixs))),
               (lambda :
                 (lambda * _: _)(
                   ':?',
                   X)))),
           ixs))))())[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ("``@`` 'list of' Mnemonic: @rray list.\n"
     '\n'
     "Creates the `list` from each expresssion's result.\n"
     'A ``:*`` unpacks the next argument.\n'
     '\n'
     '.. code-block:: REPL\n'
     '\n'
     '   #> (@ :* "AB" (math..sqrt 9) :* "XY" 2 1)\n'
     '   >>> # QzAT_\n'
     '   ... (lambda *xs:[*xs])(\n'
     "   ...   *('AB'),\n"
     "   ...   __import__('math').sqrt(\n"
     '   ...     (9)),\n'
     "   ...   *('XY'),\n"
     '   ...   (2),\n'
     '   ...   (1))\n'
     "   ['A', 'B', 3.0, 'X', 'Y', 2, 1]\n"
     '\n'
     'See also: `#<QzHASH_>`, `%<QzPCENT_>`.\n')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'QzAT_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'QzAT_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda *xs:(
  ("``#`` 'set of' Mnemonic: Hash (#) set.\n"
   '\n'
   "  Creates the `set` from each expression's result.\n"
   '  A ``:*`` unpacks the next argument.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> (# 1 :* (@ 1 2 3) 4)                ;Set, with unpacking.\n'
   '     >>> # QzHASH_\n'
   '     ... (lambda *xs:{*xs})(\n'
   '     ...   (1),\n'
   '     ...   *# QzAT_\n'
   '     ...    (lambda *xs:[*xs])(\n'
   '     ...      (1),\n'
   '     ...      (2),\n'
   '     ...      (3)),\n'
   '     ...   (4))\n'
   '     {1, 2, 3, 4}\n'
   '\n'
   '  See also: `@<QzAT_>`, `%<QzPCENT_>`.\n'
   '  '),
  # when
  (lambda b,c:c()if b else())(
    # QzET_QzET_
    (lambda x0,x1:x0 and x1())(
      xs,
      (lambda :
        __import__('operator').eq(
          ':*',
          __import__('operator').itemgetter(
            (-1))(
            xs)))),
    (lambda :
      # throw
      # hissp.macros.._macro_.throwQzSTAR_
      (lambda g:g.close()or g.throw)(c for c in'')(
        SyntaxError(
          ('trailing :*'))))),
  # let
  (lambda ixs=iter(
    xs):
    (lambda * _: _)(
      (lambda * _: _)(
        'lambda',
        (lambda * _: _)(
          ':',
          ':*',
          'xs'),
        '{*xs}'),
      ':',
      *__import__('itertools').chain.from_iterable(
         map(
           (lambda X:
             # ifQz_else
             (lambda b,c,a:c()if b else a())(
               __import__('operator').eq(
                 X,
                 (':*')),
               (lambda :
                 (lambda * _: _)(
                   X,
                   next(
                     ixs))),
               (lambda :
                 (lambda * _: _)(
                   ':?',
                   X)))),
           ixs))))())[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ("``#`` 'set of' Mnemonic: Hash (#) set.\n"
     '\n'
     "  Creates the `set` from each expression's result.\n"
     '  A ``:*`` unpacks the next argument.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> (# 1 :* (@ 1 2 3) 4)                ;Set, with unpacking.\n'
     '     >>> # QzHASH_\n'
     '     ... (lambda *xs:{*xs})(\n'
     '     ...   (1),\n'
     '     ...   *# QzAT_\n'
     '     ...    (lambda *xs:[*xs])(\n'
     '     ...      (1),\n'
     '     ...      (2),\n'
     '     ...      (3)),\n'
     '     ...   (4))\n'
     '     {1, 2, 3, 4}\n'
     '\n'
     '  See also: `@<QzAT_>`, `%<QzPCENT_>`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'QzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'QzHASH_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda *kvs:(
  ("``%`` 'dict of'. Mnemonic: `dict` of pairs (%).\n"
   '\n'
   '  Key-value pairs are implied by position.\n'
   '  A ``:**`` mapping-unpacks the next argument.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> (% 1 2  :** (dict : x 3  y 4)  5 6) ;Dict, with mapping unpacking.\n'
   '     >>> # QzPCENT_\n'
   '     ... (lambda x0,x1,x3,x4,x5:{x0:x1,**x3,x4:x5})(\n'
   '     ...   (1),\n'
   '     ...   (2),\n'
   '     ...   dict(\n'
   '     ...     x=(3),\n'
   '     ...     y=(4)),\n'
   '     ...   (5),\n'
   '     ...   (6))\n'
   "     {1: 2, 'x': 3, 'y': 4, 5: 6}\n"
   '\n'
   '     #> (%)\n'
   '     >>> # QzPCENT_\n'
   '     ... {}\n'
   '     {}\n'
   '\n'
   '  See also: `@<QzAT_>`, `#<QzHASH_>`.\n'
   '  '),
  # cond
  (lambda x0,x1,x2,x3,x4,x5:x1()if x0 else x3()if x2()else x5()if x4()else())(
    __import__('operator').mod(
      len(
        kvs),
      (2)),
    (lambda :
      # throw
      # hissp.macros.._macro_.throwQzSTAR_
      (lambda g:g.close()or g.throw)(c for c in'')(
        TypeError(
          ('extra key without value')))),
    (lambda :kvs),
    (lambda :
      (lambda * _: _)(
        (lambda * _: _)(
          'lambda',
          (lambda * _: _)(
            *__import__('itertools').starmap(
               (lambda X,Y:f'x{X}'),
               filter(
                 (lambda X:
                   __import__('operator').ne(
                     ':**',
                     __import__('operator').itemgetter(
                       (1))(
                       X))),
                 enumerate(
                   kvs)))),
          ('{{{}}}').format(
            (',').join(
              __import__('itertools').starmap(
                (lambda X,Y:
                  # ifQz_else
                  (lambda b,c,a:c()if b else a())(
                    __import__('operator').eq(
                      Y,
                      ':**'),
                    (lambda :f'**x{X+1}'),
                    (lambda :f'x{X}:x{X+1}'))),
                # Qz_QzGT_
                __import__('itertools').islice(
                  enumerate(
                    kvs),
                  (0),
                  None,
                  (2)))))),
        *filter(
           (lambda X:
             __import__('operator').ne(
               X,
               ':**')),
           kvs))),
    (lambda :':else'),
    (lambda :dict())))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ("``%`` 'dict of'. Mnemonic: `dict` of pairs (%).\n"
     '\n'
     '  Key-value pairs are implied by position.\n'
     '  A ``:**`` mapping-unpacks the next argument.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> (% 1 2  :** (dict : x 3  y 4)  5 6) ;Dict, with mapping unpacking.\n'
     '     >>> # QzPCENT_\n'
     '     ... (lambda x0,x1,x3,x4,x5:{x0:x1,**x3,x4:x5})(\n'
     '     ...   (1),\n'
     '     ...   (2),\n'
     '     ...   dict(\n'
     '     ...     x=(3),\n'
     '     ...     y=(4)),\n'
     '     ...   (5),\n'
     '     ...   (6))\n'
     "     {1: 2, 'x': 3, 'y': 4, 5: 6}\n"
     '\n'
     '     #> (%)\n'
     '     >>> # QzPCENT_\n'
     '     ... {}\n'
     '     {}\n'
     '\n'
     '  See also: `@<QzAT_>`, `#<QzHASH_>`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'QzPCENT_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'QzPCENT_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda ns=(lambda * _: _)(
  'builtins..globals'):(
  ("Hissp's bundled micro prelude.\n"
   '\n'
   'Brings Hissp up to a minimal standard of usability without adding any\n'
   'dependencies in the compiled output.\n'
   '\n'
   "Mainly intended for single-file scripts that can't have dependencies,\n"
   'or similarly constrained environments (e.g. embedded, readerless).\n'
   'There, the first form should be ``(hissp.._macro_.prelude)``,\n'
   'which is also implied in ``$ lissp -c`` commands.\n'
   '\n'
   'Larger projects with access to functional and macro libraries need not\n'
   'use this prelude at all.\n'
   '\n'
   'The prelude has several effects:\n'
   '\n'
   '* Imports `functools.partial` and `functools.reduce`.\n'
   '  Star imports from `itertools` and `operator`::\n'
   '\n'
   '   from functools import partial,reduce\n'
   '   from itertools import *;from operator import *\n'
   '\n'
   '.. _engarde:\n'
   '\n'
   '* Defines ``engarde``, which calls a function with exception handler::\n'
   '\n'
   '   def engarde(xs,h,f,/,*a,**kw):\n'
   '    try:return f(*a,**kw)\n'
   '    except xs as e:return h(e)\n'
   '\n'
   '  ``engarde`` with handlers can stack above in a single form.\n'
   '\n'
   '  See `engarde examples`_ below.\n'
   '\n'
   '.. _enter:\n'
   '\n'
   '* Defines ``enter``, which calls a function with context manager::\n'
   '\n'
   '   def enter(c,f,/,*a):\n'
   '    with c as C:return f(*a,C)\n'
   '\n'
   '  ``enter`` with context managers can stack above in a single form.\n'
   '\n'
   '  See `enter examples`_ below.\n'
   '\n'
   '.. _Ensue:\n'
   '\n'
   '* Defines the ``Ensue`` class; trampolined continuation generators::\n'
   '\n'
   "   class Ensue(__import__('collections.abc').abc.Generator):\n"
   '    send=lambda s,v:s.g.send(v);throw=lambda '
   's,*x:s.g.throw(*x);F=0;X=();Y=[]\n'
   '    def __init__(s,p):s.p,s.g,s.n=p,s._(s),s.Y\n'
   '    def _(s,k,v=None):\n'
   "     while isinstance(s:=k,__class__) and not setattr(s,'sent',v):\n"
   '      try:k,y=s.p(s),s.Y;v=(yield from y)if s.F or y is s.n else(yield y)\n'
   '      except s.X as e:v=e\n'
   '     return k\n'
   '\n'
   '  ``Ensue`` takes a step function and returns a generator. The step\n'
   '  function recieves the previous Ensue step and must return the next\n'
   '  one to continue. Returning a different type raises a `StopIteration`\n'
   '  with that object. Set the ``Y`` attribute on the current step to\n'
   '  [Y]ield a value this step. Set the ``F`` attribute to a true value\n'
   '  to yield values [F]rom the ``Y`` iterable instead. Set the ``X``\n'
   '  attribute to an e[X]ception class or tuple to catch any targeted\n'
   '  exceptions on the next step. Each step keeps a ``sent`` attribute,\n'
   '  which is the value sent to the generator this step, or the exception\n'
   '  caught this step instead.\n'
   '\n'
   '  See `Ensue examples`_ and `enter examples`_ below.\n'
   '\n'
   '  See also:\n'
   '  `types.coroutine`, `collections.abc.Generator`, `loop-from<loopQz_from>`.\n'
   '\n'
   '* Adds the bundled macros, but only if available\n'
   '  (macros are typically only used at compile time),\n'
   '  so its compiled expansion does not require Hissp to be installed.\n'
   '  (This replaces ``_macro_`` if you already had one.)::\n'
   '\n'
   "   _macro_=__import__('types').SimpleNamespace()\n"
   "   try:exec('from {}._macro_ import *',vars(_macro_))\n"
   '   except ModuleNotFoundError:pass\n'
   '\n'
   'Prelude Usage\n'
   '=============\n'
   'The REPL has the bundled macros loaded by default, but not the prelude.\n'
   'Invoke ``(prelude)`` to get the rest.\n'
   '\n'
   '.. code-block:: REPL\n'
   '\n'
   '   #> (prelude)\n'
   '   >>> # prelude\n'
   "   ... __import__('builtins').exec(\n"
   "   ...   ('from functools import partial,reduce\\n'\n"
   "   ...    'from itertools import *;from operator import *\\n'\n"
   "   ...    'def engarde(xs,h,f,/,*a,**kw):\\n'\n"
   "   ...    ' try:return f(*a,**kw)\\n'\n"
   "   ...    ' except xs as e:return h(e)\\n'\n"
   "   ...    'def enter(c,f,/,*a):\\n'\n"
   "   ...    ' with c as C:return f(*a,C)\\n'\n"
   '   ...    "class Ensue(__import__(\'collections.abc\').abc.Generator):\\n"\n'
   "   ...    ' send=lambda s,v:s.g.send(v);throw=lambda "
   "s,*x:s.g.throw(*x);F=0;X=();Y=[]\\n'\n"
   "   ...    ' def __init__(s,p):s.p,s.g,s.n=p,s._(s),s.Y\\n'\n"
   "   ...    ' def _(s,k,v=None):\\n'\n"
   '   ...    "  while isinstance(s:=k,__class__) and not '
   'setattr(s,\'sent\',v):\\n"\n'
   "   ...    '   try:k,y=s.p(s),s.Y;v=(yield from y)if s.F or y is s.n "
   "else(yield y)\\n'\n"
   "   ...    '   except s.X as e:v=e\\n'\n"
   "   ...    '  return k\\n'\n"
   '   ...    "_macro_=__import__(\'types\').SimpleNamespace()\\n"\n'
   '   ...    "try:exec(\'from hissp.macros._macro_ import '
   '*\',vars(_macro_))\\n"\n'
   "   ...    'except ModuleNotFoundError:pass'),\n"
   "   ...   __import__('builtins').globals())\n"
   '\n'
   'See also, `alias`.\n'
   '\n'
   'engarde examples\n'
   '----------------\n'
   '.. code-block:: REPL\n'
   '\n'
   '   #> (engarde `(,FloatingPointError ,ZeroDivisionError) ;two targets\n'
   '   #..         (lambda e (print "Oops!") e)    ;handler (returns exception)\n'
   '   #..         truediv 6 0)                    ;calls it on your behalf\n'
   '   >>> engarde(\n'
   '   ...   (lambda * _: _)(\n'
   '   ...     FloatingPointError,\n'
   '   ...     ZeroDivisionError),\n'
   '   ...   (lambda e:(\n'
   '   ...     print(\n'
   "   ...       ('Oops!')),\n"
   '   ...     e)[-1]),\n'
   '   ...   truediv,\n'
   '   ...   (6),\n'
   '   ...   (0))\n'
   '   Oops!\n'
   "   ZeroDivisionError('division by zero')\n"
   '\n'
   '   #> (engarde ArithmeticError repr truediv 6 0) ;superclass target\n'
   '   >>> engarde(\n'
   '   ...   ArithmeticError,\n'
   '   ...   repr,\n'
   '   ...   truediv,\n'
   '   ...   (6),\n'
   '   ...   (0))\n'
   '   "ZeroDivisionError(\'division by zero\')"\n'
   '\n'
   '   #> (engarde ArithmeticError repr truediv 6 2) ;returned answer\n'
   '   >>> engarde(\n'
   '   ...   ArithmeticError,\n'
   '   ...   repr,\n'
   '   ...   truediv,\n'
   '   ...   (6),\n'
   '   ...   (2))\n'
   '   3.0\n'
   '\n'
   '   ;; You can stack them.\n'
   '   #> (engarde Exception                       ;The outer engarde\n'
   '   #.. print\n'
   '   #.. engarde ZeroDivisionError               ; calls the inner.\n'
   '   #.. (lambda e (print "It means what you want it to mean."))\n'
   '   #.. truediv "6" 0)                          ;Try variations.\n'
   '   >>> engarde(\n'
   '   ...   Exception,\n'
   '   ...   print,\n'
   '   ...   engarde,\n'
   '   ...   ZeroDivisionError,\n'
   '   ...   (lambda e:\n'
   '   ...     print(\n'
   "   ...       ('It means what you want it to mean.'))),\n"
   '   ...   truediv,\n'
   "   ...   ('6'),\n"
   '   ...   (0))\n'
   "   unsupported operand type(s) for /: 'str' and 'int'\n"
   '\n'
   '   #> (engarde Exception\n'
   '   #..         (lambda x x.__cause__)\n'
   '   #..         (lambda : (throw-from Exception (Exception "msg"))))\n'
   '   >>> engarde(\n'
   '   ...   Exception,\n'
   '   ...   (lambda x:x.__cause__),\n'
   '   ...   (lambda :\n'
   '   ...     # throwQz_from\n'
   '   ...     # hissp.macros.._macro_.throwQzSTAR_\n'
   "   ...     (lambda g:g.close()or g.throw)(c for c in'')(\n"
   '   ...       # hissp.macros.._macro_.let\n'
   '   ...       (lambda _Qz2IKKUCBWz_G=(lambda _Qz2IKKUCBWz_x:\n'
   '   ...         # hissp.macros.._macro_.ifQz_else\n'
   '   ...         (lambda b,c,a:c()if b else a())(\n'
   '   ...           # hissp.macros.._macro_.QzET_QzET_\n'
   '   ...           (lambda x0,x1:x0 and x1())(\n'
   "   ...             __import__('builtins').isinstance(\n"
   '   ...               _Qz2IKKUCBWz_x,\n'
   "   ...               __import__('builtins').type),\n"
   '   ...             (lambda :\n'
   "   ...               __import__('builtins').issubclass(\n"
   '   ...                 _Qz2IKKUCBWz_x,\n'
   "   ...                 __import__('builtins').BaseException))),\n"
   '   ...           (lambda :_Qz2IKKUCBWz_x()),\n'
   '   ...           (lambda :_Qz2IKKUCBWz_x))):\n'
   '   ...         # hissp.macros.._macro_.attach\n'
   '   ...         # hissp.macros.._macro_.let\n'
   '   ...         (lambda _QzWG5WN73Wz_target=_Qz2IKKUCBWz_G(\n'
   '   ...           Exception):(\n'
   "   ...           __import__('builtins').setattr(\n"
   '   ...             _QzWG5WN73Wz_target,\n'
   "   ...             '__cause__',\n"
   '   ...             _Qz2IKKUCBWz_G(\n'
   '   ...               Exception(\n'
   "   ...                 ('msg')))),\n"
   '   ...           _QzWG5WN73Wz_target)[-1])())())))\n'
   "   Exception('msg')\n"
   '\n'
   'Ensue examples\n'
   '--------------\n'
   '.. code-block:: REPL\n'
   '\n'
   '   #> (define fibonacci\n'
   '   #..  (lambda (: a 1  b 1)\n'
   '   #..    (Ensue (lambda (step)\n'
   '   #..             (set@ step.Y a)            ;Y for yield.\n'
   '   #..             (fibonacci b (add a b))))))\n'
   '   >>> # define\n'
   "   ... __import__('builtins').globals().update(\n"
   '   ...   fibonacci=(lambda a=(1),b=(1):\n'
   '   ...               Ensue(\n'
   '   ...                 (lambda step:(\n'
   '   ...                   # setQzAT_\n'
   '   ...                   # hissp.macros.._macro_.let\n'
   '   ...                   (lambda _QzRMG5GSSIz_val=a:(\n'
   "   ...                     __import__('builtins').setattr(\n"
   '   ...                       step,\n'
   "   ...                       'Y',\n"
   '   ...                       _QzRMG5GSSIz_val),\n'
   '   ...                     _QzRMG5GSSIz_val)[-1])(),\n'
   '   ...                   fibonacci(\n'
   '   ...                     b,\n'
   '   ...                     add(\n'
   '   ...                       a,\n'
   '   ...                       b)))[-1]))))\n'
   '\n'
   '   #> (list (islice (fibonacci) 7))\n'
   '   >>> list(\n'
   '   ...   islice(\n'
   '   ...     fibonacci(),\n'
   '   ...     (7)))\n'
   '   [1, 1, 2, 3, 5, 8, 13]\n'
   '\n'
   '   #> (define my-range ; Terminate by not returning an Ensue.\n'
   '   #..  (lambda in\n'
   '   #..    (Ensue (lambda (step)\n'
   '   #..             (when (lt i n)             ;Acts like a while loop.\n'
   '   #..               (set@ step.Y i)\n'
   '   #..               (my-range (add i 1) n)))))) ;Conditional recursion.\n'
   '   #..\n'
   '   >>> # define\n'
   "   ... __import__('builtins').globals().update(\n"
   '   ...   myQz_range=(lambda i,n:\n'
   '   ...                Ensue(\n'
   '   ...                  (lambda step:\n'
   '   ...                    # when\n'
   '   ...                    (lambda b,c:c()if b else())(\n'
   '   ...                      lt(\n'
   '   ...                        i,\n'
   '   ...                        n),\n'
   '   ...                      (lambda :(\n'
   '   ...                        # setQzAT_\n'
   '   ...                        # hissp.macros.._macro_.let\n'
   '   ...                        (lambda _QzRMG5GSSIz_val=i:(\n'
   "   ...                          __import__('builtins').setattr(\n"
   '   ...                            step,\n'
   "   ...                            'Y',\n"
   '   ...                            _QzRMG5GSSIz_val),\n'
   '   ...                          _QzRMG5GSSIz_val)[-1])(),\n'
   '   ...                        myQz_range(\n'
   '   ...                          add(\n'
   '   ...                            i,\n'
   '   ...                            (1)),\n'
   '   ...                          n))[-1]))))))\n'
   '\n'
   '   #> (list (my-range 1 6))\n'
   '   >>> list(\n'
   '   ...   myQz_range(\n'
   '   ...     (1),\n'
   '   ...     (6)))\n'
   '   [1, 2, 3, 4, 5]\n'
   '\n'
   '   #> (Ensue (lambda (step)\n'
   '   #..         (attach step :\n'
   '   #..           F True ; Set F for yield-From mode.\n'
   "   #..           Y '(1 2 3 4 5))\n"
   '   #..         None))\n'
   '   >>> Ensue(\n'
   '   ...   (lambda step:(\n'
   '   ...     # attach\n'
   '   ...     # hissp.macros.._macro_.let\n'
   '   ...     (lambda _QzWG5WN73Wz_target=step:(\n'
   "   ...       __import__('builtins').setattr(\n"
   '   ...         _QzWG5WN73Wz_target,\n'
   "   ...         'F',\n"
   '   ...         True),\n'
   "   ...       __import__('builtins').setattr(\n"
   '   ...         _QzWG5WN73Wz_target,\n'
   "   ...         'Y',\n"
   '   ...         ((1),\n'
   '   ...          (2),\n'
   '   ...          (3),\n'
   '   ...          (4),\n'
   '   ...          (5),)),\n'
   '   ...       _QzWG5WN73Wz_target)[-1])(),\n'
   '   ...     None)[-1]))\n'
   '   <...Ensue object at ...>\n'
   '\n'
   '   #> (list _)\n'
   '   >>> list(\n'
   '   ...   _)\n'
   '   [1, 2, 3, 4, 5]\n'
   '\n'
   '   #> (define recycle\n'
   '   #..  (lambda (itr)\n'
   '   #..    (Ensue (lambda (step)\n'
   '   #..             ;; Implicit continuation; step is an Ensue.\n'
   '   #..             (attach step : Y itr  F 1)))))\n'
   '   >>> # define\n'
   "   ... __import__('builtins').globals().update(\n"
   '   ...   recycle=(lambda itr:\n'
   '   ...             Ensue(\n'
   '   ...               (lambda step:\n'
   '   ...                 # attach\n'
   '   ...                 # hissp.macros.._macro_.let\n'
   '   ...                 (lambda _QzWG5WN73Wz_target=step:(\n'
   "   ...                   __import__('builtins').setattr(\n"
   '   ...                     _QzWG5WN73Wz_target,\n'
   "   ...                     'Y',\n"
   '   ...                     itr),\n'
   "   ...                   __import__('builtins').setattr(\n"
   '   ...                     _QzWG5WN73Wz_target,\n'
   "   ...                     'F',\n"
   '   ...                     (1)),\n'
   '   ...                   _QzWG5WN73Wz_target)[-1])()))))\n'
   '\n'
   "   #> (-> '(1 2 3) recycle (islice 7) list)\n"
   '   >>> # Qz_QzGT_\n'
   '   ... list(\n'
   '   ...   islice(\n'
   '   ...     recycle(\n'
   '   ...       ((1),\n'
   '   ...        (2),\n'
   '   ...        (3),)),\n'
   '   ...     (7)))\n'
   '   [1, 2, 3, 1, 2, 3, 1]\n'
   '\n'
   '   #> (define echo\n'
   '   #..  (Ensue (lambda (step)\n'
   '   #..           (set@ step.Y step.sent)\n'
   '   #..           step)))\n'
   '   >>> # define\n'
   "   ... __import__('builtins').globals().update(\n"
   '   ...   echo=Ensue(\n'
   '   ...          (lambda step:(\n'
   '   ...            # setQzAT_\n'
   '   ...            # hissp.macros.._macro_.let\n'
   '   ...            (lambda _QzRMG5GSSIz_val=step.sent:(\n'
   "   ...              __import__('builtins').setattr(\n"
   '   ...                step,\n'
   "   ...                'Y',\n"
   '   ...                _QzRMG5GSSIz_val),\n'
   '   ...              _QzRMG5GSSIz_val)[-1])(),\n'
   '   ...            step)[-1])))\n'
   '\n'
   '   #> (.send echo None) ; Always send a None first. Same as Python.\n'
   '   >>> echo.send(\n'
   '   ...   None)\n'
   '\n'
   '   #> (.send echo "Yodle!") ; Generators are two-way.\n'
   '   >>> echo.send(\n'
   "   ...   ('Yodle!'))\n"
   "   'Yodle!'\n"
   '\n'
   '   #> (.send echo 42)\n'
   '   >>> echo.send(\n'
   '   ...   (42))\n'
   '   42\n'
   '\n'
   'enter examples\n'
   '--------------\n'
   '.. code-block:: REPL\n'
   '\n'
   '   #> (define wrap\n'
   '   #..  (contextlib..contextmanager\n'
   '   #..   (lambda (msg)\n'
   '   #..     (print "enter" msg)\n'
   '   #..     (Ensue (lambda (step)\n'
   '   #..              (set@ step.Y msg)\n'
   '   #..              (Ensue (lambda (step)\n'
   '   #..                       (print "exit" msg))))))))\n'
   '   >>> # define\n'
   "   ... __import__('builtins').globals().update(\n"
   "   ...   wrap=__import__('contextlib').contextmanager(\n"
   '   ...          (lambda msg:(\n'
   '   ...            print(\n'
   "   ...              ('enter'),\n"
   '   ...              msg),\n'
   '   ...            Ensue(\n'
   '   ...              (lambda step:(\n'
   '   ...                # setQzAT_\n'
   '   ...                # hissp.macros.._macro_.let\n'
   '   ...                (lambda _QzRMG5GSSIz_val=msg:(\n'
   "   ...                  __import__('builtins').setattr(\n"
   '   ...                    step,\n'
   "   ...                    'Y',\n"
   '   ...                    _QzRMG5GSSIz_val),\n'
   '   ...                  _QzRMG5GSSIz_val)[-1])(),\n'
   '   ...                Ensue(\n'
   '   ...                  (lambda step:\n'
   '   ...                    print(\n'
   "   ...                      ('exit'),\n"
   '   ...                      msg))))[-1])))[-1])))\n'
   '\n'
   "   #> (enter (wrap 'A)\n"
   '   #..       (lambda a (print a)))\n'
   '   >>> enter(\n'
   '   ...   wrap(\n'
   "   ...     'A'),\n"
   '   ...   (lambda a:\n'
   '   ...     print(\n'
   '   ...       a)))\n'
   '   enter A\n'
   '   A\n'
   '   exit A\n'
   '\n'
   "   #> (enter (wrap 'A)\n"
   "   #.. enter (wrap 'B)\n"
   "   #.. enter (wrap 'C) ; You can stack them.\n"
   '   #.. (lambda abc (print a b c)))\n'
   '   >>> enter(\n'
   '   ...   wrap(\n'
   "   ...     'A'),\n"
   '   ...   enter,\n'
   '   ...   wrap(\n'
   "   ...     'B'),\n"
   '   ...   enter,\n'
   '   ...   wrap(\n'
   "   ...     'C'),\n"
   '   ...   (lambda a,b,c:\n'
   '   ...     print(\n'
   '   ...       a,\n'
   '   ...       b,\n'
   '   ...       c)))\n'
   '   enter A\n'
   '   enter B\n'
   '   enter C\n'
   '   A B C\n'
   '   exit C\n'
   '   exit B\n'
   '   exit A\n'
   '\n'
   '   #> (define suppress-zde\n'
   '   #..  (contextlib..contextmanager\n'
   '   #..   (lambda :\n'
   '   #..     (Ensue (lambda (step)\n'
   '   #..              (attach step :\n'
   '   #..                Y None\n'
   '   #..                X ZeroDivisionError) ;X for eXcept (can be a tuple).\n'
   '   #..              (Ensue (lambda (step)\n'
   '   #..                       (print "Caught a" step.sent))))))))\n'
   '   >>> # define\n'
   "   ... __import__('builtins').globals().update(\n"
   "   ...   suppressQz_zde=__import__('contextlib').contextmanager(\n"
   '   ...                    (lambda :\n'
   '   ...                      Ensue(\n'
   '   ...                        (lambda step:(\n'
   '   ...                          # attach\n'
   '   ...                          # hissp.macros.._macro_.let\n'
   '   ...                          (lambda _QzWG5WN73Wz_target=step:(\n'
   "   ...                            __import__('builtins').setattr(\n"
   '   ...                              _QzWG5WN73Wz_target,\n'
   "   ...                              'Y',\n"
   '   ...                              None),\n'
   "   ...                            __import__('builtins').setattr(\n"
   '   ...                              _QzWG5WN73Wz_target,\n'
   "   ...                              'X',\n"
   '   ...                              ZeroDivisionError),\n'
   '   ...                            _QzWG5WN73Wz_target)[-1])(),\n'
   '   ...                          Ensue(\n'
   '   ...                            (lambda step:\n'
   '   ...                              print(\n'
   "   ...                                ('Caught a'),\n"
   '   ...                                step.sent))))[-1])))))\n'
   '\n'
   '   #> (enter (suppress-zde)\n'
   '   #..  (lambda _ (truediv 1 0)))\n'
   '   >>> enter(\n'
   '   ...   suppressQz_zde(),\n'
   '   ...   (lambda _:\n'
   '   ...     truediv(\n'
   '   ...       (1),\n'
   '   ...       (0))))\n'
   '   Caught a division by zero\n'
   '\n'
   '   ;; No exception, so step.sent was .send() value.\n'
   '   #> (enter (suppress-zde)\n'
   '   #..  (lambda _ (truediv 4 2)))\n'
   '   >>> enter(\n'
   '   ...   suppressQz_zde(),\n'
   '   ...   (lambda _:\n'
   '   ...     truediv(\n'
   '   ...       (4),\n'
   '   ...       (2))))\n'
   '   Caught a None\n'
   '   2.0\n'
   '\n'
   '   #> (enter (suppress-zde)\n'
   '   #..  (lambda _ (throw Exception)))\n'
   '   >>> enter(\n'
   '   ...   suppressQz_zde(),\n'
   '   ...   (lambda _:\n'
   '   ...     # throw\n'
   '   ...     # hissp.macros.._macro_.throwQzSTAR_\n'
   "   ...     (lambda g:g.close()or g.throw)(c for c in'')(\n"
   '   ...       Exception)))\n'
   '   Traceback (most recent call last):\n'
   '     ...\n'
   '   Exception\n'),
  (lambda * _: _)(
    'builtins..exec',
    (lambda * _: _)(
      'quote',
      ('from functools import partial,reduce\n'
       'from itertools import *;from operator import *\n'
       'def engarde(xs,h,f,/,*a,**kw):\n'
       ' try:return f(*a,**kw)\n'
       ' except xs as e:return h(e)\n'
       'def enter(c,f,/,*a):\n'
       ' with c as C:return f(*a,C)\n'
       "class Ensue(__import__('collections.abc').abc.Generator):\n"
       ' send=lambda s,v:s.g.send(v);throw=lambda s,*x:s.g.throw(*x);F=0;X=();Y=[]\n'
       ' def __init__(s,p):s.p,s.g,s.n=p,s._(s),s.Y\n'
       ' def _(s,k,v=None):\n'
       "  while isinstance(s:=k,__class__) and not setattr(s,'sent',v):\n"
       '   try:k,y=s.p(s),s.Y;v=(yield from y)if s.F or y is s.n else(yield y)\n'
       '   except s.X as e:v=e\n'
       '  return k\n'
       "_macro_=__import__('types').SimpleNamespace()\n"
       "try:exec('from {}._macro_ import *',vars(_macro_))\n"
       'except ModuleNotFoundError:pass').format(
        __name__)),
    ns))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ("Hissp's bundled micro prelude.\n"
     '\n'
     'Brings Hissp up to a minimal standard of usability without adding any\n'
     'dependencies in the compiled output.\n'
     '\n'
     "Mainly intended for single-file scripts that can't have dependencies,\n"
     'or similarly constrained environments (e.g. embedded, readerless).\n'
     'There, the first form should be ``(hissp.._macro_.prelude)``,\n'
     'which is also implied in ``$ lissp -c`` commands.\n'
     '\n'
     'Larger projects with access to functional and macro libraries need not\n'
     'use this prelude at all.\n'
     '\n'
     'The prelude has several effects:\n'
     '\n'
     '* Imports `functools.partial` and `functools.reduce`.\n'
     '  Star imports from `itertools` and `operator`::\n'
     '\n'
     '   from functools import partial,reduce\n'
     '   from itertools import *;from operator import *\n'
     '\n'
     '.. _engarde:\n'
     '\n'
     '* Defines ``engarde``, which calls a function with exception handler::\n'
     '\n'
     '   def engarde(xs,h,f,/,*a,**kw):\n'
     '    try:return f(*a,**kw)\n'
     '    except xs as e:return h(e)\n'
     '\n'
     '  ``engarde`` with handlers can stack above in a single form.\n'
     '\n'
     '  See `engarde examples`_ below.\n'
     '\n'
     '.. _enter:\n'
     '\n'
     '* Defines ``enter``, which calls a function with context manager::\n'
     '\n'
     '   def enter(c,f,/,*a):\n'
     '    with c as C:return f(*a,C)\n'
     '\n'
     '  ``enter`` with context managers can stack above in a single form.\n'
     '\n'
     '  See `enter examples`_ below.\n'
     '\n'
     '.. _Ensue:\n'
     '\n'
     '* Defines the ``Ensue`` class; trampolined continuation generators::\n'
     '\n'
     "   class Ensue(__import__('collections.abc').abc.Generator):\n"
     '    send=lambda s,v:s.g.send(v);throw=lambda '
     's,*x:s.g.throw(*x);F=0;X=();Y=[]\n'
     '    def __init__(s,p):s.p,s.g,s.n=p,s._(s),s.Y\n'
     '    def _(s,k,v=None):\n'
     "     while isinstance(s:=k,__class__) and not setattr(s,'sent',v):\n"
     '      try:k,y=s.p(s),s.Y;v=(yield from y)if s.F or y is s.n else(yield y)\n'
     '      except s.X as e:v=e\n'
     '     return k\n'
     '\n'
     '  ``Ensue`` takes a step function and returns a generator. The step\n'
     '  function recieves the previous Ensue step and must return the next\n'
     '  one to continue. Returning a different type raises a `StopIteration`\n'
     '  with that object. Set the ``Y`` attribute on the current step to\n'
     '  [Y]ield a value this step. Set the ``F`` attribute to a true value\n'
     '  to yield values [F]rom the ``Y`` iterable instead. Set the ``X``\n'
     '  attribute to an e[X]ception class or tuple to catch any targeted\n'
     '  exceptions on the next step. Each step keeps a ``sent`` attribute,\n'
     '  which is the value sent to the generator this step, or the exception\n'
     '  caught this step instead.\n'
     '\n'
     '  See `Ensue examples`_ and `enter examples`_ below.\n'
     '\n'
     '  See also:\n'
     '  `types.coroutine`, `collections.abc.Generator`, `loop-from<loopQz_from>`.\n'
     '\n'
     '* Adds the bundled macros, but only if available\n'
     '  (macros are typically only used at compile time),\n'
     '  so its compiled expansion does not require Hissp to be installed.\n'
     '  (This replaces ``_macro_`` if you already had one.)::\n'
     '\n'
     "   _macro_=__import__('types').SimpleNamespace()\n"
     "   try:exec('from {}._macro_ import *',vars(_macro_))\n"
     '   except ModuleNotFoundError:pass\n'
     '\n'
     'Prelude Usage\n'
     '=============\n'
     'The REPL has the bundled macros loaded by default, but not the prelude.\n'
     'Invoke ``(prelude)`` to get the rest.\n'
     '\n'
     '.. code-block:: REPL\n'
     '\n'
     '   #> (prelude)\n'
     '   >>> # prelude\n'
     "   ... __import__('builtins').exec(\n"
     "   ...   ('from functools import partial,reduce\\n'\n"
     "   ...    'from itertools import *;from operator import *\\n'\n"
     "   ...    'def engarde(xs,h,f,/,*a,**kw):\\n'\n"
     "   ...    ' try:return f(*a,**kw)\\n'\n"
     "   ...    ' except xs as e:return h(e)\\n'\n"
     "   ...    'def enter(c,f,/,*a):\\n'\n"
     "   ...    ' with c as C:return f(*a,C)\\n'\n"
     '   ...    "class Ensue(__import__(\'collections.abc\').abc.Generator):\\n"\n'
     "   ...    ' send=lambda s,v:s.g.send(v);throw=lambda "
     "s,*x:s.g.throw(*x);F=0;X=();Y=[]\\n'\n"
     "   ...    ' def __init__(s,p):s.p,s.g,s.n=p,s._(s),s.Y\\n'\n"
     "   ...    ' def _(s,k,v=None):\\n'\n"
     '   ...    "  while isinstance(s:=k,__class__) and not '
     'setattr(s,\'sent\',v):\\n"\n'
     "   ...    '   try:k,y=s.p(s),s.Y;v=(yield from y)if s.F or y is s.n "
     "else(yield y)\\n'\n"
     "   ...    '   except s.X as e:v=e\\n'\n"
     "   ...    '  return k\\n'\n"
     '   ...    "_macro_=__import__(\'types\').SimpleNamespace()\\n"\n'
     '   ...    "try:exec(\'from hissp.macros._macro_ import '
     '*\',vars(_macro_))\\n"\n'
     "   ...    'except ModuleNotFoundError:pass'),\n"
     "   ...   __import__('builtins').globals())\n"
     '\n'
     'See also, `alias`.\n'
     '\n'
     'engarde examples\n'
     '----------------\n'
     '.. code-block:: REPL\n'
     '\n'
     '   #> (engarde `(,FloatingPointError ,ZeroDivisionError) ;two targets\n'
     '   #..         (lambda e (print "Oops!") e)    ;handler (returns exception)\n'
     '   #..         truediv 6 0)                    ;calls it on your behalf\n'
     '   >>> engarde(\n'
     '   ...   (lambda * _: _)(\n'
     '   ...     FloatingPointError,\n'
     '   ...     ZeroDivisionError),\n'
     '   ...   (lambda e:(\n'
     '   ...     print(\n'
     "   ...       ('Oops!')),\n"
     '   ...     e)[-1]),\n'
     '   ...   truediv,\n'
     '   ...   (6),\n'
     '   ...   (0))\n'
     '   Oops!\n'
     "   ZeroDivisionError('division by zero')\n"
     '\n'
     '   #> (engarde ArithmeticError repr truediv 6 0) ;superclass target\n'
     '   >>> engarde(\n'
     '   ...   ArithmeticError,\n'
     '   ...   repr,\n'
     '   ...   truediv,\n'
     '   ...   (6),\n'
     '   ...   (0))\n'
     '   "ZeroDivisionError(\'division by zero\')"\n'
     '\n'
     '   #> (engarde ArithmeticError repr truediv 6 2) ;returned answer\n'
     '   >>> engarde(\n'
     '   ...   ArithmeticError,\n'
     '   ...   repr,\n'
     '   ...   truediv,\n'
     '   ...   (6),\n'
     '   ...   (2))\n'
     '   3.0\n'
     '\n'
     '   ;; You can stack them.\n'
     '   #> (engarde Exception                       ;The outer engarde\n'
     '   #.. print\n'
     '   #.. engarde ZeroDivisionError               ; calls the inner.\n'
     '   #.. (lambda e (print "It means what you want it to mean."))\n'
     '   #.. truediv "6" 0)                          ;Try variations.\n'
     '   >>> engarde(\n'
     '   ...   Exception,\n'
     '   ...   print,\n'
     '   ...   engarde,\n'
     '   ...   ZeroDivisionError,\n'
     '   ...   (lambda e:\n'
     '   ...     print(\n'
     "   ...       ('It means what you want it to mean.'))),\n"
     '   ...   truediv,\n'
     "   ...   ('6'),\n"
     '   ...   (0))\n'
     "   unsupported operand type(s) for /: 'str' and 'int'\n"
     '\n'
     '   #> (engarde Exception\n'
     '   #..         (lambda x x.__cause__)\n'
     '   #..         (lambda : (throw-from Exception (Exception "msg"))))\n'
     '   >>> engarde(\n'
     '   ...   Exception,\n'
     '   ...   (lambda x:x.__cause__),\n'
     '   ...   (lambda :\n'
     '   ...     # throwQz_from\n'
     '   ...     # hissp.macros.._macro_.throwQzSTAR_\n'
     "   ...     (lambda g:g.close()or g.throw)(c for c in'')(\n"
     '   ...       # hissp.macros.._macro_.let\n'
     '   ...       (lambda _Qz2IKKUCBWz_G=(lambda _Qz2IKKUCBWz_x:\n'
     '   ...         # hissp.macros.._macro_.ifQz_else\n'
     '   ...         (lambda b,c,a:c()if b else a())(\n'
     '   ...           # hissp.macros.._macro_.QzET_QzET_\n'
     '   ...           (lambda x0,x1:x0 and x1())(\n'
     "   ...             __import__('builtins').isinstance(\n"
     '   ...               _Qz2IKKUCBWz_x,\n'
     "   ...               __import__('builtins').type),\n"
     '   ...             (lambda :\n'
     "   ...               __import__('builtins').issubclass(\n"
     '   ...                 _Qz2IKKUCBWz_x,\n'
     "   ...                 __import__('builtins').BaseException))),\n"
     '   ...           (lambda :_Qz2IKKUCBWz_x()),\n'
     '   ...           (lambda :_Qz2IKKUCBWz_x))):\n'
     '   ...         # hissp.macros.._macro_.attach\n'
     '   ...         # hissp.macros.._macro_.let\n'
     '   ...         (lambda _QzWG5WN73Wz_target=_Qz2IKKUCBWz_G(\n'
     '   ...           Exception):(\n'
     "   ...           __import__('builtins').setattr(\n"
     '   ...             _QzWG5WN73Wz_target,\n'
     "   ...             '__cause__',\n"
     '   ...             _Qz2IKKUCBWz_G(\n'
     '   ...               Exception(\n'
     "   ...                 ('msg')))),\n"
     '   ...           _QzWG5WN73Wz_target)[-1])())())))\n'
     "   Exception('msg')\n"
     '\n'
     'Ensue examples\n'
     '--------------\n'
     '.. code-block:: REPL\n'
     '\n'
     '   #> (define fibonacci\n'
     '   #..  (lambda (: a 1  b 1)\n'
     '   #..    (Ensue (lambda (step)\n'
     '   #..             (set@ step.Y a)            ;Y for yield.\n'
     '   #..             (fibonacci b (add a b))))))\n'
     '   >>> # define\n'
     "   ... __import__('builtins').globals().update(\n"
     '   ...   fibonacci=(lambda a=(1),b=(1):\n'
     '   ...               Ensue(\n'
     '   ...                 (lambda step:(\n'
     '   ...                   # setQzAT_\n'
     '   ...                   # hissp.macros.._macro_.let\n'
     '   ...                   (lambda _QzRMG5GSSIz_val=a:(\n'
     "   ...                     __import__('builtins').setattr(\n"
     '   ...                       step,\n'
     "   ...                       'Y',\n"
     '   ...                       _QzRMG5GSSIz_val),\n'
     '   ...                     _QzRMG5GSSIz_val)[-1])(),\n'
     '   ...                   fibonacci(\n'
     '   ...                     b,\n'
     '   ...                     add(\n'
     '   ...                       a,\n'
     '   ...                       b)))[-1]))))\n'
     '\n'
     '   #> (list (islice (fibonacci) 7))\n'
     '   >>> list(\n'
     '   ...   islice(\n'
     '   ...     fibonacci(),\n'
     '   ...     (7)))\n'
     '   [1, 1, 2, 3, 5, 8, 13]\n'
     '\n'
     '   #> (define my-range ; Terminate by not returning an Ensue.\n'
     '   #..  (lambda in\n'
     '   #..    (Ensue (lambda (step)\n'
     '   #..             (when (lt i n)             ;Acts like a while loop.\n'
     '   #..               (set@ step.Y i)\n'
     '   #..               (my-range (add i 1) n)))))) ;Conditional recursion.\n'
     '   #..\n'
     '   >>> # define\n'
     "   ... __import__('builtins').globals().update(\n"
     '   ...   myQz_range=(lambda i,n:\n'
     '   ...                Ensue(\n'
     '   ...                  (lambda step:\n'
     '   ...                    # when\n'
     '   ...                    (lambda b,c:c()if b else())(\n'
     '   ...                      lt(\n'
     '   ...                        i,\n'
     '   ...                        n),\n'
     '   ...                      (lambda :(\n'
     '   ...                        # setQzAT_\n'
     '   ...                        # hissp.macros.._macro_.let\n'
     '   ...                        (lambda _QzRMG5GSSIz_val=i:(\n'
     "   ...                          __import__('builtins').setattr(\n"
     '   ...                            step,\n'
     "   ...                            'Y',\n"
     '   ...                            _QzRMG5GSSIz_val),\n'
     '   ...                          _QzRMG5GSSIz_val)[-1])(),\n'
     '   ...                        myQz_range(\n'
     '   ...                          add(\n'
     '   ...                            i,\n'
     '   ...                            (1)),\n'
     '   ...                          n))[-1]))))))\n'
     '\n'
     '   #> (list (my-range 1 6))\n'
     '   >>> list(\n'
     '   ...   myQz_range(\n'
     '   ...     (1),\n'
     '   ...     (6)))\n'
     '   [1, 2, 3, 4, 5]\n'
     '\n'
     '   #> (Ensue (lambda (step)\n'
     '   #..         (attach step :\n'
     '   #..           F True ; Set F for yield-From mode.\n'
     "   #..           Y '(1 2 3 4 5))\n"
     '   #..         None))\n'
     '   >>> Ensue(\n'
     '   ...   (lambda step:(\n'
     '   ...     # attach\n'
     '   ...     # hissp.macros.._macro_.let\n'
     '   ...     (lambda _QzWG5WN73Wz_target=step:(\n'
     "   ...       __import__('builtins').setattr(\n"
     '   ...         _QzWG5WN73Wz_target,\n'
     "   ...         'F',\n"
     '   ...         True),\n'
     "   ...       __import__('builtins').setattr(\n"
     '   ...         _QzWG5WN73Wz_target,\n'
     "   ...         'Y',\n"
     '   ...         ((1),\n'
     '   ...          (2),\n'
     '   ...          (3),\n'
     '   ...          (4),\n'
     '   ...          (5),)),\n'
     '   ...       _QzWG5WN73Wz_target)[-1])(),\n'
     '   ...     None)[-1]))\n'
     '   <...Ensue object at ...>\n'
     '\n'
     '   #> (list _)\n'
     '   >>> list(\n'
     '   ...   _)\n'
     '   [1, 2, 3, 4, 5]\n'
     '\n'
     '   #> (define recycle\n'
     '   #..  (lambda (itr)\n'
     '   #..    (Ensue (lambda (step)\n'
     '   #..             ;; Implicit continuation; step is an Ensue.\n'
     '   #..             (attach step : Y itr  F 1)))))\n'
     '   >>> # define\n'
     "   ... __import__('builtins').globals().update(\n"
     '   ...   recycle=(lambda itr:\n'
     '   ...             Ensue(\n'
     '   ...               (lambda step:\n'
     '   ...                 # attach\n'
     '   ...                 # hissp.macros.._macro_.let\n'
     '   ...                 (lambda _QzWG5WN73Wz_target=step:(\n'
     "   ...                   __import__('builtins').setattr(\n"
     '   ...                     _QzWG5WN73Wz_target,\n'
     "   ...                     'Y',\n"
     '   ...                     itr),\n'
     "   ...                   __import__('builtins').setattr(\n"
     '   ...                     _QzWG5WN73Wz_target,\n'
     "   ...                     'F',\n"
     '   ...                     (1)),\n'
     '   ...                   _QzWG5WN73Wz_target)[-1])()))))\n'
     '\n'
     "   #> (-> '(1 2 3) recycle (islice 7) list)\n"
     '   >>> # Qz_QzGT_\n'
     '   ... list(\n'
     '   ...   islice(\n'
     '   ...     recycle(\n'
     '   ...       ((1),\n'
     '   ...        (2),\n'
     '   ...        (3),)),\n'
     '   ...     (7)))\n'
     '   [1, 2, 3, 1, 2, 3, 1]\n'
     '\n'
     '   #> (define echo\n'
     '   #..  (Ensue (lambda (step)\n'
     '   #..           (set@ step.Y step.sent)\n'
     '   #..           step)))\n'
     '   >>> # define\n'
     "   ... __import__('builtins').globals().update(\n"
     '   ...   echo=Ensue(\n'
     '   ...          (lambda step:(\n'
     '   ...            # setQzAT_\n'
     '   ...            # hissp.macros.._macro_.let\n'
     '   ...            (lambda _QzRMG5GSSIz_val=step.sent:(\n'
     "   ...              __import__('builtins').setattr(\n"
     '   ...                step,\n'
     "   ...                'Y',\n"
     '   ...                _QzRMG5GSSIz_val),\n'
     '   ...              _QzRMG5GSSIz_val)[-1])(),\n'
     '   ...            step)[-1])))\n'
     '\n'
     '   #> (.send echo None) ; Always send a None first. Same as Python.\n'
     '   >>> echo.send(\n'
     '   ...   None)\n'
     '\n'
     '   #> (.send echo "Yodle!") ; Generators are two-way.\n'
     '   >>> echo.send(\n'
     "   ...   ('Yodle!'))\n"
     "   'Yodle!'\n"
     '\n'
     '   #> (.send echo 42)\n'
     '   >>> echo.send(\n'
     '   ...   (42))\n'
     '   42\n'
     '\n'
     'enter examples\n'
     '--------------\n'
     '.. code-block:: REPL\n'
     '\n'
     '   #> (define wrap\n'
     '   #..  (contextlib..contextmanager\n'
     '   #..   (lambda (msg)\n'
     '   #..     (print "enter" msg)\n'
     '   #..     (Ensue (lambda (step)\n'
     '   #..              (set@ step.Y msg)\n'
     '   #..              (Ensue (lambda (step)\n'
     '   #..                       (print "exit" msg))))))))\n'
     '   >>> # define\n'
     "   ... __import__('builtins').globals().update(\n"
     "   ...   wrap=__import__('contextlib').contextmanager(\n"
     '   ...          (lambda msg:(\n'
     '   ...            print(\n'
     "   ...              ('enter'),\n"
     '   ...              msg),\n'
     '   ...            Ensue(\n'
     '   ...              (lambda step:(\n'
     '   ...                # setQzAT_\n'
     '   ...                # hissp.macros.._macro_.let\n'
     '   ...                (lambda _QzRMG5GSSIz_val=msg:(\n'
     "   ...                  __import__('builtins').setattr(\n"
     '   ...                    step,\n'
     "   ...                    'Y',\n"
     '   ...                    _QzRMG5GSSIz_val),\n'
     '   ...                  _QzRMG5GSSIz_val)[-1])(),\n'
     '   ...                Ensue(\n'
     '   ...                  (lambda step:\n'
     '   ...                    print(\n'
     "   ...                      ('exit'),\n"
     '   ...                      msg))))[-1])))[-1])))\n'
     '\n'
     "   #> (enter (wrap 'A)\n"
     '   #..       (lambda a (print a)))\n'
     '   >>> enter(\n'
     '   ...   wrap(\n'
     "   ...     'A'),\n"
     '   ...   (lambda a:\n'
     '   ...     print(\n'
     '   ...       a)))\n'
     '   enter A\n'
     '   A\n'
     '   exit A\n'
     '\n'
     "   #> (enter (wrap 'A)\n"
     "   #.. enter (wrap 'B)\n"
     "   #.. enter (wrap 'C) ; You can stack them.\n"
     '   #.. (lambda abc (print a b c)))\n'
     '   >>> enter(\n'
     '   ...   wrap(\n'
     "   ...     'A'),\n"
     '   ...   enter,\n'
     '   ...   wrap(\n'
     "   ...     'B'),\n"
     '   ...   enter,\n'
     '   ...   wrap(\n'
     "   ...     'C'),\n"
     '   ...   (lambda a,b,c:\n'
     '   ...     print(\n'
     '   ...       a,\n'
     '   ...       b,\n'
     '   ...       c)))\n'
     '   enter A\n'
     '   enter B\n'
     '   enter C\n'
     '   A B C\n'
     '   exit C\n'
     '   exit B\n'
     '   exit A\n'
     '\n'
     '   #> (define suppress-zde\n'
     '   #..  (contextlib..contextmanager\n'
     '   #..   (lambda :\n'
     '   #..     (Ensue (lambda (step)\n'
     '   #..              (attach step :\n'
     '   #..                Y None\n'
     '   #..                X ZeroDivisionError) ;X for eXcept (can be a tuple).\n'
     '   #..              (Ensue (lambda (step)\n'
     '   #..                       (print "Caught a" step.sent))))))))\n'
     '   >>> # define\n'
     "   ... __import__('builtins').globals().update(\n"
     "   ...   suppressQz_zde=__import__('contextlib').contextmanager(\n"
     '   ...                    (lambda :\n'
     '   ...                      Ensue(\n'
     '   ...                        (lambda step:(\n'
     '   ...                          # attach\n'
     '   ...                          # hissp.macros.._macro_.let\n'
     '   ...                          (lambda _QzWG5WN73Wz_target=step:(\n'
     "   ...                            __import__('builtins').setattr(\n"
     '   ...                              _QzWG5WN73Wz_target,\n'
     "   ...                              'Y',\n"
     '   ...                              None),\n'
     "   ...                            __import__('builtins').setattr(\n"
     '   ...                              _QzWG5WN73Wz_target,\n'
     "   ...                              'X',\n"
     '   ...                              ZeroDivisionError),\n'
     '   ...                            _QzWG5WN73Wz_target)[-1])(),\n'
     '   ...                          Ensue(\n'
     '   ...                            (lambda step:\n'
     '   ...                              print(\n'
     "   ...                                ('Caught a'),\n"
     '   ...                                step.sent))))[-1])))))\n'
     '\n'
     '   #> (enter (suppress-zde)\n'
     '   #..  (lambda _ (truediv 1 0)))\n'
     '   >>> enter(\n'
     '   ...   suppressQz_zde(),\n'
     '   ...   (lambda _:\n'
     '   ...     truediv(\n'
     '   ...       (1),\n'
     '   ...       (0))))\n'
     '   Caught a division by zero\n'
     '\n'
     '   ;; No exception, so step.sent was .send() value.\n'
     '   #> (enter (suppress-zde)\n'
     '   #..  (lambda _ (truediv 4 2)))\n'
     '   >>> enter(\n'
     '   ...   suppressQz_zde(),\n'
     '   ...   (lambda _:\n'
     '   ...     truediv(\n'
     '   ...       (4),\n'
     '   ...       (2))))\n'
     '   Caught a None\n'
     '   2.0\n'
     '\n'
     '   #> (enter (suppress-zde)\n'
     '   #..  (lambda _ (throw Exception)))\n'
     '   >>> enter(\n'
     '   ...   suppressQz_zde(),\n'
     '   ...   (lambda _:\n'
     '   ...     # throw\n'
     '   ...     # hissp.macros.._macro_.throwQzSTAR_\n'
     "   ...     (lambda g:g.close()or g.throw)(c for c in'')(\n"
     '   ...       Exception)))\n'
     '   Traceback (most recent call last):\n'
     '     ...\n'
     '   Exception\n')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'prelude',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'prelude',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda *args:
  (lambda * _: _)(
    'builtins..print',
    (lambda * _: _)(
      'codecs..encode',
      (lambda * _: _)(
        'hissp.macros..QzMaybe_._TAO',
        'inspect..getsource'),
      (lambda * _: _)(
        'quote',
        'rot13')))):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'import',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'import',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda key,default,*pairs:(
  ('Switch case macro.\n'
   '\n'
   'Precomputes a lookup table (dict), so must switch on a hashable key.\n'
   "Target keys are not evaluated, so don't quote them; they must be known\n"
   'at compile time.\n'
   '\n'
   'The default case is first and required.\n'
   'The remainder are implicitly paired by position.\n'
   '\n'
   '.. code-block:: REPL\n'
   '\n'
   '   #> (any-map x \'(1 2 spam .#"42" :eggs)\n'
   '   #..  (case x (print "default")\n'
   '   #..    (0 2 .#"42") (print "even")\n'
   '   #..    (1 3 spam) (print "odd")))\n'
   '   >>> # anyQz_map\n'
   "   ... __import__('builtins').any(\n"
   "   ...   __import__('builtins').map(\n"
   '   ...     (lambda x:\n'
   '   ...       # case\n'
   "   ...       __import__('operator').getitem(\n"
   '   ...         # hissp.macros.._macro_.QzAT_\n'
   '   ...         (lambda *xs:[*xs])(\n'
   '   ...           (lambda :\n'
   '   ...             print(\n'
   "   ...               ('odd'))),\n"
   '   ...           (lambda :\n'
   '   ...             print(\n'
   "   ...               ('even'))),\n"
   '   ...           (lambda :\n'
   '   ...             print(\n'
   "   ...               ('default')))),\n"
   "   ...         {1: 0, 3: 0, 'spam': 0, 0: 1, 2: 1, '42': 1}.get(\n"
   '   ...           x,\n'
   '   ...           (-1)))()),\n'
   '   ...     ((1),\n'
   '   ...      (2),\n'
   "   ...      'spam',\n"
   "   ...      '42',\n"
   "   ...      ':eggs',)))\n"
   '   odd\n'
   '   even\n'
   '   odd\n'
   '   even\n'
   '   default\n'
   '   False\n'
   '\n'
   'See also: `cond`.\n'),
  # when
  (lambda b,c:c()if b else())(
    __import__('operator').mod(
      len(
        pairs),
      (2)),
    (lambda :
      # throw
      # hissp.macros.._macro_.throwQzSTAR_
      (lambda g:g.close()or g.throw)(c for c in'')(
        TypeError(
          ('Incomplete pair'))))),
  # let
  (lambda kss=(lambda _QzJXZWCGIRz_G:(_QzJXZWCGIRz_G[-2::-2]))(
    pairs),ts=(lambda _QzJXZWCGIRz_G:(_QzJXZWCGIRz_G[::-2]))(
    pairs):
    (lambda * _: _)(
      (lambda * _: _)(
        'operator..getitem',
        (lambda * _: _)(
          'hissp.macros.._macro_.QzAT_',
          *map(
             (lambda X:
               (lambda * _: _)(
                 'lambda',
                 ':',
                 X)),
             ts),
          (lambda * _: _)(
            'lambda',
            ':',
            default)),
        (lambda * _: _)(
          '.get',
          dict(
            __import__('itertools').chain.from_iterable(
              __import__('itertools').starmap(
                (lambda i,ks:
                  map(
                    (lambda X:
                      # QzAT_
                      (lambda *xs:[*xs])(
                        X,
                        i)),
                    ks)),
                enumerate(
                  kss)))),
          key,
          (-1)))))())[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('Switch case macro.\n'
     '\n'
     'Precomputes a lookup table (dict), so must switch on a hashable key.\n'
     "Target keys are not evaluated, so don't quote them; they must be known\n"
     'at compile time.\n'
     '\n'
     'The default case is first and required.\n'
     'The remainder are implicitly paired by position.\n'
     '\n'
     '.. code-block:: REPL\n'
     '\n'
     '   #> (any-map x \'(1 2 spam .#"42" :eggs)\n'
     '   #..  (case x (print "default")\n'
     '   #..    (0 2 .#"42") (print "even")\n'
     '   #..    (1 3 spam) (print "odd")))\n'
     '   >>> # anyQz_map\n'
     "   ... __import__('builtins').any(\n"
     "   ...   __import__('builtins').map(\n"
     '   ...     (lambda x:\n'
     '   ...       # case\n'
     "   ...       __import__('operator').getitem(\n"
     '   ...         # hissp.macros.._macro_.QzAT_\n'
     '   ...         (lambda *xs:[*xs])(\n'
     '   ...           (lambda :\n'
     '   ...             print(\n'
     "   ...               ('odd'))),\n"
     '   ...           (lambda :\n'
     '   ...             print(\n'
     "   ...               ('even'))),\n"
     '   ...           (lambda :\n'
     '   ...             print(\n'
     "   ...               ('default')))),\n"
     "   ...         {1: 0, 3: 0, 'spam': 0, 0: 1, 2: 1, '42': 1}.get(\n"
     '   ...           x,\n'
     '   ...           (-1)))()),\n'
     '   ...     ((1),\n'
     '   ...      (2),\n'
     "   ...      'spam',\n"
     "   ...      '42',\n"
     "   ...      ':eggs',)))\n"
     '   odd\n'
     '   even\n'
     '   odd\n'
     '   even\n'
     '   default\n'
     '   False\n'
     '\n'
     'See also: `cond`.\n')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'case',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'case',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda x:(
  ("``nil#`` evaluates as ``x or ()``. Adapter for 'nil punning'."),
  (lambda * _: _)(
    'hissp.macros.._macro_.QzVERT_QzVERT_',
    x,
    ()))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ("``nil#`` evaluates as ``x or ()``. Adapter for 'nil punning'.")),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'nilQzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'nilQzHASH_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda e:(
  ("``^*#`` 'synexpand' concatenative mini-language expressions\n"
   '\n'
   '  Walks e expanding any mini-language syntax found.\n'
   '\n'
   '  The mini-language supports higher-order function manipulation\n'
   '  including composition, partial application, and point-free data flow.\n'
   '\n'
   '  A mini-language expression is a tuple beginning with an element\n'
   '  containing at least one ``^`` or ``:`` character that is not the first\n'
   '  character (to avoid detecting all control words). The remainder form\n'
   '  the initial stack.\n'
   '\n'
   '  The first element must read to a `str` (typically a symbol, control\n'
   '  word, or injected string literal), is demunged, and is split into\n'
   '  terms on magic characters.\n'
   '\n'
   '  Syntax expansion builds an expression from the stack of expressions\n'
   '  operated on by the mini-language terms. The result is the stack\n'
   '  spliced into a `prog1` (or the element itself if only one remains).\n'
   '\n'
   '  The\n'
   '  `^#<QzHAT_QzHASH_>`,\n'
   '  `^^#<QzHAT_QzHAT_QzHASH_>`,\n'
   '  `^^^#<QzHAT_QzHAT_QzHAT_QzHASH_>`, and\n'
   '  `^^^^#<QzHAT_QzHAT_QzHAT_QzHAT_QzHASH_>` macros apply to terms and\n'
   '  wrap a ``^*#`` expression in a lambda of arity 1-4 (respectively)\n'
   '  using their parameters as the initial stack.\n'
   '\n'
   '  The terms are applied right-to-left, like function calls.\n'
   '  Magic characters are\n'
   '\n'
   '  ``,`` -data (Suffix)\n'
   '     Interprets callable term as data.\n'
   '  ``^`` -depth (Suffix)\n'
   '     Increases arity of a term. Assume depth 1 otherwise. Can be repeated.\n'
   '     Write after -data.\n'
   '  ``/`` DROP (term)\n'
   '     Removes expression (at depth).\n'
   '  ``&`` PICK (term)\n'
   '     Copies expression (at depth) and pushes. Non-literal expressions\n'
   '     are extracted to a local first (using `let`), and the resulting\n'
   '     symbol is copied instead.\n'
   '  ``@`` ROLL (term, default depth 2)\n'
   '     Pops expression (at depth) and pushes.\n'
   '  ``>`` MARK (term, default depth 0)\n'
   '     Inserts a sentinel object for PACK (at depth).\n'
   '  ``<`` PACK (term)\n'
   '     Pops to the first MARK (if any) and pushes as tuple.\n'
   '     With depth, looks tuple up on the next expression.\n'
   '     Used for invocations.\n'
   '  ``*`` SPLAT (term)\n'
   '     Splices an iterable (in-place, at depth).\n'
   '  ``:`` NOP (no depth)\n'
   '     Has no effect. A separator when no other magic applies.\n'
   '\n'
   '  They can be escaped with a backtick (:literal:`\\``).\n'
   '\n'
   '  Other terms are either callables or data, and read as Lissp.\n'
   '\n'
   '  Callables (default depth 1) pop args to their depth and push their\n'
   '  result. Combine with a datum for partial application.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> (define decrement ^#sub^@1)\n'
   '     >>> # define\n'
   "     ... __import__('builtins').globals().update(\n"
   '     ...   decrement=(lambda _QzX7FS3TFJz_x:\n'
   '     ...               # hissp.macros.._macro_.QzHAT_QzSTAR_QzHASH_\n'
   '     ...               sub(\n'
   '     ...                 _QzX7FS3TFJz_x,\n'
   '     ...                 (1))))\n'
   '\n'
   '     #> (decrement 5)\n'
   '     >>> decrement(\n'
   '     ...   (5))\n'
   '     4\n'
   '\n'
   '  Data terms just push themselves on the stack (default depth 0).\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> ^*#(<`@,1:2:3)\n'
   '     >>> # QzAT_\n'
   '     ... (lambda *xs:[*xs])(\n'
   '     ...   (1),\n'
   '     ...   (2),\n'
   '     ...   (3))\n'
   '     [1, 2, 3]\n'
   '\n'
   '  Increasing the depth of data to 1 implies a lookup on the next\n'
   '  expression. Methods always need a self, so they can be converted to\n'
   '  attribute lookups at the default depth of 1. Combine them to drill\n'
   '  into complex data structures.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   "     #> (^#.__class__.__name__:'spam^ (dict : spam 'eggs))\n"
   '     >>> (lambda _QzX7FS3TFJz_x:\n'
   '     ...   # hissp.macros.._macro_.QzHAT_QzSTAR_QzHASH_\n'
   "     ...   __import__('operator').attrgetter(\n"
   "     ...     '__class__.__name__')(\n"
   "     ...     __import__('operator').getitem(\n"
   '     ...       _QzX7FS3TFJz_x,\n'
   "     ...       'spam')))(\n"
   '     ...   dict(\n'
   "     ...     spam='eggs'))\n"
   "     'str'\n"
   '\n'
   '  Terms are categorized as callable or data at read time. Literals are\n'
   '  always data, but a term that reads as a `tuple` or `str` type may be\n'
   "  ambiguous, in which case it's presumed callable, unless it ends with a\n"
   '  ``,``.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> (define prod ^#reduce^mul,)\n'
   '     >>> # define\n'
   "     ... __import__('builtins').globals().update(\n"
   '     ...   prod=(lambda _QzX7FS3TFJz_x:\n'
   '     ...          # hissp.macros.._macro_.QzHAT_QzSTAR_QzHASH_\n'
   '     ...          reduce(\n'
   '     ...            mul,\n'
   '     ...            _QzX7FS3TFJz_x)))\n'
   '\n'
   '     #> (en#prod 1 2 3)\n'
   '     >>> (lambda *_Qz6RFWTTVXz_xs:\n'
   '     ...   prod(\n'
   '     ...     _Qz6RFWTTVXz_xs))(\n'
   '     ...   (1),\n'
   '     ...   (2),\n'
   '     ...   (3))\n'
   '     6\n'
   '\n'
   '     #> (define geomean ^#pow^prod@truediv^1:len&)\n'
   '     >>> # define\n'
   "     ... __import__('builtins').globals().update(\n"
   '     ...   geomean=(lambda _QzX7FS3TFJz_x:\n'
   '     ...             # hissp.macros.._macro_.QzHAT_QzSTAR_QzHASH_\n'
   '     ...             pow(\n'
   '     ...               prod(\n'
   '     ...                 _QzX7FS3TFJz_x),\n'
   '     ...               truediv(\n'
   '     ...                 (1),\n'
   '     ...                 len(\n'
   '     ...                   _QzX7FS3TFJz_x)))))\n'
   '\n'
   "     #> (geomean '(1 10))\n"
   '     >>> geomean(\n'
   '     ...   ((1),\n'
   '     ...    (10),))\n'
   '     3.1622776601683795\n'
   '\n'
   '  '),
  # ifQz_else
  (lambda b,c,a:c()if b else a())(
    # QzET_QzET_
    (lambda x0,x1:x0 and x1())(
      e,
      (lambda :
        __import__('operator').is_(
          tuple,
          type(
            e)))),
    (lambda :
      # letQz_from
      (lambda sym,*args:
        # ifQz_else
        (lambda b,c,a:c()if b else a())(
          # QzET_QzET_
          (lambda x0,x1:x0 and x1())(
            __import__('operator').is_(
              str,
              type(
                sym)),
            (lambda :
              __import__('re').search(
                ('.[:^]'),
                __import__('hissp').demunge(
                  sym)))),
          (lambda :
            _macro_._rewrite(
              __import__('re').findall(
                ('([/&@<>*:]|(?:[^,^`/&@<>*:]|`[,^/&@<>*:])+)(,?\\^*)'),
                __import__('hissp').demunge(
                  sym)),
              *map(
                 (lambda X:
                   _macro_.QzHAT_QzSTAR_QzHASH_(
                     X)),
                 args))),
          (lambda :
            (lambda * _: _)(
              *map(
                 (lambda X:
                   _macro_.QzHAT_QzSTAR_QzHASH_(
                     X)),
                 e)))))(
        *e)),
    (lambda :e)))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ("``^*#`` 'synexpand' concatenative mini-language expressions\n"
     '\n'
     '  Walks e expanding any mini-language syntax found.\n'
     '\n'
     '  The mini-language supports higher-order function manipulation\n'
     '  including composition, partial application, and point-free data flow.\n'
     '\n'
     '  A mini-language expression is a tuple beginning with an element\n'
     '  containing at least one ``^`` or ``:`` character that is not the first\n'
     '  character (to avoid detecting all control words). The remainder form\n'
     '  the initial stack.\n'
     '\n'
     '  The first element must read to a `str` (typically a symbol, control\n'
     '  word, or injected string literal), is demunged, and is split into\n'
     '  terms on magic characters.\n'
     '\n'
     '  Syntax expansion builds an expression from the stack of expressions\n'
     '  operated on by the mini-language terms. The result is the stack\n'
     '  spliced into a `prog1` (or the element itself if only one remains).\n'
     '\n'
     '  The\n'
     '  `^#<QzHAT_QzHASH_>`,\n'
     '  `^^#<QzHAT_QzHAT_QzHASH_>`,\n'
     '  `^^^#<QzHAT_QzHAT_QzHAT_QzHASH_>`, and\n'
     '  `^^^^#<QzHAT_QzHAT_QzHAT_QzHAT_QzHASH_>` macros apply to terms and\n'
     '  wrap a ``^*#`` expression in a lambda of arity 1-4 (respectively)\n'
     '  using their parameters as the initial stack.\n'
     '\n'
     '  The terms are applied right-to-left, like function calls.\n'
     '  Magic characters are\n'
     '\n'
     '  ``,`` -data (Suffix)\n'
     '     Interprets callable term as data.\n'
     '  ``^`` -depth (Suffix)\n'
     '     Increases arity of a term. Assume depth 1 otherwise. Can be repeated.\n'
     '     Write after -data.\n'
     '  ``/`` DROP (term)\n'
     '     Removes expression (at depth).\n'
     '  ``&`` PICK (term)\n'
     '     Copies expression (at depth) and pushes. Non-literal expressions\n'
     '     are extracted to a local first (using `let`), and the resulting\n'
     '     symbol is copied instead.\n'
     '  ``@`` ROLL (term, default depth 2)\n'
     '     Pops expression (at depth) and pushes.\n'
     '  ``>`` MARK (term, default depth 0)\n'
     '     Inserts a sentinel object for PACK (at depth).\n'
     '  ``<`` PACK (term)\n'
     '     Pops to the first MARK (if any) and pushes as tuple.\n'
     '     With depth, looks tuple up on the next expression.\n'
     '     Used for invocations.\n'
     '  ``*`` SPLAT (term)\n'
     '     Splices an iterable (in-place, at depth).\n'
     '  ``:`` NOP (no depth)\n'
     '     Has no effect. A separator when no other magic applies.\n'
     '\n'
     '  They can be escaped with a backtick (:literal:`\\``).\n'
     '\n'
     '  Other terms are either callables or data, and read as Lissp.\n'
     '\n'
     '  Callables (default depth 1) pop args to their depth and push their\n'
     '  result. Combine with a datum for partial application.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> (define decrement ^#sub^@1)\n'
     '     >>> # define\n'
     "     ... __import__('builtins').globals().update(\n"
     '     ...   decrement=(lambda _QzX7FS3TFJz_x:\n'
     '     ...               # hissp.macros.._macro_.QzHAT_QzSTAR_QzHASH_\n'
     '     ...               sub(\n'
     '     ...                 _QzX7FS3TFJz_x,\n'
     '     ...                 (1))))\n'
     '\n'
     '     #> (decrement 5)\n'
     '     >>> decrement(\n'
     '     ...   (5))\n'
     '     4\n'
     '\n'
     '  Data terms just push themselves on the stack (default depth 0).\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> ^*#(<`@,1:2:3)\n'
     '     >>> # QzAT_\n'
     '     ... (lambda *xs:[*xs])(\n'
     '     ...   (1),\n'
     '     ...   (2),\n'
     '     ...   (3))\n'
     '     [1, 2, 3]\n'
     '\n'
     '  Increasing the depth of data to 1 implies a lookup on the next\n'
     '  expression. Methods always need a self, so they can be converted to\n'
     '  attribute lookups at the default depth of 1. Combine them to drill\n'
     '  into complex data structures.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     "     #> (^#.__class__.__name__:'spam^ (dict : spam 'eggs))\n"
     '     >>> (lambda _QzX7FS3TFJz_x:\n'
     '     ...   # hissp.macros.._macro_.QzHAT_QzSTAR_QzHASH_\n'
     "     ...   __import__('operator').attrgetter(\n"
     "     ...     '__class__.__name__')(\n"
     "     ...     __import__('operator').getitem(\n"
     '     ...       _QzX7FS3TFJz_x,\n'
     "     ...       'spam')))(\n"
     '     ...   dict(\n'
     "     ...     spam='eggs'))\n"
     "     'str'\n"
     '\n'
     '  Terms are categorized as callable or data at read time. Literals are\n'
     '  always data, but a term that reads as a `tuple` or `str` type may be\n'
     "  ambiguous, in which case it's presumed callable, unless it ends with a\n"
     '  ``,``.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> (define prod ^#reduce^mul,)\n'
     '     >>> # define\n'
     "     ... __import__('builtins').globals().update(\n"
     '     ...   prod=(lambda _QzX7FS3TFJz_x:\n'
     '     ...          # hissp.macros.._macro_.QzHAT_QzSTAR_QzHASH_\n'
     '     ...          reduce(\n'
     '     ...            mul,\n'
     '     ...            _QzX7FS3TFJz_x)))\n'
     '\n'
     '     #> (en#prod 1 2 3)\n'
     '     >>> (lambda *_Qz6RFWTTVXz_xs:\n'
     '     ...   prod(\n'
     '     ...     _Qz6RFWTTVXz_xs))(\n'
     '     ...   (1),\n'
     '     ...   (2),\n'
     '     ...   (3))\n'
     '     6\n'
     '\n'
     '     #> (define geomean ^#pow^prod@truediv^1:len&)\n'
     '     >>> # define\n'
     "     ... __import__('builtins').globals().update(\n"
     '     ...   geomean=(lambda _QzX7FS3TFJz_x:\n'
     '     ...             # hissp.macros.._macro_.QzHAT_QzSTAR_QzHASH_\n'
     '     ...             pow(\n'
     '     ...               prod(\n'
     '     ...                 _QzX7FS3TFJz_x),\n'
     '     ...               truediv(\n'
     '     ...                 (1),\n'
     '     ...                 len(\n'
     '     ...                   _QzX7FS3TFJz_x)))))\n'
     '\n'
     "     #> (geomean '(1 10))\n"
     '     >>> geomean(\n'
     '     ...   ((1),\n'
     '     ...    (10),))\n'
     '     3.1622776601683795\n'
     '\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'QzHAT_QzSTAR_QzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'QzHAT_QzSTAR_QzHASH_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda program,*exprs:
  # ifQz_else
  (lambda b,c,a:c()if b else a())(
    not(
      program),
    (lambda :
      # case
      __import__('operator').getitem(
        # hissp.macros.._macro_.QzAT_
        (lambda *xs:[*xs])(
          (lambda :
            __import__('operator').itemgetter(
              (0))(
              exprs)),
          (lambda :
            (lambda * _: _)(
              'hissp.macros.._macro_.prog1',
              *exprs))),
        {1: 0}.get(
          len(
            exprs),
          (-1)))()),
    (lambda :
      # hissp.macros.._macro_.let
      (lambda my=__import__('types').SimpleNamespace():
        # letQz_from
        (lambda cmd,suffix:(
          # attach
          # hissp.macros.._macro_.let
          (lambda _QzZAVQQ4JMz_target=my:(
            __import__('builtins').setattr(
              _QzZAVQQ4JMz_target,
              'reader',
              __import__('hissp').reader.Lissp(
                ns=__import__('hissp.compiler',fromlist='?').NS.get())),
            __import__('builtins').setattr(
              _QzZAVQQ4JMz_target,
              'isQzQUERY_',
              (lambda X,Y:
                __import__('operator').is_(
                  X,
                  type(
                    Y)))),
            __import__('builtins').setattr(
              _QzZAVQQ4JMz_target,
              'strQzQUERY_',
              (lambda X:
                my.isQzQUERY_(
                  str,
                  X))),
            __import__('builtins').setattr(
              _QzZAVQQ4JMz_target,
              'startswithQzQUERY_',
              (lambda X,Y:
                # QzET_QzET_
                (lambda x0,x1:x0 and x1())(
                  my.strQzQUERY_(
                    X),
                  (lambda :
                    X.startswith(
                      Y))))),
            __import__('builtins').setattr(
              _QzZAVQQ4JMz_target,
              'literalQzQUERY_',
              (lambda X:
                # QzVERT_QzVERT_
                (lambda x0,x1:x0 or x1())(
                  __import__('operator').eq(
                    (),
                    X),
                  (lambda :
                    not(
                      __import__('operator').contains(
                        # QzHASH_
                        (lambda *xs:{*xs})(
                          tuple,
                          str),
                        type(
                          X))))))),
            __import__('builtins').setattr(
              _QzZAVQQ4JMz_target,
              'quotationQzQUERY_',
              (lambda X:
                # QzET_QzET_
                (lambda x0,x1:x0 and x1())(
                  my.isQzQUERY_(
                    tuple,
                    X),
                  (lambda :
                    __import__('operator').eq(
                      'quote',
                      __import__('operator').itemgetter(
                        (0))(
                        X)))))),
            __import__('builtins').setattr(
              _QzZAVQQ4JMz_target,
              'controlQz_wordQzQUERY_',
              (lambda X:
                my.startswithQzQUERY_(
                  X,
                  (':')))),
            __import__('builtins').setattr(
              _QzZAVQQ4JMz_target,
              'moduleQz_handleQzQUERY_',
              (lambda X:
                # QzET_QzET_
                (lambda x0,x1:x0 and x1())(
                  my.strQzQUERY_(
                    X),
                  (lambda :
                    X.endswith(
                      ('.')))))),
            __import__('builtins').setattr(
              _QzZAVQQ4JMz_target,
              'methodQzQUERY_',
              (lambda X:
                my.startswithQzQUERY_(
                  X,
                  ('.')))),
            __import__('builtins').setattr(
              _QzZAVQQ4JMz_target,
              'symbolQzQUERY_',
              (lambda X:
                # QzET_QzET_
                (lambda x0,x1:x0 and x1())(
                  my.strQzQUERY_(
                    X),
                  (lambda :
                    X.replace(
                      ('.'),
                      ('')).isidentifier())))),
            __import__('builtins').setattr(
              _QzZAVQQ4JMz_target,
              'G',
              None),
            __import__('builtins').setattr(
              _QzZAVQQ4JMz_target,
              'exprs',
              list(
                exprs)),
            __import__('builtins').setattr(
              _QzZAVQQ4JMz_target,
              'arity',
              suffix.count(
                ('^'))),
            __import__('builtins').setattr(
              _QzZAVQQ4JMz_target,
              'mark',
              getattr(
                __import__('unittest.mock',fromlist='?').sentinel,
                ('hissp.>'))),
            _QzZAVQQ4JMz_target)[-1])(),
          # attach
          # hissp.macros.._macro_.let
          (lambda _QzZAVQQ4JMz_target=my:(
            __import__('builtins').setattr(
              _QzZAVQQ4JMz_target,
              'iexprs',
              iter(
                my.exprs)),
            __import__('builtins').setattr(
              _QzZAVQQ4JMz_target,
              'obj',
              next(
                my.reader.reads(
                  cmd.replace(
                    ('`'),
                    (''))))),
            __import__('builtins').setattr(
              _QzZAVQQ4JMz_target,
              'arityQzPLUS_1',
              __import__('operator').add(
                (1),
                my.arity)),
            _QzZAVQQ4JMz_target)[-1])(),
          # when
          (lambda b,c:c()if b else())(
            # QzET_QzET_
            (lambda x0,x1,x2,x3,x4,x5:x0 and x1()and x2()and x3()and x4()and x5())(
              __import__('operator').eq(
                ('&'),
                cmd),
              (lambda :
                not(
                  my.literalQzQUERY_(
                    # setQzAT_
                    # hissp.macros.._macro_.let
                    (lambda _QzWBHN72I2z_val=__import__('operator').getitem(
                      exprs,
                      my.arity):(
                      __import__('builtins').setattr(
                        my,
                        'target',
                        _QzWBHN72I2z_val),
                      _QzWBHN72I2z_val)[-1])()))),
              (lambda :
                not(
                  __import__('hissp.reader',fromlist='?').is_lissp_string(
                    my.target))),
              (lambda :
                not(
                  my.controlQz_wordQzQUERY_(
                    my.target))),
              (lambda :
                not(
                  my.symbolQzQUERY_(
                    my.target))),
              (lambda :
                not(
                  my.quotationQzQUERY_(
                    my.target)))),
            (lambda :(
              # setQzAT_
              # hissp.macros.._macro_.let
              (lambda _QzWBHN72I2z_val=('{}{}').format(
                '_Qz7EYS2C3Nz_G',
                __import__('hissp.reader',fromlist='?').gensym_counter()):(
                __import__('builtins').setattr(
                  my,
                  'G',
                  _QzWBHN72I2z_val),
                _QzWBHN72I2z_val)[-1])(),
              __import__('operator').setitem(
                my.exprs,
                my.arity,
                my.G))[-1])),
          # setQzAT_
          # hissp.macros.._macro_.let
          (lambda _QzWBHN72I2z_val=# case
          __import__('operator').getitem(
            # hissp.macros.._macro_.QzAT_
            (lambda *xs:[*xs])(
              (lambda :()),
              (lambda :
                # QzAT_
                (lambda *xs:[*xs])(
                  *__import__('itertools').islice(
                     my.iexprs,
                     my.arity),
                  *next(
                     my.iexprs))),
              (lambda :
                # QzAT_
                (lambda *xs:[*xs])(
                  # let
                  (lambda x=tuple(
                    __import__('itertools').takewhile(
                      (lambda X:
                        __import__('operator').ne(
                          X,
                          my.mark)),
                      my.iexprs)):
                    # ifQz_else
                    (lambda b,c,a:c()if b else a())(
                      suffix,
                      (lambda :
                        (lambda * _: _)(
                          'operator..getitem',
                          next(
                            my.iexprs),
                          'hissp.macros..x')),
                      (lambda :x)))())),
              (lambda :
                # hissp.macros.._macro_.QzVERT_QzVERT_
                (lambda x0,x1:x0 or x1())(
                  my.exprs.insert(
                    my.arity,
                    my.mark),
                  (lambda :()))),
              (lambda :
                # QzAT_
                (lambda *xs:[*xs])(
                  my.exprs.pop(
                    my.arityQzPLUS_1))),
              (lambda :
                # QzAT_
                (lambda *xs:[*xs])(
                  __import__('operator').getitem(
                    my.exprs,
                    my.arity))),
              (lambda :
                # progn
                (lambda :(
                  my.exprs.pop(
                    my.arity),
                  ())[-1])()),
              (lambda :
                # QzAT_
                (lambda *xs:[*xs])(
                  # ifQz_else
                  (lambda b,c,a:c()if b else a())(
                    # QzVERT_QzVERT_
                    (lambda x0,x1,x2,x3,x4,x5:x0 or x1()or x2()or x3()or x4()or x5())(
                      my.literalQzQUERY_(
                        my.obj),
                      (lambda :
                        suffix.startswith(
                          (','))),
                      (lambda :
                        __import__('hissp.reader',fromlist='?').is_lissp_string(
                          my.obj)),
                      (lambda :
                        my.controlQz_wordQzQUERY_(
                          my.obj)),
                      (lambda :
                        my.moduleQz_handleQzQUERY_(
                          my.obj)),
                      (lambda :
                        my.quotationQzQUERY_(
                          my.obj))),
                    (lambda :
                      # ifQz_else
                      (lambda b,c,a:c()if b else a())(
                        my.arity,
                        (lambda :
                          (lambda * _: _)(
                            'operator..getitem',
                            next(
                              my.iexprs),
                            my.obj)),
                        (lambda :my.obj))),
                    (lambda :
                      # ifQz_else
                      (lambda b,c,a:c()if b else a())(
                        # QzVERT_QzVERT_
                        (lambda x0,x1:x0 or x1())(
                          my.arity,
                          (lambda :
                            not(
                              my.methodQzQUERY_(
                                my.obj)))),
                        (lambda :
                          (lambda * _: _)(
                            my.obj,
                            *__import__('itertools').islice(
                               my.iexprs,
                               my.arityQzPLUS_1))),
                        (lambda :
                          (lambda * _: _)(
                            (lambda * _: _)(
                              'operator..attrgetter',
                              (lambda * _: _)(
                                'quote',
                                (lambda _QzJXZWCGIRz_G:(_QzJXZWCGIRz_G[1:]))(
                                  my.obj))),
                            next(
                              my.iexprs))))))))),
            {':': 0, '*': 1, '<': 2, '>': 3, '@': 4, '&': 5, '/': 6}.get(
              cmd,
              (-1)))():(
            __import__('builtins').setattr(
              my,
              'result',
              _QzWBHN72I2z_val),
            _QzWBHN72I2z_val)[-1])(),
          # setQzAT_
          # hissp.macros.._macro_.let
          (lambda _QzWBHN72I2z_val=_macro_._rewrite(
            program,
            *my.result,
            *my.iexprs):(
            __import__('builtins').setattr(
              my,
              'result',
              _QzWBHN72I2z_val),
            _QzWBHN72I2z_val)[-1])(),
          # when
          (lambda b,c:c()if b else())(
            my.G,
            (lambda :
              # setQzAT_
              # hissp.macros.._macro_.let
              (lambda _QzWBHN72I2z_val=(lambda * _: _)(
                'hissp.macros.._macro_.let',
                (lambda * _: _)(
                  my.G,
                  my.target),
                my.result):(
                __import__('builtins').setattr(
                  my,
                  'result',
                  _QzWBHN72I2z_val),
                _QzWBHN72I2z_val)[-1])())),
          my.result)[-1])(
          *program.pop()))()))):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       '_rewrite',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    '_rewrite',
    _QzX3UIMF7Uz_fn))[-1])()

# hissp.macros.._macro_.progn
(lambda :(
  # hissp.macros.._macro_.defmacro
  # hissp.macros.._macro_.let
  (lambda _QzX3UIMF7Uz_fn=(lambda terms:(
    ("``^#`` 'synexpand-1'.\n"
     '\n'
     'Creates a lambda of arity 1 containing a `^*#<QzHAT_QzSTAR_QzHASH_>`\n'
     '(synexpand) applied with terms to a tuple of the parameters.\n'),
    (lambda * _: _)(
      'lambda',
      ('_QzP6HAZXWIz_x',),
      (lambda * _: _)(
        'hissp.macros.._macro_.QzHAT_QzSTAR_QzHASH_',
        (lambda * _: _)(
          terms,
          *('_QzP6HAZXWIz_x',)))))[-1]):(
    __import__('builtins').setattr(
      _QzX3UIMF7Uz_fn,
      '__doc__',
      ("``^#`` 'synexpand-1'.\n"
       '\n'
       'Creates a lambda of arity 1 containing a `^*#<QzHAT_QzSTAR_QzHASH_>`\n'
       '(synexpand) applied with terms to a tuple of the parameters.\n')),
    __import__('builtins').setattr(
      _QzX3UIMF7Uz_fn,
      '__qualname__',
      ('.').join(
        ('_macro_',
         'QzHAT_QzHASH_',))),
    __import__('builtins').setattr(
      __import__('operator').getitem(
        __import__('builtins').globals(),
        '_macro_'),
      'QzHAT_QzHASH_',
      _QzX3UIMF7Uz_fn))[-1])(),
  # hissp.macros.._macro_.defmacro
  # hissp.macros.._macro_.let
  (lambda _QzX3UIMF7Uz_fn=(lambda terms:(
    ("``^^#`` 'synexpand-2'.\n"
     '\n'
     'Creates a lambda of arity 2 containing a `^*#<QzHAT_QzSTAR_QzHASH_>`\n'
     '(synexpand) applied with terms to a tuple of the parameters.\n'),
    (lambda * _: _)(
      'lambda',
      ('_QzP6HAZXWIz_x',
       '_QzP6HAZXWIz_y',),
      (lambda * _: _)(
        'hissp.macros.._macro_.QzHAT_QzSTAR_QzHASH_',
        (lambda * _: _)(
          terms,
          *('_QzP6HAZXWIz_x',
            '_QzP6HAZXWIz_y',)))))[-1]):(
    __import__('builtins').setattr(
      _QzX3UIMF7Uz_fn,
      '__doc__',
      ("``^^#`` 'synexpand-2'.\n"
       '\n'
       'Creates a lambda of arity 2 containing a `^*#<QzHAT_QzSTAR_QzHASH_>`\n'
       '(synexpand) applied with terms to a tuple of the parameters.\n')),
    __import__('builtins').setattr(
      _QzX3UIMF7Uz_fn,
      '__qualname__',
      ('.').join(
        ('_macro_',
         'QzHAT_QzHAT_QzHASH_',))),
    __import__('builtins').setattr(
      __import__('operator').getitem(
        __import__('builtins').globals(),
        '_macro_'),
      'QzHAT_QzHAT_QzHASH_',
      _QzX3UIMF7Uz_fn))[-1])(),
  # hissp.macros.._macro_.defmacro
  # hissp.macros.._macro_.let
  (lambda _QzX3UIMF7Uz_fn=(lambda terms:(
    ("``^^^#`` 'synexpand-3'.\n"
     '\n'
     'Creates a lambda of arity 3 containing a `^*#<QzHAT_QzSTAR_QzHASH_>`\n'
     '(synexpand) applied with terms to a tuple of the parameters.\n'),
    (lambda * _: _)(
      'lambda',
      ('_QzP6HAZXWIz_x',
       '_QzP6HAZXWIz_y',
       '_QzP6HAZXWIz_z',),
      (lambda * _: _)(
        'hissp.macros.._macro_.QzHAT_QzSTAR_QzHASH_',
        (lambda * _: _)(
          terms,
          *('_QzP6HAZXWIz_x',
            '_QzP6HAZXWIz_y',
            '_QzP6HAZXWIz_z',)))))[-1]):(
    __import__('builtins').setattr(
      _QzX3UIMF7Uz_fn,
      '__doc__',
      ("``^^^#`` 'synexpand-3'.\n"
       '\n'
       'Creates a lambda of arity 3 containing a `^*#<QzHAT_QzSTAR_QzHASH_>`\n'
       '(synexpand) applied with terms to a tuple of the parameters.\n')),
    __import__('builtins').setattr(
      _QzX3UIMF7Uz_fn,
      '__qualname__',
      ('.').join(
        ('_macro_',
         'QzHAT_QzHAT_QzHAT_QzHASH_',))),
    __import__('builtins').setattr(
      __import__('operator').getitem(
        __import__('builtins').globals(),
        '_macro_'),
      'QzHAT_QzHAT_QzHAT_QzHASH_',
      _QzX3UIMF7Uz_fn))[-1])(),
  # hissp.macros.._macro_.defmacro
  # hissp.macros.._macro_.let
  (lambda _QzX3UIMF7Uz_fn=(lambda terms:(
    ("``^^^^#`` 'synexpand-4'.\n"
     '\n'
     'Creates a lambda of arity 4 containing a `^*#<QzHAT_QzSTAR_QzHASH_>`\n'
     '(synexpand) applied with terms to a tuple of the parameters.\n'),
    (lambda * _: _)(
      'lambda',
      ('_QzP6HAZXWIz_x',
       '_QzP6HAZXWIz_y',
       '_QzP6HAZXWIz_z',
       '_QzP6HAZXWIz_w',),
      (lambda * _: _)(
        'hissp.macros.._macro_.QzHAT_QzSTAR_QzHASH_',
        (lambda * _: _)(
          terms,
          *('_QzP6HAZXWIz_x',
            '_QzP6HAZXWIz_y',
            '_QzP6HAZXWIz_z',
            '_QzP6HAZXWIz_w',)))))[-1]):(
    __import__('builtins').setattr(
      _QzX3UIMF7Uz_fn,
      '__doc__',
      ("``^^^^#`` 'synexpand-4'.\n"
       '\n'
       'Creates a lambda of arity 4 containing a `^*#<QzHAT_QzSTAR_QzHASH_>`\n'
       '(synexpand) applied with terms to a tuple of the parameters.\n')),
    __import__('builtins').setattr(
      _QzX3UIMF7Uz_fn,
      '__qualname__',
      ('.').join(
        ('_macro_',
         'QzHAT_QzHAT_QzHAT_QzHAT_QzHASH_',))),
    __import__('builtins').setattr(
      __import__('operator').getitem(
        __import__('builtins').globals(),
        '_macro_'),
      'QzHAT_QzHAT_QzHAT_QzHAT_QzHASH_',
      _QzX3UIMF7Uz_fn))[-1])())[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda expr,file:
  (lambda * _: _)(
    'hissp.macros.._macro_.let',
    (lambda * _: _)(
      '_QzBLLLPKT7z_e',
      expr),
    (lambda * _: _)(
      'builtins..print',
      (lambda * _: _)(
        'pprint..pformat',
        (lambda * _: _)(
          'quote',
          expr),
        ':',
        'hissp.macros..sort_dicts',
        (0)),
      "('=>')",
      (lambda * _: _)(
        'builtins..repr',
        '_QzBLLLPKT7z_e'),
      ':',
      'hissp.macros..file',
      file),
    '_QzBLLLPKT7z_e')):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       '_spy',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    '_spy',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda expr,file='sys..stderr':(
  ('``spy#`` Print e => its value to the file. Return the value.\n'
   '\n'
   '  Typically used to debug a Lissp expression.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> (op#add 5 spy#!sys..stdout(op#mul 7 3))\n'
   "     >>> __import__('operator').add(\n"
   '     ...   (5),\n'
   '     ...   # hissp.._macro_._spy\n'
   '     ...   # hissp.macros.._macro_.let\n'
   "     ...   (lambda _Qz764KZBP5z_e=__import__('operator').mul(\n"
   '     ...     (7),\n'
   '     ...     (3)):(\n'
   "     ...     __import__('builtins').print(\n"
   "     ...       __import__('pprint').pformat(\n"
   "     ...         ('operator..mul',\n"
   '     ...          (7),\n'
   '     ...          (3),),\n'
   '     ...         sort_dicts=(0)),\n'
   "     ...       ('=>'),\n"
   "     ...       __import__('builtins').repr(\n"
   '     ...         _Qz764KZBP5z_e),\n'
   "     ...       file=__import__('sys').stdout),\n"
   '     ...     _Qz764KZBP5z_e)[-1])())\n'
   "     ('operator..mul', 7, 3) => 21\n"
   '     26\n'
   '\n'
   '  See also: `print`, `doto`, `progn`.\n'
   '  '),
  (lambda * _: _)(
    'hissp.._macro_._spy',
    expr,
    file))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('``spy#`` Print e => its value to the file. Return the value.\n'
     '\n'
     '  Typically used to debug a Lissp expression.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> (op#add 5 spy#!sys..stdout(op#mul 7 3))\n'
     "     >>> __import__('operator').add(\n"
     '     ...   (5),\n'
     '     ...   # hissp.._macro_._spy\n'
     '     ...   # hissp.macros.._macro_.let\n'
     "     ...   (lambda _Qz764KZBP5z_e=__import__('operator').mul(\n"
     '     ...     (7),\n'
     '     ...     (3)):(\n'
     "     ...     __import__('builtins').print(\n"
     "     ...       __import__('pprint').pformat(\n"
     "     ...         ('operator..mul',\n"
     '     ...          (7),\n'
     '     ...          (3),),\n'
     '     ...         sort_dicts=(0)),\n'
     "     ...       ('=>'),\n"
     "     ...       __import__('builtins').repr(\n"
     '     ...         _Qz764KZBP5z_e),\n'
     "     ...       file=__import__('sys').stdout),\n"
     '     ...     _Qz764KZBP5z_e)[-1])())\n'
     "     ('operator..mul', 7, 3) => 21\n"
     '     26\n'
     '\n'
     '  See also: `print`, `doto`, `progn`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'spyQzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'spyQzHASH_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda expr,file='sys..stderr':(
  ('``time#`` Print ms elapsed running e to the file. Return its value.\n'
   '\n'
   '  Typically used when optimizing a Lissp expression.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> time#!sys..stdout(time..sleep .05)\n'
   '     >>> # hissp.macros.._macro_.let\n'
   "     ... (lambda _QzPMWTVFTZz_time=__import__('time').time_ns:\n"
   '     ...   # hissp.macros.._macro_.letQz_from\n'
   '     ...   (lambda _QzPMWTVFTZz_start,_QzPMWTVFTZz_val,_QzPMWTVFTZz_end:(\n'
   "     ...     __import__('builtins').print(\n"
   "     ...       ('time# ran'),\n"
   "     ...       __import__('pprint').pformat(\n"
   "     ...         ('time..sleep',\n"
   '     ...          (0.05),),\n'
   '     ...         sort_dicts=(0)),\n'
   "     ...       ('in'),\n"
   "     ...       __import__('operator').truediv(\n"
   "     ...         __import__('operator').sub(\n"
   '     ...           _QzPMWTVFTZz_end,\n'
   '     ...           _QzPMWTVFTZz_start),\n'
   "     ...         __import__('decimal').Decimal(\n"
   '     ...           (1000000.0))),\n'
   "     ...       ('ms'),\n"
   "     ...       file=__import__('sys').stdout),\n"
   '     ...     _QzPMWTVFTZz_val)[-1])(\n'
   '     ...     *# hissp.macros.._macro_.QzAT_\n'
   '     ...      (lambda *xs:[*xs])(\n'
   '     ...        _QzPMWTVFTZz_time(),\n'
   "     ...        __import__('time').sleep(\n"
   '     ...          (0.05)),\n'
   '     ...        _QzPMWTVFTZz_time())))()\n'
   "     time# ran ('time..sleep', 0.05) in ... ms\n"
   '\n'
   '  See also: `timeit`.\n'
   '  '),
  (lambda * _: _)(
    'hissp.macros.._macro_.let',
    (lambda * _: _)(
      '_QzQOPC6NNBz_time',
      'time..time_ns'),
    (lambda * _: _)(
      'hissp.macros.._macro_.letQz_from',
      (lambda * _: _)(
        '_QzQOPC6NNBz_start',
        '_QzQOPC6NNBz_val',
        '_QzQOPC6NNBz_end'),
      (lambda * _: _)(
        'hissp.macros.._macro_.QzAT_',
        (lambda * _: _)(
          '_QzQOPC6NNBz_time'),
        expr,
        (lambda * _: _)(
          '_QzQOPC6NNBz_time')),
      (lambda * _: _)(
        'builtins..print',
        "('time# ran')",
        (lambda * _: _)(
          'pprint..pformat',
          (lambda * _: _)(
            'quote',
            expr),
          ':',
          'hissp.macros..sort_dicts',
          (0)),
        "('in')",
        (lambda * _: _)(
          'operator..truediv',
          (lambda * _: _)(
            'operator..sub',
            '_QzQOPC6NNBz_end',
            '_QzQOPC6NNBz_start'),
          (lambda * _: _)(
            'decimal..Decimal',
            (1000000.0))),
        "('ms')",
        ':',
        'hissp.macros..file',
        file),
      '_QzQOPC6NNBz_val')))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('``time#`` Print ms elapsed running e to the file. Return its value.\n'
     '\n'
     '  Typically used when optimizing a Lissp expression.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> time#!sys..stdout(time..sleep .05)\n'
     '     >>> # hissp.macros.._macro_.let\n'
     "     ... (lambda _QzPMWTVFTZz_time=__import__('time').time_ns:\n"
     '     ...   # hissp.macros.._macro_.letQz_from\n'
     '     ...   (lambda _QzPMWTVFTZz_start,_QzPMWTVFTZz_val,_QzPMWTVFTZz_end:(\n'
     "     ...     __import__('builtins').print(\n"
     "     ...       ('time# ran'),\n"
     "     ...       __import__('pprint').pformat(\n"
     "     ...         ('time..sleep',\n"
     '     ...          (0.05),),\n'
     '     ...         sort_dicts=(0)),\n'
     "     ...       ('in'),\n"
     "     ...       __import__('operator').truediv(\n"
     "     ...         __import__('operator').sub(\n"
     '     ...           _QzPMWTVFTZz_end,\n'
     '     ...           _QzPMWTVFTZz_start),\n'
     "     ...         __import__('decimal').Decimal(\n"
     '     ...           (1000000.0))),\n'
     "     ...       ('ms'),\n"
     "     ...       file=__import__('sys').stdout),\n"
     '     ...     _QzPMWTVFTZz_val)[-1])(\n'
     '     ...     *# hissp.macros.._macro_.QzAT_\n'
     '     ...      (lambda *xs:[*xs])(\n'
     '     ...        _QzPMWTVFTZz_time(),\n'
     "     ...        __import__('time').sleep(\n"
     '     ...          (0.05)),\n'
     '     ...        _QzPMWTVFTZz_time())))()\n'
     "     time# ran ('time..sleep', 0.05) in ... ms\n"
     '\n'
     '  See also: `timeit`.\n'
     '  ')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'timeQzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'timeQzHASH_',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda e,predicate,*args:(
  ('Anaphoric. Raises `AssertionError` `unless` (-> e predicate).\n'
   '\n'
   'Additional arguments are evaluated in a context where ``it`` refers\n'
   'to the result of e. These (if any) are passed to the\n'
   '`AssertionError`. Evaluates to the result of e.\n'
   '\n'
   'Assertions document assumptions that should never be false; only\n'
   'raise `AssertionError`\\ s to fail fast when there is a bug in your\n'
   'code violating one, which can never happen if the code was written\n'
   'correctly. Though implemented as exceptions in Python, they should\n'
   'almost never be caught, except (perhaps) by a supervising system\n'
   '(such as a REPL) capable of dealing with broken subsystems. They\n'
   'are not to be used like normal exceptions to handle expected cases.\n'
   '\n'
   '.. code-block:: REPL\n'
   '\n'
   '   #> (avow 7 (X#.#"X%2 == 0")\n'
   '   #..  it "That\'s odd.")\n'
   '   >>> # avow\n'
   '   ... # hissp.macros.._macro_.let\n'
   '   ... (lambda it=(7):(\n'
   '   ...   # hissp.macros.._macro_.unless\n'
   '   ...   (lambda b,a:()if b else a())(\n'
   '   ...     # hissp.macros.._macro_.Qz_QzGT_\n'
   '   ...     (lambda X:X%2 == 0)(\n'
   '   ...       it),\n'
   '   ...     (lambda :\n'
   '   ...       # hissp.macros.._macro_.throw\n'
   '   ...       # hissp.macros.._macro_.throwQzSTAR_\n'
   "   ...       (lambda g:g.close()or g.throw)(c for c in'')(\n"
   "   ...         __import__('builtins').AssertionError(\n"
   '   ...           it,\n'
   '   ...           ("That\'s odd."))))),\n'
   '   ...   it)[-1])()\n'
   '   Traceback (most recent call last):\n'
   '     ...\n'
   '   AssertionError: (7, "That\'s odd.")\n'
   '\n'
   'See also: `assert`, `assure`, `throw`.\n'),
  (lambda * _: _)(
    'hissp.macros.._macro_.let',
    (lambda * _: _)(
      'it',
      e),
    (lambda * _: _)(
      'hissp.macros.._macro_.unless',
      (lambda * _: _)(
        'hissp.macros.._macro_.Qz_QzGT_',
        'it',
        predicate),
      (lambda * _: _)(
        'hissp.macros.._macro_.throw',
        (lambda * _: _)(
          'builtins..AssertionError',
          *args))),
    'it'))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('Anaphoric. Raises `AssertionError` `unless` (-> e predicate).\n'
     '\n'
     'Additional arguments are evaluated in a context where ``it`` refers\n'
     'to the result of e. These (if any) are passed to the\n'
     '`AssertionError`. Evaluates to the result of e.\n'
     '\n'
     'Assertions document assumptions that should never be false; only\n'
     'raise `AssertionError`\\ s to fail fast when there is a bug in your\n'
     'code violating one, which can never happen if the code was written\n'
     'correctly. Though implemented as exceptions in Python, they should\n'
     'almost never be caught, except (perhaps) by a supervising system\n'
     '(such as a REPL) capable of dealing with broken subsystems. They\n'
     'are not to be used like normal exceptions to handle expected cases.\n'
     '\n'
     '.. code-block:: REPL\n'
     '\n'
     '   #> (avow 7 (X#.#"X%2 == 0")\n'
     '   #..  it "That\'s odd.")\n'
     '   >>> # avow\n'
     '   ... # hissp.macros.._macro_.let\n'
     '   ... (lambda it=(7):(\n'
     '   ...   # hissp.macros.._macro_.unless\n'
     '   ...   (lambda b,a:()if b else a())(\n'
     '   ...     # hissp.macros.._macro_.Qz_QzGT_\n'
     '   ...     (lambda X:X%2 == 0)(\n'
     '   ...       it),\n'
     '   ...     (lambda :\n'
     '   ...       # hissp.macros.._macro_.throw\n'
     '   ...       # hissp.macros.._macro_.throwQzSTAR_\n'
     "   ...       (lambda g:g.close()or g.throw)(c for c in'')(\n"
     "   ...         __import__('builtins').AssertionError(\n"
     '   ...           it,\n'
     '   ...           ("That\'s odd."))))),\n'
     '   ...   it)[-1])()\n'
     '   Traceback (most recent call last):\n'
     '     ...\n'
     '   AssertionError: (7, "That\'s odd.")\n'
     '\n'
     'See also: `assert`, `assure`, `throw`.\n')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'avow',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'avow',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda e,predicate,*args:(
  ('Anaphoric. Raises `AssertionError` `unless` (-> e predicate).\n'
   '\n'
   'As `avow`, but expansion is simply ``e`` when `__debug__` is off:\n'
   '\n'
   '.. code-block:: console\n'
   '\n'
   '    $ python -Om hissp -c "(print (assure 0 bool))"\n'
   '    0\n'
   '\n'
   '    $ lissp -c "(print (assure 0 bool))"\n'
   '    Hissp abort!\n'
   '    Traceback (most recent call last):\n'
   '      ...\n'
   '    AssertionError\n'
   '\n'
   "Note that for pre-compiled code, it's the `__debug__` state at\n"
   'compile time, not at run time, that determines if assure\n'
   'assertions are turned on.\n'
   '\n'
   'For internal integrity checks, prefer `avow` to `assure`, unless\n'
   'profiling indicates the check is unacceptably expensive in\n'
   'production, and the risk of not checking is acceptable; assume\n'
   '`__debug__` will later be turned off.\n'
   '\n'
   'Also useful at the top level for quick unit tests in smaller\n'
   'projects, because they can be turned off. Larger projects may be\n'
   'better off with `unittest` and separated test modules, which need\n'
   'not be distributed and likely produce better error messages.\n'
   '\n'
   '.. code-block:: REPL\n'
   '\n'
   '   #> (assure 7 (X#.#"X%2 == 0")\n'
   '   #..  it "That\'s odd.")\n'
   '   >>> # assure\n'
   '   ... # hissp.macros.._macro_.avow\n'
   '   ... # hissp.macros.._macro_.let\n'
   '   ... (lambda it=(7):(\n'
   '   ...   # hissp.macros.._macro_.unless\n'
   '   ...   (lambda b,a:()if b else a())(\n'
   '   ...     # hissp.macros.._macro_.Qz_QzGT_\n'
   '   ...     (lambda X:X%2 == 0)(\n'
   '   ...       it),\n'
   '   ...     (lambda :\n'
   '   ...       # hissp.macros.._macro_.throw\n'
   '   ...       # hissp.macros.._macro_.throwQzSTAR_\n'
   "   ...       (lambda g:g.close()or g.throw)(c for c in'')(\n"
   "   ...         __import__('builtins').AssertionError(\n"
   '   ...           it,\n'
   '   ...           ("That\'s odd."))))),\n'
   '   ...   it)[-1])()\n'
   '   Traceback (most recent call last):\n'
   '     ...\n'
   '   AssertionError: (7, "That\'s odd.")\n'
   '\n'
   'See also: `assert`.\n'),
  # ifQz_else
  (lambda b,c,a:c()if b else a())(
    __debug__,
    (lambda :
      (lambda * _: _)(
        'hissp.macros.._macro_.avow',
        e,
        predicate,
        *args)),
    (lambda :e)))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('Anaphoric. Raises `AssertionError` `unless` (-> e predicate).\n'
     '\n'
     'As `avow`, but expansion is simply ``e`` when `__debug__` is off:\n'
     '\n'
     '.. code-block:: console\n'
     '\n'
     '    $ python -Om hissp -c "(print (assure 0 bool))"\n'
     '    0\n'
     '\n'
     '    $ lissp -c "(print (assure 0 bool))"\n'
     '    Hissp abort!\n'
     '    Traceback (most recent call last):\n'
     '      ...\n'
     '    AssertionError\n'
     '\n'
     "Note that for pre-compiled code, it's the `__debug__` state at\n"
     'compile time, not at run time, that determines if assure\n'
     'assertions are turned on.\n'
     '\n'
     'For internal integrity checks, prefer `avow` to `assure`, unless\n'
     'profiling indicates the check is unacceptably expensive in\n'
     'production, and the risk of not checking is acceptable; assume\n'
     '`__debug__` will later be turned off.\n'
     '\n'
     'Also useful at the top level for quick unit tests in smaller\n'
     'projects, because they can be turned off. Larger projects may be\n'
     'better off with `unittest` and separated test modules, which need\n'
     'not be distributed and likely produce better error messages.\n'
     '\n'
     '.. code-block:: REPL\n'
     '\n'
     '   #> (assure 7 (X#.#"X%2 == 0")\n'
     '   #..  it "That\'s odd.")\n'
     '   >>> # assure\n'
     '   ... # hissp.macros.._macro_.avow\n'
     '   ... # hissp.macros.._macro_.let\n'
     '   ... (lambda it=(7):(\n'
     '   ...   # hissp.macros.._macro_.unless\n'
     '   ...   (lambda b,a:()if b else a())(\n'
     '   ...     # hissp.macros.._macro_.Qz_QzGT_\n'
     '   ...     (lambda X:X%2 == 0)(\n'
     '   ...       it),\n'
     '   ...     (lambda :\n'
     '   ...       # hissp.macros.._macro_.throw\n'
     '   ...       # hissp.macros.._macro_.throwQzSTAR_\n'
     "   ...       (lambda g:g.close()or g.throw)(c for c in'')(\n"
     "   ...         __import__('builtins').AssertionError(\n"
     '   ...           it,\n'
     '   ...           ("That\'s odd."))))),\n'
     '   ...   it)[-1])()\n'
     '   Traceback (most recent call last):\n'
     '     ...\n'
     '   AssertionError: (7, "That\'s odd.")\n'
     '\n'
     'See also: `assert`.\n')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'assure',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'assure',
    _QzX3UIMF7Uz_fn))[-1])()