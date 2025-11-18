#!/bin/sh

# If SCHEDULE is empty → run once
if [ -z "$SCHEDULE" ]; then
  python -m src.main
else
  # Run forever every SCHEDULE seconds
  while true; do
    python -m src.main
    sleep ${SCHEDULE}
  done
fi
