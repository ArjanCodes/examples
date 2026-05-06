#!/usr/bin/env bash

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Logging configuration
LOG_DIR="${LOG_DIR:-$SCRIPT_DIR/logs}"
LOG_FILE="${LOG_FILE:-$LOG_DIR/run_reports_$(date +%Y%m%d_%H%M%S).log}"
VERBOSE="${VERBOSE:-false}"
QUIET="${QUIET:-false}"

# Execution configuration
CONTINUE_ON_ERROR="${CONTINUE_ON_ERROR:-false}"
TIMEOUT="${TIMEOUT:-0}"  # 0 = no timeout
MAX_JOBS="${MAX_JOBS:-1}"  # 1 = sequential

# Report mappings (can be moved to config file)
declare -A REPORTS=(
  ["messy"]="messy_report.py"
  ["class-based"]="class_based_report.py"
  ["class-based-v2"]="class_based_report_v2.py"
  ["functional"]="functional_report.py"
  ["functional-v2"]="functional_report_v2.py"
  ["declarative"]="declarative_report.py"
  ["config"]="config_report.py"
  ["async"]="async_report.py"
  ["async-no-pandas"]="async_no_pandas_report.py"
  ["dataflow"]="report_dataflow.py"
  ["actor"]="report_actor_model.py"
  ["reactive"]="reactive_report.py"
  ["logic"]="logic_report.py"
)

# Execution tracking
declare -A REPORT_START_TIMES
declare -A REPORT_END_TIMES
declare -A REPORT_EXIT_CODES
SUCCESS_COUNT=0
FAILURE_COUNT=0
START_TIME=0
END_TIME=0

# ============================================================================
# Logging Functions
# ============================================================================

init_logging() {
  mkdir -p "$LOG_DIR"
  if [ ! -w "$LOG_DIR" ]; then
    echo "Error: Cannot write to log directory: $LOG_DIR" >&2
    exit 1
  fi
}

log() {
  local level="$1"
  shift
  local message="$*"
  local timestamp
  timestamp=$(date +'%Y-%m-%d %H:%M:%S')
  local log_entry="[$timestamp] [$level] $message"
  
  # Only show errors and warnings on terminal (since detailed logs go to file)
  if [ "$QUIET" = false ]; then
    case "$level" in
      ERROR)
        echo "$log_entry" >&2
        ;;
      WARN)
        echo "$log_entry" >&2
        ;;
      # INFO and DEBUG only go to log file, not terminal
    esac
  fi
  
  # Always write to log file
  echo "$log_entry" >> "$LOG_FILE"
}

log_info() { log "INFO" "$@"; }
log_warn() { log "WARN" "$@"; }
log_error() { log "ERROR" "$@"; }
log_debug() {
  if [ "$VERBOSE" = true ]; then
    log "DEBUG" "$@"
  fi
}

# ============================================================================
# Signal Handling
# ============================================================================

cleanup() {
  local exit_code="${1:-130}"
  log_warn "Received interrupt signal. Cleaning up..."
  
  # Kill any running background jobs
  jobs -p | xargs -r kill 2>/dev/null || true
  
  # Print partial summary
  if [ $START_TIME -gt 0 ]; then
    END_TIME=$(date +%s)
    print_summary
  fi
  
  exit "$exit_code"
}

trap 'cleanup 130' SIGINT SIGTERM

# ============================================================================
# Validation Functions
# ============================================================================

validate_report_key() {
  local key="$1"
  
  # Check key format (alphanumeric and hyphens only)
  if [[ ! "$key" =~ ^[a-z0-9-]+$ ]]; then
    log_error "Invalid report key format: '$key' (must be lowercase alphanumeric with hyphens)"
    return 1
  fi
  
  # Check key exists in REPORTS array
  if [ -z "${REPORTS[$key]:-}" ]; then
    log_error "Unknown report key: '$key'"
    return 1
  fi
  
  local script="${REPORTS[$key]}"
  
  # Check script file exists
  if [ ! -f "$script" ]; then
    log_error "Report script not found: '$script' for key '$key'"
    return 1
  fi
  
  # Check script is executable or readable
  if [ ! -r "$script" ]; then
    log_error "Report script is not readable: '$script'"
    return 1
  fi
  
  return 0
}

validate_environment() {
  log_debug "Validating environment..."
  
  # Check Python availability
  if ! command -v python >/dev/null 2>&1; then
    log_error "Python interpreter not found"
    return 1
  fi
  
  # Check Python version (example: require 3.8+)
  local python_version
  python_version=$(python --version 2>&1 | awk '{print $2}')
  log_debug "Python version: $python_version"
  
  # Check uv availability if uv.lock exists
  if [ -f "uv.lock" ] && ! command -v uv >/dev/null 2>&1; then
    log_warn "uv.lock found but uv not available. Using system Python."
  fi
  
  return 0
}

validate_all_report_keys() {
  local invalid_keys=()
  
  for key in "$@"; do
    if ! validate_report_key "$key"; then
      invalid_keys+=("$key")
    fi
  done
  
  if [ ${#invalid_keys[@]} -gt 0 ]; then
    log_error "Invalid report keys: ${invalid_keys[*]}"
    return 1
  fi
  
  return 0
}

# ============================================================================
# Execution Functions
# ============================================================================

determine_runner() {
  RUNNER=(python)
  if command -v uv >/dev/null 2>&1 && [ -f "$SCRIPT_DIR/uv.lock" ]; then
    RUNNER=(uv run python)
    log_debug "Using uv runner"
  else
    log_debug "Using system Python"
  fi
}

run_report_with_timeout() {
  local key="$1"
  local script="${REPORTS[$key]}"
  local cmd=("${RUNNER[@]}" "$script")
  local pid
  local exit_code=0
  
  REPORT_START_TIMES[$key]=$(date +%s)
  log_info "Starting report: $key ($script)"
  log_debug "Command: ${cmd[*]}"
  
  # Show minimal progress on terminal (only if not quiet)
  if [ "$QUIET" = false ] && [ "$DRY_RUN" = false ]; then
    echo -n "Running $key... " >&2
  fi
  
  if [ "$DRY_RUN" = true ]; then
    log_info "[DRY RUN] Would execute: ${cmd[*]}"
    if [ "$QUIET" = false ]; then
      echo "[DRY RUN]" >&2
    fi
    REPORT_EXIT_CODES[$key]=0
    REPORT_END_TIMES[$key]=$(date +%s)
    return 0
  fi
  
  # Add separator in log file for this report's output
  {
    echo ""
    echo "--- Report: $key ($script) ---"
    echo "Started at: $(date +'%Y-%m-%d %H:%M:%S')"
    echo ""
  } >> "$LOG_FILE"
  
  # Run with timeout if specified
  # By default, Python output only goes to log file (not terminal) to reduce clutter
  # Use --verbose to see Python output on terminal
  if [ "$TIMEOUT" -gt 0 ]; then
    if [ "$VERBOSE" = true ] && [ "$QUIET" = false ]; then
      # Show output on terminal and append to log file (verbose mode)
      timeout "$TIMEOUT" "${cmd[@]}" 2>&1 | tee -a "$LOG_FILE"
      exit_code=${PIPESTATUS[0]}
    else
      # Only append to log file (default behavior)
      timeout "$TIMEOUT" "${cmd[@]}" >> "$LOG_FILE" 2>&1 || exit_code=$?
    fi
    
    if [ $exit_code -eq 124 ]; then
      log_error "Report '$key' timed out after ${TIMEOUT}s"
      exit_code=124
    fi
  else
    if [ "$VERBOSE" = true ] && [ "$QUIET" = false ]; then
      # Show output on terminal and append to log file (verbose mode)
      "${cmd[@]}" 2>&1 | tee -a "$LOG_FILE"
      exit_code=${PIPESTATUS[0]}
    else
      # Only append to log file (default behavior)
      "${cmd[@]}" >> "$LOG_FILE" 2>&1 || exit_code=$?
    fi
  fi
  
  # Add separator in log file for end of report output
  {
    echo ""
    echo "--- End of report: $key (exit code: $exit_code) ---"
    echo ""
  } >> "$LOG_FILE"
  
  REPORT_END_TIMES[$key]=$(date +%s)
  REPORT_EXIT_CODES[$key]=$exit_code
  
  local duration=$((REPORT_END_TIMES[$key] - REPORT_START_TIMES[$key]))
  
  # Show minimal status on terminal
  if [ "$QUIET" = false ]; then
    if [ $exit_code -eq 0 ]; then
      echo "✓" >&2
    else
      echo "✗" >&2
    fi
  fi
  
  if [ $exit_code -eq 0 ]; then
    log_info "Completed report: $key (duration: ${duration}s)"
    ((SUCCESS_COUNT++)) || true
    return 0
  else
    log_error "Failed report: $key (exit code: $exit_code, duration: ${duration}s)"
    ((FAILURE_COUNT++)) || true
    return $exit_code
  fi
}

run_report() {
  local key="$1"
  
  if ! validate_report_key "$key"; then
    return 1
  fi
  
  if ! run_report_with_timeout "$key"; then
    if [ "$CONTINUE_ON_ERROR" = false ]; then
      log_error "Stopping execution due to failure (use --continue-on-error to continue)"
      return 1
    fi
    return 0  # Continue despite error
  fi
  
  return 0
}

# ============================================================================
# Summary & Reporting
# ============================================================================

print_summary() {
  local total=$((SUCCESS_COUNT + FAILURE_COUNT))
  local duration=0
  
  if [ $START_TIME -gt 0 ] && [ $END_TIME -gt 0 ]; then
    duration=$((END_TIME - START_TIME))
  fi
  
  # Build summary text
  local summary=""
  summary+=$'\n'
  summary+="========================================"$'\n'
  summary+="Execution Summary"$'\n'
  summary+="========================================"$'\n'
  summary+="Total reports:    $total"$'\n'
  summary+="Successful:       $SUCCESS_COUNT"$'\n'
  summary+="Failed:           $FAILURE_COUNT"$'\n'
  
  if [ $duration -gt 0 ]; then
    summary+="Total duration:   ${duration}s"$'\n'
  fi
  
  if [ $FAILURE_COUNT -gt 0 ]; then
    summary+=$'\n'
    summary+="Failed reports:"$'\n'
    for key in "${!REPORT_EXIT_CODES[@]}"; do
      if [ "${REPORT_EXIT_CODES[$key]}" -ne 0 ]; then
        local duration_key=$((REPORT_END_TIMES[$key] - REPORT_START_TIMES[$key]))
        summary+="  - $key (exit code: ${REPORT_EXIT_CODES[$key]}, duration: ${duration_key}s)"$'\n'
      fi
    done
  fi
  
  summary+="========================================"$'\n'
  summary+="Log file: $LOG_FILE"$'\n'
  summary+="========================================"$'\n'
  
  # Write to log file
  echo "$summary" >> "$LOG_FILE"
  
  # Also show on terminal (unless quiet)
  if [ "$QUIET" = false ]; then
    echo "$summary"
  fi
}

# ============================================================================
# Usage & Help
# ============================================================================

usage() {
  cat <<'EOF'
Usage: ./run_reports.sh [OPTIONS]

Run one or more sales-report implementations from this directory.

Options:
  --list                     Show available report keys.
  --run <key> [--run <key>]  Run one or more reports by key.
  --run-all                  Run every report sequentially.
  --dry-run                  Print the commands without executing them.
  --continue-on-error        Continue execution even if a report fails.
  --timeout <seconds>        Set timeout per report (0 = no timeout).
  --max-jobs <n>             Run up to N reports in parallel (default: 1).
  --verbose                  Enable verbose/debug logging.
  --quiet                    Suppress stdout (errors still shown).
  --log-dir <dir>            Specify log directory (default: ./logs).
  -h, --help                 Show this help message.

Environment Variables:
  CONTINUE_ON_ERROR          Continue on error (true/false)
  TIMEOUT                    Timeout per report in seconds
  MAX_JOBS                   Maximum parallel jobs
  VERBOSE                    Enable verbose logging
  QUIET                      Suppress stdout
  LOG_DIR                    Log directory path

Examples:
  ./run_reports.sh --list
  ./run_reports.sh --run functional --run logic
  ./run_reports.sh --run-all
  ./run_reports.sh --run-all --continue-on-error --timeout 300
  ./run_reports.sh --run-all --max-jobs 4 --verbose

Reports execute inside a uv environment when available; otherwise the
system python interpreter is used.
EOF
}

list_reports() {
  printf "Available reports:\n"
  for key in "${!REPORTS[@]}"; do
    local script="${REPORTS[$key]}"
    local status=""
    if [ ! -f "$script" ]; then
      status=" [MISSING]"
    fi
    printf "  %-20s %s%s\n" "$key" "$script" "$status"
  done | sort
}

# ============================================================================
# Main
# ============================================================================

main() {
  # Initialize
  init_logging
  log_info "Starting report execution"
  log_debug "Script directory: $SCRIPT_DIR"
  log_debug "Log file: $LOG_FILE"
  
  # Parse arguments
  RUN_ALL=false
  DRY_RUN=false
  REQUESTED_KEYS=()
  
  while (($# > 0)); do
    case "$1" in
      --list)
        list_reports
        exit 0
        ;;
      --run)
        shift || { log_error "--run requires a report key"; exit 1; }
        REQUESTED_KEYS+=("$1")
        ;;
      --run-all)
        RUN_ALL=true
        ;;
      --dry-run)
        DRY_RUN=true
        ;;
      --continue-on-error)
        CONTINUE_ON_ERROR=true
        ;;
      --timeout)
        shift || { log_error "--timeout requires a value"; exit 1; }
        TIMEOUT="$1"
        if ! [[ "$TIMEOUT" =~ ^[0-9]+$ ]]; then
          log_error "Invalid timeout value: $TIMEOUT (must be a number)"
          exit 1
        fi
        ;;
      --max-jobs)
        shift || { log_error "--max-jobs requires a value"; exit 1; }
        MAX_JOBS="$1"
        if ! [[ "$MAX_JOBS" =~ ^[0-9]+$ ]] || [ "$MAX_JOBS" -lt 1 ]; then
          log_error "Invalid max-jobs value: $MAX_JOBS (must be >= 1)"
          exit 1
        fi
        ;;
      --verbose)
        VERBOSE=true
        ;;
      --quiet)
        QUIET=true
        ;;
      --log-dir)
        shift || { log_error "--log-dir requires a path"; exit 1; }
        LOG_DIR="$1"
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        log_error "Unknown option: $1"
        echo ""
        usage
        exit 1
        ;;
    esac
    shift
  done
  
  # Validate inputs
  if [ "$RUN_ALL" = false ] && [ "${#REQUESTED_KEYS[@]}" -eq 0 ]; then
    log_error "No reports specified."
    echo ""
    usage
    exit 1
  fi
  
  # Setup
  if [ "$RUN_ALL" = true ]; then
    mapfile -t REQUESTED_KEYS < <(printf "%s\n" "${!REPORTS[@]}" | sort)
  fi
  
  # Validate environment and report keys
  if ! validate_environment; then
    exit 1
  fi
  
  if ! validate_all_report_keys "${REQUESTED_KEYS[@]}"; then
    exit 1
  fi
  
  # Determine runner
  determine_runner
  
  # Execute reports
  START_TIME=$(date +%s)
  STATUS=0
  
  for key in "${REQUESTED_KEYS[@]}"; do
    if ! run_report "$key"; then
      STATUS=1
      if [ "$CONTINUE_ON_ERROR" = false ]; then
        break
      fi
    fi
  done
  
  END_TIME=$(date +%s)
  
  # Print summary
  print_summary
  
  # Exit with appropriate code
  if [ $FAILURE_COUNT -gt 0 ]; then
    exit 1
  fi
  
  exit "$STATUS"
}

# Run main function
main "$@"

