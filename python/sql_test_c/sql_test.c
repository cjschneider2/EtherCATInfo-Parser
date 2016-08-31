#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdbool.h>

#include "./sqlite3.h"

/* ------------------------------------------------------------------------ */
/* Notes / Documentation                                                    */
/* ------------------------------------------------------------------------ */

// NOTE:
//   binding is used to replace the `?` variables in the static
//   SQL Statements. as `sqlite3_bind_*(stmt_ptr, stmt_idx, value)`

// NOTE:
//   After every query statement the sqlite3_statement need to be reset so
//   it can be queried again if needed. (This is a stateful operation.)

/* ------------------------------------------------------------------------ */
/* Defines                                                                  */
/* ------------------------------------------------------------------------ */

#define FILE_PATH "./ethercat_dev.sqlite"

/* ------------------------------------------------------------------------ */
/* Structures                                                               */
/* ------------------------------------------------------------------------ */

struct pdo_entry {
    uint32_t db_index;         /** The device identifier                 */
    uint16_t index;            /** The CAN Address of the data           */
    uint8_t  subindex;         /** The CAN Sub-Index of the data         */
    uint8_t  bit_length;       /** The bit length of the data            */
    uint8_t  direction;        /** The direction {(Tx)ransmit|(Rx)eceive}*/
    uint8_t  sync_manager;     /** The default Sync Manager for the data */
    size_t   name_idx;         /** The index into the PDO string list    */
    uint8_t  data_type;        /** The index into the PDO string list    */
};
typedef struct pdo_entry PdoEntry;

/* ------------------------------------------------------------------------ */
/* SQL - Macros                                                             */
/* ------------------------------------------------------------------------ */

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

/* ------------------------------------------------------------------------ */
/* SQL - Statements                                                         */
/* ------------------------------------------------------------------------ */

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
WHERE devices.dev_id = ?";

/* ------------------------------------------------------------------------ */
/* SQL Query Fn's                                                           */
/* ------------------------------------------------------------------------ */

int /* return { Number of Entries > 0 | EXIT_FAILURE if < 0 } */
query_find_pdos_for_dev_id (
    sqlite3 *db_ptr,
    uint32_t dev_id,
    PdoEntry *pdo_list
    )
{
    int ret = 0;            // Return value temp. value
    sqlite3_stmt *stmt_ptr; // SQL statement handle


    // Prepare an SQL statement
    PREPARE_QUERY(db_ptr, FIND_PDOS_FROM_DEV_ID, &stmt_ptr);

    // Bind the data fields to specific data (if needed)
    sqlite3_bind_int(stmt_ptr, 1, dev_id);

    // Run the query, checking for a row match
    int idx = 0;
    while ( (ret = sqlite3_step(stmt_ptr)) )
    {
        if ( ret == SQLITE_ROW )
        {
            pdo_list[idx].index = sqlite3_column_int(stmt_ptr, 3);
            pdo_list[idx].subindex = sqlite3_column_int(stmt_ptr, 4);
            pdo_list[idx].bit_length = sqlite3_column_int(stmt_ptr, 5);
            pdo_list[idx].direction = sqlite3_column_int(stmt_ptr, 6);
            pdo_list[idx].sync_manager = sqlite3_column_int(stmt_ptr, 7);
            // Unimplemented
            pdo_list[idx].name_idx = 0;
            pdo_list[idx].data_type = 0;

            idx++;
        }
        else if ( ret == SQLITE_DONE ) // Finished
        {
            break;
        }
        else // some other error / notification was returned
        {
            goto fail;
        }
    }

    // Destroy the SQL statement
    sqlite3_reset(stmt_ptr);
    FINALIZE_QUERY(stmt_ptr);
    return idx;
fail:
    sqlite3_reset(stmt_ptr);
    FINALIZE_QUERY(stmt_ptr);
    return -1;
}

/* ------------------------------------------------------------------------ */
/* Main Fn                                                                  */
/* ------------------------------------------------------------------------ */

int main () {
    int ret = 0;
    sqlite3 *db_ptr;        // Database handle

    // Open Database
    printf("Reading file: %s\n", FILE_PATH);
    ret = sqlite3_open_v2(FILE_PATH, &db_ptr, SQLITE_OPEN_READONLY, NULL);
    if ( ret != SQLITE_OK ) { sqlite3_errmsg(db_ptr); }

    {
        uint32_t db_idx = 1025;
        PdoEntry *pdo_list = calloc(100, sizeof( PdoEntry ) );
        int e_count = query_find_pdos_for_dev_id (
            db_ptr, db_idx,
            pdo_list
            );
        printf("Found: %d Entries.\n", e_count);
        free(pdo_list);
    }

    // Close Database
    printf("Closing DB file\n");
    sqlite3_close_v2(db_ptr);
    return 0;
}
