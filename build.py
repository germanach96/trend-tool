"""Genera trend-tool.html (un solo archivo, offline) incrustando SheetJS en src/app.html."""
from pathlib import Path

root = Path(__file__).parent
app = (root / "src/app.html").read_text(encoding="utf-8")
sheetjs = (root / "vendor/xlsx.full.min.js").read_text(encoding="utf-8").replace("</script", "<\\/script")
(root / "trend-tool.html").write_text(app.replace("/*__SHEETJS__*/", sheetjs), encoding="utf-8")
print("trend-tool.html generado")
