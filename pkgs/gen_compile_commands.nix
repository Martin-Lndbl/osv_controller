{
  writeScriptBin,
}:

writeScriptBin "gen_compile_commands" (builtins.readFile ./gen_compile_commands.sh)
# writeScriptBin "gen_compile_commands" ''
#   #!${python3}/bin/python3
#   ${builtins.readFile ./gen_compile_commands.py}
# ''
