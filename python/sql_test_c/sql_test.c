#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#include "./sqlite3.h"

#define FILE_PATH "./ethercat_dev.sqlite"

#define PREPARE_QUERY(db, in, out)       \
    do {                                 \
        int ret = sqlite3_prepare_v2(    \
            db,                          \
            in,                          \
            strlen(in),                  \
            out,                         \
            NULL                         \
            );                           \
        if ( ret != SQLITE_OK ) {        \
            sqlite3_errmsg(db_ptr);      \
        }                                \
    } while (false)

#define FINALIZE_QUERY(stmt_ptr)              \
    do {                                      \
        int ret = sqlite3_finalize(stmt_ptr); \
        if ( ret != SQLITE_OK ) {             \
            sqlite3_errmsg(db_ptr);           \
        }                                     \
    } while (false)

static const char SELECT_ALL_DEV_QUERY[] = "\
SELECT * \
FROM devices";

static const char FIND_DEVICE[] = "\
SELECT * \
FROM devices \
WHERE vendor_id = ? \
AND product_code = ? \
AND revision = ?";

static const char FIND_PDOS_FROM_DEV_ID[] = "\
SELECT pdos.* \
FROM devices \
INNER JOIN pdos \
ON devices.dev_id = pdos.db_idx \
WHERE devices.dev_id = 5";

int main () {
    int ret = 0;
    sqlite3 *db_ptr;        // Database handle
    sqlite3_stmt *stmt_ptr; // SQL statement handle


    // Open Database
    printf("Reading file: %s\n", FILE_PATH);
    ret = sqlite3_open_v2(FILE_PATH, &db_ptr, SQLITE_OPEN_READONLY, NULL);
    if ( ret != SQLITE_OK ) { sqlite3_errmsg(db_ptr); }

    // Execute a single SQL Statement
    {
        // Prepare an SQL statement
        PREPARE_QUERY(db_ptr, SELECT_ALL_DEV_QUERY, &stmt_ptr);

        // Bind the data fields to specific data (if needed)

        // Run the query, checking for a row match
        {
            int ret;
            while ( (ret = sqlite3_step(stmt_ptr)) ) {
                if ( ret == SQLITE_ROW ) {
                    int vendor_id = sqlite3_column_int(stmt_ptr, 1);
                    int product_code = sqlite3_column_int(stmt_ptr, 2);
                    int revision = sqlite3_column_int(stmt_ptr, 3);
                    const unsigned char *dev_type =
                        sqlite3_column_text(stmt_ptr, 4);
                    printf("Device: {%d}:{%d}:{%d}:%s\n",
                           vendor_id,
                           product_code,
                           revision,
                           dev_type);
                } else if ( ret == SQLITE_DONE ) {
                    // reset the query statement
                    sqlite3_reset(stmt_ptr);
                    break;
                } else {
                    // some other err / notification
                    sqlite3_reset(stmt_ptr);
                    break;
                }
            }
        }

        // Destroy the SQL statement
        FINALIZE_QUERY(stmt_ptr);
    }

    // Close Database
    printf("Closing DB file\n");
    sqlite3_close_v2(db_ptr);
    return 0;
}
