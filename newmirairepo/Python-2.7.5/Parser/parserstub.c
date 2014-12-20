#include "Python.h"

PyAPI_FUNC(int) PyParser_ParseStringFlagsFilenameEx(int a, int b, int c, int d, int e, int f)
{
	return 0;
}

#define PSUDOFUNC(x) PyAPI_FUNC(int) x(int a) {return 0;}

PSUDOFUNC(PyParser_ParseFileFlagsEx)
PSUDOFUNC(PyParser_ParseFileFlags)
PSUDOFUNC(PyParser_ParseStringFlags)
PSUDOFUNC(PyParser_ParseStringFlagsFilename)

PyAPI_DATA(int) Py_TabcheckFlag = 0;

PSUDOFUNC(PyGrammar_FindDFA)