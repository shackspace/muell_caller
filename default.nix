{ pkgs ? import <nixpkgs> {} }:
with pkgs.python3Packages;
let
  inp = [
    python
    requests
    docopt
    paramiko
  ];
in buildPythonPackage {
  name = "call_muell-2017-06-01";
  src = ./.;
  buildInputs = inp;
}
