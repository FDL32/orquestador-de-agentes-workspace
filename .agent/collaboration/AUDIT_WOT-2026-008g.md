# AUDIT_WOT-2026-008g.md

## Checklist Manager

- [ ] La DEC existe y es documental.
- [ ] La DEC distingue backend IA, rol, artefacto y supervisor runtime.
- [ ] `audit_*` queda como familia transversal, no como rol auditor.
- [ ] La tabla de prompts contiene 20 archivos fisicos y marca `review_manager.md` como legacy stub.
- [ ] AGENTS.md contiene "Backends y roles".
- [ ] No hay renames, moves ni frontmatter.
- [ ] `discover_skills.py --check-naming` pasa.
- [ ] Encoding guard pasa sobre DEC + AGENTS.md.
- [ ] validate --json termina en 0 errors / 0 warnings.

## Anti-patrones

- Aceptar claims de inventario sin comando/evidencia.
- Forzar auditor_* por uniformidad visual cuando el prompt es multi-rol.
- Cambiar bus/runtime bajo una DEC documental.
- Dejar mojibake o control chars en el packet.