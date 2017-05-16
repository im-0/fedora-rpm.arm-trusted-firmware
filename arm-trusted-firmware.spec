# Main version is relevant but initially we'll likely be pulling in snapshots
#global candidate rc2

# Binaries not used in standard manner so debuginfo is useless
%global debug_package %{nil}

Name:      arm-trusted-firmware
Version:   1.3
Release:   2%{?candidate:.%{candidate}}%{?dist}
Summary:   ARM Trusted Firmware
License:   BSD
URL:       https://github.com/ARM-software/arm-trusted-firmware/wiki
Source0:   https://github.com/ARM-software/arm-trusted-firmware/archive/v%{version}.tar.gz
# https://github.com/apritzel/arm-trusted-firmware/tree/allwinner
Source1:   arm-trusted-firmware-AW-aa75c8d.tar.gz

# At the moment we're only building on aarch64
ExclusiveArch: aarch64

BuildRequires:  dtc
BuildRequires:  gcc

%description
ARM Trusted firmware is a reference implementation of secure world software for
ARMv8-A including Exception Level 3 (EL3) software. It provides a number of
standard ARM interfaces like Power State Coordination (PSCI), Trusted Board
Boot Requirements (TBBR) and Secure Monitor.

Note: the contents of this package are generally just consumed by bootloaders
such as u-boot. As such the binaries aren't of general interest to users.

%ifarch aarch64
%package     -n arm-trusted-firmware-armv8
Summary:     ARM Trusted Firmware for ARMv8-A

%description -n arm-trusted-firmware-armv8
ARM Trusted Firmware binaries for various  ARMv8-A SoCs.

Note: the contents of this package are generally just consumed by bootloaders
such as u-boot. As such the binaries aren't of general interest to users.
%endif

%prep
%setup -q -n %{name}-%{version}%{?candidate:-%{candidate}}

tar xf %{SOURCE1}

%build

%ifarch aarch64
#for soc in juno rk3368 rk3399
#do
## At the moment we're only making the secure firmware (bl31)
#make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" PLAT=$(echo $soc) bl31
#done

# Build AllWinner branch
pushd arm-trusted-firmware-AW
for soc in sun50iw1p1
do
# At the moment we're only making the secure firmware (bl31)
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" PLAT=$(echo $soc) bl31
done
popd
%endif


%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}

%ifarch aarch64
#for soc in juno rk3368 rk3399
#do
#mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/$(echo $soc)/
# for file in bl31.bin
# do
#  if [ -f build/$(echo $soc)/release/$(echo $file) ]; then
#    install -p -m 0644 build/$(echo $soc)/release/$(echo $file) /$RPM_BUILD_ROOT%{_datadir}/%{name}/$(echo $soc)/
#  fi
# done
#done

# Install AllWinner branch
pushd arm-trusted-firmware-AW
for soc in sun50iw1p1
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/$(echo $soc)/
 for file in bl31.bin
 do
  if [ -f build/$(echo $soc)/release/$(echo $file) ]; then
    install -p -m 0644 build/$(echo $soc)/release/$(echo $file) /$RPM_BUILD_ROOT%{_datadir}/%{name}/$(echo $soc)/
  fi
 done
done
popd
%endif

%ifarch aarch64
%files -n arm-trusted-firmware-armv8
%license license.md
%{_datadir}/%{name}
%endif

%changelog
* Tue Apr 25 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.3-2
- Add support for AllWinner SoCs

* Mon Apr 24 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.3-1
- Initial package
