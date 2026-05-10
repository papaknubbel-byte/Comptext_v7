import subprocess
import json
import os
import sys
import time

def run_command(command, description):
    print(f"[*] Running: {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    report = {
        "timestamp": time.time(),
        "system": "CompText V6 Auto-Validator",
        "results": {}
    }

    # 1. Unit Tests & Coverage
    print("\n[Phase 1] Unit Tests & Coverage")
    res = run_command("pytest tests/ --cov=src --cov-report=json", "Pytest with Coverage")
    report["results"]["unit_tests"] = {
        "success": res["success"],
        "summary": "All tests passed" if res["success"] else "Some tests failed"
    }
    if os.path.exists("coverage.json"):
        with open("coverage.json", "r") as f:
            cov_data = json.load(f)
            report["results"]["unit_tests"]["coverage_pct"] = cov_data["totals"]["percent_covered"]

    # 2. Security Audit (Bandit)
    print("\n[Phase 2] Security Audit")
    res = run_command("bandit -r src/ -f json", "Bandit Security Scan")
    if res["stdout"]:
        try:
            # Strip info logs before JSON
            json_str = res["stdout"]
            if "{" in json_str:
                json_str = json_str[json_str.find("{"):]
            bandit_data = json.loads(json_str)
            report["results"]["security"] = {
                "issues_found": len(bandit_data["results"]),
                "severity_breakdown": bandit_data["metrics"]["_totals"]
            }
        except Exception as e:
            report["results"]["security"] = {"error": f"Failed to parse bandit output: {e}"}

    # 3. Performance Benchmark
    print("\n[Phase 3] Performance Benchmark")
    res = run_command("pytest tests/test_performance.py -v", "Performance Validation")
    report["results"]["performance"] = {
        "success": res["success"],
        "details": res["stdout"] if res["success"] else res["stderr"]
    }

    # Final Score Calculation
    score = 0
    if report["results"]["unit_tests"]["success"]: score += 40
    score += min(40, int(report["results"]["unit_tests"].get("coverage_pct", 0) * 0.4))
    if report["results"]["security"].get("issues_found", 10) == 0: score += 20
    
    report["quality_score"] = score

    print("\n" + "="*50)
    print(f"VALIDATION COMPLETE - Quality Score: {score}/100")
    print("="*50)
    
    with open("validation_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"Report saved to validation_report.json")

if __name__ == "__main__":
    main()
