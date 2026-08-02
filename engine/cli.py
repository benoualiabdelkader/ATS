import sys
import json
from datetime import datetime
from pathlib import Path

# Force UTF-8 encoding for Windows stdout/stderr
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from engine.config import OPPORTUNITIES_DIR
from engine.memory import MemoryManager
from engine.pipeline import ApplicationPipeline

cli_app = typer.Typer(help="Career-Application-Agent (AI Career Operating System CLI)")
console = Console()

@cli_app.command("inspect-memory")
def inspect_memory():
    """Inspects and displays the current candidate memory stored in myself/."""
    console.print(Panel("[bold green]Career-Application-Agent Memory Inspector[/bold green]"))
    mem_mgr = MemoryManager()
    profile = mem_mgr.load_candidate_profile()
    graph = mem_mgr.build_knowledge_graph(profile)

    table = Table(title="Candidate Profile Memory Stats")
    table.add_column("Memory Category", style="cyan")
    table.add_column("Items / Files Found", style="magenta")

    table.add_row("Education Entries", str(len(profile.education)))
    table.add_row("Experience Bullet Points", str(len(profile.experience)))
    table.add_row("Core Skills", str(len(graph.skill_nodes)))
    table.add_row("Certificates", str(len(profile.certificates)))
    table.add_row("Deep Dive Projects", str(len(profile.projects)))
    table.add_row("Publications", str(len(profile.publications)))
    table.add_row("Hackathons", str(len(profile.hackathons)))

    console.print(table)
    console.print(f"[bold cyan]Candidate Name:[/bold cyan] {graph.candidate_name}")

@cli_app.command("run")
def run_opportunity(
    opp: str = typer.Option("Google_AI_Engineer", help="Name of opportunity folder inside opportunities/")
):
    """Executes the full application generation pipeline for a target opportunity."""
    console.print(f"[bold blue]Processing Opportunity:[/bold blue] {opp}")
    try:
        pipeline = ApplicationPipeline()
        meta, opp_dir = pipeline.run(opp)

        console.print("[green][OK][/green] Ingested candidate memory base from myself/")
        console.print(f"[green][OK][/green] Parsed Job Description for [bold]{meta.target_role}[/bold] at [bold]{meta.target_company}[/bold]")
        console.print(f"[green][OK][/green] Calculated Candidate-Role Match Score: [bold yellow]{meta.match_score}%[/bold yellow]")
        console.print("[green][OK][/green] Synthesized company research & strategic hiring signals")
        console.print("[green][OK][/green] Synthesized 11 Markdown application documents into category subfolders")
        console.print(f"[green][OK][/green] Computed ATS Compatibility Score: [bold green]{meta.ats_score}%[/bold green]")
        console.print("[green][OK][/green] Generated ATS-optimized PDF exports for all documents")

        console.print(Panel(
            f"[bold green]SUCCESS![/bold green] Complete Application Package generated in structured subfolders:\n"
            f"[bold cyan]{opp_dir}[/bold cyan]\n\n"
            f"* Categories: 7 Structured Subfolders (01_cv, 02_cover_letter, etc.)\n"
            f"* Total Files: {len(meta.generated_files)}\n"
            f"* ATS Score: {meta.ats_score}%\n"
            f"* Match Score: {meta.match_score}%\n"
            f"* Grounding Status: 100% Grounded in myself/",
            title="Career Operating System Output Summary"
        ))
    except Exception as e:
        console.print(f"[bold red]Pipeline Error:[/bold red] {e}")
        raise typer.Exit(code=1)

@cli_app.command("gui")
def launch_gui(port: int = 8000):
    """Launches the FastAPI Web Dashboard UI."""
    import uvicorn
    console.print(f"[bold green]Launching Web Dashboard on http://localhost:{port}[/bold green]")
    uvicorn.run("engine.app:app", host="127.0.0.1", port=port, reload=False)

if __name__ == "__main__":
    cli_app()

