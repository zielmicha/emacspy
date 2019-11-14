all: emacspy.so

emacspy.c: emacspy.pyx
	cython -3 emacspy.pyx

emacspy.so: emacspy.c stub.c
	gcc -fPIC -g -DCYTHON_FAST_THREAD_STATE=0 -I$HOME/apps/emacs-26.3/src emacspy.c stub.c -o emacspy.so -shared $(shell pkg-config --cflags --libs python3)
