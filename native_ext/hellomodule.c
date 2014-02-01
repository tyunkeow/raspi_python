#include <Python.h>
#include <numpy/arrayobject.h>
#include <stdio.h>

static PyObject* compute_distance(PyObject* self, PyObject* args)
{

    PyObject *map_obj;

    int x0, y0, x1, y1;
    int max_x = 1000, max_y = 1000;
    int dx, dy, sx, sy, err, e2;

    if (!PyArg_ParseTuple(args, "iiiiO", &x0, &y0, &x1, &y1, &map_obj)) //
        return NULL;

    PyObject *map_array = PyArray_FROM_OTF(map_obj, NPY_LONG, NPY_IN_ARRAY);

    /* If that didn't work, throw an exception. */
    if (map_array == NULL) {
        Py_XDECREF(map_array);
        return NULL;
    }

    //printf("Dimensionen=%d\n", PyArray_NDIM(map_array));

    max_x = 1000; //(int)PyArray_DIM(map_array, 0);
    max_y= 800; //(int)PyArray_DIM(map_array, 1);

    dx = abs(x1-x0);
    dy = -abs(y1-y0);
    if (x0 < x1)
        sx = 1;
    else
        sx = -1;

    if (y0 < y1)
        sy = 1;
    else
        sy = -1;
    err = dx+dy;

    for(;;) {
        if (x0 < 0 || x0 >= max_x || y0 < 0 || y0 >= max_y)
            break;
        //printf("%d %d", x0, y0);
        long val = (long) PyArray_GETPTR2 (map_array, x0, y0);
        if (val == 1) {
            // 1 means "wall" => collision found
            break;
        }

        // Normal Bresenham Alg stops at target x1, y1
        // We want to proceed until a wall is hit => skip test
        //if (x0 == x1 && y0 == y1)
        //    break;

        e2 = 2*err;

        if (e2 > dy) {
            err += dy;
            x0 += sx;
        }

//        if (x0 == x1 && y0 == y1) {
//            break;
//        }

        if (e2 < dx) {
            err += dx;
            y0 += sy;
        }
    };

    //dist = sqrt((x2-self.x)**2 + (y2-self.y)**2)

    // clean up refcount
    Py_DECREF(map_array);
    PyObject *ret = Py_BuildValue("ii", x0, y0);
    return ret;
    //Py_RETURN_NONE;
}

static PyMethodDef HelloMethods[] =
{
     {"compute_distance", compute_distance, METH_VARARGS, "Greet somebody."},
     {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC inithello(void)
{
     PyObject *result = Py_InitModule("hello", HelloMethods);
     if (result == NULL)
        return;

     /* Load `numpy` functionality. */
    import_array();
}