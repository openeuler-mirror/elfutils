# -*- rpm-spec from http://elfutils.org/ -*-
Name: elfutils
Version: 0.187
Release: 12
Summary: A collection of utilities and DSOs to handle ELF files and DWARF data
URL: http://elfutils.org/
License: GPLv3+ and (GPLv2+ or LGPLv3+)
Source: ftp://sourceware.org/pub/elfutils/%{version}/elfutils-%{version}.tar.bz2

Patch0: Fix-segfault-in-eu-ar-m.patch
Patch1: Fix-error-of-parsing-object-file-perms.patch
Patch2: Fix-issue-of-moving-files-by-ar-or-br.patch
Patch3: Get-instance-correctly-for-eu-ar-N-option.patch
Patch4: elfutils-Add-sw64-architecture.patch
Patch5: backport-PR29926-debuginfod-Fix-usage-of-deprecated-CURLINFO_.patch
Patch6: backport-debuginfod-Define-CURL_AT_LEAST_VERSION-if-necessary.patch
Patch7: backport-debuginfod-client-Use-CURLOPT_PROTOCOLS_STR-for-libc.patch

Requires: elfutils-libelf = %{version}-%{release}
Requires: elfutils-libs = %{version}-%{release}
Requires: glibc >= 2.7 libstdc++
Recommends: elfutils-extra

BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: gcc >= 4.1.2-33 m4 zlib-devel gdb-headless gcc-c++
BuildRequires: bzip2-devel xz-devel xz-libs zstd-devel

#for debuginfod
BuildRequires: pkgconfig(libmicrohttpd) >= 0.9.33
BuildRequires: pkgconfig(libcurl) >= 7.29.0
BuildRequires: pkgconfig(sqlite3) >= 3.7.17
BuildRequires: pkgconfig(libarchive) >= 3.1.2

%define _gnu %{nil}
%define _programprefix eu-

%description
Elfutils is a collection of utilities, including stack (to show
backtraces), nm (for listing symbols from object files), size
(for listing the section sizes of an object or archive file),
strip (for discarding symbols), elflint (to check for well-formed ELF files) and
elfcompress (to compress or decompress ELF sections).
Also included are helper libraries which implement DWARF, ELF,
and machine-specific ELF handling and process introspection.
It also provides a DSO which allows reading and
writing ELF files on a high level. Third party programs depend on
this package to read internals of ELF files. 
Yama sysctl setting to enable default attach scope settings
enabling programs to use ptrace attach, access to
/proc/PID/{mem,personality,stack,syscall}, and the syscalls
process_vm_readv and process_vm_writev which are used for
interprocess services, communication and introspection
(like synchronisation, signaling, debugging, tracing and
profiling) of processes.

%package extra
Summary: extra package including debug tools
Provides: elfutils-extra
Requires: elfutils = %{version}-%{release}

%description extra
The extra package contains debug tools.
readelf - to see the raw ELF file structures

%package libs
Summary: Libraries to handle compiled objects
License: GPLv2+ or LGPLv3+
Requires: elfutils-libelf = %{version}-%{release}
Requires: default-yama-scope

%description libs
The elfutils-libs package contains libraries which implement DWARF, ELF,
and machine-specific ELF handling and process introspection.  These
libraries are used by the programs in the elfutils package.  The
elfutils-devel package enables building other programs using these
libraries.

%package devel
Summary: Development libraries to handle compiled objects.
License: GPLv2+ or LGPLv3+
Provides:  elfutils-libelf-devel-static elfutils-devel-static
Obsoletes: elfutils-libelf-devel-static < %{version}-%{release} elfutils-devel-static < %{version}-%{release}
Requires: elfutils-libs = %{version}-%{release}
Requires: elfutils-libelf-devel = %{version}-%{release}

%description devel
The elfutils-devel package contains the libraries to create
applications for handling compiled objects.  libebl provides some
higher-level ELF access functionality.  libdw provides access to
the DWARF debugging information.  libasm provides a programmable
assembler interface. libelf allows you to
access the internals of the ELF object file format, so you can see the
different sections of an ELF file.

%package libelf
Summary: Library to read and write ELF files
License: GPLv2+ or LGPLv3+

%description libelf
The elfutils-libelf package provides a DSO which allows reading and
writing ELF files on a high level.  Third party programs depend on
this package to read internals of ELF files.  The programs of the
elfutils package use it also to generate new ELF files.

%package libelf-devel
Summary: Development support for libelf
License: GPLv2+ or LGPLv3+
Requires: elfutils-libelf = %{version}-%{release}
Conflicts: libelf-devel

%description libelf-devel
The elfutils-libelf-devel package contains the libraries to create
applications for handling compiled objects.  libelf allows you to
access the internals of the ELF object file format, so you can see the
different sections of an ELF file.

%package default-yama-scope
Summary: Default yama attach scope sysctl setting
License: GPLv2+ or LGPLv3+
Provides: default-yama-scope
BuildArch: noarch

%description default-yama-scope
Yama sysctl setting to enable default attach scope settings
enabling programs to use ptrace attach, access to
/proc/PID/{mem,personality,stack,syscall}, and the syscalls
process_vm_readv and process_vm_writev which are used for
interprocess services, communication and introspection
(like synchronisation, signaling, debugging, tracing and
profiling) of processes.

%package help
Summary: Help documents for elfutils

%description help
This package contains help documents for elfutils

%package debuginfod-client
Summary: Library and command line client for build-id HTTP ELF/DWARF server
License: GPLv3+ and (GPLv2+ or LGPLv3+)

%package debuginfod-client-devel
Summary: Libraries and headers to build debuginfod client applications
License: GPLv2+ or LGPLv3+

%package debuginfod
Summary: HTTP ELF/DWARF file server addressed by build-id
License: GPLv3+
BuildRequires: systemd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(pre): shadow-utils
# To extract .deb files with a bsdtar (=libarchive) subshell
Requires: bsdtar

%description debuginfod-client
The elfutils-debuginfod-client package contains shared libraries
dynamically loaded from -ldw, which use a debuginfod service
to look up debuginfo and associated data. Also includes a
command-line frontend.

%description debuginfod-client-devel
The elfutils-debuginfod-client-devel package contains the libraries
to create applications to use the debuginfod service.

%description debuginfod
The elfutils-debuginfod package contains the debuginfod binary
and control files for a service that can provide ELF/DWARF
files to remote clients, based on build-id identification.
The ELF/DWARF file searching functions in libdwfl can query
such servers to download those files on demand.

%prep
%setup -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%ifarch sw_64
%patch4 -p1
%endif
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
%if "%toolchain" == "clang"
  CFLAGS="$CFLAGS -Wno-error=gnu-variable-sized-type-not-at-end -Wno-error=unused-but-set-variable -Wno-error=unused-but-set-parameter"
  CXXFLAGS="$CXXFLAGS -Wno-error=unused-const-variable"
%endif

%configure --program-prefix=%{_programprefix}
%make_build

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}

%make_install
chmod +x ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/lib*.so*

rm ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/debuginfod.sh
rm ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/debuginfod.csh

install -Dm0644 config/10-default-yama-scope.conf ${RPM_BUILD_ROOT}%{_sysctldir}/10-default-yama-scope.conf
install -Dm0644 config/debuginfod.service ${RPM_BUILD_ROOT}%{_unitdir}/debuginfod.service
install -Dm0644 config/debuginfod.sysconfig ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/debuginfod
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/cache/debuginfod
touch ${RPM_BUILD_ROOT}%{_localstatedir}/cache/debuginfod/debuginfod.sqlite

%check
# run-debuginfod-find.sh is a bad test
%make_build check || (cat tests/test-suite.log; true)

%clean
rm -rf ${RPM_BUILD_ROOT}

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig
%post libelf -p /sbin/ldconfig
%postun libelf -p /sbin/ldconfig
%post debuginfod-client -p /sbin/ldconfig
%postun debuginfod-client -p /sbin/ldconfig

%post default-yama-scope
if [ -x /usr/lib/systemd/systemd-sysctl ] ; then
%sysctl_apply 10-default-yama-scope.conf
fi

%files
%defattr(-,root,root)
%license COPYING COPYING-GPLV2 COPYING-LGPLV3
%doc README TODO CONTRIBUTING
%{_bindir}/eu-elfcompress
%{_bindir}/eu-strip
%{_bindir}/eu-addr2line
%{_bindir}/eu-ar
%{_bindir}/eu-elfclassify
%{_bindir}/eu-elfcmp
%{_bindir}/eu-elflint
%{_bindir}/eu-findtextrel
%{_bindir}/eu-make-debug-archive
%{_bindir}/eu-ranlib
%{_bindir}/eu-size
%{_bindir}/eu-stack
%{_bindir}/eu-strings
%{_bindir}/eu-unstrip

%files libs
%license COPYING-GPLV2 COPYING-LGPLV3
%{_libdir}/libasm-%{version}.so
%{_libdir}/libdw-%{version}.so
%{_libdir}/libasm.so.*
%{_libdir}/libdw.so.*

%files extra
%{_bindir}/eu-objdump
%{_bindir}/eu-readelf
%{_bindir}/eu-nm

%files devel
%defattr(-,root,root)
%{_includedir}/dwarf.h
%dir %{_includedir}/elfutils
%{_includedir}/elfutils/elf-knowledge.h
%{_includedir}/elfutils/known-dwarf.h
%{_includedir}/elfutils/libasm.h
%{_includedir}/elfutils/libdw.h
%{_includedir}/elfutils/libdwelf.h
%{_includedir}/elfutils/libdwfl.h
%{_includedir}/elfutils/version.h
%{_libdir}/libasm.a
%{_libdir}/libasm.so
%{_libdir}/libdw.a
%{_libdir}/libdw.so
%{_libdir}/libelf.a
%{_libdir}/pkgconfig/libdw.pc

%files libelf
%license COPYING-GPLV2 COPYING-LGPLV3
%{_libdir}/libelf-%{version}.so
%{_libdir}/libelf.so.*
%{_datadir}/locale/*/LC_MESSAGES/elfutils.mo

%files libelf-devel
%{_includedir}/libelf.h
%{_includedir}/gelf.h
%{_includedir}/nlist.h
%{_libdir}/libelf.so
%{_libdir}/pkgconfig/libelf.pc

%files default-yama-scope
%{_sysctldir}/10-default-yama-scope.conf

%files help
%{_mandir}/man1/eu-*.1*
%{_mandir}/man1/debuginfod-find.1*
%{_mandir}/man3/debuginfod_*.3*
%{_mandir}/man3/elf_*.3*
%{_mandir}/man7/debuginfod*.7.*
%{_mandir}/man8/debuginfod.8*

%files debuginfod-client
%defattr(-,root,root)
%{_libdir}/libdebuginfod-%{version}.so
%{_bindir}/debuginfod-find
%{_libdir}/libdebuginfod.so.*

%files debuginfod-client-devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/libdebuginfod.pc
%{_includedir}/elfutils/debuginfod.h
%{_libdir}/libdebuginfod.so
 
%files debuginfod
%defattr(-,root,root)
%{_bindir}/debuginfod
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/debuginfod
%{_unitdir}/debuginfod.service
%{_sysconfdir}/sysconfig/debuginfod

%dir %attr(0700,debuginfod,debuginfod) %{_localstatedir}/cache/debuginfod
%verify(not md5 size mtime) %attr(0600,debuginfod,debuginfod) %{_localstatedir}/cache/debuginfod/debuginfod.sqlite

%pre debuginfod
getent group debuginfod >/dev/null || groupadd -r debuginfod
getent passwd debuginfod >/dev/null || \
  useradd -r -g debuginfod -d /var/cache/debuginfod -s /sbin/nologin \
          -c "elfutils debuginfo server" debuginfod
exit 0

%post debuginfod
%systemd_post debuginfod.service

%postun debuginfod
%systemd_postun_with_restart debuginfod.service

%changelog
* Tue Apr 25 2023 jammyjellyfish <jammyjellyfish255@outlook.com> - 0.187-12
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:Fix clang build error

* Fri Mar 10 2023 yixiangzhike<yixiangzhike007@163.com> - 0.187-11
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:Fix failure of compiling with curl-7.88.1

* Mon Nov 14 2022 wuzx<wuzx1226@qq.com> - 0.187-10
- Type:feature
- CVE:NA
- SUG:NA
- DESC:Add sw64 architecture

* Tue Nov 1 2022 zhangruifang <zhangruifang1@h-partners.com> - 0.187-9
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Delete the permission(750) setting for eu-*

* Tue Sep 20 2022 hubin <hubin73@huawei.com> - 0.187-8
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:change readelf permission

* Tue Sep 20 2022 hubin <hubin73@huawei.com> - 0.187-7
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:change permission to 750 and move debug tools into extra package

* Fri Sep 9 2022 fuanan <fuanan3@h-partners.com> - 0.187-6
- Fix "/usr/lib64/libdebuginfod.so.1" not found when uninstall elfutils-debuginfod-client-devel
- Fix Obsoletes in spec

* Fri Aug 26 2022 panxiaohe <panxh.life@foxmail.com> - 0.187-5
- Get instance correctly for eu-ar -N option
- Use make macros

* Wed Aug 24 2022 yixiangzhike <yixiangzhike007@163.com> - 0.187-4
- Fix issue of moving files by ar or br

* Tue Aug 16 2022 yixiangzhike <yixiangzhike007@163.com> - 0.187-3
- Fix error of parsing object file perms

* Tue Jul 19 2022 Hugel <gengqihu1@h-partners.com> - 0.187-2
- Add some compression support

* Fri Jul 1 2022 panxiaohe <panxh.life@foxmail.com> - 0.187-1
- update version to 0.187

* Mon Jun 27 2022 zhangruifang <zhangruifang1@h-partners.com> - 0.185-5
- fix segfault in eu-ar -m

* Thu Feb 17 2022 panxiaohe <panxh.life@foxmail.com> - 0.185-4
- fix wrong use of stdin for eu-elfclassify --no-stdin option

* Wed Sep 15 2021 panxiaohe <panxiaohe@huawei.com> - 0.185-3
- detach subpackages elfutils-libs, elfutils-libelf,
  elfutils-libelf-devel, elfutils-default-yama-scope

* Tue Jul 27 2021 panxiaohe <panxiaohe@huawei.com> - 0.185-2
- fix make check about bad test

* Mon Jul 19 2021 panxiaohe <panxiaohe@huawei.com> - 0.185-1
- update version to 0.185

* Sat Jun 5 2021 wangchen <wangchen137@huawei.com> - 0.182-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add gcc-c++ to BuildRequires

* Tue Jan 26 2021 yang_zhuang_zhuang <yangzhuangzhuang1@huawei.com> - 0.182-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update version to 0.182

* Wed Jul 29 2020 yang_zhuang_zhuang <yangzhuangzhuang1@huawei.com> - 0.180-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update version to 0.180

* Thu Oct 10 2019 Yalong Guan <guanyalong@huawei.com> - 0.177-3
- Type: Reorganization
- ID:NA
- SUG:NA
- DESC: move license files to license folder.

* Mon Sep 9 2019 Yalong Guan <guanyalong@huawei.com> - 0.177-2
- Type: Reorganization
- ID:NA
- SUG:restart
- DESC: Repartition files to different packages.

* Tue Aug 13 2019 Mark Wielaard <mark@klomp.org> 0.177-1
- elfclassify: New tool to analyze ELF objects.
- readelf: Print DW_AT_data_member_location as decimal offset.
           Decode DW_AT_discr_list block attributes.
- libdw: Add DW_AT_GNU_numerator, DW_AT_GNU_denominator and DW_AT_GNU_bias.
- libdwelf: Add dwelf_elf_e_machine_string.
            dwelf_elf_begin now only returns NULL when there is an error
            reading or decompressing a file. If the file is not an ELF file
            an ELF handle of type ELF_K_NONE is returned.
- backends: Add support for C-SKY.

* Thu Feb 14 2019 Mark Wielaard <mark@klomp.org> 0.176-1
- build: Add new --enable-install-elfh option.
  Do NOT use this for system installs (it overrides glibc elf.h).
- backends: riscv improved core file and return value location support.
- Fixes CVE-2019-7146, CVE-2019-7148, CVE-2019-7149, CVE-2019-7150,
        CVE-2019-7664, CVE-2019-7665.

* Wed Nov 14 2018 Mark Wielaard <mark@klomp.org> 0.175-1
- readelf: Handle mutliple .debug_macro sections.
  Recognize and parse GNU Property notes, NT_VERSION notes and
  GNU Build Attribute ELF Notes.
- strip: Handle SHT_GROUP correctly.
  Add strip --reloc-debug-sections-only option.
  Handle relocations against GNU compressed sections.
- libdwelf: New function dwelf_elf_begin.
- libcpu: Recognize bpf jump variants BPF_JLT, BPF_JLE, BPF_JSLT
  and BPF_JSLE.
- backends: RISCV handles ADD/SUB relocations.
  Handle SHT_X86_64_UNWIND.
- Fixes CVE-2018-18310, CVE-2018-18520 and CVE-2018-18521.

* Fri Sep 14 2018 Mark Wielaard <mark@klomp> 0.174-1
- libelf, libdw and all tools now handle extended shnum and shstrndx
  correctly.
- elfcompress: Don't rewrite input file if no section data needs
  updating.  Try harder to keep same file mode bits (suid) on rewrite.
- strip: Handle mixed (out of order) allocated/non-allocated sections.
- unstrip: Handle SHT_GROUP sections.
- backends: RISCV and M68K now have backend implementations to
  generate CFI based backtraces.
- Fixes CVE-2018-16062, CVE-2018-16402 and CVE-2018-16403.

* Fri Jun 29 2018 Mark Wielaard,,, <mark@klomp.org> 0.173-1
- More fixes for crashes and hangs found by afl-fuzz. In particular
  various functions now detect and break infinite loops caused by bad
  DIE tree cycles.
- readelf: Will now lookup the size and signedness of constant value
  types to display them correctly (and not just how they were encoded).
- libdw: New function dwarf_next_lines to read CU-less .debug_line data.
  dwarf_begin_elf now accepts ELF files containing just .debug_line
  or .debug_frame sections (which can be read without needing a DIE
  tree from the .debug_info section).
  Removed dwarf_getscn_info, which was never implemented.
- backends: Handle BPF simple relocations.
  The RISCV backends now handles ABI specific CFI and knows about
  RISCV register types and names.

* Mon Jun 11 2018 Mark Wielaard <mark@klomp.org> 0.172-1
- No functional changes compared to 0.171.
- Various bug fixes in libdw and eu-readelf dealing with bad DWARF5
  data. Thanks to running the afl fuzzer on eu-readelf and various
  testcases.
- eu-readelf -N is ~15% faster.

* Fri Jun 01 2018 Mark Wielaard <mark@klomp.org> 0.171-1
- DWARF5 and split dwarf, including GNU DebugFission, support.
- readelf: Handle all new DWARF5 sections.
  --debug-dump=info+ will show split unit DIEs when found.
  --dwarf-skeleton can be used when inspecting a .dwo file.
  Recognizes GNU locviews with --debug-dump=loc.
- libdw: New functions dwarf_die_addr_die, dwarf_get_units,
  dwarf_getabbrevattr_data and dwarf_cu_info.
  libdw will now try to resolve the alt file on first use
  when not set yet with dwarf_set_alt.
  dwarf_aggregate_size() now works with multi-dimensional arrays.
- libdwfl: Use process_vm_readv when available instead of ptrace.
- backends: Add a RISC-V backend.

* Wed Aug  2 2017 Mark Wielaard <mark@klomp.org> 0.170-1
- libdw: Added new DWARF5 attribute, tag, character encoding,
  language code, calling convention, defaulted member function
  and macro constants to dwarf.h.
  New functions dwarf_default_lower_bound and dwarf_line_file.
  dwarf_peel_type now handles DWARF5 immutable, packed and shared tags.
  dwarf_getmacros now handles DWARF5 .debug_macro sections.
- strip: Add -R, --remove-section=SECTION and --keep-section=SECTION.
- backends: The bpf disassembler is now always build on all platforms.

* Fri May  5 2017 Mark Wielaard <mark@klomp.org> 0.169-1
- backends: Add support for EM_PPC64 GNU_ATTRIBUTES.
  Frame pointer unwinding fallback support for i386, x86_64, aarch64.
- translations: Update Polish translation.

* Tue Dec 27 2016 Mark Wielaard <mark@klomp.org> 0.168-1
- http://elfutils.org/ is now hosted at http://sourceware.org/elfutils/
- libelf: gelf_newehdr and gelf_newehdr now return void *.
- libdw: dwarf.h corrected the DW_LANG_PLI constant name (was DW_LANG_PL1).
- readelf: Add optional --symbols[=SECTION] argument to select section name.

* Thu Aug  4 2016 Mark Wielaard <mjw@redhat.com> 0.167-1
- libasm: Add eBPF disassembler for EM_BPF files.
- backends: Add m68k and BPF backends.
- ld: Removed.
- dwelf: Add ELF/DWARF string table creation functions.
  dwelf_strtab_init, dwelf_strtab_add, dwelf_strtab_add_len,
  dwelf_strtab_finalize, dwelf_strent_off, dwelf_strent_str and
  dwelf_strtab_free.

* Thu Mar 31 2016 Mark Wielaard <mjw@redhat.com> 0.166-1
- config: The default program prefix for the installed tools is now
  eu-. Use configure --program-prefix="" to not use a program prefix.

* Fri Jan  8 2016 Mark Wielaard <mjw@redhat.com> 0.165-1
- elfcompress: New utility to compress or decompress ELF sections.
- readelf: Add -z,--decompress option.
- libelf: Add elf_compress, elf_compress_gnu, elf32_getchdr,
  elf64_getchdr and gelf_getchdr.
- libdwelf: New function dwelf_scn_gnu_compressed_size.
- config: Add libelf and libdw pkg-config files.
- backends: sparc support for core and live backtraces.
- translations: Updated Polish translation.

* Thu Oct 15 2015 Mark Wielaard <mjw@redhat.com> 0.164-1
- strip, unstrip: Handle ELF files with merged strtab/shstrtab
  tables. Handle missing SHF_INFO_LINK section flags.
- libelf: Use int64_t for offsets in libelf.h instead of loff_t.
- libdw: dwarf.h Add preliminary DWARF5 DW_LANG_Haskell.
- libdwfl: dwfl_standard_find_debuginfo now searches any subdir of
  the binary path under the debuginfo root when the separate
  debug file couldn't be found by build-id.
  dwfl_linux_proc_attach can now be called before any Dwfl_Modules
  have been reported.
- backends: Better sparc and sparc64 support.
- translations: Updated Ukrainian translation.
- Provide default-yama-scope subpackage.

* Fri Jun 19 2015 Mark Wielaard <mjw@redhat.com> 0.163-1
- Bug fixes only, no new features.

* Wed Jun 10 2015 Mark Wielaard <mjw@redhat.com> 0.162-1
- libdw: Install new header elfutils/known-dwarf.h.
  dwarf.h Add preliminary DWARF5 constants DW_TAG_atomic_type,
  DW_LANG_Fortran03, DW_LANG_Fortran08. dwarf_peel_type now also
  handles DW_TAG_atomic_type.
- addr2line: Input addresses are now always interpreted as
  hexadecimal numbers, never as octal or decimal numbers.
  New option -a, --addresses to print address before each entry.
  New option -C, --demangle to show demangled symbols.
  New option --pretty-print to print all information on one line.
- ar: CVE-2014-9447 Directory traversal vulnerability in ar
  extraction.
- backends: x32 support.

* Thu Dec 18 2014 Mark Wielaard <mjw@redhat.com> 0.161-1
- libdw: New function dwarf_peel_type. dwarf_aggregate_size now uses
  dwarf_peel_type to also provide the sizes of qualified types.
  dwarf_getmacros will now serve either of .debug_macro and
  .debug_macinfo transparently.  New interfaces dwarf_getmacros_off,
  dwarf_macro_getsrcfiles, dwarf_macro_getparamcnt, and
  dwarf_macro_param are available for more generalized inspection of
  macros and their parameters.
  dwarf.h: Add DW_AT_GNU_deleted, DW_AT_noreturn, DW_LANG_C11,
  DW_LANG_C_plus_plus_11 and DW_LANG_C_plus_plus_14.

* Mon Aug 25 2014 Mark Wielaard <mjw@redhat.com> 0.160-1
- libdw: New functions dwarf_cu_getdwarf, dwarf_cu_die.
  dwarf.h remove non-existing DW_TAG_mutable_type.
- libdwfl: Handle LZMA .ko.xz compressed kernel modules.
- unstrip: New option -F, --force to combining files even if some ELF
  headers don't seem to match.
- backends: Handle ARM THUMB functions. Add support for ppc64le ELFv2 abi.

* Sat May 17 2014 Mark Wielaard <mjw@redhat.com> 0.159-1
- stack: New option -d, --debugname to lookup DWARF debuginfo name 
  for frame.  New option -i, --inlines to show inlined frames 
  using DWARF debuginfo.
- libdwelf: New libdwelf.h header for libdw.so DWARF ELF Low-level 
  Functions.  New function dwelf_elf_gnu_debuglink, 
  dwelf_dwarf_gnu_debugaltlink, and dwelf_elf_gnu_build_id.
- libdw: Support for DWZ multifile forms DW_FORM_GNU_ref_alt and      
  DW_FORM_GNU_strp_alt is now enabled by default and no longer        
  experimental. Added new functions dwarf_getalt and dwarf_setalt       
  to get or set the alternative debug file used for the alt FORMs.     
  The dwfl_linux_proc_find_elf callback will now find ELF from       
  process memory for (deleted) files if the Dwfl has process state     
  attached.
- libdwfl: The dwfl_build_id_find_debuginfo and 
  dwfl_standard_find_debuginfo functions will now try to 
  resolve and set the alternative debug file.
- backends: Add CFI unwinding for arm. Relies on .debug_frame.        
  Add arm process initial register state compatible mode to AARCH64. 
  Add aarch64 native and core unwind support.
- other: All separate elfutils-robustify patches have been merged.    
  CVE-2014-0172 Check overflow before calling malloc to uncompress 
  data.

* Fri Jan  3 2014 Mark Wielaard <mjw@redhat.com> 0.158-1
- libdwfl: dwfl_core_file_report has new parameter executable.
  New functions dwfl_module_getsymtab_first_global,
  dwfl_module_getsym_info and dwfl_module_addrinfo.
  Added unwinder with type Dwfl_Thread_Callbacks, opaque types
  Dwfl_Thread and Dwfl_Frame and functions dwfl_attach_state,
  dwfl_pid, dwfl_thread_dwfl, dwfl_thread_tid, dwfl_frame_thread,
  dwfl_thread_state_registers, dwfl_thread_state_register_pc,
  dwfl_getthread_frames, dwfl_getthreads, dwfl_thread_getframes
  and dwfl_frame_pc.
- addr2line: New option -x to show the section an address was found in.
- stack: New utility that uses the new unwinder for processes and cores.
- backends: Unwinder support for i386, x86_64, s390, s390x, ppc and ppc64.
  aarch64 support.

* Mon Sep 30 2013 Mark Wielaard <mjw@redhat.com> 0.157-1
- libdw: Add new functions dwarf_getlocations, dwarf_getlocation_attr 
         and dwarf_getlocation_die.
- readelf: Show contents of NT_SIGINFO and NT_FILE core notes.
- addr2line: Support -i, --inlines output option.
- backends: abi_cfi hook for arm, ppc and s390.

* Thu Jul 25 2013 Jan Kratochvil <jan.kratochvil@redhat.com> 0.156-1
- lib: New macro COMPAT_VERSION_NEWPROTO.
- libdw: Handle GNU extension opcodes in dwarf_getlocation.
- libdwfl: Fix STB_GLOBAL over STB_WEAK preference in 
  dwfl_module_addrsym.          Add minisymtab support.          Add 
  parameter add_p_vaddr to dwfl_report_elf.          Use DT_DEBUG 
  library search first.
- libebl: Handle new core note types in EBL.
- backends: Interpret NT_ARM_VFP.           Implement core file 
  registers parsing for s390/s390x.
- readelf: Add --elf-section input option to inspect an embedded ELF 
  file.          Add -U, --unresolved-address-offsets output control.   
         Add --debug-dump=decodedline support.          Accept version 
  8 .gdb_index section format.          Adjust output formatting width. 
           When highpc is in constant form print it also as address.    
        Display raw .debug_aranges. Use libdw only for decodedaranges.
- elflint: Add __bss_start__ to the list of allowed symbols.
- tests: Add configure --enable-valgrind option to run all tests 
  under valgrind.        Enable automake parallel-tests for make check.
- translations: Updated Polish translation.
- Updates for Automake 1.13.

* Fri Aug 24 2012 Mark Wielaard <mjw@redhat.com> 0.155-1
- libelf: elf*_xlatetomd now works for cross-endian ELF note data.    
       elf_getshdr now works consistently on non-mmaped ELF files after 
          calling elf_cntl(ELF_C_FDREAD).         Implement support for 
  ar archives with 64-bit symbol table.
- libdw: dwarf.h corrected the DW_LANG_ObjC constant name (was 
  DW_LANG_Objc).        Any existing sources using the old name will 
  have to be updated.        Add DW_MACRO_GNU .debug_macro type 
  encodings constants, DW_ATE_UTF        and DW_OP_GNU_parameter_ref to 
  dwarf.h.        Experimental support for DWZ multifile forms 
  DW_FORM_GNU_ref_alt        and DW_FORM_GNU_strp_alt.  Disabled by 
  default.  Use configure        --enable-dwz to test it.
- readelf: Add .debug_macro parsing support.          Add .gdb_index 
  version 7 parsing support.          Recognize DW_OP_GNU_parameter_ref.
- backends: Add support for Tilera TILE-Gx processor.
- translations: Updated Ukrainian translation.

* Fri Jun 22 2012 Mark Wielaard <mjw@redhat.com> 0.154-1
- libelf: [g]elf[32|64]_offscn() do not match SHT_NOBITS sections at 
  OFFSET.
- libdw: dwarf_highpc function now handles DWARF 4 DW_AT_high_pc 
  constant form.        Fix bug using dwarf_next_unit to iterate over 
  .debug_types.
- elflint: Now accepts gold linker produced executables.
- The license is now GPLv2/LGPLv3+ for the libraries and GPLv3+ for 
  stand-alone programs. There is now also a formal CONTRIBUTING 
  document describing how to submit patches.

* Thu Feb 23 2012 Mark Wielaard <mjw@redhat.com> 0.153-1
- libdw: Support reading .zdebug_* DWARF sections compressed via zlib.
- libdwfl: Speed up dwfl_module_addrsym.
- nm: Support C++ demangling.
- ar: Support D modifier for "deterministic output" with no 
  uid/gid/mtime info.     The U modifier is the inverse.     elfutils 
  can be configured with the --enable-deterministic-archives     option 
  to make the D behavior the default when U is not specified.
- ranlib: Support -D and -U flags with same meaning.
- readelf: Improve output of -wline. Add support for printing SDT elf 
  notes.          Add printing of .gdb_index section. 	 Support for 
  typed DWARF stack, call_site and entry_value.
- strip: Add --reloc-debug-sections option.        Improved SHT_GROUP 
  sections handling.

* Tue Feb 15 2011  <drepper@gmail.com> 0.152-1
- Various build and warning nits fixed for newest GCC and Autoconf.
- libdwfl: Yet another prelink-related fix for another regression.
  	 Look for Linux kernel images in files named with compression
  suffixes.
- elfcmp: New flag --ignore-build-id to ignore differing build ID
  bits. 	New flag -l/--verbose to print all differences.

* Wed Jan 12 2011  <drepper@gmail.com> 0.151-1
- libdwfl: Fix for more prelink cases with separate debug file.
- strip: New flag --strip-sections to remove section headers entirely.

* Mon Nov 22 2010  <drepper@gmail.com> 0.150-1
- libdw: Fix for handling huge .debug_aranges section.
- libdwfl: Fix for handling prelinked DSO with separate debug file.
- findtextrel: Fix diagnostics to work with usual section ordering.
- libebl: i386 backend fix for multi-register integer return value
  location.

* Mon Sep 13 2010  <drepper@redhat.com> 0.149-1
- libdw: Decode new DW_OP_GNU_implicit_pointer operation;        new
  function dwarf_getlocation_implicit_pointer.
- libdwfl: New function dwfl_dwarf_line.
- addr2line: New flag -F/--flags to print more DWARF line information
  details.
- strip: -g recognizes .gdb_index as a debugging section.

* Mon Jun 28 2010  <drepper@redhat.com> 0.148-1
- libdw: Accept DWARF 4 format: new functions dwarf_next_unit,
  dwarf_offdie_types.        New functions dwarf_lineisa,
  dwarf_linediscriminator, dwarf_lineop_index.
- libdwfl: Fixes in core-file handling, support cores from PIEs.
  	 When working from build IDs, don't open a named file that
  mismatches.
- readelf: Handle DWARF 4 formats.

* Mon May  3 2010 Ulrich Drepper <drepper@redhat.com> 0.147-1
- libdw: Fixes in CFI handling, best possible handling of bogus CFA
  ops.
- libdwfl: Ignore R_*_NONE relocs, works around old (binutils) ld -r
  bugs.

* Wed Apr 21 2010  <drepper@redhat.com> 0.146-1
- libdwfl: New function dwfl_core_file_report.

* Tue Feb 23 2010 Ulrich Drepper <drepper@redhat.com> 0.145-1
- Fix build with --disable-dependency-tracking.
- Fix build with most recent glibc headers.
- libelf: More robust to bogus section headers.
- libdw: Fix CFI decoding.
- libdwfl: Fix address bias returned by CFI accessors. 	 Fix core
  file module layout identification.
- readelf: Fix CFI decoding.

* Thu Jan 14 2010  <drepper@redhat.com> 0.144-1
- libelf: New function elf_getphdrnum. 	Now support using more than
  65536 program headers in a file.
- libdw: New function dwarf_aggregate_size for computing (constant)
  type        sizes, including array_type cases with nontrivial
  calculation.
- readelf: Don't give errors for missing info under -a.
  Handle Linux "VMCOREINFO" notes under -n.

* Mon Sep 21 2009  <drepper@redhat.com> 0.143-1
- libdw: Various convenience functions for individual attributes now
  use dwarf_attr_integrate to look up indirect inherited
  attributes.  Location expression handling now supports
  DW_OP_implicit_value.
- libdwfl: Support automatic decompression of files in XZ format,
  and of Linux kernel images made with bzip2 or LZMA (as well
  as gzip).

* Mon Jun 29 2009  <drepper@redhat.com> 0.142-1
- libelf: Add elf_getshdrnum alias for elf_getshnum and elf_getshdrstrndx alias
  for elf_getshstrndx and deprecate original names.  Sun screwed up
  their implementation and asked for a solution.
- libebl: Add support for STB_GNU_UNIQUE.
- elflint: Add support for STB_GNU_UNIQUE.
- readelf: Add -N option, speeds up DWARF printing without address->name lookups.
- libdw: Add support for decoding DWARF CFI into location description form.
  Handle some new DWARF 3 expression operations previously omitted.
  Basic handling of some new encodings slated for DWARF

* Thu Apr 23 2009 Ulrich Drepper <drepper@redhat.com> 0.141-1
- libebl: sparc backend fixes; 	some more arm backend support
- libdwfl: fix dwfl_module_build_id for prelinked DSO case;
  fixes in core file support; 	 dwfl_module_getsym interface
  improved for non-address symbols
- strip: fix infinite loop on strange inputs with -f
- addr2line: take -j/--section=NAME option for binutils compatibility
  	   (same effect as '(NAME)0x123' syntax already supported)

* Mon Feb 16 2009 Ulrich Drepper <drepper@redhat.com> 0.140-1
- libelf: Fix regression in creation of section header
- libdwfl: Less strict behavior if DWARF reader ist just used to
  display data

* Thu Jan 22 2009 Ulrich Drepper <drepper@redhat.com> 0.139-1
- libcpu: Add Intel SSE4 disassembler support
- readelf: Implement call frame information and exception handling
  dumping.          Add -e option.  Enable it implicitly for -a.
- elflint: Check PT_GNU_EH_FRAME program header entry.
- libdwfl: Support automatic gzip/bzip2 decompression of ELF files.

* Wed Dec 31 2008 Roland McGrath <roland@redhat.com> 0.138-1
- Install <elfutils/version.h> header file for applications to use in
  source version compatibility checks.
- libebl: backend fixes for i386 TLS relocs; backend support for
  NT_386_IOPERM
- libcpu: disassembler fixes
- libdwfl: bug fixes
- libelf: bug fixes
- nm: bug fixes for handling corrupt input files

* Tue Aug 26 2008 Ulrich Drepper <drepper@redhat.com> 0.137-1
- Minor fixes for unreleased 0.136 release.

* Mon Aug 25 2008 Ulrich Drepper <drepper@redhat.com> 0.136-1
- libdwfl: bug fixes; new segment interfaces;	 all the libdwfl-based
 tools now support --core=COREFILE option

* Mon May 12 2008 Ulrich Drepper <drepper@redhat.com> 0.135-1
- libdwfl: bug fixes
- strip: changed handling of ET_REL files wrt symbol tables and relocs

* Tue Apr  8 2008 Ulrich Drepper <drepper@redhat.com> 0.134-1
- elflint: backend improvements for sparc, alpha
- libdwfl, libelf: bug fixes

* Sat Mar  1 2008 Ulrich Drepper <drepper@redhat.com> 0.133-1
- readelf, elflint, libebl: SHT_GNU_ATTRIBUTE section handling (readelf -A)
- readelf: core note handling for NT_386_TLS, NT_PPC_SPE, Alpha NT_AUXV
- libdwfl: bug fixes and optimization in relocation handling
- elfcmp: bug fix for non-allocated section handling
- ld: implement newer features of binutils linker.

* Mon Jan 21 2008 Ulrich Drepper <drepper@redhat.com> 0.132-1
- libcpu: Implement x86 and x86-64 disassembler.
- libasm: Add interface for disassembler.
- all programs: add debugging of branch prediction.
- libelf: new function elf_scnshndx.

* Sun Nov 11 2007 Ulrich Drepper <drepper@redhat.com> 0.131-1
- libdw: DW_FORM_ref_addr support; dwarf_formref entry point now depreca
ted;       bug fixes for oddly-formatted DWARF
- libdwfl: bug fixes in offline archive support, symbol table handling;
	 apply partial relocations for dwfl_module_address_section on
ET_REL
- libebl: powerpc backend support for Altivec registers

* Mon Oct 15 2007 Ulrich Drepper <drepper@redhat.com> 0.130-1
- readelf: -p option can take an argument like -x for one section,
	 or no argument (as before) for all SHF_STRINGS sections;
	 new option --archive-index (or -c);	 improved -n output fo
r core files, on many machines
- libelf: new function elf_getdata_rawchunk, replaces gelf_rawchunk;
	new functions gelf_getnote, gelf_getauxv, gelf_update_auxv
- readelf, elflint: handle SHT_NOTE sections without requiring phdrs
- elflint: stricter checks on debug sections
- libdwfl: new functions dwfl_build_id_find_elf, dwfl_build_id_find_debu
ginfo,	 dwfl_module_build_id, dwfl_module_report_build_id;	 suppo
rt dynamic symbol tables found via phdrs;	 dwfl_standard_find_de
buginfo now uses build IDs when available
- unstrip: new option --list (or -n)
- libebl: backend improvements for sparc, alpha, powerpc

* Tue Aug 14 2007 Ulrich Drepper <drepper@redhat.com> 0.129-1
- readelf: new options --hex-dump (or -x), --strings (or -p)
- addr2line: new option --symbols (or -S)

* Wed Apr 18 2007 Ulrich Drepper <drepper@redhat.com> 0.127-1
- libdw: new function dwarf_getsrcdirs
- libdwfl: new functions dwfl_module_addrsym, dwfl_report_begin_add,
	 dwfl_module_address_section

* Mon Feb  5 2007 Ulrich Drepper <drepper@redhat.com> 0.126-1
- new program: ar

* Mon Dec 18 2006 Ulrich Drepper <drepper@redhat.com> 0.125-1
- elflint: Compare DT_GNU_HASH tests.
- move archives into -static RPMs
- libelf, elflint: better support for core file handling

* Tue Oct 10 2006 Ulrich Drepper <drepper@redhat.com> 0.124-1
- libebl: sparc backend support for return value location
- libebl, libdwfl: backend register name support extended with more info
- libelf, libdw: bug fixes for unaligned accesses on machines that care
- readelf, elflint: trivial bugs fixed

* Mon Aug 14 2006 Roland McGrath <roland@redhat.com> 0.123-1
- libebl: Backend build fixes, thanks to Stepan Kasal.
- libebl: ia64 backend support for register names, return value location
- libdwfl: Handle truncated linux kernel module section names.
- libdwfl: Look for linux kernel vmlinux files with .debug suffix.
- elflint: Fix checks to permit --hash-style=gnu format.

* Wed Jul 12 2006 Ulrich Drepper <drepper@redhat.com> 0.122-1
- libebl: add function to test for relative relocation
- elflint: fix and extend DT_RELCOUNT/DT_RELACOUNT checks
- elflint, readelf: add support for DT_GNU_HASHlibelf: add elf_gnu_hash
- elflint, readelf: add support for 64-bit SysV-style hash tables
- libdwfl: new functions dwfl_module_getsymtab, dwfl_module_getsym.

* Wed Jun 14 2006  <drepper@redhat.com> 0.121-1
- libelf: bug fixes for rewriting existing files when using mmap.
- make all installed headers usable in C++ code.
- readelf: better output format.
- elflint: fix tests of dynamic section content.
- ld: Implement --as-needed, --execstack, PT_GNU_STACK.  Many small patc
hes.
- libdw, libdwfl: handle files without aranges info.

* Tue Apr  4 2006 Ulrich Drepper <drepper@redhat.com> 0.120-1
- Bug fixes.
- dwarf.h updated for DWARF 3.0 final specification.
- libdwfl: New function dwfl_version.
- The license is now GPL for most files.  The libelf, libebl, libdw,and
libdwfl libraries have additional exceptions.  Add reference toOIN.

* Thu Jan 12 2006 Roland McGrath <roland@redhat.com> 0.119-1
- elflint: more tests.
- libdwfl: New function dwfl_module_register_names.
- libebl: New backend hook for register names.

* Tue Dec  6 2005 Ulrich Drepper <drepper@redhat.com> 0.118-1
- elflint: more tests.
- libdwfl: New function dwfl_module_register_names.
- libebl: New backend hook for register names.

* Thu Nov 17 2005 Ulrich Drepper <drepper@redhat.com> 0.117-1
- libdwfl: New function dwfl_module_return_value_location.
- libebl: Backend improvements for several CPUs.

* Mon Oct 31 2005 Ulrich Drepper <drepper@redhat.com> 0.116-1
- libdw: New functions dwarf_ranges, dwarf_entrypc, dwarf_diecu,       d
warf_entry_breakpoints.  Removed Dwarf_Func type and functions       d
warf_func_name, dwarf_func_lowpc, dwarf_func_highpc,       dwarf_func_
entrypc, dwarf_func_die; dwarf_getfuncs callback now uses       Dwarf_
Die, and dwarf_func_file, dwarf_func_line, dwarf_func_col       replac
ed by dwarf_decl_file, dwarf_decl_line, dwarf_decl_column;       dwarf
_func_inline, dwarf_func_inline_instances now take Dwarf_Die.       Ty
pe Dwarf_Loc renamed to Dwarf_Op; dwarf_getloclist,       dwarf_addrlo
clists renamed dwarf_getlocation, dwarf_getlocation_addr.

* Fri Sep  2 2005 Ulrich Drepper <drepper@redhat.com> 0.115-1
- libelf: speed-ups of non-mmap reading.
- strings: New program.
- Implement --enable-gcov option for configure.
- libdw: New function dwarf_getscopes_die.

* Wed Aug 24 2005 Ulrich Drepper <drepper@redhat.com> 0.114-1
- libelf: new function elf_getaroff
- libdw: Added dwarf_func_die, dwarf_func_inline, dwarf_func_inline_inst
ances.
- libdwfl: New functions dwfl_report_offline, dwfl_offline_section_addre
ss,	 dwfl_linux_kernel_report_offline.
- ranlib: new program

* Mon Aug 15 2005 Ulrich Drepper <drepper@redhat.com> 0.114-1
- libelf: new function elf_getaroff
- ranlib: new program

* Wed Aug 10 2005 Ulrich Drepper <@redhat.com> 0.113-1
- elflint: relax a bit. Allow version definitions for defined symbols ag
ainstDSO versions also for symbols in nobits sections.  Allow .rodata
sectionto have STRINGS and MERGE flag set.
- strip: add some more compatibility with binutils.

* Sat Aug  6 2005 Ulrich Drepper <@redhat.com> 0.113-1
- elflint: relax a bit. Allow version definitions for defined symbols ag
ainstDSO versions also for symbols in nobits sections.  Allow .rodata
sectionto have STRINGS and MERGE flag set.

* Sat Aug  6 2005 Ulrich Drepper <@redhat.com> 0.113-1
- elflint: relax a bit. Allow version definitions for defined symbols ag
ainstDSO versions also for symbols in nobits sections.

* Fri Aug  5 2005 Ulrich Drepper <@redhat.com> 0.112-1
- elfcmp: some more relaxation.
- elflint: many more tests, especially regarding to symbol versioning.
- libelf: Add elfXX_offscn and gelf_offscn.
- libasm: asm_begin interface changes.
- libebl: Add three new interfaces to directly access machine, class, an
ddata encoding information.
- objdump: New program.  Just the beginning.

* Thu Jul 28 2005 Ulrich Drepper <@redhat.com> 0.111-1
- libdw: now contains all of libdwfl.  The latter is not installed anymore.
- elfcmp: little usability tweak, name and index of differing section is
 printed.

* Sun Jul 24 2005 Ulrich Drepper <@redhat.com> 0.110-1
- libelf: fix a numbe rof problems with elf_update
- elfcmp: fix a few bugs.  Compare gaps.
- Fix a few PLT problems and mudflap build issues.
- libebl: Don't expose Ebl structure definition in libebl.h.  It's now p
rivate.

* Thu Jul 21 2005 Ulrich Drepper <@redhat.com> 0.109-1
- libebl: Check for matching modules.
- elflint: Check that copy relocations only happen for OBJECT or NOTYPE
symbols.
- elfcmp: New program.
- libdwfl: New library.

* Mon May  9 2005 Ulrich Drepper <@redhat.com> 0.108-1
- strip: fix bug introduced in last change
- libdw: records returned by dwarf_getsrclines are now sorted by address

* Sun May  8 2005 Ulrich Drepper <@redhat.com> 0.108-1
- strip: fix bug introduced in last change

* Sun May  8 2005 Ulrich Drepper <@redhat.com> 0.107-1
- readelf: improve DWARF output format
- strip: support Linux kernel modules

* Fri Apr 29 2005 Ulrich Drepper <drepper@redhat.com> 0.107-1
- readelf: improve DWARF output format

* Mon Apr  4 2005 Ulrich Drepper <drepper@redhat.com> 0.106-1
- libdw: Updated dwarf.h from DWARF3 speclibdw: add new funtions dwarf_f
unc_entrypc, dwarf_func_file, dwarf_func_line,dwarf_func_col, dwarf_ge
tsrc_file

* Fri Apr  1 2005 Ulrich Drepper <drepper@redhat.com> 0.105-1
- addr2line: New program
- libdw: add new functions: dwarf_addrdie, dwarf_macro_*, dwarf_getfuncs
,dwarf_func_*.
- findtextrel: use dwarf_addrdie

* Mon Mar 28 2005 Ulrich Drepper <drepper@redhat.com> 0.104-1
- findtextrel: New program.

* Mon Mar 21 2005 Ulrich Drepper <drepper@redhat.com> 0.103-1
- libdw: Fix using libdw.h with gcc < 4 and C++ code.  Compiler bug.

* Tue Feb 22 2005 Ulrich Drepper <drepper@redhat.com> 0.102-1
- More Makefile and spec file cleanups.

* Fri Jan 16 2004 Jakub Jelinek <jakub@redhat.com> 0.94-1
- upgrade to 0.94

* Fri Jan 16 2004 Jakub Jelinek <jakub@redhat.com> 0.93-1
- upgrade to 0.93

* Thu Jan  8 2004 Jakub Jelinek <jakub@redhat.com> 0.92-1
- full version
- macroized spec file for GPL or OSL builds
- include only libelf under GPL plus wrapper scripts

* Wed Jan  7 2004 Jakub Jelinek <jakub@redhat.com> 0.91-2
- macroized spec file for GPL or OSL builds

* Wed Jan  7 2004 Ulrich Drepper <drepper@redhat.com>
- split elfutils-devel into two packages.

* Wed Jan  7 2004 Jakub Jelinek <jakub@redhat.com> 0.91-1
- include only libelf under GPL plus wrapper scripts

* Tue Dec 23 2003 Jeff Johnson <jbj@redhat.com> 0.89-3
- readelf, not readline, in %%description (#111214).

* Fri Sep 26 2003 Bill Nottingham <notting@redhat.com> 0.89-1
- update to 0.89 (fix eu-strip)

* Tue Sep 23 2003 Jakub Jelinek <jakub@redhat.com> 0.86-3
- update to 0.86 (fix eu-strip on s390x/alpha)
- libebl is an archive now; remove references to DSO

* Mon Jul 14 2003 Jeff Johnson <jbj@redhat.com> 0.84-3
- upgrade to 0.84 (readelf/elflint improvements, rawhide bugs fixed).

* Fri Jul 11 2003 Jeff Johnson <jbj@redhat.com> 0.83-3
- upgrade to 0.83 (fix invalid ELf handle on *.so strip, more).

* Wed Jul  9 2003 Jeff Johnson <jbj@redhat.com> 0.82-3
- upgrade to 0.82 (strip tests fixed on big-endian).

* Tue Jul  8 2003 Jeff Johnson <jbj@redhat.com> 0.81-3
- upgrade to 0.81 (strip excludes unused symtable entries, test borked).

* Thu Jun 26 2003 Jeff Johnson <jbj@redhat.com> 0.80-3
- upgrade to 0.80 (debugedit changes for kernel in progress).

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 21 2003 Jeff Johnson <jbj@redhat.com> 0.79-2
- upgrade to 0.79 (correct formats for size_t, more of libdw "works").

* Mon May 19 2003 Jeff Johnson <jbj@redhat.com> 0.78-2
- upgrade to 0.78 (libdwarf bugfix, libdw additions).

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- debuginfo rebuild

* Thu Feb 20 2003 Jeff Johnson <jbj@redhat.com> 0.76-2
- use the correct way of identifying the section via the sh_info link.

* Sat Feb 15 2003 Jakub Jelinek <jakub@redhat.com> 0.75-2
- update to 0.75 (eu-strip -g fix)

* Tue Feb 11 2003 Jakub Jelinek <jakub@redhat.com> 0.74-2
- update to 0.74 (fix for writing with some non-dirty sections)

* Thu Feb  6 2003 Jeff Johnson <jbj@redhat.com> 0.73-3
- another -0.73 update (with sparc fixes).
- do "make check" in %%check, not %%install, section.

* Mon Jan 27 2003 Jeff Johnson <jbj@redhat.com> 0.73-2
- update to 0.73 (with s390 fixes).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 22 2003 Jakub Jelinek <jakub@redhat.com> 0.72-4
- fix arguments to gelf_getsymshndx and elf_getshstrndx
- fix other warnings
- reenable checks on s390x

* Sat Jan 11 2003 Karsten Hopp <karsten@redhat.de> 0.72-3
- temporarily disable checks on s390x, until someone has
  time to look at it

* Thu Dec 12 2002 Jakub Jelinek <jakub@redhat.com> 0.72-2
- update to 0.72

* Wed Dec 11 2002 Jakub Jelinek <jakub@redhat.com> 0.71-2
- update to 0.71

* Wed Dec 11 2002 Jeff Johnson <jbj@redhat.com> 0.69-4
- update to 0.69.
- add "make check" and segfault avoidance patch.
- elfutils-libelf needs to run ldconfig.

* Tue Dec 10 2002 Jeff Johnson <jbj@redhat.com> 0.68-2
- update to 0.68.

* Fri Dec  6 2002 Jeff Johnson <jbj@redhat.com> 0.67-2
- update to 0.67.

* Tue Dec  3 2002 Jeff Johnson <jbj@redhat.com> 0.65-2
- update to 0.65.

* Mon Dec  2 2002 Jeff Johnson <jbj@redhat.com> 0.64-2
- update to 0.64.

* Sun Dec 1 2002 Ulrich Drepper <drepper@redhat.com> 0.64
- split packages further into elfutils-libelf

* Sat Nov 30 2002 Jeff Johnson <jbj@redhat.com> 0.63-2
- update to 0.63.

* Fri Nov 29 2002 Ulrich Drepper <drepper@redhat.com> 0.62
- Adjust for dropping libtool

* Sun Nov 24 2002 Jeff Johnson <jbj@redhat.com> 0.59-2
- update to 0.59

* Thu Nov 14 2002 Jeff Johnson <jbj@redhat.com> 0.56-2
- update to 0.56

* Thu Nov  7 2002 Jeff Johnson <jbj@redhat.com> 0.54-2
- update to 0.54

* Sun Oct 27 2002 Jeff Johnson <jbj@redhat.com> 0.53-2
- update to 0.53
- drop x86_64 hack, ICE fixed in gcc-3.2-11.

* Sat Oct 26 2002 Jeff Johnson <jbj@redhat.com> 0.52-3
- get beehive to punch a rhpkg generated package.

* Wed Oct 23 2002 Jeff Johnson <jbj@redhat.com> 0.52-2
- build in 8.0.1.
- x86_64: avoid gcc-3.2 ICE on x86_64 for now.

* Tue Oct 22 2002 Ulrich Drepper <drepper@redhat.com> 0.52
- Add libelf-devel to conflicts for elfutils-devel

* Mon Oct 21 2002 Ulrich Drepper <drepper@redhat.com> 0.50
- Split into runtime and devel package

* Fri Oct 18 2002 Ulrich Drepper <drepper@redhat.com> 0.49
- integrate into official sources

* Wed Oct 16 2002 Jeff Johnson <jbj@redhat.com> 0.46-1
- Swaddle.
