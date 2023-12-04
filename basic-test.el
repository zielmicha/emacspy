(defun basic-test () ""
       (add-to-list 'load-path ".")
       (load "emacspy")
       (princ "After emacspy")
       (eval-python "print('Hello world')")
       (princ "After eval-python"))
(basic-test)
