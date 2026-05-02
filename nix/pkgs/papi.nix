{
  stdenv,
  fetchurl,
}:

stdenv.mkDerivation rec {
  version = "7.2.0";
  pname = "papi";

  src = fetchurl {
    url = "http://icl.utk.edu/projects/papi/downloads/papi-${version}.tar.gz";
    sha256 = "sha256-qb/4nM85kV1yngiuCgxqcc4Ou+mEEemi6zyDyNsK85w=";
  };

  setSourceRoot = ''
    sourceRoot=$(echo */src)
  '';

  dontStrip = true;
}
