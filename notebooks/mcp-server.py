from fastmcp import FastMCP

# 1. MCP-Server instanziieren
mcp = FastMCP("Hochschul-Info-Assistant")


# 2. Tool 1: Abfrage von Studiengangsinformationen
@mcp.tool()
def get_program_details(program_name: str) -> dict[str, str | int]:
    """Liefert Basisdaten (ECTS, Dauer, Abschluss) zu einem bestimmten Studiengang.

    Verfügbare Studiengänge: 'Data Science', 'Digital Business'.
    """
    programs = {
        "Data Science": {
            "ects": 180,
            "duration_semesters": 6,
            "degree": "BSc",
            "language": "Deutsch/Englisch",
        },
        "Digital Business": {
            "ects": 180,
            "duration_semesters": 6,
            "degree": "BA",
            "language": "Deutsch",
        },
    }
    return programs.get(
        program_name, {"error": "Studiengang nicht gefunden."}
    )


# 3. Tool 2: Einfache Berechnung (ECTS in Workload-Stunden)
@mcp.tool()
def calculate_workload(ects: int) -> dict[str, int]:
    """Berechnet den geschätzten Gesamtarbeitsaufwand in Stunden für eine ECTS-Anzahl (1 ECTS = 25h)."""
    return {"ects": ects, "total_workload_hours": ects * 25}


# 4. Resource: Statischer Campus-Kontext
@mcp.resource("config://opening-hours")
def get_library_hours() -> str:
    """Gibt die aktuellen Öffnungszeiten der Hochschulbibliothek zurück."""
    return "Bibliothek Campus Zentrum: Mo–Fr 08:00–20:00 Uhr | Sa 09:00–14:00 Uhr"


if __name__ == "__main__":
    mcp.run()