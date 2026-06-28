"""
MASTER RUNNER
Runs the full pipeline in order:
  1. generate_data.py
  2. clean_data.py
  3. analysis.py
  4. test_edge_cases.py
Prints a summary of what ran and passed.
"""
import subprocess
import sys

STEPS = [
    ("Data Generation", "generate_data.py"),
    ("Data Cleaning", "clean_data.py"),
    ("SQL Analysis", "analysis.py"),
    ("Edge Case Tests", "test_edge_cases.py"),
]


def run_step(name, script):
    print("\n" + "#" * 70)
    print(f"# RUNNING: {name} ({script})")
    print("#" * 70)
    try:
        result = subprocess.run([sys.executable, script], check=False)
        success = result.returncode == 0
        if not success:
            print(f"\n!! {script} exited with non-zero return code {result.returncode}")
        return success
    except Exception as e:
        print(f"\n!! Failed to run {script}: {e}")
        return False


def main():
    print("=" * 70)
    print("E-COMMERCE ORDER ANALYTICS SYSTEM - FULL PIPELINE")
    print("=" * 70)

    results = []
    for name, script in STEPS:
        success = run_step(name, script)
        results.append((name, script, success))

    print("\n" + "=" * 70)
    print("PIPELINE SUMMARY")
    print("=" * 70)
    for name, script, success in results:
        status = "PASSED/RAN" if success else "FAILED"
        print(f"  [{status}] {name} ({script})")

    n_failed = sum(1 for _, _, success in results if not success)
    print("-" * 70)
    if n_failed == 0:
        print("All steps completed successfully.")
    else:
        print(f"{n_failed} step(s) failed. See output above for details.")
    print("=" * 70)
    print("\nNote: report_tool.py is interactive and not run as part of this pipeline.")
    print("Run it separately with: python report_tool.py")


if __name__ == "__main__":
    main()
