self: super: {
  likwid = super.likwid.overrideAttrs (oldAttrs: rec {
    src = super.fetchFromGitHub {
      owner = "RRZE-HPC";
      repo = "likwid";
      rev = "c85d659a7a308816a3cfd987ad0b8ec63d30901f";
      hash = "sha256-AWJ8OPnhWNdYmPLxC+xJQ1VkbydujU0OKZsz93FCYRQ=";
    };
    DEBUGFLAGS = "-fdebug-prefix-map=.=${src} -fdebug-prefix-map=/build/source=${src}";
    makeFlags = (oldAttrs.makeFlags or [ ]) ++ [
      "DEBUG=true"
      "CFLAGS=$(DEBUGFLAGS)"
      "CXXFLAGS=$(DEBUGFLAGS)"
    ];
    dontStrip = true;
  });
}
