{ inputs, ... }:

final: _prev: {
  capstan = _prev.callPackage ./pkgs/capstan.nix { };
  osv-boost = _prev.boost.override {
    enableStatic = true;
    enableShared = false;
  };
  osv-ssl = inputs.nixpkgs-2211.legacyPackages.${_prev.system}.openssl_1_1.out;
  osv-ssl-hdr = inputs.nixpkgs-2211.legacyPackages.${_prev.system}.openssl_1_1.dev;
  gen_compile_commands = _prev.callPackage ./pkgs/gen_compile_commands.nix { };
}
