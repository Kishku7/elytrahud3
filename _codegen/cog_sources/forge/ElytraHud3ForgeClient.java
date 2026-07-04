// SHARED SOURCE (single source, Cog-driven drift) -- no 26 twin (Forge ends at 1.21.8). The class
// body is ONE definition; only the per-era overlay-API drift (imports/init/register/tick) is
// Cog-selected in compat_forge. Materialized into each pre-26 cell's gen/ by scripts/cog-gen.ps1;
// edit the brain (compat_forge), never gen/ (disposable, gitignored).
//[[[cog
// import sys; sys.path.insert(0, codegen); import compat_forge as compat
// compat.emit_client(cog, ver, codegen)
//]]]
//[[[end]]]
