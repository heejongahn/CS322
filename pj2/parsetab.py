
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = '\xe0\x84\xee\x95\xc3\xde\xf0\xa9&\x0eN\xab\xf7\xa3}\x13'
    
_lr_action_items = {'DAGGER':([2,4,5,6,8,9,10,11,],[-8,6,6,-5,-6,6,-7,6,]),'UNION':([2,4,5,6,8,9,10,11,],[-8,7,7,-5,-6,7,-7,-4,]),'SYMBOL':([0,2,3,4,5,6,7,8,9,10,11,],[2,-8,2,2,2,-5,2,-6,2,-7,-4,]),'ASTERISK':([2,4,5,6,8,9,10,11,],[-8,8,8,-5,-6,8,-7,8,]),'LPAREN':([0,2,3,4,5,6,7,8,9,10,11,],[3,-8,3,3,3,-5,3,-6,3,-7,-4,]),'RPAREN':([2,5,6,8,9,10,11,],[-8,10,-5,-6,-3,-7,-4,]),'$end':([0,1,2,4,6,8,9,10,11,],[-2,0,-8,-1,-5,-6,-3,-7,-4,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,3,4,5,7,9,11,],[4,5,9,9,11,9,9,]),'statement':([0,],[1,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> expression','statement',1,'p_statement_expr','C:/Users/Nobell_User/PycharmProjects/automata2/automata2.py',40),
  ('statement -> <empty>','statement',0,'p_statement_none','C:/Users/Nobell_User/PycharmProjects/automata2/automata2.py',44),
  ('expression -> expression expression','expression',2,'p_expression_ampersand','C:/Users/Nobell_User/PycharmProjects/automata2/automata2.py',48),
  ('expression -> expression UNION expression','expression',3,'p_expression_union','C:/Users/Nobell_User/PycharmProjects/automata2/automata2.py',52),
  ('expression -> expression DAGGER','expression',2,'p_expression_dagger','C:/Users/Nobell_User/PycharmProjects/automata2/automata2.py',56),
  ('expression -> expression ASTERISK','expression',2,'p_expression_asterisk','C:/Users/Nobell_User/PycharmProjects/automata2/automata2.py',60),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','C:/Users/Nobell_User/PycharmProjects/automata2/automata2.py',64),
  ('expression -> SYMBOL','expression',1,'p_expression_symbol','C:/Users/Nobell_User/PycharmProjects/automata2/automata2.py',68),
]
