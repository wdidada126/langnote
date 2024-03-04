cget

https://cget.readthedocs.io/en/latest/

pip3 install --user cget

cget install pfultz2/cget-recipes

-- Installing: /home/wdidada/cget/cget/pkg/pfultz2__cget-recipes/install/etc/cget/recipes//amanieu
-- Installing: /home/wdidada/cget/cget/pkg/pfultz2__cget-recipes/install/etc/cget/recipes//amanieu/asyncplusplus
-- Installing: /home/wdidada/cget/cget/pkg/pfultz2__cget-recipes/install/etc/cget/recipes//amanieu/asyncplusplus/package.txt
-- Installing: /home/wdidada/cget/cget/pkg/pfultz2__cget-recipes/install/share//cmake
-- Installing: /home/wdidada/cget/cget/pkg/pfultz2__cget-recipes/install/share//cmake/cget-recipe-utils-config.cmake
Successfully installed pfultz2/cget-recipes



Integration with cmake
By default, cget creates a cmake toolchain file with the settings necessary to build and find the libraries in the cget prefix. The toolchain file is at $CGET_PREFIX/cget.cmake. If another toolchain needs to be used, it can be specified with the init command:

cget init --toolchain my_cmake_toolchain.cmake
Also, the C++ version can be set for the toolchain as well:

cget init --std=c++14
Which is necessary to use modern C++ on many compilers.
