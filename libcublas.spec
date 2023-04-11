%global debug_package %{nil}
%global __strip /bin/true
%global _missing_build_ids_terminate_build 0
%global _build_id_links none
%global major_package_version 12-0

Name:           libcublas
Epoch:          1
Version:        12.1.0.26
Release:        1%{?dist}
Summary:        NVIDIA CUDA Basic Linear Algebra Subroutines (cuBLAS) libraries
License:        CUDA Toolkit
URL:            https://developer.nvidia.com/cuda-toolkit
ExclusiveArch:  x86_64 ppc64le aarch64

Source0:        https://developer.download.nvidia.com/compute/cuda/redist/%{name}/linux-x86_64/%{name}-linux-x86_64-%{version}-archive.tar.xz
Source1:        https://developer.download.nvidia.com/compute/cuda/redist/%{name}/linux-ppc64le/%{name}-linux-ppc64le-%{version}-archive.tar.xz
Source2:        https://developer.download.nvidia.com/compute/cuda/redist/%{name}/linux-aarch64/%{name}-linux-aarch64-%{version}-archive.tar.xz
Source3:        cublas.pc
Source4:        cublasLt.pc

Requires(post): ldconfig
Conflicts:      %{name}-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
# Drop in 11.7:
Provides:       cuda-cublas = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      cuda-cublas < %{?epoch:%{epoch}:}%{version}-%{release}

%description
The NVIDIA CUDA Basic Linear Algebra Subroutines (cuBLAS) library is a
GPU-accelerated version of the complete standard BLAS library that delivers 6x
to 17x faster performance than the latest MKL BLAS.

%package devel
Summary:        Development files for NVIDIA CUDA Basic Linear Algebra Subroutines (cuBLAS)
Requires:       %{name}%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-devel-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
# Drop in 11.7:
Provides:       cuda-cublas-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      cuda-cublas-devel < %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
This package provides development files for the NVIDIA CUDA Basic Linear
Algebra Subroutines (cuBLAS) libraries.

%package static
Summary:        Static libraries for NVIDIA CUDA Basic Linear Algebra Subroutines (cuBLAS)
Requires:       %{name}-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
# Drop in 11.7:
Provides:       cuda-cublas-static = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      cuda-cublas-static < %{?epoch:%{epoch}:}%{version}-%{release}

%description static
This package contains static libraries for the NVIDIA CUDA Basic Linear Algebra
Subroutines (cuBLAS).

%prep
%ifarch x86_64
%setup -q -n %{name}-linux-x86_64-%{version}-archive
%endif

%ifarch ppc64le
%setup -q -T -b 1 -n %{name}-linux-ppc64le-%{version}-archive
%endif

%ifarch aarch64
%setup -q -T -b 2 -n %{name}-linux-aarch64-%{version}-archive
%endif

%install
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_libdir}/pkgconfig/

cp -fr include/* %{buildroot}%{_includedir}/
cp -fr lib/lib* %{buildroot}%{_libdir}/
cp -fr %{SOURCE3} %{SOURCE4} %{buildroot}/%{_libdir}/pkgconfig/

# Set proper variables
sed -i \
    -e 's|CUDA_VERSION|%{version}|g' \
    -e 's|LIBDIR|%{_libdir}|g' \
    -e 's|INCLUDE_DIR|%{_includedir}|g' \
    %{buildroot}/%{_libdir}/pkgconfig/*.pc

%{?ldconfig_scriptlets}

%files
%license LICENSE
%{_libdir}/libcublas.so.*
%{_libdir}/libcublasLt.so.*
%{_libdir}/libnvblas.so.*

%files devel
%doc src
%{_includedir}/nvblas.h
%{_includedir}/cublasLt.h
%{_includedir}/cublas_v2.h
%{_includedir}/cublas.h
%{_includedir}/cublas_api.h
%{_includedir}/cublasXt.h
%{_libdir}/libcublas.so
%{_libdir}/libcublasLt.so
%{_libdir}/libnvblas.so
%{_libdir}/pkgconfig/cublas.pc
%{_libdir}/pkgconfig/cublasLt.pc

%files static
%{_libdir}/libcublas_static.a
%{_libdir}/libcublasLt_static.a

%changelog
* Tue Apr 11 2023 Simone Caronni <negativo17@gmail.com> - 1:12.1.0.26-1
- Update to 12.1.0.26.

* Sat Feb 25 2023 Simone Caronni <negativo17@gmail.com> - 1:12.0.2.224-1
- Update to 12.0.2.224.

* Tue Dec 13 2022 Simone Caronni <negativo17@gmail.com> - 1:12.0.1.189-1
- Update to 12.0.1.189.

* Fri Nov 11 2022 Simone Caronni <negativo17@gmail.com> - 1:11.11.3.6-1
- Update to 11.11.3.6.
- Use aarch64 archive in place of sbsa.

* Sun Sep 04 2022 Simone Caronni <negativo17@gmail.com> - 1:11.10.3.66-1
- Update to 11.10.3.66.

* Thu Jun 23 2022 Simone Caronni <negativo17@gmail.com> - 1:11.10.1.25-1
- Update to 11.10.1.25.

* Thu Mar 31 2022 Simone Caronni <negativo17@gmail.com> - 1:11.9.2.110-1
- Update to 11.9.2.110 (CUDA 11.6.2).

* Wed Jan 26 2022 Simone Caronni <negativo17@gmail.com> - 1:11.8.1.74-1
- First build with the new tarball components.

