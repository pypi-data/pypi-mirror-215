{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python311 mongosh mongodb-tools mysql mydumper postgresql minio-client
  ];
}
