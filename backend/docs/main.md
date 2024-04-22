## Summary

The `run_parser` function is a scheduled task that runs periodically every 60 seconds on the startup of a FastAPI application. It performs parsing and data insertion into a database. The function retrieves data from JSON files, converts the data into schema objects, inserts the districts and deadlines data into the database using the `insert_districts` and `insert_deadlines` methods of the `Service` class, and logs the success or failure of the insertion. Finally, it logs a message indicating the completion of the scheduled task.

## Example Usage

```python
@app.on_event("startup")
@repeat_every(seconds=60, logger=parser_logger)
async def run_parser():
    ...
```

## Code Analysis

### Inputs

- `app`: The FastAPI application instance.
- `parser_logger`: The logger object used for logging.

---

### Flow

1. The function logs the start of the scheduled task.
2. An instance of the `Service` class is created.
3. The function retrieves the districts and deadlines data from JSON files and converts them into schema objects.
4. The function logs the retrieved districts and deadlines data.
5. The function inserts the districts data into the database using the `insert_districts` method of the `Service` class.
6. If the insertion is successful, the function logs a success message. Otherwise, it logs an error message and stops the execution of the task.
7. The function inserts the deadlines data into the database using the `insert_deadlines` method of the `Service` class.
8. If the insertion is successful, the function logs a success message. Otherwise, it logs an error message and stops the execution of the task.
9. The function logs a message indicating the completion of the scheduled task.

---

### Outputs

None

---
