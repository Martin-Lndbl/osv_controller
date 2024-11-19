{
  description = "OSv flake";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, flake-utils, }@inputs:
    flake-utils.lib.eachDefaultSystem
      (system:
        let
          pkgs = import nixpkgs {
            inherit system;
            overlays = [ (import ./overlays.nix { inherit inputs; }) ];
          };
        in
        {
          packages.capstan = pkgs.capstan;

          devShell = pkgs.mkShell {

            # Don't add glib.static here - As there is an issue with wcslen defined twice.
            # If you want to use statically linked executables, build them manually before calling ./scripts/build
            nativeBuildInputs = with pkgs; [
              ack # grep tool
              ant # java dev lib
              autoconf
              automake
              bash
              binutils
              bisoncpp
              gdb # gnu debugger
              # glibc.static
              gnumake
              gnupatch
              flamegraph # code hierarchy visualization
              libedit
              libgcc # Compiler
              libtool
              libvirt
              lua53Packages.lua
              ncurses
              pkg-config
              pax-utils # elf security library
              pyright
              python3
              python312Packages.requests
              p11-kit # PKCS#11 loader
              qemu_full # hypervisor
              readline # interactive line editing
              unzip
              zulu8 # Java jdk
              flex
              bison
            ];

            buildInputs = with pkgs; [
              osv-boost # C++ libraries
              readline # interactive line editing
              libaio # I/O library
              openssl # SSL/TLS library
              clang-tools_18 # language server
            ];

            LD_LIBRARY_PATH = "${pkgs.readline}/lib";
            LUA_LIB_PATH = "${pkgs.lua53Packages.lua}/lib";
            GOMP_DIR = pkgs.libgcc.lib;

            CAPSTAN_QEMU_PATH = "${pkgs.qemu}/bin/qemu-system-x86_64";

            shellHook = ''
              # /bin/bash --version >/dev/null 2>&1 || {
              #   echo >&2 "Error: /bin/bash is required but was not found.  Aborting."
              #   echo >&2 "If you're on NixOs, consider using https://github.com/Mic92/envfs."
              #   exit 1
              #   }

              export OSV_BASE=$(git rev-parse --show-toplevel)
              export OSV_BUILD_PATH=$OSV_BASE/build/release.x64

              mkdir $TMP/openssl-all
              ln -rsf ${pkgs.openssl}/* $TMP/openssl-all
              ln -rsf ${pkgs.openssl.dev}/* $TMP/openssl-all
              ln -rsf ${pkgs.openssl.out}/* $TMP/openssl-all
              export OPENSSL_DIR="$TMP/openssl-all";
              export OPENSSL_LIB_PATH="$TMP/openssl-all/lib";

              mkdir $TMP/libboost
              export boost_base="$TMP/libboost"
              ln -s ${pkgs.osv-boost}/lib/* $TMP/libboost/
              for file in $TMP/libboost/*-x64*; do mv "$file" "''${file//-x64/}"; done
            '';
          };
        }
      );
}
