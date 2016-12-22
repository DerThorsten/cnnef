#define BOOST_TEST_MODULE cnnefTestMarray

#include <boost/test/unit_test.hpp>

#include <iostream> 

#include "cnnef/tools/runtime_check.hxx"
#include "cnnef/marray/marray.hxx"


BOOST_AUTO_TEST_CASE(StridesTest)
{
    std::vector<size_t> shape({10,20});
    cnnef::marray::Marray<int> a(shape.begin(), shape.end());
    CNNEF_TEST_OP(a.strides(1),==,1);
    CNNEF_TEST_OP(a.strides(0),==,20);
}

