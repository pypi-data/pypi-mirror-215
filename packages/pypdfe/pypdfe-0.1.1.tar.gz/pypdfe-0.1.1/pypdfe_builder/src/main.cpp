#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "PDF-Estimator/mvPDFMain.cpp"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

void get_pdf(py::array_t<double, py::array::f_style | py::array::forcecast> distribution, int return_size,
        int debug, py::array_t<double, py::array::f_style> x, py::array_t<double, py::array::f_style> pdf) {

    // access the numpy arrays in place
    py::buffer_info distribution_info = distribution.request();
    double* distribution_p = static_cast<double*>(distribution_info.ptr);
    py::buffer_info x_info = x.request();
    double* x_p = static_cast<double*>(x_info.ptr);
    py::buffer_info pdf_info = pdf.request();
    double* pdf_p = static_cast<double*>(pdf_info.ptr);

    int nPts = distribution_info.shape[0];
    int nDims = distribution_info.shape[1];

    estimatePDFmv(distribution_p, &nPts, &nDims, &return_size, &debug, x_p, pdf_p);
}

PYBIND11_MODULE(_core, m) {
    m.doc() = R"pbdoc(
        Dr. Jennfier Farmer's PDF-Estimator in python
        ---------------------------------------------

        .. currentmodule:: pypdfe

        .. autosummary::
           :toctree: _generate

           getpdf

        usage::
            [put usage info here]
    )pbdoc";

    m.def("get_pdf", &get_pdf);

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
