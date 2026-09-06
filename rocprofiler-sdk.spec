# Modern ROCm profiler SDK (includes ROCTx). TheRock 10.0.

Name:		rocprofiler-sdk
Version:	10.0.0
Release:	1
Summary:	ROCm performance analysis SDK
License:	MIT
Group:		Development/Tools
URL:		https://github.com/ROCm/rocm-systems
Source0:	https://github.com/ROCm/rocm-systems/releases/download/therock-10.0/rocprofiler-sdk.tar.gz#/rocprofiler-sdk-%{version}.tar.gz

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
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
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(yaml-0.1)

%description
rocprofiler-sdk provides rocprofv3, librocprofiler-sdk, and
librocprofiler-sdk-roctx (the TheRock replacement for
libroctx64). PyTorch Kineto and RCCL ROCTx look for this.

%package devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and CMake package for rocprofiler-sdk.

%prep
%autosetup -n rocprofiler-sdk -p1

%build
%cmake %{rocm_cmake_fhs} \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DROCPROFILER_BUILD_TESTS=OFF \
	-DROCPROFILER_BUILD_SAMPLES=OFF \
	-DROCPROFILER_BUILD_BENCHMARK=OFF \
	-DROCPROFILER_BUILD_DOCS=OFF \
	-DROCPROFILER_BUILD_FMT=OFF \
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
