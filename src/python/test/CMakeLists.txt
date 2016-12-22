
include(PythonLibTest)

if(NOSETESTS_PATH)

    file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/python_test)


    add_custom_target(python-test)

    add_python_test_target(python-test-a
        test_python.py
    )


    add_dependencies(python-test python-test-a)



endif()
