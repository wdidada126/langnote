# opencv
https://opencv.org/

c语言，很容易转为汇编语言，拿着反汇编代码看，哪些汇编代码对应哪些c代码，我是很容易看出来的。
用c语言编写的代码，你非常清楚现在操作系统在干什么事情，线程在如何进行切换。
golang最早的编译器，首先就是将golang先转换成c代码，再转成汇编。

c++ linker
换mold，作者说编译chrome也就比gnu ld快了20多倍吧

分布式编译很快，有时候我还想故意让它慢一点呢，太快了没有用c++的仪式感了

哎，C++现在变巨坑了。标准接近年更，10年前我还敢说自己精通C++，现在我只能说大概还懂个皮毛。0x草案是C++最佳状态，叠加11里线程及衍生特性是很好的补完。但是auto、constexpr、lambda之类的出现让我只想吐槽这是什么玩意儿，连deprecated都写进标准我能粗口么。现在C++委员会应该集体跳槽去做个全新的C艹艹。C++应该专注于性能类的改进，而不是解决易用性和兼容并包的问题，那些是胶水的事。

auto和lambda属于pl的很正统的语法家族，哪个现代化语言没有？你吐槽这个说明你确实该退休了

https://www.shenlanxueyuan.com/channel/UXyGQTGDt7/detail

cuda

图形学这个本科学校也不开什么比较好的课程，要是硕士考这方向算法也是进去搬砖（还不如隔壁组做视觉的）数字媒体技术这个专业说实话还是很贴这一块的，但是就现在而言整个行业上下和学校上下都没打通，都在蒙头自干自的。

## 编译

### windows
可以直接下载dll文件

### ubuntu
Build core modules

https://docs.opencv.org/4.9.0/d7/d9f/tutorial_linux_install.html

# Install minimal prerequisites (Ubuntu 18.04 as reference)
sudo apt update && sudo apt install -y cmake g++ wget unzip
# Download and unpack sources
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.x.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.x.zip
unzip opencv.zip
unzip opencv_contrib.zip
# Create build directory and switch into it
mkdir -p build && cd build
# Configure
cmake -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib-4.x/modules ../opencv-4.x
# Build
cmake --build .


make: *** [Makefile:74: install] Error 1
@edidada ➜ /workspaces/github_codespaces_compile/build (main) $ sudo cmake --build . --target install
[  0%] Built target opencv_dnn_plugins
[  0%] Built target opencv_highgui_plugins
[  0%] Built target jsimd
[  1%] Built target libopenjp2
[  1%] Built target opencv_videoio_plugins
[  1%] Built target ittnotify
[  2%] Built target ippiw
[  6%] Built target opencv_core
[ 10%] Built target opencv_imgproc
[ 12%] Built target libjpeg-turbo
[ 14%] Built target libtiff
[ 19%] Built target libwebp
[ 23%] Built target IlmImf
[ 24%] Built target opencv_imgcodecs
[ 25%] Built target opencv_videoio
[ 26%] Built target opencv_highgui
[ 26%] Built target opencv_ts
[ 27%] Built target opencv_perf_core
[ 29%] Built target opencv_test_core
[ 29%] Built target opencv_flann
[ 29%] Built target opencv_test_flann
[ 30%] Built target opencv_perf_imgproc
[ 32%] Built target opencv_test_imgproc
[ 32%] Built target opencv_intensity_transform
[ 32%] Built target opencv_test_intensity_transform
[ 32%] Built target opencv_ml
[ 32%] Built target opencv_test_ml
[ 32%] Built target opencv_phase_unwrapping
[ 32%] Built target opencv_test_phase_unwrapping
[ 32%] Built target opencv_photo
[ 32%] Built target opencv_perf_photo
[ 33%] Built target opencv_test_photo
[ 33%] Built target opencv_plot
[ 34%] Built target opencv_quality
[ 34%] Built target opencv_test_quality
[ 34%] Built target opencv_reg
[ 34%] Built target opencv_perf_reg
[ 34%] Built target opencv_test_reg
[ 34%] Built target opencv_signal
[ 34%] Built target opencv_perf_signal
[ 34%] Built target opencv_test_signal
[ 34%] Built target opencv_surface_matching
[ 35%] Built target opencv_xphoto
[ 36%] Built target opencv_perf_xphoto
[ 37%] Built target opencv_test_xphoto
[ 39%] Built target libprotobuf
[ 46%] Built target opencv_dnn
[ 46%] Built target opencv_perf_dnn
[ 46%] Built target opencv_test_dnn
[ 46%] Built target opencv_dnn_superres
[ 47%] Built target opencv_perf_dnn_superres
[ 48%] Built target opencv_test_dnn_superres
[ 49%] Built target opencv_features2d
[ 49%] Built target opencv_perf_features2d
[ 50%] Built target opencv_test_features2d
[ 50%] Built target opencv_fuzzy
[ 50%] Built target opencv_test_fuzzy
[ 50%] Built target opencv_hfs
[ 50%] Built target opencv_img_hash
[ 50%] Built target opencv_test_img_hash
[ 50%] Built target opencv_perf_imgcodecs
[ 51%] Built target opencv_test_imgcodecs
[ 51%] Built target opencv_line_descriptor
[ 52%] Built target opencv_perf_line_descriptor
[ 52%] Built target opencv_test_line_descriptor
[ 53%] Built target opencv_saliency
[ 53%] Built target opencv_test_saliency
[ 53%] Built target opencv_text
[ 53%] Built target opencv_test_text
[ 53%] Built target opencv_perf_videoio
[ 53%] Built target opencv_test_videoio
[ 55%] Built target opencv_calib3d
[ 56%] Built target opencv_perf_calib3d
[ 58%] Built target opencv_test_calib3d
[ 60%] Built target opencv_datasets
[ 60%] Built target opencv_test_highgui
[ 61%] Built target opencv_mcc
[ 62%] Built target opencv_test_mcc
[ 64%] Built target opencv_objdetect
[ 64%] Built target opencv_perf_objdetect
[ 65%] Built target opencv_test_objdetect
[ 65%] Built target opencv_rapid
[ 65%] Built target opencv_test_rapid
[ 66%] Built target opencv_rgbd
[ 67%] Built target opencv_perf_rgbd
[ 68%] Built target opencv_test_rgbd
[ 68%] Built target opencv_shape
[ 68%] Built target opencv_test_shape
[ 68%] Built target opencv_structured_light
[ 68%] Built target opencv_test_structured_light
[ 69%] Built target opencv_video
[ 70%] Built target opencv_perf_video
[ 71%] Built target opencv_test_video
[ 71%] Built target opencv_videostab
[ 72%] Built target opencv_test_videostab
[ 74%] Built target opencv_wechat_qrcode
[ 74%] Built target opencv_perf_wechat_qrcode
[ 74%] Built target opencv_test_wechat_qrcode
[ 75%] Built target opencv_xfeatures2d
[ 76%] Built target opencv_perf_xfeatures2d
[ 76%] Built target opencv_test_xfeatures2d
[ 78%] Built target opencv_ximgproc
[ 78%] Built target opencv_perf_ximgproc
[ 79%] Built target opencv_test_ximgproc
[ 79%] Built target opencv_xobjdetect
[ 80%] Built target opencv_waldboost_detector
[ 80%] Built target opencv_aruco
[ 80%] Built target opencv_perf_aruco
[ 80%] Built target opencv_test_aruco
[ 80%] Built target opencv_bgsegm
[ 80%] Built target opencv_test_bgsegm
[ 81%] Built target opencv_bioinspired
[ 81%] Built target opencv_perf_bioinspired
[ 81%] Built target opencv_test_bioinspired
[ 81%] Built target opencv_ccalib
[ 81%] Built target opencv_dnn_objdetect
[ 81%] Built target opencv_dpm
[ 82%] Built target opencv_face
[ 82%] Built target opencv_test_face
[ 83%] Built target ade
[ 89%] Built target opencv_gapi
[ 90%] Built target opencv_perf_gapi
[ 94%] Built target opencv_test_gapi
[ 94%] Built target opencv_optflow
[ 94%] Built target opencv_perf_optflow
[ 94%] Built target opencv_test_optflow
[ 95%] Built target opencv_stitching
[ 95%] Built target opencv_perf_stitching
[ 96%] Built target opencv_test_stitching
[ 97%] Built target opencv_superres
[ 97%] Built target opencv_perf_superres
[ 97%] Built target opencv_test_superres
[ 99%] Built target opencv_tracking
[ 99%] Built target opencv_perf_tracking
[ 99%] Built target opencv_test_tracking
[ 99%] Built target opencv_stereo
[ 99%] Built target opencv_perf_stereo
[ 99%] Built target opencv_test_stereo
[ 99%] Built target gen_opencv_java_source
[ 99%] Built target opencv_java_jar_source_copy
[ 99%] Built target opencv_java_jar_sources
[100%] Built target opencv_java_jar
[100%] Built target opencv_java
[100%] Built target opencv_annotation
[100%] Built target opencv_visualisation
[100%] Built target opencv_interactive-calibration
[100%] Built target opencv_version
[100%] Built target opencv_model_diagnostics
Install the project...
-- Install configuration: "Release"
-- Installing: /usr/local/share/licenses/opencv4/ippicv-readme.htm
-- Installing: /usr/local/share/licenses/opencv4/ippicv-EULA.txt
-- Installing: /usr/local/share/licenses/opencv4/ippicv-third-party-programs.txt
-- Installing: /usr/local/share/licenses/opencv4/ippiw-support.txt
-- Installing: /usr/local/share/licenses/opencv4/ippiw-third-party-programs.txt
-- Installing: /usr/local/share/licenses/opencv4/ippiw-EULA.txt
-- Installing: /usr/local/share/licenses/opencv4/flatbuffers-LICENSE.txt
-- Installing: /usr/local/share/licenses/opencv4/opencl-headers-LICENSE.txt
-- Installing: /usr/local/share/licenses/opencv4/ade-LICENSE
-- Installing: /usr/local/include/opencv4/opencv2/cvconfig.h
-- Installing: /usr/local/include/opencv4/opencv2/opencv_modules.hpp
-- Installing: /usr/local/lib/cmake/opencv4/OpenCVModules.cmake
-- Installing: /usr/local/lib/cmake/opencv4/OpenCVModules-release.cmake
-- Installing: /usr/local/lib/cmake/opencv4/OpenCVConfig-version.cmake
-- Installing: /usr/local/lib/cmake/opencv4/OpenCVConfig.cmake
-- Installing: /usr/local/bin/setup_vars_opencv4.sh
-- Installing: /usr/local/share/opencv4/valgrind.supp
-- Installing: /usr/local/share/opencv4/valgrind_3rdparty.supp
-- Installing: /usr/local/share/licenses/opencv4/libjpeg-turbo-README.md
-- Installing: /usr/local/share/licenses/opencv4/libjpeg-turbo-LICENSE.md
-- Installing: /usr/local/share/licenses/opencv4/libjpeg-turbo-README.ijg
-- Installing: /usr/local/share/licenses/opencv4/libtiff-COPYRIGHT
-- Installing: /usr/local/share/licenses/opencv4/libopenjp2-README.md
-- Installing: /usr/local/share/licenses/opencv4/libopenjp2-LICENSE
-- Installing: /usr/local/share/licenses/opencv4/openexr-LICENSE
-- Installing: /usr/local/share/licenses/opencv4/openexr-AUTHORS.ilmbase
-- Installing: /usr/local/share/licenses/opencv4/openexr-AUTHORS.openexr
-- Installing: /usr/local/share/licenses/opencv4/protobuf-LICENSE
-- Installing: /usr/local/share/licenses/opencv4/protobuf-README.md
-- Installing: /usr/local/share/licenses/opencv4/ittnotify-LICENSE.BSD
-- Installing: /usr/local/share/licenses/opencv4/ittnotify-LICENSE.GPL
-- Installing: /usr/local/include/opencv4/opencv2/opencv.hpp
-- Installing: /usr/local/lib/libopencv_core.so.4.9.0
-- Installing: /usr/local/lib/libopencv_core.so.409
-- Set runtime path of "/usr/local/lib/libopencv_core.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_core.so
-- Installing: /usr/local/include/opencv4/opencv2/core.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/affine.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/async.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/base.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/bindings_utils.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/bufferpool.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/check.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/core.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/core_c.h
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda.inl.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/block.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/border_interpolate.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/color.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/common.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/datamov_utils.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/detail/color_detail.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/detail/reduce.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/detail/reduce_key_val.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/detail/transform_detail.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/detail/type_traits_detail.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/detail/vec_distance_detail.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/dynamic_smem.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/emulation.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/filters.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/funcattrib.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/functional.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/limits.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/reduce.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/saturate_cast.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/scan.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/simd_functions.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/transform.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/type_traits.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/utility.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/vec_distance.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/vec_math.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/vec_traits.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/warp.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/warp_reduce.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda/warp_shuffle.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda_stream_accessor.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cuda_types.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cv_cpu_dispatch.h
-- Installing: /usr/local/include/opencv4/opencv2/core/cv_cpu_helper.h
-- Installing: /usr/local/include/opencv4/opencv2/core/cvdef.h
-- Installing: /usr/local/include/opencv4/opencv2/core/cvstd.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cvstd.inl.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/cvstd_wrapper.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/detail/async_promise.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/detail/dispatch_helper.impl.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/detail/exception_ptr.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/directx.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/dualquaternion.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/dualquaternion.inl.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/eigen.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/fast_math.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/hal.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/interface.h
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/intrin.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/intrin_avx.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/intrin_avx512.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/intrin_cpp.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/intrin_forward.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/intrin_lasx.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/intrin_lsx.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/intrin_msa.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/intrin_neon.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/intrin_rvv.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/intrin_rvv071.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/intrin_rvv_010_compat_non-policy.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/intrin_rvv_010_compat_overloaded-non-policy.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/intrin_rvv_011_compat.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/intrin_rvv_compat_overloaded.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/intrin_rvv_scalable.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/intrin_sse.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/intrin_sse_em.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/intrin_vsx.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/intrin_wasm.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/msa_macros.h
-- Installing: /usr/local/include/opencv4/opencv2/core/hal/simd_utils.impl.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/mat.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/mat.inl.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/matx.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/neon_utils.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/ocl.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/ocl_genbase.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/opencl/ocl_defs.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/opencl/opencl_info.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/opencl/opencl_svm.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/opencl/runtime/autogenerated/opencl_clblas.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/opencl/runtime/autogenerated/opencl_clfft.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/opencl/runtime/autogenerated/opencl_core.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/opencl/runtime/autogenerated/opencl_core_wrappers.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/opencl/runtime/autogenerated/opencl_gl.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/opencl/runtime/autogenerated/opencl_gl_wrappers.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/opencl/runtime/opencl_clblas.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/opencl/runtime/opencl_clfft.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/opencl/runtime/opencl_core.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/opencl/runtime/opencl_core_wrappers.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/opencl/runtime/opencl_gl.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/opencl/runtime/opencl_gl_wrappers.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/opencl/runtime/opencl_svm_20.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/opencl/runtime/opencl_svm_definitions.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/opencl/runtime/opencl_svm_hsa_extension.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/opengl.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/operations.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/optim.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/ovx.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/parallel/backend/parallel_for.openmp.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/parallel/backend/parallel_for.tbb.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/parallel/parallel_backend.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/persistence.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/quaternion.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/quaternion.inl.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/saturate.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/simd_intrinsics.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/softfloat.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/sse_utils.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/traits.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/types.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/types_c.h
-- Installing: /usr/local/include/opencv4/opencv2/core/utility.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/utils/allocator_stats.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/utils/allocator_stats.impl.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/utils/filesystem.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/utils/fp_control_utils.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/utils/instrumentation.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/utils/logger.defines.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/utils/logger.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/utils/logtag.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/utils/tls.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/utils/trace.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/va_intel.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/version.hpp
-- Installing: /usr/local/include/opencv4/opencv2/core/vsx_utils.hpp
-- Installing: /usr/local/share/licenses/opencv4/SoftFloat-COPYING.txt
-- Installing: /usr/local/lib/libopencv_flann.so.4.9.0
-- Installing: /usr/local/lib/libopencv_flann.so.409
-- Set runtime path of "/usr/local/lib/libopencv_flann.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_flann.so
-- Installing: /usr/local/include/opencv4/opencv2/flann.hpp
-- Installing: /usr/local/include/opencv4/opencv2/flann/all_indices.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/allocator.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/any.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/autotuned_index.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/composite_index.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/config.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/defines.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/dist.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/dummy.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/dynamic_bitset.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/flann.hpp
-- Installing: /usr/local/include/opencv4/opencv2/flann/flann_base.hpp
-- Installing: /usr/local/include/opencv4/opencv2/flann/general.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/ground_truth.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/hdf5.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/heap.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/hierarchical_clustering_index.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/index_testing.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/kdtree_index.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/kdtree_single_index.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/kmeans_index.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/linear_index.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/logger.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/lsh_index.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/lsh_table.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/matrix.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/miniflann.hpp
-- Installing: /usr/local/include/opencv4/opencv2/flann/nn_index.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/object_factory.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/params.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/random.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/result_set.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/sampling.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/saving.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/simplex_downhill.h
-- Installing: /usr/local/include/opencv4/opencv2/flann/timer.h
-- Installing: /usr/local/lib/libopencv_imgproc.so.4.9.0
-- Installing: /usr/local/lib/libopencv_imgproc.so.409
-- Set runtime path of "/usr/local/lib/libopencv_imgproc.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_imgproc.so
-- Installing: /usr/local/include/opencv4/opencv2/imgproc.hpp
-- Installing: /usr/local/include/opencv4/opencv2/imgproc/bindings.hpp
-- Installing: /usr/local/include/opencv4/opencv2/imgproc/detail/gcgraph.hpp
-- Installing: /usr/local/include/opencv4/opencv2/imgproc/hal/hal.hpp
-- Installing: /usr/local/include/opencv4/opencv2/imgproc/hal/interface.h
-- Installing: /usr/local/include/opencv4/opencv2/imgproc/imgproc.hpp
-- Installing: /usr/local/include/opencv4/opencv2/imgproc/imgproc_c.h
-- Installing: /usr/local/include/opencv4/opencv2/imgproc/segmentation.hpp
-- Installing: /usr/local/include/opencv4/opencv2/imgproc/types_c.h
-- Installing: /usr/local/lib/libopencv_intensity_transform.so.4.9.0
-- Installing: /usr/local/lib/libopencv_intensity_transform.so.409
-- Set runtime path of "/usr/local/lib/libopencv_intensity_transform.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_intensity_transform.so
-- Installing: /usr/local/include/opencv4/opencv2/intensity_transform.hpp
-- Installing: /usr/local/lib/libopencv_ml.so.4.9.0
-- Installing: /usr/local/lib/libopencv_ml.so.409
-- Set runtime path of "/usr/local/lib/libopencv_ml.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_ml.so
-- Installing: /usr/local/include/opencv4/opencv2/ml.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ml/ml.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ml/ml.inl.hpp
-- Installing: /usr/local/lib/libopencv_phase_unwrapping.so.4.9.0
-- Installing: /usr/local/lib/libopencv_phase_unwrapping.so.409
-- Set runtime path of "/usr/local/lib/libopencv_phase_unwrapping.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_phase_unwrapping.so
-- Installing: /usr/local/include/opencv4/opencv2/phase_unwrapping.hpp
-- Installing: /usr/local/include/opencv4/opencv2/phase_unwrapping/histogramphaseunwrapping.hpp
-- Installing: /usr/local/include/opencv4/opencv2/phase_unwrapping/phase_unwrapping.hpp
-- Installing: /usr/local/lib/libopencv_photo.so.4.9.0
-- Installing: /usr/local/lib/libopencv_photo.so.409
-- Set runtime path of "/usr/local/lib/libopencv_photo.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_photo.so
-- Installing: /usr/local/include/opencv4/opencv2/photo.hpp
-- Installing: /usr/local/include/opencv4/opencv2/photo/cuda.hpp
-- Installing: /usr/local/include/opencv4/opencv2/photo/legacy/constants_c.h
-- Installing: /usr/local/include/opencv4/opencv2/photo/photo.hpp
-- Installing: /usr/local/lib/libopencv_plot.so.4.9.0
-- Installing: /usr/local/lib/libopencv_plot.so.409
-- Set runtime path of "/usr/local/lib/libopencv_plot.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_plot.so
-- Installing: /usr/local/include/opencv4/opencv2/plot.hpp
-- Installing: /usr/local/lib/libopencv_quality.so.4.9.0
-- Installing: /usr/local/lib/libopencv_quality.so.409
-- Set runtime path of "/usr/local/lib/libopencv_quality.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_quality.so
-- Installing: /usr/local/include/opencv4/opencv2/quality.hpp
-- Installing: /usr/local/include/opencv4/opencv2/quality/quality_utils.hpp
-- Installing: /usr/local/include/opencv4/opencv2/quality/qualitybase.hpp
-- Installing: /usr/local/include/opencv4/opencv2/quality/qualitybrisque.hpp
-- Installing: /usr/local/include/opencv4/opencv2/quality/qualitygmsd.hpp
-- Installing: /usr/local/include/opencv4/opencv2/quality/qualitymse.hpp
-- Installing: /usr/local/include/opencv4/opencv2/quality/qualitypsnr.hpp
-- Installing: /usr/local/include/opencv4/opencv2/quality/qualityssim.hpp
-- Installing: /usr/local/share/opencv4/quality/brisque_model_live.yml
-- Installing: /usr/local/share/opencv4/quality/brisque_range_live.yml
-- Installing: /usr/local/lib/libopencv_reg.so.4.9.0
-- Installing: /usr/local/lib/libopencv_reg.so.409
-- Set runtime path of "/usr/local/lib/libopencv_reg.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_reg.so
-- Installing: /usr/local/include/opencv4/opencv2/reg/map.hpp
-- Installing: /usr/local/include/opencv4/opencv2/reg/mapaffine.hpp
-- Installing: /usr/local/include/opencv4/opencv2/reg/mapper.hpp
-- Installing: /usr/local/include/opencv4/opencv2/reg/mappergradaffine.hpp
-- Installing: /usr/local/include/opencv4/opencv2/reg/mappergradeuclid.hpp
-- Installing: /usr/local/include/opencv4/opencv2/reg/mappergradproj.hpp
-- Installing: /usr/local/include/opencv4/opencv2/reg/mappergradshift.hpp
-- Installing: /usr/local/include/opencv4/opencv2/reg/mappergradsimilar.hpp
-- Installing: /usr/local/include/opencv4/opencv2/reg/mapperpyramid.hpp
-- Installing: /usr/local/include/opencv4/opencv2/reg/mapprojec.hpp
-- Installing: /usr/local/include/opencv4/opencv2/reg/mapshift.hpp
-- Installing: /usr/local/lib/libopencv_signal.so.4.9.0
-- Installing: /usr/local/lib/libopencv_signal.so.409
-- Set runtime path of "/usr/local/lib/libopencv_signal.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_signal.so
-- Installing: /usr/local/include/opencv4/opencv2/signal.hpp
-- Installing: /usr/local/include/opencv4/opencv2/signal/signal_resample.hpp
-- Installing: /usr/local/lib/libopencv_surface_matching.so.4.9.0
-- Installing: /usr/local/lib/libopencv_surface_matching.so.409
-- Set runtime path of "/usr/local/lib/libopencv_surface_matching.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_surface_matching.so
-- Installing: /usr/local/include/opencv4/opencv2/surface_matching.hpp
-- Installing: /usr/local/include/opencv4/opencv2/surface_matching/icp.hpp
-- Installing: /usr/local/include/opencv4/opencv2/surface_matching/pose_3d.hpp
-- Installing: /usr/local/include/opencv4/opencv2/surface_matching/ppf_helpers.hpp
-- Installing: /usr/local/include/opencv4/opencv2/surface_matching/ppf_match_3d.hpp
-- Installing: /usr/local/include/opencv4/opencv2/surface_matching/t_hash_int.hpp
-- Installing: /usr/local/lib/libopencv_xphoto.so.4.9.0
-- Installing: /usr/local/lib/libopencv_xphoto.so.409
-- Set runtime path of "/usr/local/lib/libopencv_xphoto.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_xphoto.so
-- Installing: /usr/local/include/opencv4/opencv2/xphoto.hpp
-- Installing: /usr/local/include/opencv4/opencv2/xphoto/bm3d_image_denoising.hpp
-- Installing: /usr/local/include/opencv4/opencv2/xphoto/dct_image_denoising.hpp
-- Installing: /usr/local/include/opencv4/opencv2/xphoto/inpainting.hpp
-- Installing: /usr/local/include/opencv4/opencv2/xphoto/oilpainting.hpp
-- Installing: /usr/local/include/opencv4/opencv2/xphoto/tonemap.hpp
-- Installing: /usr/local/include/opencv4/opencv2/xphoto/white_balance.hpp
-- Installing: /usr/local/lib/libopencv_dnn.so.4.9.0
-- Installing: /usr/local/lib/libopencv_dnn.so.409
-- Set runtime path of "/usr/local/lib/libopencv_dnn.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_dnn.so
-- Installing: /usr/local/include/opencv4/opencv2/dnn.hpp
-- Installing: /usr/local/include/opencv4/opencv2/dnn/all_layers.hpp
-- Installing: /usr/local/include/opencv4/opencv2/dnn/dict.hpp
-- Installing: /usr/local/include/opencv4/opencv2/dnn/dnn.hpp
-- Installing: /usr/local/include/opencv4/opencv2/dnn/dnn.inl.hpp
-- Installing: /usr/local/include/opencv4/opencv2/dnn/layer.details.hpp
-- Installing: /usr/local/include/opencv4/opencv2/dnn/layer.hpp
-- Installing: /usr/local/include/opencv4/opencv2/dnn/shape_utils.hpp
-- Installing: /usr/local/include/opencv4/opencv2/dnn/utils/debug_utils.hpp
-- Installing: /usr/local/include/opencv4/opencv2/dnn/utils/inference_engine.hpp
-- Installing: /usr/local/include/opencv4/opencv2/dnn/version.hpp
-- Installing: /usr/local/lib/libopencv_dnn_superres.so.4.9.0
-- Installing: /usr/local/lib/libopencv_dnn_superres.so.409
-- Set runtime path of "/usr/local/lib/libopencv_dnn_superres.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_dnn_superres.so
-- Installing: /usr/local/include/opencv4/opencv2/dnn_superres.hpp
-- Installing: /usr/local/lib/libopencv_features2d.so.4.9.0
-- Installing: /usr/local/lib/libopencv_features2d.so.409
-- Set runtime path of "/usr/local/lib/libopencv_features2d.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_features2d.so
-- Installing: /usr/local/include/opencv4/opencv2/features2d.hpp
-- Installing: /usr/local/include/opencv4/opencv2/features2d/features2d.hpp
-- Installing: /usr/local/include/opencv4/opencv2/features2d/hal/interface.h
-- Installing: /usr/local/share/licenses/opencv4/mscr-chi_table_LICENSE.txt
-- Installing: /usr/local/lib/libopencv_fuzzy.so.4.9.0
-- Installing: /usr/local/lib/libopencv_fuzzy.so.409
-- Set runtime path of "/usr/local/lib/libopencv_fuzzy.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_fuzzy.so
-- Installing: /usr/local/include/opencv4/opencv2/fuzzy.hpp
-- Installing: /usr/local/include/opencv4/opencv2/fuzzy/fuzzy_F0_math.hpp
-- Installing: /usr/local/include/opencv4/opencv2/fuzzy/fuzzy_F1_math.hpp
-- Installing: /usr/local/include/opencv4/opencv2/fuzzy/fuzzy_image.hpp
-- Installing: /usr/local/include/opencv4/opencv2/fuzzy/types.hpp
-- Installing: /usr/local/lib/libopencv_hfs.so.4.9.0
-- Installing: /usr/local/lib/libopencv_hfs.so.409
-- Set runtime path of "/usr/local/lib/libopencv_hfs.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_hfs.so
-- Installing: /usr/local/include/opencv4/opencv2/hfs.hpp
-- Installing: /usr/local/lib/libopencv_img_hash.so.4.9.0
-- Installing: /usr/local/lib/libopencv_img_hash.so.409
-- Set runtime path of "/usr/local/lib/libopencv_img_hash.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_img_hash.so
-- Installing: /usr/local/include/opencv4/opencv2/img_hash.hpp
-- Installing: /usr/local/include/opencv4/opencv2/img_hash/average_hash.hpp
-- Installing: /usr/local/include/opencv4/opencv2/img_hash/block_mean_hash.hpp
-- Installing: /usr/local/include/opencv4/opencv2/img_hash/color_moment_hash.hpp
-- Installing: /usr/local/include/opencv4/opencv2/img_hash/img_hash_base.hpp
-- Installing: /usr/local/include/opencv4/opencv2/img_hash/marr_hildreth_hash.hpp
-- Installing: /usr/local/include/opencv4/opencv2/img_hash/phash.hpp
-- Installing: /usr/local/include/opencv4/opencv2/img_hash/radial_variance_hash.hpp
-- Installing: /usr/local/lib/libopencv_imgcodecs.so.4.9.0
-- Installing: /usr/local/lib/libopencv_imgcodecs.so.409
-- Set runtime path of "/usr/local/lib/libopencv_imgcodecs.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_imgcodecs.so
-- Installing: /usr/local/include/opencv4/opencv2/imgcodecs.hpp
-- Installing: /usr/local/include/opencv4/opencv2/imgcodecs/imgcodecs.hpp
-- Installing: /usr/local/include/opencv4/opencv2/imgcodecs/imgcodecs_c.h
-- Installing: /usr/local/include/opencv4/opencv2/imgcodecs/ios.h
-- Installing: /usr/local/include/opencv4/opencv2/imgcodecs/legacy/constants_c.h
-- Installing: /usr/local/include/opencv4/opencv2/imgcodecs/macosx.h
-- Installing: /usr/local/lib/libopencv_line_descriptor.so.4.9.0
-- Installing: /usr/local/lib/libopencv_line_descriptor.so.409
-- Set runtime path of "/usr/local/lib/libopencv_line_descriptor.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_line_descriptor.so
-- Installing: /usr/local/include/opencv4/opencv2/line_descriptor.hpp
-- Installing: /usr/local/include/opencv4/opencv2/line_descriptor/descriptor.hpp
-- Installing: /usr/local/lib/libopencv_saliency.so.4.9.0
-- Installing: /usr/local/lib/libopencv_saliency.so.409
-- Set runtime path of "/usr/local/lib/libopencv_saliency.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_saliency.so
-- Installing: /usr/local/include/opencv4/opencv2/saliency.hpp
-- Installing: /usr/local/include/opencv4/opencv2/saliency/saliencyBaseClasses.hpp
-- Installing: /usr/local/include/opencv4/opencv2/saliency/saliencySpecializedClasses.hpp
-- Installing: /usr/local/lib/libopencv_text.so.4.9.0
-- Installing: /usr/local/lib/libopencv_text.so.409
-- Set runtime path of "/usr/local/lib/libopencv_text.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_text.so
-- Installing: /usr/local/include/opencv4/opencv2/text.hpp
-- Installing: /usr/local/include/opencv4/opencv2/text/erfilter.hpp
-- Installing: /usr/local/include/opencv4/opencv2/text/ocr.hpp
-- Installing: /usr/local/include/opencv4/opencv2/text/swt_text_detection.hpp
-- Installing: /usr/local/include/opencv4/opencv2/text/textDetector.hpp
-- Installing: /usr/local/lib/libopencv_videoio.so.4.9.0
-- Installing: /usr/local/lib/libopencv_videoio.so.409
-- Set runtime path of "/usr/local/lib/libopencv_videoio.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_videoio.so
-- Installing: /usr/local/include/opencv4/opencv2/videoio.hpp
-- Installing: /usr/local/include/opencv4/opencv2/videoio/cap_ios.h
-- Installing: /usr/local/include/opencv4/opencv2/videoio/legacy/constants_c.h
-- Installing: /usr/local/include/opencv4/opencv2/videoio/registry.hpp
-- Installing: /usr/local/include/opencv4/opencv2/videoio/videoio.hpp
-- Installing: /usr/local/include/opencv4/opencv2/videoio/videoio_c.h
-- Installing: /usr/local/lib/libopencv_calib3d.so.4.9.0
-- Installing: /usr/local/lib/libopencv_calib3d.so.409
-- Set runtime path of "/usr/local/lib/libopencv_calib3d.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_calib3d.so
-- Installing: /usr/local/include/opencv4/opencv2/calib3d.hpp
-- Installing: /usr/local/include/opencv4/opencv2/calib3d/calib3d.hpp
-- Installing: /usr/local/include/opencv4/opencv2/calib3d/calib3d_c.h
-- Installing: /usr/local/lib/libopencv_datasets.so.4.9.0
-- Installing: /usr/local/lib/libopencv_datasets.so.409
-- Set runtime path of "/usr/local/lib/libopencv_datasets.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_datasets.so
-- Installing: /usr/local/include/opencv4/opencv2/datasets/ar_hmdb.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/ar_sports.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/dataset.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/fr_adience.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/fr_lfw.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/gr_chalearn.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/gr_skig.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/hpe_humaneva.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/hpe_parse.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/ir_affine.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/ir_robot.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/is_bsds.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/is_weizmann.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/msm_epfl.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/msm_middlebury.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/or_imagenet.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/or_mnist.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/or_pascal.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/or_sun.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/pd_caltech.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/pd_inria.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/slam_kitti.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/slam_tumindoor.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/sr_bsds.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/sr_div2k.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/sr_general100.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/tr_chars.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/tr_icdar.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/tr_svt.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/track_alov.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/track_vot.hpp
-- Installing: /usr/local/include/opencv4/opencv2/datasets/util.hpp
-- Installing: /usr/local/lib/libopencv_highgui.so.4.9.0
-- Installing: /usr/local/lib/libopencv_highgui.so.409
-- Set runtime path of "/usr/local/lib/libopencv_highgui.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_highgui.so
-- Installing: /usr/local/include/opencv4/opencv2/highgui.hpp
-- Installing: /usr/local/include/opencv4/opencv2/highgui/highgui.hpp
-- Installing: /usr/local/include/opencv4/opencv2/highgui/highgui_c.h
-- Installing: /usr/local/lib/libopencv_mcc.so.4.9.0
-- Installing: /usr/local/lib/libopencv_mcc.so.409
-- Set runtime path of "/usr/local/lib/libopencv_mcc.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_mcc.so
-- Installing: /usr/local/include/opencv4/opencv2/mcc.hpp
-- Installing: /usr/local/include/opencv4/opencv2/mcc/ccm.hpp
-- Installing: /usr/local/include/opencv4/opencv2/mcc/checker_detector.hpp
-- Installing: /usr/local/include/opencv4/opencv2/mcc/checker_model.hpp
-- Installing: /usr/local/lib/libopencv_objdetect.so.4.9.0
-- Installing: /usr/local/lib/libopencv_objdetect.so.409
-- Set runtime path of "/usr/local/lib/libopencv_objdetect.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_objdetect.so
-- Installing: /usr/local/include/opencv4/opencv2/objdetect.hpp
-- Installing: /usr/local/include/opencv4/opencv2/objdetect/aruco_board.hpp
-- Installing: /usr/local/include/opencv4/opencv2/objdetect/aruco_detector.hpp
-- Installing: /usr/local/include/opencv4/opencv2/objdetect/aruco_dictionary.hpp
-- Installing: /usr/local/include/opencv4/opencv2/objdetect/barcode.hpp
-- Installing: /usr/local/include/opencv4/opencv2/objdetect/charuco_detector.hpp
-- Installing: /usr/local/include/opencv4/opencv2/objdetect/detection_based_tracker.hpp
-- Installing: /usr/local/include/opencv4/opencv2/objdetect/face.hpp
-- Installing: /usr/local/include/opencv4/opencv2/objdetect/graphical_code_detector.hpp
-- Installing: /usr/local/include/opencv4/opencv2/objdetect/objdetect.hpp
-- Installing: /usr/local/lib/libopencv_rapid.so.4.9.0
-- Installing: /usr/local/lib/libopencv_rapid.so.409
-- Set runtime path of "/usr/local/lib/libopencv_rapid.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_rapid.so
-- Installing: /usr/local/include/opencv4/opencv2/rapid.hpp
-- Installing: /usr/local/lib/libopencv_rgbd.so.4.9.0
-- Installing: /usr/local/lib/libopencv_rgbd.so.409
-- Set runtime path of "/usr/local/lib/libopencv_rgbd.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_rgbd.so
-- Installing: /usr/local/include/opencv4/opencv2/rgbd.hpp
-- Installing: /usr/local/include/opencv4/opencv2/rgbd/colored_kinfu.hpp
-- Installing: /usr/local/include/opencv4/opencv2/rgbd/depth.hpp
-- Installing: /usr/local/include/opencv4/opencv2/rgbd/detail/pose_graph.hpp
-- Installing: /usr/local/include/opencv4/opencv2/rgbd/dynafu.hpp
-- Installing: /usr/local/include/opencv4/opencv2/rgbd/intrinsics.hpp
-- Installing: /usr/local/include/opencv4/opencv2/rgbd/kinfu.hpp
-- Installing: /usr/local/include/opencv4/opencv2/rgbd/large_kinfu.hpp
-- Installing: /usr/local/include/opencv4/opencv2/rgbd/linemod.hpp
-- Installing: /usr/local/include/opencv4/opencv2/rgbd/volume.hpp
-- Installing: /usr/local/lib/libopencv_shape.so.4.9.0
-- Installing: /usr/local/lib/libopencv_shape.so.409
-- Set runtime path of "/usr/local/lib/libopencv_shape.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_shape.so
-- Installing: /usr/local/include/opencv4/opencv2/shape.hpp
-- Installing: /usr/local/include/opencv4/opencv2/shape/emdL1.hpp
-- Installing: /usr/local/include/opencv4/opencv2/shape/hist_cost.hpp
-- Installing: /usr/local/include/opencv4/opencv2/shape/shape.hpp
-- Installing: /usr/local/include/opencv4/opencv2/shape/shape_distance.hpp
-- Installing: /usr/local/include/opencv4/opencv2/shape/shape_transformer.hpp
-- Installing: /usr/local/lib/libopencv_structured_light.so.4.9.0
-- Installing: /usr/local/lib/libopencv_structured_light.so.409
-- Set runtime path of "/usr/local/lib/libopencv_structured_light.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_structured_light.so
-- Installing: /usr/local/include/opencv4/opencv2/structured_light.hpp
-- Installing: /usr/local/include/opencv4/opencv2/structured_light/graycodepattern.hpp
-- Installing: /usr/local/include/opencv4/opencv2/structured_light/sinusoidalpattern.hpp
-- Installing: /usr/local/include/opencv4/opencv2/structured_light/structured_light.hpp
-- Installing: /usr/local/lib/libopencv_video.so.4.9.0
-- Installing: /usr/local/lib/libopencv_video.so.409
-- Set runtime path of "/usr/local/lib/libopencv_video.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_video.so
-- Installing: /usr/local/include/opencv4/opencv2/video.hpp
-- Installing: /usr/local/include/opencv4/opencv2/video/background_segm.hpp
-- Installing: /usr/local/include/opencv4/opencv2/video/detail/tracking.detail.hpp
-- Installing: /usr/local/include/opencv4/opencv2/video/legacy/constants_c.h
-- Installing: /usr/local/include/opencv4/opencv2/video/tracking.hpp
-- Installing: /usr/local/include/opencv4/opencv2/video/video.hpp
-- Installing: /usr/local/lib/libopencv_videostab.so.4.9.0
-- Installing: /usr/local/lib/libopencv_videostab.so.409
-- Set runtime path of "/usr/local/lib/libopencv_videostab.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_videostab.so
-- Installing: /usr/local/include/opencv4/opencv2/videostab.hpp
-- Installing: /usr/local/include/opencv4/opencv2/videostab/deblurring.hpp
-- Installing: /usr/local/include/opencv4/opencv2/videostab/fast_marching.hpp
-- Installing: /usr/local/include/opencv4/opencv2/videostab/fast_marching_inl.hpp
-- Installing: /usr/local/include/opencv4/opencv2/videostab/frame_source.hpp
-- Installing: /usr/local/include/opencv4/opencv2/videostab/global_motion.hpp
-- Installing: /usr/local/include/opencv4/opencv2/videostab/inpainting.hpp
-- Installing: /usr/local/include/opencv4/opencv2/videostab/log.hpp
-- Installing: /usr/local/include/opencv4/opencv2/videostab/motion_core.hpp
-- Installing: /usr/local/include/opencv4/opencv2/videostab/motion_stabilizing.hpp
-- Installing: /usr/local/include/opencv4/opencv2/videostab/optical_flow.hpp
-- Installing: /usr/local/include/opencv4/opencv2/videostab/outlier_rejection.hpp
-- Installing: /usr/local/include/opencv4/opencv2/videostab/ring_buffer.hpp
-- Installing: /usr/local/include/opencv4/opencv2/videostab/stabilizer.hpp
-- Installing: /usr/local/include/opencv4/opencv2/videostab/wobble_suppression.hpp
-- Installing: /usr/local/lib/libopencv_wechat_qrcode.so.4.9.0
-- Installing: /usr/local/lib/libopencv_wechat_qrcode.so.409
-- Set runtime path of "/usr/local/lib/libopencv_wechat_qrcode.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_wechat_qrcode.so
-- Installing: /usr/local/include/opencv4/opencv2/wechat_qrcode.hpp
-- Installing: /usr/local/lib/libopencv_xfeatures2d.so.4.9.0
-- Installing: /usr/local/lib/libopencv_xfeatures2d.so.409
-- Set runtime path of "/usr/local/lib/libopencv_xfeatures2d.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_xfeatures2d.so
-- Installing: /usr/local/include/opencv4/opencv2/xfeatures2d.hpp
-- Installing: /usr/local/include/opencv4/opencv2/xfeatures2d/cuda.hpp
-- Installing: /usr/local/include/opencv4/opencv2/xfeatures2d/nonfree.hpp
-- Installing: /usr/local/lib/libopencv_ximgproc.so.4.9.0
-- Installing: /usr/local/lib/libopencv_ximgproc.so.409
-- Set runtime path of "/usr/local/lib/libopencv_ximgproc.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_ximgproc.so
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/brightedges.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/color_match.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/deriche_filter.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/disparity_filter.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/edge_drawing.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/edge_filter.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/edgeboxes.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/edgepreserving_filter.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/estimated_covariance.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/fast_hough_transform.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/fast_line_detector.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/find_ellipses.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/fourier_descriptors.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/lsc.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/paillou_filter.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/peilin.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/radon_transform.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/ridgefilter.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/run_length_morphology.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/scansegment.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/seeds.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/segmentation.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/slic.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/sparse_match_interpolator.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/structured_edge_detection.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ximgproc/weighted_median_filter.hpp
-- Installing: /usr/local/lib/libopencv_xobjdetect.so.4.9.0
-- Installing: /usr/local/lib/libopencv_xobjdetect.so.409
-- Set runtime path of "/usr/local/lib/libopencv_xobjdetect.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_xobjdetect.so
-- Installing: /usr/local/include/opencv4/opencv2/xobjdetect.hpp
-- Installing: /usr/local/bin/opencv_waldboost_detector
-- Set runtime path of "/usr/local/bin/opencv_waldboost_detector" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_aruco.so.4.9.0
-- Installing: /usr/local/lib/libopencv_aruco.so.409
-- Set runtime path of "/usr/local/lib/libopencv_aruco.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_aruco.so
-- Installing: /usr/local/include/opencv4/opencv2/aruco.hpp
-- Installing: /usr/local/include/opencv4/opencv2/aruco/aruco_calib.hpp
-- Installing: /usr/local/include/opencv4/opencv2/aruco/charuco.hpp
-- Installing: /usr/local/lib/libopencv_bgsegm.so.4.9.0
-- Installing: /usr/local/lib/libopencv_bgsegm.so.409
-- Set runtime path of "/usr/local/lib/libopencv_bgsegm.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_bgsegm.so
-- Installing: /usr/local/include/opencv4/opencv2/bgsegm.hpp
-- Installing: /usr/local/lib/libopencv_bioinspired.so.4.9.0
-- Installing: /usr/local/lib/libopencv_bioinspired.so.409
-- Set runtime path of "/usr/local/lib/libopencv_bioinspired.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_bioinspired.so
-- Installing: /usr/local/include/opencv4/opencv2/bioinspired.hpp
-- Installing: /usr/local/include/opencv4/opencv2/bioinspired/bioinspired.hpp
-- Installing: /usr/local/include/opencv4/opencv2/bioinspired/retina.hpp
-- Installing: /usr/local/include/opencv4/opencv2/bioinspired/retinafasttonemapping.hpp
-- Installing: /usr/local/include/opencv4/opencv2/bioinspired/transientareassegmentationmodule.hpp
-- Installing: /usr/local/lib/libopencv_ccalib.so.4.9.0
-- Installing: /usr/local/lib/libopencv_ccalib.so.409
-- Set runtime path of "/usr/local/lib/libopencv_ccalib.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_ccalib.so
-- Installing: /usr/local/include/opencv4/opencv2/ccalib.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ccalib/multicalib.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ccalib/omnidir.hpp
-- Installing: /usr/local/include/opencv4/opencv2/ccalib/randpattern.hpp
-- Installing: /usr/local/lib/libopencv_dnn_objdetect.so.4.9.0
-- Installing: /usr/local/lib/libopencv_dnn_objdetect.so.409
-- Set runtime path of "/usr/local/lib/libopencv_dnn_objdetect.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_dnn_objdetect.so
-- Installing: /usr/local/include/opencv4/opencv2/core_detect.hpp
-- Installing: /usr/local/lib/libopencv_dpm.so.4.9.0
-- Installing: /usr/local/lib/libopencv_dpm.so.409
-- Set runtime path of "/usr/local/lib/libopencv_dpm.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_dpm.so
-- Installing: /usr/local/include/opencv4/opencv2/dpm.hpp
-- Installing: /usr/local/lib/libopencv_face.so.4.9.0
-- Installing: /usr/local/lib/libopencv_face.so.409
-- Set runtime path of "/usr/local/lib/libopencv_face.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_face.so
-- Installing: /usr/local/include/opencv4/opencv2/face.hpp
-- Installing: /usr/local/include/opencv4/opencv2/face/bif.hpp
-- Installing: /usr/local/include/opencv4/opencv2/face/face_alignment.hpp
-- Installing: /usr/local/include/opencv4/opencv2/face/facemark.hpp
-- Installing: /usr/local/include/opencv4/opencv2/face/facemarkAAM.hpp
-- Installing: /usr/local/include/opencv4/opencv2/face/facemarkLBF.hpp
-- Installing: /usr/local/include/opencv4/opencv2/face/facemark_train.hpp
-- Installing: /usr/local/include/opencv4/opencv2/face/facerec.hpp
-- Installing: /usr/local/include/opencv4/opencv2/face/mace.hpp
-- Installing: /usr/local/include/opencv4/opencv2/face/predict_collector.hpp
-- Installing: /usr/local/lib/libopencv_gapi.so.4.9.0
-- Installing: /usr/local/lib/libopencv_gapi.so.409
-- Set runtime path of "/usr/local/lib/libopencv_gapi.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_gapi.so
-- Installing: /usr/local/include/opencv4/opencv2/gapi.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/core.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/cpu/core.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/cpu/gcpukernel.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/cpu/imgproc.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/cpu/ot.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/cpu/stereo.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/cpu/video.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/fluid/core.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/fluid/gfluidbuffer.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/fluid/gfluidkernel.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/fluid/imgproc.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/garg.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/garray.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gasync_context.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gcall.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gcommon.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gcompiled.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gcompiled_async.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gcompoundkernel.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gcomputation.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gcomputation_async.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gframe.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gkernel.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gmat.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gmetaarg.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gopaque.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gproto.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gpu/core.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gpu/ggpukernel.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gpu/imgproc.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gscalar.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gstreaming.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gtransform.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gtype_traits.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/gtyped.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/imgproc.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/infer.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/infer/bindings_ie.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/infer/bindings_onnx.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/infer/bindings_ov.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/infer/ie.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/infer/onnx.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/infer/ov.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/infer/parsers.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/media.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/oak/infer.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/oak/oak.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/ocl/core.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/ocl/goclkernel.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/ocl/imgproc.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/opencv_includes.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/operators.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/ot.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/own/assert.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/own/convert.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/own/cvdefs.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/own/exports.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/own/mat.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/own/saturate.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/own/scalar.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/own/types.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/plaidml/core.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/plaidml/gplaidmlkernel.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/plaidml/plaidml.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/python/python.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/render.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/render/render.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/render/render_types.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/rmat.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/s11n.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/s11n/base.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/stereo.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/streaming/cap.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/streaming/desync.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/streaming/format.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/streaming/gstreamer/gstreamerpipeline.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/streaming/gstreamer/gstreamersource.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/streaming/meta.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/streaming/onevpl/accel_types.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/streaming/onevpl/cfg_params.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/streaming/onevpl/data_provider_interface.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/streaming/onevpl/default.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/streaming/onevpl/device_selector_interface.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/streaming/onevpl/source.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/streaming/queue_source.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/streaming/source.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/streaming/sync.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/util/any.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/util/compiler_hints.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/util/copy_through_move.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/util/optional.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/util/throw.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/util/type_traits.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/util/util.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/util/variant.hpp
-- Installing: /usr/local/include/opencv4/opencv2/gapi/video.hpp
-- Installing: /usr/local/share/licenses/opencv4/vasot-LICENSE.txt
-- Installing: /usr/local/lib/libopencv_optflow.so.4.9.0
-- Installing: /usr/local/lib/libopencv_optflow.so.409
-- Set runtime path of "/usr/local/lib/libopencv_optflow.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_optflow.so
-- Installing: /usr/local/include/opencv4/opencv2/optflow.hpp
-- Installing: /usr/local/include/opencv4/opencv2/optflow/motempl.hpp
-- Installing: /usr/local/include/opencv4/opencv2/optflow/pcaflow.hpp
-- Installing: /usr/local/include/opencv4/opencv2/optflow/rlofflow.hpp
-- Installing: /usr/local/include/opencv4/opencv2/optflow/sparse_matching_gpc.hpp
-- Installing: /usr/local/lib/libopencv_stitching.so.4.9.0
-- Installing: /usr/local/lib/libopencv_stitching.so.409
-- Set runtime path of "/usr/local/lib/libopencv_stitching.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_stitching.so
-- Installing: /usr/local/include/opencv4/opencv2/stitching.hpp
-- Installing: /usr/local/include/opencv4/opencv2/stitching/detail/autocalib.hpp
-- Installing: /usr/local/include/opencv4/opencv2/stitching/detail/blenders.hpp
-- Installing: /usr/local/include/opencv4/opencv2/stitching/detail/camera.hpp
-- Installing: /usr/local/include/opencv4/opencv2/stitching/detail/exposure_compensate.hpp
-- Installing: /usr/local/include/opencv4/opencv2/stitching/detail/matchers.hpp
-- Installing: /usr/local/include/opencv4/opencv2/stitching/detail/motion_estimators.hpp
-- Installing: /usr/local/include/opencv4/opencv2/stitching/detail/seam_finders.hpp
-- Installing: /usr/local/include/opencv4/opencv2/stitching/detail/timelapsers.hpp
-- Installing: /usr/local/include/opencv4/opencv2/stitching/detail/util.hpp
-- Installing: /usr/local/include/opencv4/opencv2/stitching/detail/util_inl.hpp
-- Installing: /usr/local/include/opencv4/opencv2/stitching/detail/warpers.hpp
-- Installing: /usr/local/include/opencv4/opencv2/stitching/detail/warpers_inl.hpp
-- Installing: /usr/local/include/opencv4/opencv2/stitching/warpers.hpp
-- Installing: /usr/local/lib/libopencv_superres.so.4.9.0
-- Installing: /usr/local/lib/libopencv_superres.so.409
-- Set runtime path of "/usr/local/lib/libopencv_superres.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_superres.so
-- Installing: /usr/local/include/opencv4/opencv2/superres.hpp
-- Installing: /usr/local/include/opencv4/opencv2/superres/optical_flow.hpp
-- Installing: /usr/local/lib/libopencv_tracking.so.4.9.0
-- Installing: /usr/local/lib/libopencv_tracking.so.409
-- Set runtime path of "/usr/local/lib/libopencv_tracking.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_tracking.so
-- Installing: /usr/local/include/opencv4/opencv2/tracking.hpp
-- Installing: /usr/local/include/opencv4/opencv2/tracking/feature.hpp
-- Installing: /usr/local/include/opencv4/opencv2/tracking/kalman_filters.hpp
-- Installing: /usr/local/include/opencv4/opencv2/tracking/onlineBoosting.hpp
-- Installing: /usr/local/include/opencv4/opencv2/tracking/tldDataset.hpp
-- Installing: /usr/local/include/opencv4/opencv2/tracking/tracking.hpp
-- Installing: /usr/local/include/opencv4/opencv2/tracking/tracking_by_matching.hpp
-- Installing: /usr/local/include/opencv4/opencv2/tracking/tracking_internals.hpp
-- Installing: /usr/local/include/opencv4/opencv2/tracking/tracking_legacy.hpp
-- Installing: /usr/local/lib/libopencv_stereo.so.4.9.0
-- Installing: /usr/local/lib/libopencv_stereo.so.409
-- Set runtime path of "/usr/local/lib/libopencv_stereo.so.4.9.0" to "/usr/local/lib"
-- Installing: /usr/local/lib/libopencv_stereo.so
-- Installing: /usr/local/include/opencv4/opencv2/stereo.hpp
-- Installing: /usr/local/include/opencv4/opencv2/stereo/descriptor.hpp
-- Installing: /usr/local/include/opencv4/opencv2/stereo/quasi_dense_stereo.hpp
-- Installing: /usr/local/include/opencv4/opencv2/stereo/stereo.hpp
-- Installing: /usr/local/share/java/opencv4/libopencv_java490.so
-- Set runtime path of "/usr/local/share/java/opencv4/libopencv_java490.so" to "/usr/local/lib"
-- Installing: /usr/local/share/java/opencv4/opencv-490.jar
-- Installing: /usr/local/share/opencv4/haarcascades/haarcascade_eye.xml
-- Installing: /usr/local/share/opencv4/haarcascades/haarcascade_eye_tree_eyeglasses.xml
-- Installing: /usr/local/share/opencv4/haarcascades/haarcascade_frontalcatface.xml
-- Installing: /usr/local/share/opencv4/haarcascades/haarcascade_frontalcatface_extended.xml
-- Installing: /usr/local/share/opencv4/haarcascades/haarcascade_frontalface_alt.xml
-- Installing: /usr/local/share/opencv4/haarcascades/haarcascade_frontalface_alt2.xml
-- Installing: /usr/local/share/opencv4/haarcascades/haarcascade_frontalface_alt_tree.xml
-- Installing: /usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml
-- Installing: /usr/local/share/opencv4/haarcascades/haarcascade_fullbody.xml
-- Installing: /usr/local/share/opencv4/haarcascades/haarcascade_lefteye_2splits.xml
-- Installing: /usr/local/share/opencv4/haarcascades/haarcascade_license_plate_rus_16stages.xml
-- Installing: /usr/local/share/opencv4/haarcascades/haarcascade_lowerbody.xml
-- Installing: /usr/local/share/opencv4/haarcascades/haarcascade_profileface.xml
-- Installing: /usr/local/share/opencv4/haarcascades/haarcascade_righteye_2splits.xml
-- Installing: /usr/local/share/opencv4/haarcascades/haarcascade_russian_plate_number.xml
-- Installing: /usr/local/share/opencv4/haarcascades/haarcascade_smile.xml
-- Installing: /usr/local/share/opencv4/haarcascades/haarcascade_upperbody.xml
-- Installing: /usr/local/share/opencv4/lbpcascades/lbpcascade_frontalcatface.xml
-- Installing: /usr/local/share/opencv4/lbpcascades/lbpcascade_frontalface.xml
-- Installing: /usr/local/share/opencv4/lbpcascades/lbpcascade_frontalface_improved.xml
-- Installing: /usr/local/share/opencv4/lbpcascades/lbpcascade_profileface.xml
-- Installing: /usr/local/share/opencv4/lbpcascades/lbpcascade_silverware.xml
-- Installing: /usr/local/bin/opencv_annotation
-- Set runtime path of "/usr/local/bin/opencv_annotation" to "/usr/local/lib"
-- Installing: /usr/local/bin/opencv_visualisation
-- Set runtime path of "/usr/local/bin/opencv_visualisation" to "/usr/local/lib"
-- Installing: /usr/local/bin/opencv_interactive-calibration
-- Set runtime path of "/usr/local/bin/opencv_interactive-calibration" to "/usr/local/lib"
-- Installing: /usr/local/bin/opencv_version
-- Set runtime path of "/usr/local/bin/opencv_version" to "/usr/local/lib"
-- Installing: /usr/local/bin/opencv_model_diagnostics
-- Set runtime path of "/usr/local/bin/opencv_model_diagnostics" to "/usr/local/lib"
@edidada ➜ /workspaces/github_codespaces_compile/build (main) $ 


## 版本

4.9.0
opencv/4.5.5