import os
import re
import inspect

from cudatext import *
#from cudax_lib import get_translation
from cudatext_keys import VK_SPACE

#_   = get_translation(__file__)  # I18N

class Command:
  
  def __init__(self):
    self._globals = None
    
  def on_start(self, ed_self):
    hcons = app_proc(PROC_GET_CONSOLE_FORM, '')
    
    h_in = dlg_proc(hcons, DLG_CTL_HANDLE, name='input')
    self.ed_in = Editor(h_in)
     
    dlg_proc(hcons, DLG_PROP_SET, prop={ 
        'keypreview': True, # Should be True if form needs to handle on_key_down.
        'on_key_down': self.on_cns_key,
        })
      
    return

  def on_cns_key(self, id_dlg, key_code, data='', info=''):
    state = data
    if key_code == VK_SPACE  and state == 'c':
      self.complete()
        
  def complete(self, *args, **vargs):
      # get Console locals()
      if Parcel._locals == None:
        app_proc(PROC_EXEC_PYTHON, 'from cuda_console_complete.cns_complete import Parcel; '+
              'Parcel._locals = locals()')

      comp = None
      text = self.ed_in.get_text_all().strip()

      caretx = self.ed_in.get_carets()[0][0]
      textr = text[:caretx][::-1] # text before caret reversed (for regex)
      
      m = re.search('^[a-zA-Z0-9_.]+', textr)
      if m:
        text = m[0][::-1]
      else:
        text = ''
      
      # method, field
      if '.' in text: 
          spl = text.split('.')
          
          if len(spl) == 2:
            replace_l = len(spl[1])
            
            # search for target object
            var = Parcel._locals.get(spl[0])
            if var == None: # not in locals, search globals
              var = self._get_globals().get(spl[0])
            
            if var != None:
              comp = self._get_comp(obj=var, pre=spl[1])
      # var
      elif text: 
          replace_l = len(text)
          comp = self._get_comp(obj=None, pre=text)
          
      if comp:
        comp.sort()
        
        self.ed_in.complete('\n'.join(comp), replace_l, 0)
          
      
  def _get_comp(self, obj, pre):
    dir_res = dir(obj)  if obj != None else  set((*Parcel._locals, *self._get_globals()))
        
    comp = []
    for name in dir_res:
        if not name.startswith(pre)   or name.startswith('__'):
          continue
          
        if obj != None:
          f = getattr(obj, name)  
        else:
          f = Parcel._locals.get(name, self._get_globals().get(name))
            
        if not callable(f):
          comp.append(f'{name}|{name}')
            
        else:
          
          try:
            # ArgSpec( args=['id_menu', 'id_action', 'command', 'caption', 'index', 'hotkey', 'tag'], 
            #          varargs=None, keywords=None, 
            #          defaults=('', '', -1, '', ''))
            spec = inspect.getfullargspec(f)
          except TypeError:
            spec = None
            
          if spec:
              sargs = []
              arglen = len(spec.args) if spec.args else 0
              deflen = len(spec.defaults) if spec.defaults else 0
              noargs = arglen-deflen
              for i in range(arglen):
                if i == 0 and spec.args[i] == 'self':
                  continue
                  
                if i < noargs:
                  sargs.append(f'{spec.args[i]}')
                else:
                  sargs.append(f'{spec.args[i]}={spec.defaults[i-noargs].__repr__()}')
              
              comp.append(f'{name}|{name}|({", ".join(sargs)})')
              worked = True
          else:
              comp.append(f'{name}|{name}()')
          
    self._globals = None
    return comp
    
  def _get_globals(self):
    if self._globals == None:
      self._globals = globals()
    return self._globals
      
class Parcel:
  _locals = None
    