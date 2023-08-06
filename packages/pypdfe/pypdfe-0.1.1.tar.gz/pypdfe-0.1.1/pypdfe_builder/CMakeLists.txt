cmake_minimum_required(VERSION 3.15...3.26)

project(
  ${SKBUILD_PROJECT_NAME}
  VERSION ${SKBUILD_PROJECT_VERSION}
  LANGUAGES CXX)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 CONFIG REQUIRED)

set(SOURCES
    src/main.cpp
    src/PDF-Estimator/callPDF.cpp
    src/PDF-Estimator/callPDF.h
    src/PDF-Estimator/ChebyShev.cpp
    src/PDF-Estimator/ChebyShev.h
    src/PDF-Estimator/InputData.cpp
    src/PDF-Estimator/InputData.h
    src/PDF-Estimator/InputParameters.cpp
    src/PDF-Estimator/InputParameters.h
    src/PDF-Estimator/JointProbability.cpp
    src/PDF-Estimator/JointProbability.h
    src/PDF-Estimator/MinimizeScore.cpp
    src/PDF-Estimator/MinimizeScore.h
    src/PDF-Estimator/OutputControl.cpp
    src/PDF-Estimator/OutputControl.h
    src/PDF-Estimator/Score.cpp
    src/PDF-Estimator/Score.h
    src/PDF-Estimator/ScoreQZ.cpp
    src/PDF-Estimator/ScoreQZ.h
    src/PDF-Estimator/Variable.cpp
    src/PDF-Estimator/Variable.h
    src/PDF-Estimator/WriteResults.cpp
    src/PDF-Estimator/WriteResults.h
    )

python_add_library(_core MODULE ${SOURCES} WITH_SOABI)

target_link_libraries(_core PRIVATE pybind11::headers)
target_compile_definitions(_core PRIVATE VERSION_INFO=${PROJECT_VERSION})

message("=============================================================================================================")
message("SKBUILD_PROJECT_NAME: ${SKBUILD_PROJECT_NAME}")
message("=============================================================================================================")

install(TARGETS _core DESTINATION ${SKBUILD_PROJECT_NAME})
