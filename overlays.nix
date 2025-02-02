{ inputs, ... }:

final: _prev: {
  capstan = _prev.callPackage ./pkgs/capstan.nix { };
  boost175 = inputs.nixpkgs-2311.legacyPackages.${_prev.system}.boost175;
  osv-boost = inputs.nixpkgs-2311.legacyPackages.${_prev.system}.boost.override {
    enableStatic = true;
    enableShared = false;
  };
  osv-ssl = inputs.nixpkgs-2211.legacyPackages.${_prev.system}.openssl_1_1.out;
  osv-ssl-hdr = inputs.nixpkgs-2211.legacyPackages.${_prev.system}.openssl_1_1.dev;
  gen_compile_commands = _prev.callPackage ./pkgs/gen_compile_commands.nix { };
}
