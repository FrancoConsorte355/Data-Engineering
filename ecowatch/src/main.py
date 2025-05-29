# src/main.py
import sys
import os
from datetime import datetime
from colorama import init, Fore, Style
from src.cache.temporal_cache import TemporalCache
from src.services.ingest_service import IngestService
from src.reports.factory import ReportFactory

init(autoreset=True)

def prompt(msg, example=None):
    txt = Fore.CYAN + msg + (f" {Fore.GREEN}(e.g., {example})" if example else "") + "\n> "
    return input(txt + Style.RESET_ALL).strip()


def main():
    print(Fore.MAGENTA + Style.BRIGHT + "=== Ecowatch Logs Report ===")

    # Reference time input
    ref_input = prompt("Enter reference time [ISO]", "2025-05-01T08:05:00") or "2025-05-01T08:05:00"
    try:
        ref_time = datetime.fromisoformat(ref_input)
    except ValueError:
        print(Fore.RED + "Invalid time format, using default.")
        ref_time = datetime.fromisoformat("2025-05-01T08:05:00")

    # Time window input
    win_str = prompt("Enter time window in minutes", "5")
    try:
        win_min = int(win_str)
    except ValueError:
        print(Fore.RED + "Invalid number, using 5 minutes.")
        win_min = 5
    win_sec = win_min * 60

    # Ingest data into cache
    cache = TemporalCache(window_seconds=win_sec, now_fn=lambda: ref_time)
    IngestService(cache=cache).run()

    # Filter by sala
    records = cache.get_all()
    salas = sorted({r.sala for r in records})
    print(Fore.YELLOW + "Available salas:" + Style.RESET_ALL, ", ".join(salas))
    rooms_str = prompt("Select salas separated by comma or 'all'", ", ".join(salas)) or 'all'
    selected = salas if rooms_str.lower() == 'all' else [s.strip() for s in rooms_str.split(',')]
    filtered = [r for r in records if r.sala in selected]

    # Choose report types (multiple allowed)
    print(Fore.BLUE + "\nSelect report types (comma separated):")
    print("  1) Text: Status by Sala")
    print("  2) Text: Critical Alerts")
    print("  3) Tabular: Pandas Status Report (CSV/Excel export)")
    choices_str = input(Fore.CYAN + "Enter choices [e.g., 1,3]: " + Style.RESET_ALL).strip()
    choices = {c.strip() for c in choices_str.split(',') if c.strip() in {'1','2','3'}}

    if not choices:
        print(Fore.RED + "No valid choice entered; exiting.")
        sys.exit(1)

    # Prepare export directories under a single parent
    base_export_dir = os.path.join(os.getcwd(), 'exportacion_archivos')
    csv_dir = os.path.join(base_export_dir, 'exportacion_CSV')
    excel_dir = os.path.join(base_export_dir, 'exportacion_EXCEL')
    os.makedirs(csv_dir, exist_ok=True)
    os.makedirs(excel_dir, exist_ok=True)

    # Process each selected report
    for choice in sorted(choices):
        if choice == '1':
            print(Fore.BLUE + f"\n--- Status by Sala (window={win_min}min) ---")
            status = ReportFactory.get('status_by_sala').generate(filtered)
            for sala, info in status.items():
                print(Fore.GREEN + sala + Style.RESET_ALL)
                for log in info['logs']:
                    print(f"  {log.timestamp.isoformat()} | T={log.temperatura} H={log.humedad}% CO2={log.co2}ppm | {log.estado}")
                print(Fore.CYAN + "  Metrics:")
                for field, vals in info['metrics'].items():
                    print(f"    {field.title()}: avg={vals['avg']:.1f}, max={vals['max']:.1f}, min={vals['min']:.1f}")
            print(Style.RESET_ALL)

        elif choice == '2':
            print(Fore.RED + f"\n--- Critical Alerts (count={len(filtered)}) ---")
            alerts = ReportFactory.get('critical_alerts').generate(filtered)
            for log in alerts:
                print(Fore.RED + f"  {log.timestamp.isoformat()} | {log.sala} | {log.mensaje}")
            print(Style.RESET_ALL)

        elif choice == '3':
            report = ReportFactory.get('pandas_status')
            df = report.generate(filtered)
            print(Fore.GREEN + "\nGenerated DataFrame:")
            print(df)
            export = input(Fore.CYAN + "\nExport to (1) CSV, (2) Excel, or press Enter to skip: " + Style.RESET_ALL).strip()
            if export == '1':
                filename = input("Enter CSV file name (e.g., report.csv): ").strip() or 'report.csv'
                path = os.path.join(csv_dir, filename)
                report.export_csv(df, path)
                print(Fore.YELLOW + f"Exported to {path}")
            elif export == '2':
                filename = input("Enter Excel file name (e.g., report.xlsx): ").strip() or 'report.xlsx'
                path = os.path.join(excel_dir, filename)
                report.export_excel(df, path)
                print(Fore.YELLOW + f"Exported to {path}")
            print(Style.RESET_ALL)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nOperation cancelled by user.")
        sys.exit(0)
