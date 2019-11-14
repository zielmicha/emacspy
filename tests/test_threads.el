(add-to-list 'load-path "~/emacspy")
(load "~/emacspy/emacspy")
(exec-python "import sys, os; sys.path+=[os.path.expanduser('~/emacspy'), os.path.expanduser('~/emacspy/tests')]")
(exec-python "import test_threads")
