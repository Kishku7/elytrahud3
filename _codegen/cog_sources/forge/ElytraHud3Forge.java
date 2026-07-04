// SHARED SOURCE (single source, Cog-driven drift) -- no 26 twin (Forge ends at 1.21.8). ONE entry;
// only the ctor era (classic no-arg vs injected-context) is Cog-selected in compat_forge.
// Materialized into each pre-26 cell's gen/ by scripts/cog-gen.ps1; edit the brain, never gen/.
//[[[cog
// import sys; sys.path.insert(0, codegen); import compat_forge as compat
// compat.emit_entry(cog, ver, codegen)
//]]]
//[[[end]]]
