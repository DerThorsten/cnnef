#pragma once
#ifndef CNNEF_MARRAY_MARRAY_HXX
#define CNNEF_MARRAY_MARRAY_HXX

#define HAVE_CPP11_INITIALIZER_LISTS
#define HAVE_CPP11_STD_ARRAY
#include <andres/marray.hxx>

namespace cnnef{
namespace marray{
    using namespace andres;
}

namespace tools{

    template<class T, class COORD>
    inline void readSubarray(
        const marray::View<T> array,
        const COORD & beginCoord,
        const COORD & endCoord,
        marray::View<T> & subarray
    ){

        const auto dim = array.dimension();
        std::vector<int64_t> subShape(array.dimension());
        for(auto d = 0 ; d<dim; ++d){
            subShape[d] = beginCoord[d] - endCoord[d];
        }
        subarray = array.view(beginCoord.begin(), subShape.begin());
    }
}

}

#endif
