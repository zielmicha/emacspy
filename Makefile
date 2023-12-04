OS_NAME := $(shell uname)

ifeq ($(OS_NAME), Linux)
all: emacspy.so
else
ifeq ($(OS_NAME), Darwin)
all: emacspy.dylib
endif
endif
emacspy.c: emacspy.pyx
	cython -3 emacspy.pyx

ifeq ($(OS_NAME), Linux)
emacspy.so: emacspy.c stub.c
	gcc -fPIC -g -DCYTHON_FAST_THREAD_STATE=0 -DCYTHON_PEP489_MULTI_PHASE_INIT=0 emacspy.c stub.c -o emacspy.so -Wl,--no-undefined -shared \
	$(shell python3-config --cflags --libs --embed)
else
ifeq ($(OS_NAME), Darwin)
emacspy.dylib: emacspy.c stub.c
	gcc -fPIC -g -DCYTHON_FAST_THREAD_STATE=0 -DCYTHON_PEP489_MULTI_PHASE_INIT=0 emacspy.c stub.c -o emacspy.dylib -shared \
	$(shell python3-config --cflags --ldflags --libs --embed)
else
	echo "Unsupported platform $(OS_NAME)"
endif
endif

test:
	emacs --script basic-test.el
clean:
	rm -rf emacspy.so emacspy.dylib emacspy.dylib.dSYM
