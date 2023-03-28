import os
import re
import inspect

from cudatext import *
#from cudax_lib import get_translation

#_   = get_translation(__file__)  # I18N

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'plugins.ini')
SECTION = 'console_complete'

VK_SPACE = 0x20

prefix = 'id'
replace_right_part = True
add_func_params = True

def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'

class Command:
  def __init__(self):
    self.load_cfg()

    hcons = app_proc(PROC_GET_CONSOLE_FORM, '')

    h_in = dlg_proc(hcons, DLG_CTL_HANDLE, name='input')
    self.ed_in = Editor(h_in)


  def load_cfg(self):
    global prefix
    global replace_right_part
    global add_func_params

    prefix = ini_read(fn_config, SECTION, 'prefix', prefix)
    replace_right_part = str_to_bool(
          ini_read(fn_config, SECTION, 'replace_right_part', bool_to_str(replace_right_part)))
    add_func_params = str_to_bool(
          ini_read(fn_config, SECTION, 'add_func_params', bool_to_str(add_func_params)))

  def config(self):
    global prefix
    global replace_right_part
    global add_func_params

    ini_write(fn_config, SECTION, 'prefix', value=prefix)
    ini_write(fn_config, SECTION, 'replace_right_part', value=bool_to_str(replace_right_part))
    ini_write(fn_config, SECTION, 'add_func_params', value=bool_to_str(add_func_params))
    file_open(fn_config)

  def on_save(self, ed_self):
    if ed_self.get_filename() == fn_config:
      self.load_cfg()

  def on_console_complete(self, ed_self):
    self.complete()
    return True

  def complete(self, *args, **vargs):
      if self.ed_in.get_prop(PROP_FOCUSED):
        edt = self.ed_in
      elif ed.get_prop(PROP_FOCUSED)  and  ed.get_prop(PROP_LEXER_CARET) == 'Python':
        edt = ed
      else:
        return

      # get Console variables
      if Parcel._globals == None:
        app_proc(PROC_EXEC_PYTHON, 'from cudatext import *; from cuda_console_complete.cns_complete import Parcel; '+
              'Parcel._globals = globals(); del Parcel;')

      caretx, carety, _x2, _y2 = edt.get_carets()[0]
      comp = None
      replace_r = 0
      text_start = edt.get_text_line(carety)

      textr = text_start[:caretx][::-1] # text before caret reversed (for regex)

      m = re.search('^([a-zA-Z0-9_.]+)([\'"])?', textr)
      if m:
        grs = m.groups()
        if grs[1] != None: # have a "
          text = ''
        else:
          text = grs[0][::-1]

        right_text = text_start[caretx:]
        m = re.search('^([a-zA-Z0-9_.]+)([\'"])?', right_text)
        if m:
          grs = m.groups()
          if grs[1] != None: # have a "
            text = ''
          elif replace_right_part:
            replace_r = len(grs[0])

      else: # no match
        text = ''

      # method, field
      if '.' in text:
          spl = text.split('.')

          replace_l = len(spl[-1])

          # search for target object
          var = None
          for fname in spl[:-1]:
            if var is None:
              var = Parcel._globals.get(fname)
            else:
              var = getattr(var, fname, None)

            if var is None:
              break

          if var != None:
            comp = self._get_comp(obj=var, pre=spl[-1])

      # var
      elif text:
          replace_l = len(text)
          comp = self._get_comp(obj=None, pre=text)

      if comp:
        comp.sort()

        edt.complete('\n'.join(comp), replace_l, replace_r)


  def _get_comp(self, obj, pre):
    dir_res = dir(obj)  if obj != None else  Parcel._globals

    comp = []
    for name in dir_res:
        if not name.startswith(pre)   or name.startswith('__'):
          continue

        if obj != None:
          f = getattr(obj, name)
        else:
          f = Parcel._globals.get(name)

        if not add_func_params  or not callable(f):
          comp.append(prefix +'|'+ name)

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
                  sargs.append(spec.args[i])
                else:
                  sargs.append(spec.args[i] +'='+ spec.defaults[i-noargs].__repr__())

              comp.append('{0}|{1}|({2})'.format(prefix, name, ", ".join(sargs)))
          else:
              comp.append(prefix +'|'+ name)

    return comp

class Parcel:
  _globals = None
