# Main version is relevant but initially we'll likely be pulling in snapshots
%global candidate rc0
# git archive --format=tar --prefix=arm-trusted-firmware-1.3/ 38fe380 | xz > arm-trusted-firmware-1.3-38fe380.tar.xz
#global githash 38fe380

# Binaries not used in standard manner so debuginfo is useless
%global debug_package %{nil}

Name:      arm-trusted-firmware
Version:   1.4
Release:   0.1%{?candidate:.%{candidate}}%{?githash:.%{githash}}%{?dist}
Summary:   ARM Trusted Firmware
License:   BSD
URL:       https://github.com/ARM-software/arm-trusted-firmware/wiki

Source0:   https://github.com/ARM-software/arm-trusted-firmware/archive/v%{version}-rc0.tar.gz
# Source0:   %{name}-%{version}-%{githash}.tar.xz
# https://github.com/apritzel/arm-trusted-firmware/tree/allwinner
Source1:   arm-trusted-firmware-AW-aa75c8d.tar.gz

# At the moment we're only building on aarch64
ExclusiveArch: aarch64

BuildRequires:  dtc
BuildRequires:  gcc
# This is needed for rk3399 which while aarch64 has an onboard Cortex-M0 base PMU
BuildRequires:  gcc-arm-linux-gnu

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

# Fix the name of the cross compile for the rk3399 Cortex-M0 PMU
sed -i 's/arm-none-eabi-/arm-linux-gnu-/' plat/rockchip/rk3399/drivers/m0/Makefile
tar xf %{SOURCE1}

%build

%ifarch aarch64
for soc in juno rk3399 rk3368 rk3328 hikey hikey960
do
# At the moment we're only making the secure firmware (bl31)
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" PLAT=$(echo $soc) bl31
done

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
for soc in juno rk3399 rk3368 rk3328 hikey hikey960
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/$(echo $soc)/
 for file in bl31.bin
 do
  if [ -f build/$(echo $soc)/release/$(echo $file) ]; then
    install -p -m 0644 build/$(echo $soc)/release/$(echo $file) /$RPM_BUILD_ROOT%{_datadir}/%{name}/$(echo $soc)/
  fi
 done
done

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
* Fri Jun 30 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.4-0.1-rc0
- New 1.4 rc0 release
- Build hikey960

* Thu Jun  8 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.3-3.f9a050e
- Move to upstream git snapshot
- Build new hikey and rk3328

* Tue Apr 25 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.3-2
- Add support for AllWinner SoCs

* Mon Apr 24 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.3-1
- Initial package
