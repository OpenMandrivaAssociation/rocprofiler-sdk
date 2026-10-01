# Modern ROCm profiler SDK (includes ROCTx). TheRock 10.0.

Name:		rocprofiler-sdk
Version:	10.0.0
Release:	1
Summary:	ROCm performance analysis SDK
License:	MIT
Group:		Development/Tools
URL:		https://github.com/ROCm/rocm-systems
Source0:	https://github.com/ROCm/rocm-systems/releases/download/therock-10.0/rocprofiler-sdk.tar.gz#/rocprofiler-sdk-%{version}.tar.gz
# Empty git submodules in the release tarball. Unpacked in %%prep so
# cmake does not try to clone them. Builders have no network.
Source1:	cereal-rocprofiler.tar.gz
Source2:	ELFIO-Release_3.12.tar.gz
Source3:	GOTCHA-rocprofiler.tar.gz
Source4:	PTL-rocprofiler.tar.gz
Source5:	perfetto-sdk-v44.0.tar.xz
Source6:	otf2-3.0.3.tar.gz
Patch0:		rocprofiler-sdk-system-json.patch
Patch1:		rocprofiler-sdk-offline-otf2.patch
Patch2:		rocprofiler-sdk-clang.patch

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
# OTF2 is autotools and is driven by ExternalProject, which calls make.
BuildRequires:	make
BuildRequires:	hipcc
BuildRequires:	rocm-hip-devel
BuildRequires:	rocm-runtime-devel
BuildRequires:	cmake(rocprofiler-register)
BuildRequires:	aqlprofile-devel
BuildRequires:	pkgconfig(libdw)
BuildRequires:	pkgconfig(libelf)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	cmake(rocm-core)
BuildRequires:	cmake(fmt)
BuildRequires:	cmake(absl)
BuildRequires:	cmake(yaml-cpp)
BuildRequires:	cmake(pybind11)
BuildRequires:	cmake(nlohmann_json)
BuildRequires:	pkgconfig(sqlite3)

%description
rocprofiler-sdk provides rocprofv3, librocprofiler-sdk, and
librocprofiler-sdk-roctx (the TheRock replacement for
libroctx64). PyTorch Kineto and RCCL ROCTx look for this.

%package devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name}%{?_isa} = %{EVRD}

%description devel
Headers and CMake package for rocprofiler-sdk.

%prep
%autosetup -n rocprofiler-sdk -p1
tar -C external/cereal --strip-components=1 -xf %{SOURCE1}
tar -C external/elfio --strip-components=1 -xf %{SOURCE2}
# ELFIO 3.12 uses uint16_t before including cstdint. Clang rejects that.
sed -i '0,/^#ifdef __cplusplus$/s//#ifdef __cplusplus\n#include <cstdint>/' external/elfio/elfio/elf_types.hpp
tar -C external/gotcha --strip-components=1 -xf %{SOURCE3}
tar -C external/ptl --strip-components=1 -xf %{SOURCE4}
tar -C external/perfetto --strip-components=1 -xf %{SOURCE5}
tar -C %{_builddir} -xf %{SOURCE6}

%build
# ATT quick scan needs rocprof-trace-decoder, which is not packaged.
%cmake %{rocm_cmake_fhs} \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DROCPROFILER_BUILD_TESTS=OFF \
	-DROCPROFILER_BUILD_SAMPLES=OFF \
	-DROCPROFILER_BUILD_BENCHMARK=OFF \
	-DROCPROFILER_BUILD_DOCS=OFF \
	-DROCPROFILER_BUILD_FMT=OFF \
	-DROCPROFILER_BUILD_GHC_FS=OFF \
	-DROCPROFILER_BUILD_ABSEIL=OFF \
	-DROCPROFILER_BUILD_YAML_CPP=OFF \
	-DROCPROFILER_BUILD_PYBIND11=OFF \
	-DROCPROFILER_DISABLE_ATT_QUICK_SCAN=ON \
	-DROCM_PATH=%{_prefix} \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

%files
%license LICENSE.md
%doc README.md CHANGELOG.md
%{_libdir}/librocprofiler-sdk.so.*
%{_libdir}/librocprofiler-sdk-roctx.so.*
%{_bindir}/rocprofv3
%{_libdir}/rocprofiler-sdk/

%files devel
%{_includedir}/rocprofiler-sdk/
%{_libdir}/librocprofiler-sdk.so
%{_libdir}/librocprofiler-sdk-roctx.so
%{_libdir}/cmake/rocprofiler-sdk/
