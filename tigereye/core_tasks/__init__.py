from .plotting import plot_task
from .printing import print_task
from .verifying import verify_task
from .cleaning import clean_task

tasks = {
    "plot":     plot_task,
    "print":    print_task,
    "verify":   verify_task,
    "clean":    clean_task,
}
