/*
 * Fast Media Cleaner - C Extension for Python
 * High-performance operations for fingerprint removal
 */

#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Fast byte pattern removal
static PyObject* remove_byte_patterns(PyObject* self, PyObject* args) {
    const char* data;
    Py_ssize_t data_len;
    PyObject* patterns_list;
    
    if (!PyArg_ParseTuple(args, "y#O", &data, &data_len, &patterns_list)) {
        return NULL;
    }
    
    // Convert patterns list to C array
    Py_ssize_t num_patterns = PyList_Size(patterns_list);
    char** patterns = malloc(num_patterns * sizeof(char*));
    int* pattern_lens = malloc(num_patterns * sizeof(int));
    
    for (Py_ssize_t i = 0; i < num_patterns; i++) {
        PyObject* pattern = PyList_GetItem(patterns_list, i);
        patterns[i] = (char*)PyBytes_AsString(pattern);
        pattern_lens[i] = PyBytes_Size(pattern);
    }
    
    // Create output buffer
    char* output = malloc(data_len);
    Py_ssize_t output_len = 0;
    
    // Process data
    for (Py_ssize_t i = 0; i < data_len; i++) {
        int skip = 0;
        
        // Check for patterns
        for (Py_ssize_t p = 0; p < num_patterns; p++) {
            if (i + pattern_lens[p] <= data_len && 
                memcmp(data + i, patterns[p], pattern_lens[p]) == 0) {
                i += pattern_lens[p] - 1; // Skip pattern
                skip = 1;
                break;
            }
        }
        
        if (!skip) {
            output[output_len++] = data[i];
        }
    }
    
    PyObject* result = PyBytes_FromStringAndSize(output, output_len);
    
    free(patterns);
    free(pattern_lens);
    free(output);
    
    return result;
}

// Fast pixel noise addition
static PyObject* add_pixel_noise(PyObject* self, PyObject* args) {
    const char* image_data;
    Py_ssize_t data_len;
    double intensity;
    
    if (!PyArg_ParseTuple(args, "y#d", &image_data, &data_len, &intensity)) {
        return NULL;
    }
    
    char* output = malloc(data_len);
    srand(time(NULL));
    
    for (Py_ssize_t i = 0; i < data_len; i++) {
        int noise = (rand() % 256 - 128) * intensity;
        int new_val = (unsigned char)image_data[i] + noise;
        
        // Clamp to valid range
        if (new_val < 0) new_val = 0;
        if (new_val > 255) new_val = 255;
        
        output[i] = (char)new_val;
    }
    
    PyObject* result = PyBytes_FromStringAndSize(output, data_len);
    free(output);
    
    return result;
}

// Fast entropy calculation
static PyObject* calculate_entropy(PyObject* self, PyObject* args) {
    const char* data;
    Py_ssize_t data_len;
    
    if (!PyArg_ParseTuple(args, "y#", &data, &data_len)) {
        return NULL;
    }
    
    int frequency[256] = {0};
    
    // Count byte frequencies
    for (Py_ssize_t i = 0; i < data_len; i++) {
        frequency[(unsigned char)data[i]]++;
    }
    
    // Calculate entropy
    double entropy = 0.0;
    for (int i = 0; i < 256; i++) {
        if (frequency[i] > 0) {
            double probability = (double)frequency[i] / data_len;
            entropy -= probability * log2(probability);
        }
    }
    
    return PyFloat_FromDouble(entropy);
}

// Method definitions
static PyMethodDef FastCleanerMethods[] = {
    {"remove_byte_patterns", remove_byte_patterns, METH_VARARGS, "Remove byte patterns from data"},
    {"add_pixel_noise", add_pixel_noise, METH_VARARGS, "Add noise to image data"},
    {"calculate_entropy", calculate_entropy, METH_VARARGS, "Calculate data entropy"},
    {NULL, NULL, 0, NULL}
};

// Module definition
static struct PyModuleDef fastcleanermodule = {
    PyModuleDef_HEAD_INIT,
    "fast_cleaner",
    "Fast C operations for media cleaning",
    -1,
    FastCleanerMethods
};

// Module initialization
PyMODINIT_FUNC PyInit_fast_cleaner(void) {
    return PyModule_Create(&fastcleanermodule);
}