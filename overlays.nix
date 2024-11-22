{ inputs, ... }:

final: _prev: {
  capstan = _prev.callPackage ./pkgs/capstan.nix { };
  osv-boost = _prev.boost.override {
    enableStatic = true;
    enableShared = false;
  };
  gen_compile_commands = _prev.callPackage ./pkgs/gen_compile_commands.nix { };
}
