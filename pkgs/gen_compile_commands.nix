{
  compiledb,
  writeScriptBin,
}:

writeScriptBin "osv_compile_commands" ''
  #!/bin/bash

  if [ -z "$1" ]; then
    echo "You need to supply an image name as argument"
    exit 1
  fi

  make_output=$(mktemp)

  ./scripts/build clean
  ./scripts/build -j $(nproc) image=$1 V=1 > $make_output
  ${compiledb}/bin/compiledb --parse $make_output
''

# writeScriptBin "gen_compile_commands" (builtins.readFile ./gen_compile_commands.sh)
# writeScriptBin "gen_compile_commands" ''
#   #!${python3}/bin/python3
#   ${builtins.readFile ./gen_compile_commands.py}
# ''
